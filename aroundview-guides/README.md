# KADEA K-FHDSVM 어라운드뷰 가이드 (영상 4편 + PDF 4종)

첨부 문서(KADEA K-FHDSVM 박스 매뉴얼 V01, 제어기 제품 사양서 Rev0.1, Calibration/펌웨어 업데이트 가이드)와
현대 유니버스 12m 카메라 장착 도면을 기준으로 만든 설치·사용 가이드입니다. 모두 무료 오픈소스 도구로 만들었습니다.

| # | 주제 | 영상 (1280×720 MP4) | 길이 | PDF (A4) |
|---|------|------|------|-----|
| 1 | 장착 | `video/KADEA_AVM_01_install.mp4` | 약 2분 51초 | `pdf/KADEA_AVM_01_install.pdf` |
| 2 | 캘리브레이션 | `video/KADEA_AVM_02_calibration.mp4` | 약 2분 24초 | `pdf/KADEA_AVM_02_calibration.pdf` |
| 3 | 펌웨어 업데이트 | `video/KADEA_AVM_03_firmware.mp4` | 약 1분 18초 | `pdf/KADEA_AVM_03_firmware.pdf` |
| 4 | 작동 설명 | `video/KADEA_AVM_04_operation.mp4` | 약 2분 11초 | `pdf/KADEA_AVM_04_operation.pdf` |

> ⚠ **카메라는 반드시 수직면에 부착** — 하향 42~45°는 카메라 하우징에 내장되어 있으므로 쐐기(웨지) 브래킷 없이
> 차체 수직면에 평평하게 밀착 부착합니다. (장착·캘리브레이션 영상/PDF에 모두 포함)

## 커넥터 — 무엇을 어디에 연결하나

| 본체 커넥터 | 연결 대상 | 구분 |
|---|---|---|
| **카메라 커넥터** (뒷면, 흰색 16핀) | 카메라 젠더 케이블 → 4갈래 FRONT/REAR/LEFT/RIGHT → 카메라 연장 케이블 → 각 카메라 | 필수 |
| **전원 커넥터** (앞면, 파란색 24핀) | 전원 케이블 (아래 결선) | 필수 |
| 전원 케이블의 **AHD/CVBS RCA** | 모니터 출력 연장 케이블의 노란 RCA | 필수 (RCA 모니터) |
| **USB** (앞면) | 모니터 터치 USB / 업데이트·캘리브레이션용 USB 메모리 (서로 다른 포트) | 필수 |
| HDMI (뒷면) | HDMI 입력 모니터 사용 시 | 선택 |
| MicroSD (앞면) | 녹화용 카드 | 권장 |
| DIP 스위치 (뒷면) | AHD/HDMI 출력 720p·1080p 설정 | 설정 |

전원 케이블 결선 (라벨 기준, 핀 번호는 매뉴얼 V01):

| 선 색 | 라벨 | 핀 | 연결 | 구분 |
|---|---|---|---|---|
| 노랑 | ACC | 23 | ACC(키 ON) 전원 + (5A 퓨즈 내장) | 필수 |
| 검정 | GND | 24 | 차체 접지 | 필수 |
| 갈색 | REVERSE | 13 | 후진등 + 신호 | 권장 |
| 파랑 | LEFT | 14 | 좌측 방향지시등 신호 | 권장 |
| 빨강 | RIGHT | 12 | 우측 방향지시등 신호 | 권장 |
| 흰/주황/검정 | CAN_H / CAN_L / CAN_GND | – | 차량 CAN 연동 시에만 | 선택 |
| 빨강/검정 | SPK+ / SPK GND | – | 외장 스피커 | 선택 |
| 3.5파이 | IR | 7/8/9 | IR 리시버 | 선택 |
| 초록/검정 | UART | 3/4/6 | 진단용 | 미사용 |

빨간선이 SPK+와 RIGHT 두 가지이므로 반드시 선 라벨로 구분하고, 사용하지 않는 선은 끝단을 절연합니다.

KAM_2510 모니터: ① USB(2m) → 본체 USB ② 노란 RCA → 본체 AHD/CVBS ③ 전원 연장 케이블 → 차량 전원.

### 원본 문서 간 차이 (제조사 확인 권장)
- **USB 포트**: Calibration/펌웨어 가이드는 USB 메모리를 *USB 2.0* 포트에 꽂으라고 하지만, 사양서 표에는
  *USB 3.0 HOST = 업데이트·캘리브레이션*, *USB 2.0 OTG = 모니터 터치*로 적혀 있습니다. 가이드에서는
  "USB 2.0 우선, 인식되지 않으면 다른 포트"로 안내했습니다.
- **전원 커넥터 핀**: 매뉴얼 V01은 12=RIGHT_IND, 14=LEFT_IND인데 사양서는 두 핀 모두 NC로 적혀 있습니다.
  SPK와 CAN 핀 배정도 두 문서가 다릅니다. 선 라벨을 기준으로 결선하세요.
- **카메라 커넥터 핀 번호**: 두 문서의 번호 체계가 다르지만, 젠더 케이블에 이미 결선되어 있어 현장 작업에는 영향이 없습니다.

## 영상에 음성(내레이션) 넣기 — 무료
이 작업 환경에서는 온라인 TTS에 접속할 수 없어서 영상은 **자막형(무음 트랙 포함)**으로 만들었습니다.
각 영상과 같은 이름의 `.srt` 파일이 내레이션 대본이며, 타이밍도 영상에 맞춰져 있습니다.
- **Vrew / CapCut (무료)**: 영상과 SRT를 불러온 뒤 "AI 목소리"로 한국어 더빙
- **직접 녹음**: SRT 문장을 읽어 녹음한 뒤 영상 편집기에서 합치기
- **YouTube 업로드**: 업로드 후 자막 파일로 `.srt`를 추가하면 자막 on/off 가능

## 다시 만들기 (내용 수정 후)
```bash
pip install playwright==1.56.0 imageio-ffmpeg pymupdf pillow   # 크로미움은 playwright 로 설치
sudo apt-get install fonts-nanum                                  # 한글 폰트
python3 build/build.py            # 영상 4개 + PDF 4개
python3 build/build.py video 02_calibration   # 특정 영상만
python3 build/build.py pdf        # PDF만
```
- 영상 슬라이드·자막: `build/videos.py`
- PDF 본문: `build/docs.py`
- 도식(수직 부착, 연결도)과 결선표: `build/common.py`
- 이미지: `assets/img/` (원본 매뉴얼에서 추출한 이미지)
