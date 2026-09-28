"""KADEA 어라운드뷰 가이드 영상(MP4) / 설명서(PDF) 빌드.

사용법:
    python3 build/build.py            # 영상 4개 + PDF 4개
    python3 build/build.py video      # 영상만
    python3 build/build.py pdf        # PDF만

필요: playwright(chromium), imageio-ffmpeg, 한글 폰트(NanumGothic / NanumSquare)
모두 무료·오픈소스 도구만 사용한다.
"""
import html
import subprocess
import sys
import tempfile
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
from common import ROOT, img_url  # noqa: E402
import videos  # noqa: E402
import docs  # noqa: E402

W, H = 1280, 720
FPS = 25
FADE = 0.5  # 크로스페이드(초)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

SLIDE_CSS = (Path(__file__).parent / "slide.css").read_text(encoding="utf-8")


def duration(cap: str) -> float:
    """자막을 편하게 읽을 수 있는 시간 (한글 약 8.5자/초)."""
    return round(max(5.0, len(cap) / 8.5 + 1.5), 1)


def slide_html(video, i, s):
    n = len(video["slides"])
    prog = (i + 1) / n * 100
    head = "" if s.get("cover") else f"""
<header><img class="logo" src="{img_url('logo')}"><span class="vt">{video['title']}</span>
<span class="st">{html.escape(s['title'])}</span><span class="pg">{i + 1} / {n}</span></header>"""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{SLIDE_CSS}</style></head>
<body><div class="slide {'is-cover' if s.get('cover') else ''}">{head}
<main>{s['body']}</main>
<footer class="cap">{html.escape(s['cap'])}</footer>
<div class="prog" style="width:{prog:.1f}%"></div></div></body></html>"""


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_video(page, video, outdir: Path):
    tmp = Path(tempfile.mkdtemp(prefix=video["slug"]))
    pngs, durs = [], []
    for i, s in enumerate(video["slides"]):
        page.set_content(slide_html(video, i, s), wait_until="load")
        p = tmp / f"s{i:02d}.png"
        page.screenshot(path=str(p))
        pngs.append(p)
        durs.append(duration(s["cap"]))

    # ffmpeg: 각 슬라이드를 정지 영상으로 넣고 xfade 로 이어붙임
    cmd = [FFMPEG, "-y", "-loglevel", "error"]
    for p, d in zip(pngs, durs):
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", str(d + FADE), "-i", str(p)]
    total = sum(durs) + FADE
    cmd += ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo"]
    filt, prev, off = [], "0:v", 0.0
    for k in range(1, len(pngs)):
        off += durs[k - 1]
        out = f"v{k}"
        filt.append(f"[{prev}][{k}:v]xfade=transition=fade:duration={FADE}:offset={off:.2f}[{out}]")
        prev = out
    filt.append(f"[{prev}]format=yuv420p[vout]")
    cmd += ["-filter_complex", ";".join(filt), "-map", "[vout]", "-map", f"{len(pngs)}:a",
            "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage", "-crf", "24",
            "-r", str(FPS), "-c:a", "aac", "-b:a", "64k", "-shortest", "-movflags", "+faststart",
            str(outdir / f"KADEA_AVM_{video['slug']}.mp4")]
    subprocess.run(cmd, check=True)

    # 자막(내레이션 대본) SRT — 음성 녹음/무료 TTS 더빙 시 사용
    t, lines = 0.0, []
    for i, (s, d) in enumerate(zip(video["slides"], durs), 1):
        lines += [str(i), f"{srt_time(t + 0.2)} --> {srt_time(t + d)}", s["cap"], ""]
        t += d
    (outdir / f"KADEA_AVM_{video['slug']}.srt").write_text("\n".join(lines), encoding="utf-8")
    print(f"  {video['slug']}: {len(pngs)} slides, {t:.0f}s")
    # 썸네일
    (outdir / "thumbs").mkdir(exist_ok=True)
    pngs[0].replace(outdir / "thumbs" / f"{video['slug']}.png")
    return t


def build_pdfs(browser, outdir: Path):
    page = browser.new_page()
    for d in docs.ALL:
        page.set_content(docs.render(d), wait_until="load")
        out = outdir / f"KADEA_AVM_{d['slug']}.pdf"
        page.pdf(path=str(out), format="A4", print_background=True,
                 margin=dict(top="16mm", bottom="16mm", left="14mm", right="14mm"),
                 display_header_footer=True,
                 header_template=f'<div style="font-size:7.5px;width:100%;padding:0 14mm;color:#888;'
                                 f'font-family:NanumGothic;display:flex;justify-content:space-between">'
                                 f'<span>KADEA K-FHDSVM 어라운드뷰</span><span>{d["title"]}</span></div>',
                 footer_template='<div style="font-size:7.5px;width:100%;text-align:center;color:#888;'
                                 'font-family:NanumGothic"><span class="pageNumber"></span> / '
                                 '<span class="totalPages"></span></div>')
        print(f"  {out.name}")
    page.close()


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        if what in ("all", "video"):
            out = ROOT / "video"
            out.mkdir(exist_ok=True)
            page = browser.new_page(viewport=dict(width=W, height=H))
            only = sys.argv[2:]  # 예: build.py video 01_install
            for v in videos.ALL:
                if not only or v["slug"] in only:
                    build_video(page, v, out)
            page.close()
        if what in ("all", "pdf"):
            out = ROOT / "pdf"
            out.mkdir(exist_ok=True)
            build_pdfs(browser, out)
        browser.close()


if __name__ == "__main__":
    main()
