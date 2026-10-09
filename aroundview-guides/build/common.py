"""공통 스타일 / HTML 헬퍼."""
import base64
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"


@lru_cache(maxsize=None)
def img_url(name: str) -> str:
    """assets/img/<name>.jpg 를 data URI 로 (브라우저가 file:// 을 막으므로 인라인)."""
    p = IMG / (name if "." in name else f"{name}.jpg")
    if not p.exists():
        raise FileNotFoundError(p)
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()


def img(name, cap=None, cls="", style=""):
    c = f'<figcaption>{cap}</figcaption>' if cap else ""
    return f'<figure class="{cls}" style="{style}"><img src="{img_url(name)}">{c}</figure>'


def ul(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def table(head, rows, cls=""):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


def chip(color, label):
    """전선 색상 칩."""
    border = "#999" if color in ("#ffffff", "#f5f5f5") else color
    return (f'<span class="chip"><i style="background:{color};border-color:{border}"></i>'
            f'{label}</span>')


# --------------------------------------------------------------------------
# 도식: 카메라 수직면 부착
# --------------------------------------------------------------------------
def svg_vertical(width=560):
    return f"""
<svg viewBox="0 0 560 300" width="{width}" xmlns="http://www.w3.org/2000/svg" font-family="NanumSquare, NanumGothic">
  <!-- OK -->
  <rect x="0" y="0" width="270" height="300" rx="14" fill="#eaf7ee"/>
  <text x="135" y="30" text-anchor="middle" font-size="19" font-weight="800" fill="#1b7a3a">✔ 올바른 부착</text>
  <rect x="60" y="50" width="16" height="230" fill="#555"/>
  <text x="50" y="170" font-size="13" fill="#333" transform="rotate(-90 50 170)" text-anchor="middle">차체 수직면 (90°)</text>
  <rect x="76" y="110" width="34" height="46" rx="6" fill="#222"/>
  <circle cx="100" cy="140" r="9" fill="#2f7cf6"/>
  <polygon points="100,140 245,285 150,290" fill="#2f7cf6" opacity=".18"/>
  <line x1="100" y1="140" x2="235" y2="275" stroke="#2f7cf6" stroke-width="2.5" stroke-dasharray="6 5"/>
  <line x1="100" y1="140" x2="240" y2="140" stroke="#999" stroke-width="1.5"/>
  <path d="M170 140 A70 70 0 0 1 150 190" fill="none" stroke="#e03131" stroke-width="2.5"/>
  <text x="178" y="178" font-size="17" font-weight="800" fill="#e03131">42~45°</text>
  <text x="175" y="75" text-anchor="middle" font-size="13" fill="#333">하향 각도는 하우징에 내장</text>
  <!-- NG -->
  <rect x="290" y="0" width="270" height="300" rx="14" fill="#fdecec"/>
  <text x="425" y="30" text-anchor="middle" font-size="19" font-weight="800" fill="#c92a2a">✘ 잘못된 부착</text>
  <line x1="340" y1="50" x2="372" y2="215" stroke="#555" stroke-width="16"/>
  <text x="440" y="80" text-anchor="middle" font-size="13" fill="#333">경사면 / 쐐기(웨지) 브래킷</text>
  <polygon points="380,120 410,112 418,160 388,168" fill="#888"/>
  <rect x="410" y="112" width="30" height="44" rx="6" fill="#222" transform="rotate(-12 425 134)"/>
  <line x1="430" y1="140" x2="485" y2="225" stroke="#c92a2a" stroke-width="2.5" stroke-dasharray="6 5"/>
  <text x="425" y="258" text-anchor="middle" font-size="14" fill="#c92a2a" font-weight="700">하향 각도 이중 적용 →</text>
  <text x="425" y="280" text-anchor="middle" font-size="14" fill="#c92a2a" font-weight="700">탑뷰 왜곡 · 보정 실패</text>
</svg>"""


# --------------------------------------------------------------------------
# 도식: K-FHDSVM 연결 개요
# --------------------------------------------------------------------------
def svg_connect(width=1100):
    box = lambda x, y, w, h, t, fill="#fff", stroke="#333", fs=15, tc="#111": (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        + "".join(f'<text x="{x + w / 2}" y="{y + h / 2 + 5 + (i - (len(t.split("|")) - 1) / 2) * (fs + 3)}" '
                  f'text-anchor="middle" font-size="{fs}" fill="{tc}" font-weight="700">{s}</text>'
                  for i, s in enumerate(t.split("|"))))
    line = lambda x1, y1, x2, y2, c="#333": f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="3"/>'
    parts = [
        box(430, 150, 240, 150, "K-FHDSVM|어라운드뷰 본체", "#1d2733", "#1d2733", 20, "#fff"),
        # 카메라
        box(20, 20, 150, 44, "전방 카메라 FRONT", "#e7f0ff", "#2f7cf6", 14),
        box(20, 80, 150, 44, "후방 카메라 REAR", "#eef8e8", "#5c940d", 14),
        box(20, 140, 150, 44, "좌측 카메라 LEFT", "#fff1e6", "#e8590c", 14),
        box(20, 200, 150, 44, "우측 카메라 RIGHT", "#fbeaf5", "#ae3ec9", 14),
        box(220, 90, 150, 110, "카메라 연장|케이블 ×4|→ 카메라 젠더|케이블(4갈래)", "#fff", "#333", 13),
        line(170, 42, 220, 110), line(170, 102, 220, 130), line(170, 162, 220, 160), line(170, 222, 220, 185),
        line(370, 170, 430, 190),
        '<text x="378" y="215" font-size="11" fill="#333">16핀</text>',
        # 전원
        box(760, 20, 320, 60, "전원 케이블 (24핀 전원 커넥터)|ACC·GND·후진·방향지시", "#fff8db", "#f08c00", 14),
        line(670, 180, 760, 50),
        box(760, 100, 150, 44, "ACC 키 전원 (노랑)", "#fff", "#f08c00", 13),
        box(930, 100, 150, 44, "차체 접지 GND (검정)", "#fff", "#333", 13),
        line(835, 80, 835, 100), line(1005, 80, 1005, 100),
        # 모니터
        box(760, 190, 320, 120, "KAM_2510 모니터|① USB(터치) → 본체 USB|② 노란 RCA → AHD/CVBS 출력|③ 빨간 전원잭 → 차량 전원", "#e6fcf5", "#0ca678", 13),
        line(670, 225, 760, 235),
        # USB / SD
        box(430, 330, 240, 44, "MicroSD (녹화) · DIP 스위치", "#f1f3f5", "#868e96", 13),
        box(20, 300, 360, 70, "USB 메모리 (펌웨어 / 캘리브레이션 파일)|USB 2.0 포트 (가이드 기준)", "#f3f0ff", "#7048e8", 13),
        line(380, 330, 430, 280), line(550, 300, 550, 330),
    ]
    return (f'<svg viewBox="0 0 1100 390" width="{width}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="NanumSquare, NanumGothic">{"".join(parts)}</svg>')


# 본체 전원 케이블 결선표 (KADEA K-FHDSVM 매뉴얼 V01 기준)
POWER_ROWS = [
    [chip("#f2c200", "노랑"), "ACC", "23", "ACC(키 ON) 전원 + · 5A 퓨즈 내장", "<b>필수</b>"],
    [chip("#111111", "검정"), "GND", "24", "차체 접지(볼트 체결부)", "<b>필수</b>"],
    [chip("#8b4513", "갈색"), "REVERSE", "13", "후진등 + 신호", "권장"],
    [chip("#1c6dd0", "파랑"), "LEFT", "14", "좌측 방향지시등 신호", "권장"],
    [chip("#e03131", "빨강"), "RIGHT", "12", "우측 방향지시등 신호", "권장"],
    ["RCA 잭", "AHD/CVBS", "11 / 10", "모니터 영상 입력(노란 RCA)", "<b>필수</b>*"],
    [chip("#ffffff", "흰") + chip("#f76707", "주황") + chip("#111111", "검정"), "CAN_H · CAN_L · CAN_GND", "–", "차량 CAN 연동 시에만", "선택"],
    [chip("#e03131", "빨강") + chip("#111111", "검정"), "SPK+ · SPK GND", "–", "외장 스피커", "선택"],
    ["3.5파이 잭", "IR", "7 / 8 / 9", "IR 리시버", "선택"],
    [chip("#2f9e44", "초록") + chip("#111111", "검정"), "UART", "3 / 4 / 6", "진단·서비스용", "미사용"],
]
POWER_HEAD = ["전선 색", "라벨", "핀", "연결 위치", "구분"]


# --------------------------------------------------------------------------
# 화면 위 화살표/번호 표시: marked("cal_menubar", [dict(x=.43, y=.8, label="A", d="s"), ...])
#   x, y : 이미지 안의 위치 (0~1 비율)
#   d    : 화살표가 들어오는 방향 (s, n, e, w, se, sw, ne, nw) / kind="badge" 는 번호 원만 표시
# --------------------------------------------------------------------------
_DIRS = {"s": (0, 1), "n": (0, -1), "e": (1, 0), "w": (-1, 0),
         "se": (.75, .75), "sw": (-.75, .75), "ne": (.75, -.75), "nw": (-.75, -.75)}


def marked(name, marks, width=560, cap=None, pad=0):
    from PIL import Image
    w0, h0 = Image.open(IMG / f"{name}.jpg").size
    W, H = width, round(width * h0 / w0)
    k = max(.7, min(1.0, W / 560))                    # 작은 이미지는 화살표도 작게
    red, ring = "#e03131", 20 * k
    parts = []
    for m in marks:
        x, y = m["x"] * W, m["y"] * H
        if m.get("kind") == "badge":
            bx, by = x + m.get("dx", 0), y + m.get("dy", -34)
            parts.append(f'<circle cx="{bx}" cy="{by}" r="16" fill="{red}" stroke="#fff" stroke-width="3"/>'
                         f'<text x="{bx}" y="{by + 7}" text-anchor="middle" font-size="19" font-weight="800" '
                         f'fill="#fff">{m["label"]}</text>')
            continue
        if m.get("kind") == "box":                     # 영역 강조 사각형
            bw, bh = m["w"] * W, m["h"] * H
            parts.append(f'<rect x="{x - bw / 2}" y="{y - bh / 2}" width="{bw}" height="{bh}" rx="8" fill="none" '
                         f'stroke="#fff" stroke-width="8"/><rect x="{x - bw / 2}" y="{y - bh / 2}" width="{bw}" '
                         f'height="{bh}" rx="8" fill="none" stroke="{red}" stroke-width="4.5"/>')
            r = max(bw, bh) / 2
            if m.get("badge"):
                bx, by = x - bw / 2, y - bh / 2
                parts.append(f'<circle cx="{bx}" cy="{by}" r="14" fill="{red}" stroke="#fff" stroke-width="3"/>'
                             f'<text x="{bx}" y="{by + 6}" text-anchor="middle" font-size="17" font-weight="800" '
                             f'fill="#fff">{m["badge"]}</text>')
        else:
            r = ring
            parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#fff" stroke-width="8"/>'
                         f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{red}" stroke-width="4.5"/>')
        if m.get("d") is None:
            continue
        ux, uy = _DIRS[m["d"]]
        L = m.get("len", 64) * k
        if m.get("kind") == "box":
            r = (abs(ux) * m["w"] * W + abs(uy) * m["h"] * H) / (abs(ux) + abs(uy)) / 2
        sx, sy = x + ux * (r + 4), y + uy * (r + 4)
        tx, ty = x + ux * (r + L), y + uy * (r + L)
        parts.append(f'<line x1="{tx}" y1="{ty}" x2="{sx}" y2="{sy}" stroke="#fff" stroke-width="11" stroke-linecap="round"/>'
                     f'<line x1="{tx}" y1="{ty}" x2="{sx}" y2="{sy}" stroke="{red}" stroke-width="6" '
                     f'stroke-linecap="round" marker-end="url(#ah)"/>')
        lab = m.get("label")
        if lab:
            fs = round(19 * k)
            tw = sum(fs if ord(ch) > 0x2000 else fs * .62 for ch in lab) + 20
            if uy == 0:
                lx, ly = (tx + 6 if ux > 0 else tx - tw - 6), ty - 17
            else:
                lx = tx - tw / 2 + ux * (tw / 2 - 6)
                ly = ty + 4 if uy > 0 else ty - 38
            lx = min(max(lx, -40), W + 40 - tw)
            parts.append(f'<rect x="{lx}" y="{ly}" width="{tw}" height="{fs + 15}" rx="8" fill="{red}" stroke="#fff" stroke-width="2"/>'
                         f'<text x="{lx + tw / 2}" y="{ly + fs + 3}" text-anchor="middle" font-size="{fs}" '
                         f'font-weight="800" fill="#fff">{lab}</text>')
    svg = (f'<svg class="mk-ov" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="NanumSquare, NanumGothic">'
           f'<defs><marker id="ah" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="{red}"/></marker></defs>{"".join(parts)}</svg>')
    c = f'<figcaption>{cap}</figcaption>' if cap else ""
    return (f'<figure class="mk-fig" style="margin:{pad}px 0"><div class="mk" style="width:{W}px;height:{H}px">'
            f'<img src="{img_url(name)}" style="width:{W}px;height:{H}px">{svg}</div>{c}</figure>')
