"""A4 PDF 설명서 4종 (첨부된 KADEA 매뉴얼 · 사양서 · 캘리브레이션 가이드 기준)."""
from pathlib import Path

from common import img, ul, table, svg_vertical, svg_connect, img_url, POWER_ROWS, POWER_HEAD

DOC_CSS = (Path(__file__).parent / "doc.css").read_text(encoding="utf-8")

VERTICAL_BOX = f"""
<div class="callout red">
  <div class="ct">⚠ 카메라는 반드시 수직면에 부착하십시오</div>
  <p>카메라 하우징에는 약 <b>42~45°의 하향(dip) 각도가 이미 내장</b>되어 있습니다.
  차체의 <b>수직면(90°)에 평평하게 밀착</b>하여 부착하고, 쐐기(웨지) 브래킷·경사면 부착·임의 각도 조정은 하지 마십시오.
  각도가 이중으로 적용되면 탑뷰가 왜곡되고 캘리브레이션이 실패합니다.</p>
  <div class="center">{svg_vertical(430)}</div>
</div>"""


def cover(no, title, sub, pic):
    return f"""
<section class="cover">
  <img class="logo" src="{img_url('logo')}">
  <div class="cv-no">K-FHDSVM 어라운드뷰 가이드 {no} / 4</div>
  <h1>{title}</h1>
  <p class="sub">{sub}</p>
  <div class="cv-pic">{img(pic)}</div>
  <div class="cv-meta">기준 문서: KADEA K-FHDSVM 어라운드뷰 박스 매뉴얼 V01 · K-FHDSVM 제어기 제품 사양서 Rev0.1 ·
  K-FHDSVM Calibration / 펌웨어 업데이트 가이드 (2025)</div>
</section>"""


def render(d):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{DOC_CSS}</style></head>
<body>{d['html']}</body></html>"""


# ============================================================================
INSTALL = dict(slug="01_install", title="장착 설명서", html=cover(
    1, "어라운드뷰 장착 설명서", "카메라 4채널 장착 · 본체/모니터 배선 · 장착 후 점검", "box_3d") + f"""
<h2>1. 구성품</h2>
<div class="g4">
{img("box_top", "K-FHDSVM 본체")}{img("camera", "카메라 ×4")}{img("cam_gender", "카메라 젠더 케이블")}{img("ext_cable", "카메라 연장 케이블")}
{img("power_cable", "전원 케이블")}{img("bracket", "카메라 장착 브래킷")}{img("sdcard", "MicroSD 카드")}{img("mon", "KAM_2510 모니터 (별도 세트)")}
</div>
<p class="small">KAM_2510 모니터 세트: 모니터 본체 · 모니터 출력(RCA) 연장 케이블 · 모니터 전원 연장 케이블 · 모니터 브라켓 · 고정 볼트 세트</p>

<h2>2. 작업 전 주의사항</h2>
{ul([
    "차량 <b>시동을 끄고</b> 장착 작업을 하십시오.",
    "본 제품은 <b>DC 12V / 24V</b> 차량 전용입니다 (동작 전압 DC 9~32V). 그 외 차량에 설치하지 마십시오 — 파손 및 화재 위험.",
    "카메라 커넥터 연결부는 <b>절연 테이프</b>로 보호하십시오.",
    "카메라 커넥터 연결 시 무리한 힘을 가하여 구부리면 파손될 수 있습니다.",
    "배선은 배기·엔진 등 열원과 조향·서스펜션 등 가동부를 피해 고정하십시오.",
])}

<h2>3. 카메라 장착</h2>
{VERTICAL_BOX}
<h3>3-1. 장착 위치 — 현대 유니버스 12m 예시</h3>
<div class="fig-full">{img("universe12m_mounting")}</div>
{table(["카메라", "x (mm, 후면 기준)", "y (mm, 좌 +)", "z 높이 (mm, 지면 기준)", "비고"], [
    ["<b style='color:#1c6dd0'>FRONT</b>", "12,000", "0", "3,000", "전면, 차량 중심선"],
    ["<b style='color:#5c940d'>REAR</b>", "0", "0", "3,210", "후면, 차량 중심선"],
    ["<b style='color:#e8590c'>LEFT</b>", "6,000", "+1,248", "3,110", "좌측면, 전장의 50%"],
    ["<b style='color:#ae3ec9'>RIGHT</b>", "6,000", "−1,248", "3,110", "우측면, 전장의 50%"],
])}
<p class="small">원점 = 후면 중앙 · 지면 (0,0,0) · 전장 L 12,000 / 전폭 W 2,495 / 전고 H 3,490 / 축거 WB 6,120 ·
<b class="red">위치 허용 오차 ±30mm (캘리브레이션으로 자동 보정되지 않음)</b></p>

<h3>3-2. 부착 요령</h3>
{ul([
    "<b>카메라는 반드시 수직면에 밀착하여 부착</b> — 하향 42~45°는 하우징에 내장되어 있으므로 별도 각도를 주지 않습니다.",
    "전방·후방 카메라는 차량 <b>중심선(CL)</b> 위에, 좌·우 카메라는 차량 길이의 <b>50%</b> 지점에 좌우 같은 높이로 부착합니다.",
    "카메라 상단의 <b>▼ 표시가 위</b>를 향하도록 부착합니다.",
    "제공된 카메라 장착 브래킷으로 흔들림 없이 고정하고, 렌즈 시야를 차체·미러·몰딩이 가리지 않는지 확인합니다.",
    "케이블 인입부는 방수 처리(실리콘/그로밋)하고 케이블 타이로 고정합니다.",
])}

<h2>4. 본체 포트</h2>
<div class="g2">{img("box_front", "앞면: 전원 커넥터(24핀) · USB 2.0 · USB 3.0 · MicroSD")}{img("box_rear", "뒷면: 카메라 커넥터(16핀) · HDMI · DIP 스위치")}</div>

<h2>5. 연결 — 무엇을 어디에 꽂나</h2>
<div class="center">{svg_connect(690)}</div>
{table(["커넥터 / 케이블", "연결 위치", "구분"], [
    ["카메라 젠더 케이블 (16핀)", "본체 뒷면 <b>카메라 커넥터</b> → 4갈래 FRONT/REAR/LEFT/RIGHT → 연장 케이블 → 각 카메라", "필수"],
    ["전원 케이블 (24핀)", "본체 앞면 <b>전원 커넥터</b> → ACC · GND · 후진 · 방향지시 (아래 결선표)", "필수"],
    ["전원 케이블의 RCA (AHD/CVBS)", "모니터 출력 연장 케이블의 <b>노란 RCA</b>", "필수(RCA 모니터)"],
    ["모니터 USB 케이블 (2m)", "본체 USB 포트 — 모니터 <b>터치 조작</b>용", "필수(터치 사용)"],
    ["모니터 전원 연장 케이블", "차량 전원 (빨간 DC 잭)", "필수"],
    ["HDMI", "HDMI 입력 모니터 사용 시 본체 HDMI", "선택"],
    ["MicroSD 카드", "본체 앞면 SD 슬롯 — 녹화용", "권장"],
    ["USB 메모리", "펌웨어 업데이트 · 캘리브레이션 시에만 (USB 2.0 포트, 가이드 기준)", "작업 시"],
])}

<h3>5-1. 카메라 연결</h3>
<div class="g2">{img("cam_conn", "16핀 카메라 커넥터")}{img("cam_gender", "카메라 젠더 케이블 (4갈래)")}</div>
{ul([
    "카메라 젠더 케이블을 본체 뒷면 <b>카메라 커넥터(16핀)</b>에 ‘딸깍’ 소리가 날 때까지 끼웁니다.",
    "젠더 케이블 각 갈래의 <b>FRONT / REAR / LEFT / RIGHT</b> 라벨을 확인하고, 같은 위치 카메라의 연장 케이블과 연결합니다. 라벨이 바뀌면 화면의 위치도 바뀝니다.",
    "카메라 측 4핀 방수 커넥터(흰·빨·노·검)는 끝까지 체결한 뒤 절연 테이프로 감쌉니다.",
])}
{table(["핀", "신호", "핀", "신호", "핀", "신호", "핀", "신호"], [
    ["1", "POWER_LEFT", "3", "GND_LEFT", "5", "POWER_RIGHT", "7", "GND_RIGHT"],
    ["2", "TRIG_LEFT", "4", "SIGNAL_LEFT", "6", "TRIG_RIGHT", "8", "SIGNAL_RIGHT"],
    ["9", "POWER_REAR", "11", "GND_REAR", "13", "POWER_FRONT", "15", "GND_FRONT"],
    ["10", "TRIG_REAR", "12", "SIGNAL_REAR", "14", "TRIG_FRONT", "16", "SIGNAL_FRONT"],
], "pins")}
<p class="small">카메라 커넥터 핀맵 (KADEA 매뉴얼 V01 기준, 참고용 — 젠더 케이블이 결선되어 있으므로 현장 결선 불필요)</p>

<h3>5-2. 전원 케이블 결선</h3>
{table(POWER_HEAD, POWER_ROWS)}
<p class="small">* 모니터를 RCA(AHD/CVBS)로 연결하는 경우 필수. 핀 번호는 KADEA K-FHDSVM 매뉴얼 V01 기준.<br>
<b class="red">빨간선은 SPK+ 와 RIGHT 두 가지이므로 반드시 선 라벨로 구분하십시오.</b> 사용하지 않는 선은 끝단을 절연 처리하여 정리합니다.
ACC 선에는 5A 퓨즈가 내장되어 있습니다.</p>
<div class="fig-full">{img("wiring_diagram")}</div>

<h3>5-3. 모니터 (KAM_2510) 연결</h3>
<div class="g2">{img("mon_diagram")}<div>{ul([
    "① 모니터 <b>USB 케이블(2m)</b> → 어라운드뷰 BOX USB 2.0 또는 USB 3.0 포트",
    "② 모니터 <b>출력 연장 케이블(노란 RCA)</b> → 어라운드뷰 BOX <b>AHD/CVBS</b> 커넥터",
    "③ 모니터 <b>전원 연장 케이블</b> → 차량 전원",
    "터치 USB와 업데이트/캘리브레이션용 USB 메모리는 <b>서로 다른 포트</b>를 사용합니다 (권장: 메모리 → USB 2.0, 터치 → USB 3.0).",
])}</div></div>

<h3>5-4. MicroSD · DIP 스위치</h3>
{ul([
    "녹화용 MicroSD 카드를 앞면 슬롯에 삽입합니다 (H.265, 2분 단위 파일, 상시/이벤트 녹화).",
    "뒷면 DIP 스위치로 AHD / HDMI 출력 해상도(<b>720p 또는 1080p</b>, 30fps)를 모니터 사양에 맞게 설정한 뒤 전원을 다시 인가합니다.",
])}

<h2>6. 장착 후 점검</h2>
<div class="g2">{img("ui_main")}<div>{ul([
    "ACC ON 후 약 <b>3.5초 이내</b> 부팅되는지 확인",
    "4채널 카메라 영상이 모두 출력되는지 확인",
    "전방/후방/좌/우 영상 위치가 바뀌지 않았는지 확인",
    "렌즈 오염·가림 여부 확인",
    "이상 없으면 <b>캘리브레이션</b> 진행 (가이드 2/4)",
])}</div></div>

<h2>7. 주요 사양</h2>
{table(["항목", "사양"], [
    ["카메라", "AHD FHD 1920×1080 @30fps × 4채널"],
    ["디스플레이 출력", "AHD 720p/1080p 30fps (DIP) · HDMI 720p/1080p (DIP) · CVBS"],
    ["동작 전원 / 온도", "DC 9~32V (ACC / B+) · −30 ~ 75°C (보관 −40 ~ 85°C)"],
    ["부팅 / 지연", "3.5초 이하 / 200ms 이하"],
    ["저장", "MicroSD (녹화), eMMC 4GB"],
    ["USB", "USB 2.0 OTG · USB 3.0 HOST"],
    ["객체 감지", "사람 · 차량 (NPU 1 TOPS), 화면 표시 + 스피커 알람"],
])}
""")

# ============================================================================
CALIB = dict(slug="02_calibration", title="캘리브레이션 설명서", html=cover(
    2, "캘리브레이션 설명서", "보정판 설치 · 자동 보정(Auto-Calibration)", "cal_screen") + f"""
<h2>0. 사전 확인</h2>
{VERTICAL_BOX}
{ul([
    "4개 카메라가 규정 위치(허용 오차 ±30mm)에 <b>수직면 밀착</b>으로 장착되어 있는지 확인합니다. 위치 오차·기울어짐은 캘리브레이션으로 보정되지 않습니다.",
    "4채널 영상이 올바른 위치(FRONT/REAR/LEFT/RIGHT)로 출력되는지 확인합니다.",
])}

<h2>Step 1. 보정판 설치</h2>
<div class="g2">{img("cal_layout", "보정판 배치 (전/후 0.5m · 좌/우 3m)", cls="tallfig")}<div>
<h3>보정판 설치하는 법</h3>
{ul([
    "<b>전/후방 보정판</b>: 차량 범퍼와 패턴 사이 <b class='red'>0.5m</b><br><span class='small'>※ 차량의 범퍼부터 패턴의 시작 지점까지</span>",
    "<b>좌/우 보정판</b>: 전방 보정판의 ■ 와 <b class='red'>3m</b><br><span class='small'>※ 전방 패턴 시작부터 사이드 패턴 시작 지점까지</span>",
])}
<h3>설치 시 주의사항</h3>
{ul([
    "차량이 정차 가능하고 패턴 규격에 맞는 설치 공간이 필요합니다.",
    "바닥이 굴곡이 없고 <b>수평</b>이 유지되는 공간을 권장합니다.",
    "조명 환경이 고르고 주변에 간섭 물체가 없는 공간을 권장합니다.",
])}
<h3>준비사항</h3>
{ul(["USB 메모리 — 3가지 파일을 <b>압축 및 폴더 해제</b>하여 저장: <b>MCS, LBS, MASTERCAL</b>"])}
{img("cal_files", "예) .calibrationtool.mcs · HMC_Xcient_12m.lbs · HMC_Xcient_12m.mastercal")}
<p class="small">LBS / MASTERCAL 파일은 차종별로 다릅니다. 장착 차종에 맞는 파일을 사용하십시오.</p>
</div></div>

<h2>Step 2. Auto-Calibration</h2>
<h3>2-1. Calibration Tool 활성화</h3>
<div class="g2">{img("box_top", "USB 2.0 포트")}<div>{ul([
    "A. 전원 <b>OFF</b> 상태",
    "B. (.calibrationtool.mcs) 외 2개 파일이 담긴 USB를 연결 (<b>USB 2.0</b>)",
    "C. 전원 <b>ON</b>",
    "D. Calibration Tool 활성화 (어라운드뷰 화면에서 활성화됩니다)",
])}</div></div>

<h3>2-2. Calibration 메뉴</h3>
<div class="g2">{img("cal_menu")}{table(["버튼", "기능"], [
    ["Cam view", "기본 보정 화면"], ["Params", "차량 전장 입력"], ["Close", "Calibration Tool 닫기"],
    ["Apply", "현재 적용된 차량 및 Calibration 저장"], ["Smart / 0x4", "상용차용 “Smart” / 승용차용 “0x4”"],
    ["Detect", "Calibration 실행"], ["Load Master", "USB에 저장된 차량 모델링 변경"]])}</div>

<h3>2-3. Calibration 방법</h3>
<div class="g2"><div>{ul([
    "A. 좌측 상단 ▽ 를 이용하여 <b>0x4 → Smart</b> 로 변경",
    "B. <b>Load Master</b> 선택 → 우측의 차량 모델이 변경됨",
    "C. 상단의 <b>Params</b> 진입 후 <b>Vehicle Length</b> 조절하여 실제 차량 길이 입력 (터치 드래그로 조절 가능, 예: 유니버스 12m → 12000)",
    "D. <b>Detect</b> → 보정 시작 (Front → Rear → Left → Right 순으로 자동 진행)",
    "E. <b>Cam view</b> 로 복귀 이후 <b>Detect</b> 실행",
    "F. 성공 시 <b>APPLY</b> / 실패 시 다시 <b>Detect</b> 로 보정 진행",
    "G. 성공 후 <b>재부팅</b>",
    "H. 반복 실패 시 보정판 거리(0.5m / 3m)·바닥 수평·조명을 다시 확인한 뒤 재시도",
])}</div><div>{img("cal_params", "Params → Vehicle Length")}{img("cal_screen", "Cam view")}</div></div>

<h2>Step 3. 최종 확인</h2>
{ul([
    "USB 메모리를 제거하고 재부팅 후 탑뷰에서 카메라 경계의 선·패턴이 자연스럽게 이어지는지 확인합니다.",
    "어긋나면 보정판 위치를 다시 확인하고 자동 보정을 반복합니다.",
    "카메라 교체·충격·위치 변경 시에는 반드시 재보정합니다.",
])}
""")

# ============================================================================
FIRMWARE = dict(slug="03_firmware", title="펌웨어 업데이트 설명서", html=cover(
    3, "펌웨어 업데이트 설명서", "USB 메모리를 이용한 K-FHDSVM 소프트웨어 업데이트", "upd_run") + f"""
<h2>1. 준비 사항</h2>
{ul([
    "USB 메모리",
    "펌웨어 파일 <code>update-2100r.iu4</code> — USB 최상위(루트)에 복사",
    "업데이트 중 전원이 끊기지 않도록 차량 전원(ACC) 유지",
])}
<div class="callout"><div class="ct">USB 포트</div><p>펌웨어/캘리브레이션 가이드는 <b>USB 2.0</b> 포트 사용을 안내합니다.
모니터 터치 USB는 다른 포트에 그대로 연결해 두십시오. USB가 인식되지 않으면 다른 USB 포트(USB 3.0)로 옮겨 다시 시도합니다.</p></div>

<h2>2. 업데이트 방법</h2>
<div class="g2">{img("sw_info", "S/W Information — “Version” V 바로 위 5번 터치")}{img("sw_update", "좌측 메뉴 하단에 Update 버튼 생성")}</div>
{ul([
    "① 펌웨어 파일이 있는 USB를 본체 USB 포트(USB 2.0)에 연결합니다.",
    "② 어라운드뷰 화면 하단 ⚙ → <b>Settings</b> 창에서 <b>S/W Information</b>(소프트웨어 정보) 창을 활성화합니다.",
    "③ <b>“Version” 글씨의 V 글자 바로 위쪽 영역을 5번 연속 터치</b>합니다.",
    "④ 좌측 메뉴 창 가장 하단에 <b>Update</b> 버튼이 생성됩니다.",
    "⑤ Update 버튼을 누르면 바로 업데이트가 시작됩니다 (SVM UPDATE 화면).",
    "⑥ <b>UPDATE COMPLETE</b> 문구가 뜨면 USB 장치를 제거하고 제어기 전원을 껐다 켭니다.",
])}
<div class="g3">{img("sw_info_ko", "한글 UI: 좌측 하단 ‘업데이트’")}{img("upd_run", "SVM UPDATE — 전원 OFF 금지")}{img("upd_done", "UPDATE COMPLETE — USB 제거 후 재시작")}</div>
<div class="callout red"><div class="ct">⚠ 주의</div><p>업데이트 진행 중에는 <b>전원(ACC)을 끄거나 USB를 제거하지 마십시오.</b> 제어기가 손상될 수 있습니다.</p></div>

<h2>3. 업데이트 후 확인</h2>
{ul([
    "S/W 정보 창에서 버전(App / MCU Version)이 변경되었는지 확인합니다.",
    "4채널 영상이 정상 출력되는지 확인합니다.",
    "탑뷰 정합이 틀어졌다면 캘리브레이션을 다시 진행합니다 (가이드 2/4).",
])}
""")

# ============================================================================
OPERATION = dict(slug="04_operation", title="작동 설명서", html=cover(
    4, "어라운드뷰 작동 설명서", "화면 구성 · 3D/2D 뷰 · 설정 · 녹화 · 객체 감지 · 모니터 조작", "ui_3d_car") + f"""
<h2>1. 시스템 개요</h2>
{ul([
    "차량 신호를 처리하여 영상 기반의 다양한 기능을 운전자에게 제공하는 <b>주차 보조 시스템</b>입니다.",
    "ACC ON 후 약 <b>3.5초</b> 이내 부팅, 영상 지연 200ms 이하.",
    "FHD 1080p 카메라 4채널 합성 → <b>탑뷰 · 3D 뷰 · 2D 뷰</b>. 모니터 터치(C-Touch)로 조작합니다.",
])}

<h2>2. 메인 화면</h2>
<div class="g2">{img("ui_main", "좌측 메뉴: BACK · HOME · 3D VIEW · PARKING · REC · SETTING")}{img("set_mode", "하단 메뉴바: 상부감시 · 하부감시 · 후방 IR · 어라운드 · 상/하부 · 4분할 · ⚙")}</div>

<h2>3. 3D 뷰</h2>
{table(["모드", "진입 방법", "화면 구성"], [
    ["3D 뷰", "설정 창에서 3D 모드 설정", "전방 · 좌측 후방 · 우측 후방 · 후방 · 후방 트레일러 · 전방 세차"],
    ["3D 와이드 뷰", "3D 모드에서 확대 버튼", "위 6개 뷰의 와이드 화면"],
    ["3D 회전 뷰", "회전 아이콘", "12 · 10 · 9 · 7 · 6 · 5 · 3 · 1시 방향 (시계 방향)"],
    ["3D 와이드 회전 뷰", "확대 아이콘 → 3D 뷰 조작", "와이드 회전"],
])}
<div class="g3">{img("ui_3d", "3D 전방")}{img("ui_wide", "3D 와이드")}{img("ui_rot", "3D 회전")}</div>

<h2>4. 2D 뷰</h2>
<p>설정 창에서 2D 모드 설정 — 전방 와이드 · 전방+탑뷰 · 후방 와이드 · 후방+탑뷰 · 전방 듀얼 사이드 · 후방 듀얼 사이드 · 좌측 전방 · 좌측 후방 · 우측 전방 · 우측 후방 (10종)</p>
<div class="g2">{img("ui_2d_rear", "2D 후방 + 탑뷰")}{img("ui_2d_dual", "2D 전방 듀얼 사이드")}</div>

<h2>5. 설정</h2>
<h3>5-1. 모드 설정</h3>
<div class="g4">{img("set_2d3d", "뷰 모드 2D/3D")}{img("set_top", "탑뷰 위치 (왼쪽/오른쪽)")}{img("set_color", "차량 색상 · 투명도")}{img("set_blind", "블라인드 뷰")}</div>
<div class="g4">{img("set_lang", "언어 선택")}</div>
<h3>5-2. 시스템 설정</h3>
<div class="g3">{img("set_rec", "상시 녹화 설정/해제")}{img("set_time", "시간 설정")}{img("set_sd", "SD 카드 포맷 (녹화 영상 전체 삭제)")}</div>

<h2>6. 녹화 · 재생</h2>
{table(["항목", "사양"], [
    ["저장 장치", "MicroSD 카드"], ["영상 방식", "H.265, 2분 단위 파일"], ["녹화", "상시 녹화 · 주차/이벤트 녹화 · 30fps"],
    ["재생", "비디오 리스트 → 상시/수동(이벤트) 목록 → 4분할 또는 전·후·좌·우 채널별 재생"],
])}
<div class="g3">{img("vid_list", "비디오 리스트")}{img("vid_4ch", "4분할 재생")}{img("vid_front", "전방 채널 재생")}</div>

<h2>7. 객체 감지</h2>
<p>4채널 카메라 기반으로 <b>사람 · 차량</b>을 감지하여 2D / 3D / 탑뷰 화면에 표시하고, 모니터 스피커로 알람을 울립니다.</p>
<div class="g2">{img("od_3d", "3D 뷰 + 탑뷰 기반 객체 감지")}{img("od_2d", "2D 뷰 + 탑뷰 기반 객체 감지")}</div>

<h2>8. 모니터 KAM_2510 조작</h2>
<div class="fig-full">{img("mon_buttons")}</div>
{table(["버튼", "기능"], [
    ["⏻", "전원"], ["&lt; / &gt;", "숫자(값) 조정 − / +"],
    ["M", "설정 모드 진입 · PICTURE → GENERAL → SYSTEM 이동 / 종료"],
    ["OK", "각 설정 모드의 하위 목록 이동 (밝기 → 대비 → 채도 …)"], ["↩", "위로 이동"],
])}
<p class="small">5초 이상 조작하지 않으면 설정 모드가 종료됩니다.</p>

<h2>9. 안전 안내</h2>
<div class="callout red"><div class="ct">⚠ 운전 보조 장치입니다</div><p>화면만 의존하지 말고 반드시 육안·미러로 주변을 직접 확인하십시오.
렌즈가 오염되면 부드러운 천으로 닦고, 카메라에 충격이 있거나 위치가 바뀌면 재캘리브레이션하십시오.</p></div>
""")

ALL = [INSTALL, CALIB, FIRMWARE, OPERATION]
