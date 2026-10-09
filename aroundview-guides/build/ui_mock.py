"""Calibration Tool 메뉴 화면을 선명하게 다시 그린다 (원본 캡처가 작아 확대하면 깨지므로).

원본(Calibration 가이드 캡처)과 같은 배치·문구로 HTML 을 그리고 2배 해상도로 저장한다.
    python3 build/ui_mock.py   → assets/img/cal_menubar.jpg, cal_paramsbar.jpg
좌표는 원본을 4배(메뉴바)·2.6배(Params) 확대한 크기 기준이라 videos.py 의 화살표 위치가 그대로 맞는다.
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

IMG = Path(__file__).resolve().parent.parent / "assets" / "img"

BASE = """<style>
* { box-sizing: border-box; margin: 0; }
body { width: %dpx; height: %dpx; position: relative; overflow: hidden; background: #f3f4f6;
       font-family: Arial, "NanumGothic", sans-serif; color: #1f2937; }
.b { position: absolute; display: flex; align-items: center; justify-content: center; border-radius: 3px; }
.btn { background: #bcd6f5; border: 1px solid #9cbfe9; }
.tab { background: #dfe3e8; border: 1px solid #c8ced6; }
.sel { background: #bcd6f5; border: 1px solid #9cbfe9; }
.fld { background: #fff; border: 1px solid #d5d9df; }
.lbl { position: absolute; }
</style>"""


def box(cls, x1, y1, x2, y2, text, fs, extra=""):
    return (f'<div class="b {cls}" style="left:{x1}px;top:{y1}px;width:{x2 - x1}px;height:{y2 - y1}px;'
            f'font-size:{fs}px;{extra}">{text}</div>')


def menubar():
    W, H = 608, 232
    h = BASE % (W, H) + "".join([
        box("btn", 18, 18, 158, 62, "Cam view", 25),
        box("tab", 166, 18, 286, 62, "Params", 25),
        f'<div style="position:absolute;left:0;top:66px;width:{W}px;height:1px;background:#d5d9df"></div>',
        box("btn", 16, 72, 104, 114, "Close", 24),
        box("btn", 153, 72, 240, 116, "Apply", 24),
        box("fld", 14, 166, 240, 212, "Smart", 24, "justify-content:flex-start;padding-left:10px"),
        box("btn", 243, 166, 287, 212, "&#9660;", 24),
        box("btn", 298, 166, 404, 212, "Detect", 24),
        box("btn", 408, 166, 594, 212, "Load Master", 24),
        f'<div style="position:absolute;left:0;top:216px;width:{W}px;height:{H - 216}px;'
        f'background:linear-gradient(90deg,#3b3f45,#6b6f73 40%,#2c2f33 60%,#55595e)"></div>',
    ])
    return h, W, H


def paramsbar():
    W, H = 598, 124
    f = 15
    h = BASE % (W, H) + "".join([
        box("tab", 2, 3, 70, 27, "Cam view", f - 1),
        box("sel", 72, 3, 132, 27, "Params", f - 1),
        box("fld", 4, 33, 96, 56, "-1270", f), box("fld", 100, 33, 196, 56, "10500", f),
        box("fld", 200, 33, 296, 56, "1270", f), box("fld", 300, 33, 376, 56, "0", f),
        f'<div class="lbl" style="left:382px;top:36px;font-size:{f - 1}px">Clip Area: left/front/right/back</div>',
        f'<div class="lbl" style="left:8px;top:63px;font-size:{f}px">Camera</div>',
        f'<div class="lbl" style="left:188px;top:63px;font-size:{f}px">:</div>',
        box("fld", 200, 61, 470, 84, "Analog_FHD", f, "justify-content:flex-start;padding-left:8px"),
        box("btn", 446, 62, 469, 83, "&#9660;", f - 3),
        f'<div class="lbl" style="left:8px;top:89px;font-size:{f}px">Vehicle Length</div>',
        f'<div class="lbl" style="left:188px;top:89px;font-size:{f}px">:</div>',
        box("fld", 200, 87, 470, 110, "10500", f),
        f'<div class="lbl" style="left:480px;top:89px;font-size:{f}px">mm</div>',
    ])
    return h, W, H


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for name, fn in [("cal_menubar", menubar), ("cal_paramsbar", paramsbar)]:
            html, W, H = fn()
            pg = b.new_page(viewport=dict(width=W, height=H), device_scale_factor=2)
            pg.set_content(f"<!doctype html><html><head><meta charset='utf-8'></head><body>{html}</body></html>")
            pg.screenshot(path=str(IMG / f"{name}.jpg"), type="jpeg", quality=95)
            pg.close()
            print(name)
        b.close()


if __name__ == "__main__":
    main()
