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
