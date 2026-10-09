"""4개 영상의 슬라이드 + 자막(내레이션) 정의.

각 슬라이드: dict(title=..., body=HTML, cap=자막 문장)
- 자막 길이에 따라 슬라이드 표시 시간이 자동 계산된다 (build.py).
"""
from common import img, ul, table, chip, svg_vertical, svg_connect, marked, POWER_ROWS, POWER_HEAD


def cover(no, title, sub, pic):
    return dict(cover=True, title=title, cap=sub, body=f"""
<div class="cover">
  <div class="cv-l">
    <div class="cv-no">PART {no} / 4</div>
    <h1>{title}</h1>
    <p>{sub}</p>
    <div class="cv-model">K-FHDSVM 4채널 FHD 어라운드뷰</div>
  </div>
  <div class="cv-r">{img(pic)}</div>
</div>""")


def ending(msg, nxt):
    return dict(cover=True, title="마무리", cap=msg, body=f"""
<div class="ending">
  {img("logo", cls="end-logo")}
  <h2>{msg}</h2>
  <p>{nxt}</p>
</div>""")


VERTICAL_NOTE = '<div class="warn big">⚠ 카메라는 <b>수직면</b>에 부착 · 경사면은 <b>동봉 고무 스페이서</b>로 최대한 수직에 맞추십시오.</div>'

# ============================================================================
# 1. 장착
# ============================================================================
INSTALL = dict(
    slug="01_install", title="어라운드뷰 장착", slides=[
        cover(1, "어라운드뷰 장착 방법", "카데아 K-FHDSVM 어라운드뷰의 장착 방법을 안내합니다.", "box_3d"),
        dict(title="구성품 확인", cap="먼저 구성품을 확인합니다. 본체, 카메라 4개, 카메라 젠더 케이블, 카메라 연장 케이블, 전원 케이블, 카메라 장착 브래킷, 마이크로 SD 카드입니다.",
             body=f"""<div class="grid4">
{img("box_top", "K-FHDSVM 본체")}{img("camera", "카메라 ×4")}{img("cam_gender", "카메라 젠더 케이블")}{img("ext_cable", "카메라 연장 케이블")}
{img("power_cable", "전원 케이블")}{img("bracket", "카메라 장착 브래킷")}{img("sdcard", "MicroSD 카드")}{img("mon", "KAM_2510 모니터(별도)")}
</div>"""),
        dict(title="작업 전 안전 주의사항", cap="작업 전에는 반드시 시동을 끄십시오. 본 제품은 DC 12V·24V 차량 전용이며, 커넥터는 무리한 힘을 주지 말고 연결부는 절연 테이프로 보호합니다.",
             body=f"""<div class="split"><div>{img("box_front")}</div><div>{ul([
                 "차량 시동을 <b>끄고</b> 장착 작업",
                 "<b>DC 12V / 24V</b> 차량 전용 (동작 전압 9~32V)",
                 "카메라 커넥터 연결부는 <b>절연 테이프</b>로 보호",
                 "커넥터를 무리하게 꺾거나 당기지 않기 (핀 파손 주의)",
                 "배선은 열원·가동부(조향·서스펜션) 피해서 고정",
             ], "big")}</div></div>"""),
        dict(title="카메라 장착 위치 (현대 유니버스 12m 예시)", cap="카메라는 전방, 후방, 좌측, 우측 네 곳에 장착합니다. 유니버스 12m 기준 좌표는 표와 같고, 위치 허용 오차는 ±30mm입니다.",
             body=f"""<div class="split wide-l"><div>{img("universe12m_mounting", cls="shadow tall")}</div><div>
{table(["카메라", "x (mm)", "y (mm)", "높이 z"], [
    ['<b style="color:#1c6dd0">FRONT</b>', "12,000", "0", "3,000"],
    ['<b style="color:#5c940d">REAR</b>', "0", "0", "3,210"],
    ['<b style="color:#e8590c">LEFT</b>', "6,000", "+1,248", "3,110"],
    ['<b style="color:#ae3ec9">RIGHT</b>', "6,000", "−1,248", "3,110"],
], "tbl")}
<p class="note">원점: 후면 중앙 · 지면 / 좌우 카메라는 차량 길이의 50% 지점<br><b style="color:#c92a2a">허용 오차 ±30mm (자동 보정되지 않음)</b></p></div></div>"""),
        dict(title="★ 가장 중요: 카메라는 수직면에 부착", cap="가장 중요한 점입니다. 카메라는 차체의 수직면에 밀착하여 부착합니다. 약 42~45°의 하향 각도가 하우징에 이미 내장되어 있습니다. 부착면이 경사져 있으면 동봉된 고무 스페이서를 사용해 최대한 수직에 맞춰 부착하세요.",
             body=f"""<div class="center">{svg_vertical(1080)}</div>{VERTICAL_NOTE}"""),
        dict(title="카메라 부착 요령", cap="전방과 후방 카메라는 차량 중심선에, 좌우 카메라는 차량 길이의 중앙에 맞춥니다. 카메라 상단 삼각형 표시가 위를 향하게 하고, 브래킷으로 수직면에 단단히 고정합니다.",
             body=f"""<div class="split"><div class="row2">{img("camera", "카메라")}{img("bracket", "브래킷 · 고무 스페이서")}</div><div>{ul([
                 "전방·후방: 차량 <b>중심선(CL)</b> 위",
                 "좌·우: 차량 길이의 <b>50%</b> 지점, 좌우 동일 높이",
                 "카메라 상단 <b>▼ 표시가 위</b>를 향하도록",
                 "<b>수직면에 밀착</b> · 경사면은 <b>고무 스페이서</b>로 수직 보정",
                 "렌즈 시야를 차체·미러가 가리지 않는지 확인",
             ], "big")}</div></div>"""),
        dict(title="본체 포트 구성", cap="본체 앞면에는 전원 커넥터, USB 2.0, USB 3.0, 마이크로 SD 슬롯이 있고, 뒷면에는 카메라 커넥터, HDMI, 딥 스위치가 있습니다.",
             body=f"""<div class="stack">{marked("box_front", [dict(x=.285, y=.42, w=.18, h=.40, kind="box", d="s", len=26, label="전원 24핀"), dict(x=.475, y=.45, w=.08, h=.26, kind="box", d="s", len=26, label="USB 2.0"), dict(x=.61, y=.45, w=.07, h=.26, kind="box", d="n", len=22, label="USB 3.0"), dict(x=.73, y=.48, w=.07, h=.18, kind="box", d="e", len=40, label="MicroSD")], width=560, pad=30)}
{marked("box_rear", [dict(x=.255, y=.42, w=.14, h=.42, kind="box", d="s", len=26, label="카메라 16핀"), dict(x=.46, y=.48, w=.10, h=.25, kind="box", d="s", len=26, label="HDMI"), dict(x=.79, y=.48, w=.08, h=.22, kind="box", d="e", len=40, label="DIP")], width=560, pad=30)}</div>"""),
        dict(title="전체 연결 개요", cap="전체 연결은 이렇습니다. 네 대의 카메라는 연장 케이블과 젠더 케이블을 거쳐 카메라 커넥터로, 전원 케이블은 전원 커넥터로, 모니터는 영상 출력과 USB로 연결합니다.",
             body=f'<div class="center">{svg_connect(1180)}</div>'),
        dict(title="카메라 연결", cap="카메라 젠더 케이블을 본체 뒷면의 16핀 카메라 커넥터에 딸깍 소리가 나도록 끼웁니다. 네 갈래의 FRONT, REAR, LEFT, RIGHT 라벨을 확인해 같은 위치 카메라의 연장 케이블과 연결합니다.",
             body=f"""<div class="split"><div class="row2">{img("cam_conn", "16핀 카메라 커넥터")}{img("cam_gender", "4갈래 젠더 케이블")}</div><div>{ul([
                 "젠더 케이블 → 본체 <b>카메라 커넥터(16핀)</b>",
                 "갈래 라벨 <b>FRONT / REAR / LEFT / RIGHT</b> 확인",
                 "연장 케이블 → 해당 위치 카메라(4핀 방수 커넥터)",
                 "라벨이 바뀌면 화면 위치가 뒤바뀜",
                 "방수 커넥터는 끝까지 체결 후 절연 테이프",
             ], "big")}</div></div>"""),
        dict(title="전원 케이블 결선", cap="전원 케이블은 노란선을 ACC 전원에, 검정선을 차체 접지에 연결합니다. 갈색은 후진 신호, 파랑과 빨강은 좌우 방향지시등 신호입니다. 선 색이 겹치는 경우가 있으니 라벨로 확인하세요.",
             body=f"""{table(POWER_HEAD, POWER_ROWS[:6], "tbl power")}<p class="note">* 모니터를 RCA(AHD/CVBS)로 연결하는 경우 필수 · 핀 번호는 KADEA K-FHDSVM 매뉴얼 V01 기준 · <b>빨강은 SPK+와 RIGHT 두 가지 — 반드시 라벨 확인</b></p>"""),
        dict(title="선택 배선", cap="CAN, 스피커, IR, UART 선은 선택 사항입니다. 사용하지 않는 선은 끝단을 절연 처리해 묶어 둡니다. HDMI 모니터를 사용할 경우 뒷면 HDMI 포트로 연결할 수 있습니다.",
             body=f"""<div class="split"><div>{img("wiring_diagram", cls="shadow")}</div><div>{table(POWER_HEAD[1:], [r[1:] for r in POWER_ROWS[6:]], "tbl sm")}
<p class="note">사용하지 않는 선은 <b>끝단 절연</b> 후 정리<br>HDMI 출력: 720p / 1080p (DIP 스위치 설정)</p></div></div>"""),
        dict(title="모니터(KAM_2510) 연결", cap="모니터는 세 가지를 연결합니다. 첫째 USB 케이블을 본체 USB 포트에, 둘째 노란색 영상 케이블을 본체 AHD/CVBS 출력에, 셋째 전원 연장 케이블을 차량 전원에 연결합니다.",
             body=f"""<div class="split"><div>{img("mon_diagram")}</div><div>{ul([
                 "① <b>USB(2m)</b> → 본체 USB 포트 (터치 조작)",
                 "② <b>노란 RCA</b> 출력 케이블 → 본체 <b>AHD/CVBS</b>",
                 "③ <b>빨간 전원잭</b> → 차량 전원",
                 "터치 USB와 업데이트용 USB 메모리는 <b>서로 다른 포트</b>에",
             ], "big")}<div class="row3">{img("mon_rca")}{img("mon_pwr")}{img("mon_bracket")}</div></div></div>"""),
        dict(title="MicroSD · DIP 스위치", cap="녹화용 마이크로 SD 카드를 앞면 슬롯에 끼웁니다. 뒷면 딥 스위치로 모니터 출력 해상도, 720p 또는 1080p를 모니터 사양에 맞게 설정합니다.",
             body=f"""<div class="split"><div class="row2">{img("sdcard")}{img("box_rear")}</div><div>{ul([
                 "MicroSD: 앞면 슬롯, 상시·이벤트 녹화용",
                 "DIP 스위치: AHD / HDMI 출력 <b>720p · 1080p</b> 선택",
                 "설정 변경 후 전원 재인가",
             ], "big")}</div></div>"""),
        dict(title="장착 후 점검", cap="시동을 켜면 약 3.5초 안에 부팅됩니다. 네 카메라 영상이 모두 나오는지, 전후좌우 위치가 맞는지 확인한 뒤 캘리브레이션을 진행합니다.",
             body=f"""<div class="split"><div>{img("ui_main", cls="shadow fill")}</div><div>{ul([
                 "ACC ON → 부팅 약 <b>3.5초</b>",
                 "4채널 영상이 모두 출력되는지",
                 "전방/후방/좌/우 위치가 바뀌지 않았는지",
                 "렌즈 오염·가림 없는지",
                 "다음 단계 → <b>캘리브레이션</b>",
             ], "big")}</div></div>"""),
        ending("장착이 끝났습니다. 다음 영상에서 캘리브레이션을 진행합니다.", "다음: PART 2 캘리브레이션"),
    ])

# ============================================================================
# 2. 캘리브레이션
# ============================================================================
CALIB = dict(
    slug="02_calibration", title="캘리브레이션", slides=[
        cover(2, "캘리브레이션 방법", "어라운드뷰 탑뷰 영상을 정확하게 맞추는 캘리브레이션 방법입니다.", "cal_screen"),
        dict(title="준비물", cap="준비물은 보정판 세트와 USB 메모리입니다. USB에는 MCS, LBS, MASTERCAL 세 가지 파일을 압축을 풀어 저장합니다. 파일은 차종별로 다르니 해당 차종 파일을 사용하세요.",
             body=f"""<div class="split"><div>{img("cal_files", "USB에 저장할 3개 파일 (예: HMC_Xcient_12m)", cls="fill")}</div><div>{ul([
                 "보정판(캘리브레이션 패턴) 세트",
                 "USB 메모리 — <b>.calibrationtool.mcs · .lbs · .mastercal</b>",
                 "압축 해제 후 저장 (폴더째 X)",
                 "<b>차종별 파일</b> 사용 (예시는 Xcient 12m)",
                 "줄자 (0.5m / 3m 측정)",
             ], "big")}</div></div>"""),
        dict(title="작업 장소 조건", cap="차량이 정차할 수 있고 패턴을 펼칠 공간이 필요합니다. 바닥은 굴곡 없이 수평이어야 하고, 조명이 고르며 주변에 간섭 물체가 없는 곳을 권장합니다.",
             body=f"""<div class="split"><div>{img("cal_points", cls="shadow fill")}</div><div>{ul([
                 "차량 정차 + 패턴 설치 공간 확보",
                 "바닥: <b>굴곡 없고 수평</b>",
                 "조명 균일, 강한 역광·그림자 X",
                 "패턴 주변 간섭 물체 X",
             ], "big")}</div></div>"""),
        dict(title="사전 확인: 카메라 부착 상태", cap="캘리브레이션 전에 카메라가 수직으로(경사면은 고무 스페이서로 보정) 규정 위치에 부착되어 있는지 확인합니다. 위치 오차 ±30mm를 넘거나 기울어진 장착은 캘리브레이션으로 보정되지 않습니다.",
             body=f"""<div class="center">{svg_vertical(1000)}</div>{VERTICAL_NOTE}"""),
        dict(title="Step 1. 보정판 설치", cap="전방과 후방 보정판은 차량 범퍼에서 패턴 시작점까지 0.5m 떨어뜨립니다. 좌우 보정판은 전방 패턴 시작점에서 사이드 패턴 시작점까지 3m 위치에 놓습니다.",
             body=f"""<div class="split"><div class="center">{img("cal_layout", cls="tall")}</div><div>{ul([
                 "전·후방 보정판: 범퍼 → 패턴 시작점 <b class='red'>0.5m</b>",
                 "좌·우 보정판: 전방 패턴 시작점 → 사이드 패턴 시작점 <b class='red'>3m</b>",
                 "패턴은 차량 중심선과 평행·대칭",
                 "패턴이 구겨지거나 들뜨지 않게",
             ], "big")}</div></div>"""),
        dict(title="Step 2. Calibration Tool 활성화", cap="전원을 끈 상태에서 세 파일이 담긴 USB를 본체 USB 2.0 포트에 연결합니다. 전원을 켜면 어라운드뷰 화면에서 캘리브레이션 툴이 활성화됩니다.",
             body=f"""<div class="split"><div>{img("box_top", "USB 2.0 포트 (가이드 기준)")}</div><div>{ul([
                 "① 전원 <b>OFF</b>",
                 "② 파일 3개 USB → <b>USB 2.0</b> 포트",
                 "③ 전원 <b>ON</b>",
                 "④ 어라운드뷰 화면에서 Calibration Tool 활성화",
             ], "big steps")}</div></div>"""),
        dict(title="Calibration 메뉴", cap="메뉴를 살펴봅니다. Cam view는 기본 보정 화면, Params는 차량 전장 입력, Apply는 저장, Smart는 상용차 모드, Detect는 보정 실행, Load Master는 USB의 차량 모델 불러오기입니다.",
             body=f"""<div class="split"><div>{marked("cal_menubar", [dict(x=.145, y=.17, w=.25, h=.20, kind="box", badge="1"), dict(x=.375, y=.17, w=.20, h=.20, kind="box", badge="2"), dict(x=.10, y=.40, w=.17, h=.18, kind="box", badge="3"), dict(x=.32, y=.41, w=.16, h=.18, kind="box", badge="4"), dict(x=.434, y=.81, w=.075, h=.20, kind="box", badge="5"), dict(x=.58, y=.82, w=.155, h=.20, kind="box", badge="6"), dict(x=.82, y=.82, w=.31, h=.20, kind="box", badge="7")], width=560, cap="Calibration 화면 좌측 상단 메뉴 (확대 재구성)")}</div><div>{table(["#", "버튼", "기능"], [
                 ["1", "Cam view", "기본 보정 화면"], ["2", "Params", "차량 전장(길이) 입력"], ["3", "Close", "Calibration Tool 닫기"],
                 ["4", "Apply", "적용 차량·Calibration 저장"], ["5", "Smart ▼ / 0x4", "상용차 Smart / 승용차 0x4"],
                 ["6", "Detect", "Calibration 실행"], ["7", "Load Master", "USB의 차량 모델 불러오기"]], "tbl sm")}</div></div>"""),
        dict(title="자동 보정 ① 모드·차량 모델", cap="먼저 좌측 상단 선택 상자에서 0x4를 Smart로 바꿉니다(상용차). 그다음 Load Master를 누르면 우측 차량 모델이 USB의 차종으로 바뀝니다.",
             body=f"""<div class="split"><div>{marked("cal_menubar", [
                 dict(x=.434, y=.81, w=.075, h=.20, kind="box", d="s", len=34, label="A. ▼ → Smart 선택"),
                 dict(x=.82, y=.82, w=.31, h=.20, kind="box", d="s", len=34, label="B. Load Master")], width=560, pad=50)}</div><div>{ul([
                 "A. 좌측 상단 ▽ → <b>0x4 → Smart</b> (상용차)",
                 "B. <b>Load Master</b> → 우측 차량 모델 변경 확인",
             ], "big steps")}</div></div>"""),
        dict(title="자동 보정 ② 차량 길이 입력", cap="상단의 Params로 들어가 Vehicle Length에 실제 차량 길이를 입력합니다. 터치 드래그로도 조절할 수 있습니다. 유니버스 12m라면 12,000mm입니다.",
             body=f"""<div class="split"><div class="center">{marked("cal_paramsbar", [
                 dict(x=.197, y=.13, w=.13, h=.22, kind="box", d="e", len=120, label="① Params"),
                 dict(x=.55, y=.80, w=.30, h=.22, kind="box", d="s", len=30, label="② 차량 길이 입력 (mm)")], width=580, pad=40)}
{marked("cal_params", [dict(x=.36, y=.38, w=.42, h=.30, kind="box", d="s", len=40, label="터치 드래그로 조절")], width=370, pad=20, cap="실제 화면")}</div><div>{ul([
                 "C. <b>Params</b> → <b>Vehicle Length</b>",
                 "실제 차량 전장 입력 (mm)",
                 "터치 드래그로 길이 조절 가능",
                 "예) 유니버스 12m → <b>12000</b>",
             ], "big steps")}</div></div>"""),
        dict(title="자동 보정 ③ Detect 실행", cap="Detect를 누르면 보정이 시작되며 전방, 후방, 좌측, 우측 순서로 자동 진행됩니다. Cam view로 돌아온 뒤 Detect를 실행합니다.",
             body=f"""<div class="split"><div>{marked("cal_menubar", [
                 dict(x=.58, y=.82, w=.155, h=.20, kind="box", d="s", len=34, label="D. Detect → 보정 시작"),
                 dict(x=.145, y=.17, w=.25, h=.20, kind="box", d="n", len=30, label="E. Cam view 복귀 → Detect")], width=560, pad=55)}</div><div>{ul([
                 "D. <b>Detect</b> → 보정 시작",
                 "Front → Rear → Left → Right 자동 진행",
                 "E. <b>Cam view</b> 복귀 후 <b>Detect</b> 실행",
             ], "big steps")}</div></div>"""),
        dict(title="자동 보정 ④ 저장 · 재부팅", cap="성공하면 APPLY를 눌러 저장하고, 실패하면 보정판 위치와 조명을 확인한 뒤 다시 Detect를 실행합니다. 성공 후에는 반드시 재부팅합니다.",
             body=f"""<div class="center">{marked("cal_menubar", [dict(x=.32, y=.41, w=.16, h=.18, kind="box", d="e", len=330, label="성공 → APPLY 저장"), dict(x=.58, y=.82, w=.155, h=.20, kind="box", d="s", len=26, label="실패 → 다시 Detect")], width=470, pad=34)}</div>
<div class="flow">
<div class="fbox ok">성공 → <b>APPLY</b><br>저장</div><div class="farrow">→</div>
<div class="fbox">재부팅</div><div class="farrow">→</div><div class="fbox">탑뷰 확인</div></div>
<div class="flow"><div class="fbox ng">실패 → 다시 <b>Detect</b></div><div class="farrow">→</div><div class="fbox ng">반복 실패 → 보정판 거리·조명 재확인</div></div>"""),
        dict(title="최종 확인", cap="USB를 제거하고 탑뷰에서 차량 주변 선과 패턴이 카메라 경계에서 자연스럽게 이어지는지 확인합니다. 어긋나면 보정판 위치를 다시 확인하고 자동 보정을 반복합니다.",
             body=f"""<div class="split"><div>{marked("ui_3d_car", [dict(x=.80, y=.53, w=.30, h=.86, kind="box", d="w", len=60, label="탑뷰 경계 확인")], width=580)}</div><div>{ul([
                 "USB 메모리 제거",
                 "탑뷰 경계에서 패턴·선이 <b>이어지는지</b>",
                 "어긋나면 보정판 위치 확인 후 자동 보정 반복",
                 "카메라 위치를 옮겼다면 <b>재보정</b> 필요",
             ], "big")}</div></div>"""),
        ending("캘리브레이션이 완료되었습니다.", "다음: PART 3 펌웨어 업데이트"),
    ])

# ============================================================================
# 3. 펌웨어 업데이트
# ============================================================================
FIRMWARE = dict(
    slug="03_firmware", title="펌웨어 업데이트", slides=[
        cover(3, "펌웨어 업데이트 방법", "USB 메모리로 K-FHDSVM 펌웨어를 업데이트하는 방법입니다.", "upd_run"),
        dict(title="준비물", cap="USB 메모리와 펌웨어 파일 update-2100r.iu4를 준비합니다. 파일은 USB의 최상위 위치에 복사합니다.",
             body=f"""<div class="split"><div>{img("box_top", "USB 2.0 포트 (가이드 기준)")}</div><div>{ul([
                 "USB 메모리",
                 "펌웨어 파일 <code>update-2100r.iu4</code>",
                 "USB <b>최상위(루트)</b>에 복사",
                 "차량 전원(ACC) 유지 — 업데이트 중 끄지 않기",
             ], "big")}</div></div>"""),
        dict(title="① USB 연결", cap="어라운드뷰가 켜진 상태에서 펌웨어 파일이 들어 있는 USB를 본체의 USB 2.0 포트에 연결합니다. 모니터 터치 USB는 다른 포트에 그대로 둡니다.",
             body=f"""<div class="split"><div>{img("box_front", "앞면 USB 2.0 / USB 3.0")}</div><div>{ul([
                 "펌웨어 USB → <b>USB 2.0</b> 포트",
                 "모니터 터치 USB는 그대로 (다른 포트)",
                 "인식 안 되면 다른 USB 포트로 재시도",
             ], "big")}</div></div>"""),
        dict(title="② S/W Information 열기", cap="어라운드뷰 화면 왼쪽 메뉴의 SETTING 버튼을 눌러 설정으로 들어간 뒤 S/W Information(소프트웨어 정보) 창을 엽니다.",
             body=f"""<div class="split"><div>{marked("ui_main", [dict(x=.05, y=.90, d="e", len=70, label="① SETTING")], width=580, cap="왼쪽 메뉴 SETTING")}</div><div>{marked("set_mode_nobar", [dict(x=.20, y=.90, w=.32, h=.17, kind="box", d="e", len=90, label="② 소프트웨어 정보")], width=580, cap="설정 화면")}</div></div>
{ul(["① 왼쪽 메뉴 <b>SETTING</b> → ② <b>S/W Information</b> (소프트웨어 정보)"], "inline")}"""),
        dict(title="③ 숨은 메뉴: Version 위 5번 터치", cap="“Version” 글자에서 V 바로 위쪽 영역을 5번 연속으로 터치합니다. 그러면 좌측 메뉴 가장 아래에 Update 버튼이 나타납니다.",
             body=f"""<div class="split"><div>{marked("sw_info", [dict(x=.475, y=.175, w=.08, h=.09, kind="box", d="e", len=150, label="V 바로 위 5번 터치")], width=580, cap="“Version” 의 V 바로 위 → 5번 연속 터치")}</div><div>{marked("sw_update", [dict(x=.16, y=.92, w=.27, h=.13, kind="box", d="e", len=110, label="Update 생성")], width=580, cap="좌측 메뉴 하단에 Update 생성")}</div></div>"""),
        dict(title="④ Update 실행", cap="Update 버튼을 누르면 바로 업데이트가 시작됩니다. SVM UPDATE 화면이 나오는 동안 절대 전원을 끄지 마십시오.",
             body=f"""<div class="split"><div>{marked("sw_info_ko", [dict(x=.17, y=.91, w=.28, h=.13, kind="box", d="e", len=110, label="업데이트 누르기")], width=580, cap="한글 화면: 좌측 하단 ‘업데이트’")}</div><div>{img("upd_run", "SVM UPDATE — 전원 끄지 마세요", cls="shadow fill")}</div></div>
<div class="warn">⚠ 업데이트 중 전원(ACC) OFF · USB 제거 금지</div>"""),
        dict(title="⑤ 완료 후 재시작", cap="UPDATE COMPLETE 문구가 나오면 USB를 제거하고 본체 전원을 껐다가 다시 켭니다.",
             body=f"""<div class="split"><div>{img("upd_done", "UPDATE COMPLETE", cls="shadow fill")}</div><div>{ul([
                 "“UPDATE COMPLETE” 확인",
                 "USB 메모리 <b>제거</b>",
                 "본체 전원 <b>OFF → ON</b>",
             ], "big steps")}</div></div>"""),
        dict(title="⑥ 버전 확인", cap="재부팅 후 소프트웨어 정보 창에서 버전이 바뀌었는지 확인합니다. 탑뷰 정합이 틀어졌다면 캘리브레이션을 다시 진행합니다.",
             body=f"""<div class="split"><div>{marked("sw_info_ko", [dict(x=.17, y=.75, w=.28, h=.13, kind="box", d="e", len=110, label="소프트웨어 정보"),
                 dict(x=.80, y=.95, w=.36, h=.12, kind="box", d="n", len=60, label="버전 확인")], width=580)}</div><div>{ul([
                 "S/W 정보에서 <b>버전</b> 확인",
                 "영상 4채널 정상 출력 확인",
                 "탑뷰 정합 이상 시 → 캘리브레이션",
             ], "big")}</div></div>"""),
        ending("펌웨어 업데이트가 완료되었습니다.", "다음: PART 4 작동 설명"),
    ])

# ============================================================================
# 4. 작동 설명
# ============================================================================
OPERATION = dict(
    slug="04_operation", title="작동 설명", slides=[
        cover(4, "어라운드뷰 작동 설명", "K-FHDSVM 어라운드뷰의 화면 구성과 주요 기능을 소개합니다.", "ui_3d_car"),
        dict(title="시스템 개요", cap="시동을 켜면 약 3.5초 안에 부팅되고, 네 대의 FHD 카메라 영상을 합성해 탑뷰, 3D뷰, 2D뷰를 보여줍니다. 녹화와 사람, 차량 감지 기능도 제공합니다.",
             body=f"""<div class="split"><div>{img("ui_main", cls="shadow fill")}</div><div>{ul([
                 "부팅 약 <b>3.5초</b> · 지연 200ms 이하",
                 "FHD 1080p 카메라 <b>4채널</b>",
                 "<b>3D / 2D / 탑뷰</b> — 모니터 터치 조작",
                 "MicroSD <b>상시·이벤트 녹화</b>",
                 "<b>사람·차량 감지</b> 알림",
             ], "big")}</div></div>"""),
        dict(title="메인 화면 구성", cap="왼쪽 메뉴에는 뒤로, 홈, 3D 뷰, 주차, 녹화, 설정 버튼이 있습니다. 설정 버튼을 누르면 모드 설정, 시스템 설정, 비디오 리스트, 소프트웨어 정보 메뉴가 나옵니다.",
             body=f"""<div class="split"><div>{marked("ui_main", [dict(x=.05, y=.08, d="e", len=50, label="뒤로"),
                 dict(x=.05, y=.25, d="e", len=50, label="홈"), dict(x=.05, y=.42, d="e", len=50, label="3D 뷰"),
                 dict(x=.05, y=.58, d="e", len=50, label="주차"), dict(x=.05, y=.74, d="e", len=50, label="녹화"),
                 dict(x=.05, y=.90, d="e", len=50, label="설정")], width=580, cap="좌측 메뉴")}</div><div>{marked("set_mode_nobar", [dict(x=.20, y=.55, w=.38, h=.88, kind="box")], width=540, cap="설정 화면")}
{ul(["BACK · HOME · 3D VIEW · PARKING · REC · SETTING", "설정: 모드 설정 · 시스템 설정 · 비디오 리스트 · 소프트웨어 정보"], "sm")}</div></div>"""),
        dict(title="3D 뷰", cap="3D 뷰에서는 전방, 좌측 후방, 우측 후방, 후방, 트레일러, 전방 세차 뷰를 볼 수 있습니다. 설정에서 3D 모드를 선택하고 화면을 터치해 조작합니다.",
             body=f"""<div class="grid3">{marked("ui_3d", [dict(x=.05, y=.42, d="e", len=44, label="3D 뷰")], width=370, cap="3D 전방")}{img("ui_3d_rl", "3D 좌측 후방")}{img("ui_trailer", "3D 트레일러")}</div>
<p class="note center">전방 · 좌측 후방 · 우측 후방 · 후방 · 후방 트레일러 · 전방 세차 뷰</p>"""),
        dict(title="3D 와이드 · 회전 뷰", cap="확대 버튼을 누르면 더 넓은 와이드 뷰로 바뀝니다. 회전 아이콘을 누르면 차량 주위를 시계 방향으로 돌아가며 12시, 10시, 9시 방향 등에서 볼 수 있습니다.",
             body=f"""<div class="split"><div>{marked("ui_wide", [dict(x=.55, y=.09, d="sw", len=70, label="확대 버튼")], width=580, cap="3D 와이드 뷰 (확대 버튼)")}</div><div>{marked("ui_rot", [dict(x=.685, y=.5, d="w", len=60, label="회전")], width=580, cap="3D 회전 뷰 (회전 아이콘)")}</div></div>"""),
        dict(title="2D 뷰", cap="2D 모드에서는 전방 와이드, 전방과 탑뷰, 후방 와이드, 후방과 탑뷰, 듀얼 사이드, 좌우 전후방 뷰 등 열 가지 화면을 사용할 수 있습니다.",
             body=f"""<div class="split"><div>{marked("ui_2d_rear", [dict(x=.32, y=.85, w=.30, h=.26, kind="box", d="ne", len=60, label="주차 가이드선")], width=580, cap="2D 후방 + 탑뷰 (주차 가이드선)")}</div><div>{ul([
                 "전방 와이드 / 전방 + 탑뷰", "후방 와이드 / 후방 + 탑뷰",
                 "전방·후방 듀얼 사이드", "좌측 전방 · 좌측 후방", "우측 전방 · 우측 후방",
             ], "big")}</div></div>"""),
        dict(title="설정 ① 모드 설정", cap="설정의 모드 설정에서는 2D와 3D 뷰 모드, 탑뷰 위치, 차량 색상과 투명도, 블라인드 뷰, 언어를 바꿀 수 있습니다.",
             body=f"""<div class="grid2">{marked("set_2d3d", [dict(x=.30, y=.5, d="w", len=50, label="2D"), dict(x=.69, y=.5, d="e", len=50, label="3D")], width=420, cap="뷰 모드 2D/3D")}{marked("set_top", [dict(x=.30, y=.5), dict(x=.69, y=.5, d="e", len=50, label="선택")], width=420, cap="탑뷰 위치")}{marked("set_color", [dict(x=.18, y=.5, d="sw", len=40, label="색상"), dict(x=.82, y=.5, w=.08, h=.32, kind="box", d="e", len=40, label="투명도")], width=420, cap="차량 색상·투명도")}{marked("set_lang", [dict(x=.69, y=.5, d="e", len=50, label="한국어")], width=420, cap="언어 선택")}</div>"""),
        dict(title="설정 ② 시스템 설정", cap="시스템 설정에서는 상시 녹화 켜기와 끄기, 시간 설정, SD 카드 포맷을 할 수 있습니다. 포맷하면 저장된 영상이 모두 삭제되니 주의하세요.",
             body=f"""<div class="grid3">{marked("set_rec", [dict(x=.30, y=.5, d="n", len=40, label="설정"), dict(x=.69, y=.5, d="n", len=40, label="해제")], width=370, pad=34, cap="상시 녹화 설정/해제")}{marked("set_time", [dict(x=.50, y=.44, w=.76, h=.30, kind="box", d="n", len=40, label="▲▼ 조정")], width=370, pad=34, cap="시간 설정")}{marked("set_sd", [dict(x=.30, y=.75, d="n", len=44, label="확인 = 포맷")], width=370, pad=34, cap="SD 카드 포맷")}</div>
<div class="warn">⚠ SD 포맷 시 녹화 영상 전체 삭제</div>"""),
        dict(title="녹화 영상 재생", cap="비디오 리스트에서 상시 녹화와 이벤트 녹화 파일을 고를 수 있습니다. 4분할 화면이나 전방, 후방, 좌측, 우측 카메라별로 재생합니다.",
             body=f"""<div class="split"><div>{marked("vid_4ch", [dict(x=.054, y=.59, d="e", len=60, label="4분할"), dict(x=.45, y=.81, w=.44, h=.14, kind="box", d="n", len=46, label="재생 버튼")], width=580, cap="4분할 재생")}</div><div>{img("vid_front", "채널별(전방) 재생", cls="shadow fill")}
{ul(["H.265 · 2분 단위 파일", "상시 녹화 / 이벤트 녹화 목록"], "sm")}</div></div>"""),
        dict(title="객체 감지", cap="사람과 차량이 감지되면 2D, 3D, 탑뷰 화면에 표시되고 모니터 스피커로 알람이 울립니다.",
             body=f"""<div class="split"><div>{marked("od_3d", [dict(x=.12, y=.40, w=.22, h=.34, kind="box", d="s", len=50, label="차량 감지 표시")], width=580, cap="3D + 탑뷰 감지")}</div><div>{marked("od_2d", [dict(x=.575, y=.50, w=.11, h=.60, kind="box", d="w", len=50, label="사람 감지")], width=580, cap="2D + 탑뷰 감지")}</div></div>"""),
        dict(title="모니터 KAM_2510 조작", cap="모니터 버튼은 전원, <, >, M, OK, 뒤로 버튼입니다. M 버튼으로 PICTURE, GENERAL, SYSTEM 설정을 오가며 밝기와 대비 등을 조절합니다.",
             body=f"""<div class="center">{marked("mon_buttons", [dict(x=.60, y=.5, w=.08, h=.75, kind="box", d="s", len=22, label="M 메뉴"), dict(x=.755, y=.5, w=.10, h=.75, kind="box", d="s", len=22, label="OK 선택")], width=560, pad=0)}</div><div class="split"><div>{img("mon_osd")}</div><div>{ul([
                 "⏻ 전원 · &lt; &gt; 값 조정",
                 "<b>M</b>: PICTURE → GENERAL → SYSTEM",
                 "<b>OK</b>: 하위 항목 이동 · ↩ 위로",
                 "5초 이상 무조작 시 설정 종료",
             ], "sm")}</div></div>"""),
        dict(title="안전 운행 안내", cap="어라운드뷰는 운전 보조 장치입니다. 화면만 믿지 말고 반드시 직접 주변을 확인하세요. 렌즈는 부드러운 천으로 깨끗하게 유지합니다.",
             body=f"""<div class="split"><div>{img("ui_main", cls="shadow fill")}</div><div>{ul([
                 "운전 <b>보조</b> 장치 — 반드시 직접 확인",
                 "렌즈 오염·물기 → 부드러운 천으로 청소",
                 "카메라 충격·위치 변경 시 <b>재보정</b>",
                 "이상 시 KADEA 서비스 문의",
             ], "big")}</div></div>"""),
        ending("카데아 어라운드뷰와 함께 안전 운행하세요.", "KADEA K-FHDSVM"),
    ])

ALL = [INSTALL, CALIB, FIRMWARE, OPERATION]
