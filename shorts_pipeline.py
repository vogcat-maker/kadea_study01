"""기차 여행 쇼츠 자동 생성 파이프라인.

1. Claude로 60초 쇼츠 대본 + 장면별 Higgsfield 프롬프트를 생성 (구조화 출력으로 JSON 보장)
2. 장면마다 Higgsfield로 9:16 영상 생성을 요청하고 완료될 때까지 폴링
3. 장면마다 ElevenLabs로 한국어 내레이션(voiceover_kr)을 MP3로 생성
4. 기획안(plan.json)과 장면별 영상(MP4)·음성(MP3)을 output/<노선>/ 아래에 저장

사용법:
    export ANTHROPIC_API_KEY=...
    export HIGGSFIELD_API_KEY=...
    export ELEVENLABS_API_KEY=...
    python shorts_pipeline.py "스위스 빙하 특급 (Glacier Express)"
    python shorts_pipeline.py "시베리아 횡단열차" --plan-only   # 영상 생성 없이 기획안만
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import anthropic
import requests
from pydantic import BaseModel, Field

CLAUDE_MODEL = "claude-opus-5-5"

# Higgsfield 엔드포인트는 계정의 공식 API 문서에 맞게 환경 변수로 지정한다.
# {task_id} 자리표시자는 상태 조회 URL에 그대로 치환된다.
HIGGSFIELD_GENERATE_URL = os.environ.get(
    "HIGGSFIELD_GENERATE_URL", "https://api.higgsfield.ai/v1/video/generate"
)
HIGGSFIELD_STATUS_URL = os.environ.get(
    "HIGGSFIELD_STATUS_URL", "https://api.higgsfield.ai/v1/video/status/{task_id}"
)
# ElevenLabs TTS 설정
ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
ELEVENLABS_MODEL = "eleven_multilingual_v2"
# 차분하고 신뢰감 있는 다큐멘터리 내레이터 톤의 목소리 ID.
# 기본값은 'Antoni'이며, Voice Library에서 고른 성우 목소리 ID로 ELEVENLABS_VOICE_ID를 지정해 바꿀 수 있다.
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "ErXwobaYiN019PkySvjV")
ELEVENLABS_VOICE_SETTINGS = {
    "stability": 0.4,  # 낮을수록 억양·감정 표현이 풍부해진다
    "similarity_boost": 0.75,  # 높을수록 원래 목소리에 가깝고 선명해진다
}

POLL_INTERVAL_SEC = 5
POLL_TIMEOUT_SEC = 15 * 60

SYSTEM_PROMPT = """너는 세계 최고의 여행 다큐멘터리 쇼츠(Shorts) 제작자이자 비디오 프롬프트 엔지니어링 전문가야.
사용자가 특정 '기차 여행 노선'을 주면, 60초 분량의 쇼츠 대본과 Higgsfield AI 비디오 생성을 위한 장면별 프롬프트를 만든다.

[제약 사항]
1. 대본은 시청자의 시선을 끄는 후킹으로 시작할 것. 첫 장면 내레이션에서 3초 안에 호기심을 자극한다.
2. 각 장면(Scene)은 3~5초 분량으로 기획하고, 모든 장면의 합이 약 60초가 되게 한다 (보통 12~15개 장면).
   내레이션은 해당 장면 길이 안에 자연스럽게 읽힐 분량(한국어 기준 초당 약 4~5음절)으로 쓴다.
3. Higgsfield 프롬프트는 영어로 작성하며, 카메라 움직임, 피사체, 조명, 환경, 해상도를 매우 구체적으로 묘사할 것.
   (예: "Cinematic drone shot, tracking a red vintage train moving through a snow-covered mountain valley, photorealistic, 4k, volumetric lighting")
   쇼츠용 세로 화면(vertical 9:16 framing)을 전제로 구도를 잡는다.
4. 노선의 실제 지리, 대표 구간, 열차의 실제 외형과 색상을 사실에 맞게 반영한다. 확실하지 않은 수치나 사실은 지어내지 않는다.
5. 마지막 장면은 여운이 남는 마무리나 시청자 행동 유도(구독, 저장 등)로 끝낸다."""


class Scene(BaseModel):
    scene_number: int
    duration_sec: int = Field(description="장면 길이(초), 3~5")
    voiceover_kr: str
    higgsfield_prompt_en: str


class ShortsPlan(BaseModel):
    title: str
    scenes: list[Scene]


# 1. Claude를 통해 대본 및 비디오 프롬프트 생성
def generate_script_and_prompts(train_route: str) -> ShortsPlan:
    client = anthropic.Anthropic()  # ANTHROPIC_API_KEY 환경 변수 사용

    response = client.messages.parse(
        model=CLAUDE_MODEL,
        max_tokens=16000,
        thinking={"type": "adaptive"},
        output_config={"effort": "medium"},
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"이번에 제작할 기차 여행 노선은 '{train_route}'야. 쇼츠 기획안을 만들어줘.",
            }
        ],
        output_format=ShortsPlan,
    )

    if response.stop_reason == "refusal":
        raise RuntimeError(f"Claude가 요청을 거절했습니다: {response.stop_details}")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("응답이 max_tokens에서 잘렸습니다. max_tokens를 늘려 다시 시도하세요.")

    return response.parsed_output


# 2. Higgsfield API를 통해 영상 생성
def generate_video_with_higgsfield(prompt: str, duration: int, api_key: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "aspect_ratio": "9:16",  # 쇼츠용 세로 비율
        "duration": duration,
        "motion_intensity": 0.6,
    }

    print(f"🎥 Higgsfield 영상 생성 요청 중: {prompt[:50]}...")
    response = requests.post(HIGGSFIELD_GENERATE_URL, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    task_id = response.json().get("task_id")
    if not task_id:
        raise RuntimeError(f"task_id가 응답에 없습니다: {response.text[:200]}")

    # 폴링(Polling) 방식으로 완료 대기 (무한 대기 방지용 타임아웃 포함)
    status_url = HIGGSFIELD_STATUS_URL.format(task_id=task_id)
    deadline = time.monotonic() + POLL_TIMEOUT_SEC
    while time.monotonic() < deadline:
        status_resp = requests.get(status_url, headers=headers, timeout=30)
        status_resp.raise_for_status()
        status_data = status_resp.json()

        status = status_data.get("status")
        if status == "completed":
            return status_data["video_url"]
        if status == "failed":
            raise RuntimeError(f"영상 생성 실패 (task_id={task_id}): {status_data}")

        time.sleep(POLL_INTERVAL_SEC)

    raise TimeoutError(f"영상 생성이 {POLL_TIMEOUT_SEC}초 안에 끝나지 않았습니다 (task_id={task_id})")


# 3. ElevenLabs API를 통해 내레이션 음성(MP3) 생성
def generate_audio(text: str, dest: Path, api_key: str) -> Path:
    url = ELEVENLABS_TTS_URL.format(voice_id=ELEVENLABS_VOICE_ID)
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": ELEVENLABS_MODEL,
        "voice_settings": ELEVENLABS_VOICE_SETTINGS,
    }

    print(f"🎙️ ElevenLabs 음성 생성 중: {text[:30]}...")
    response = requests.post(
        url,
        json=payload,
        headers=headers,
        params={"output_format": "mp3_44100_128"},
        timeout=120,
    )
    if response.status_code != 200:
        raise RuntimeError(f"음성 생성 실패 ({response.status_code}): {response.text[:300]}")
    dest.write_bytes(response.content)
    return dest


def download_file(url: str, dest: Path) -> None:
    with requests.get(url, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                f.write(chunk)


def slugify(text: str) -> str:
    slug = re.sub(r"[^\w가-힣]+", "_", text).strip("_")
    return slug[:60] or "route"


# 4. 메인 파이프라인 실행
def main() -> int:
    parser = argparse.ArgumentParser(description="기차 여행 쇼츠 대본 + Higgsfield 영상 생성")
    parser.add_argument("route", nargs="?", default="스위스 빙하 특급 (Glacier Express)")
    parser.add_argument("--plan-only", action="store_true", help="영상 생성 없이 기획안 JSON만 생성")
    parser.add_argument("--out", default="output", help="결과 저장 폴더")
    args = parser.parse_args()

    higgsfield_key = os.environ.get("HIGGSFIELD_API_KEY")
    elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
    if not args.plan_only:
        missing = [
            name
            for name, value in (("HIGGSFIELD_API_KEY", higgsfield_key), ("ELEVENLABS_API_KEY", elevenlabs_key))
            if not value
        ]
        if missing:
            print(f"환경 변수가 없습니다: {', '.join(missing)}. --plan-only로 기획안만 만들 수 있습니다.")
            return 1

    out_dir = Path(args.out) / slugify(args.route)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{args.route}] 기획을 시작합니다...")
    try:
        plan = generate_script_and_prompts(args.route)
    except anthropic.APIError as e:
        print(f"Claude API 오류: {e}")
        return 1

    plan_path = out_dir / "plan.json"
    plan_path.write_text(json.dumps(plan.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(s.duration_sec for s in plan.scenes)
    print(f"\n제목: {plan.title}  ({len(plan.scenes)}개 장면, 약 {total}초)")
    print(f"기획안 저장: {plan_path}")

    if args.plan_only:
        print(json.dumps(plan.model_dump(), ensure_ascii=False, indent=2))
        return 0

    failed = []
    for scene in plan.scenes:
        print(f"\n--- Scene {scene.scene_number} ({scene.duration_sec}s) ---")
        print(f"내레이션: {scene.voiceover_kr}")
        prefix = out_dir / f"scene_{scene.scene_number:02d}"

        # 영상(MP4): 한 장면이 실패해도 음성과 나머지 장면은 계속 생성한다
        duration = min(max(scene.duration_sec, 3), 5)
        try:
            video_url = generate_video_with_higgsfield(scene.higgsfield_prompt_en, duration, higgsfield_key)
            download_file(video_url, prefix.with_suffix(".mp4"))
            print(f"✅ 영상 저장: {prefix.with_suffix('.mp4')}")
        except (requests.RequestException, RuntimeError, TimeoutError) as e:
            print(f"❌ Scene {scene.scene_number} 영상 실패: {e}")
            failed.append(f"scene {scene.scene_number} video")

        # 음성(MP3)
        try:
            generate_audio(scene.voiceover_kr, prefix.with_suffix(".mp3"), elevenlabs_key)
            print(f"✅ 음성 저장: {prefix.with_suffix('.mp3')}")
        except (requests.RequestException, RuntimeError) as e:
            print(f"❌ Scene {scene.scene_number} 음성 실패: {e}")
            failed.append(f"scene {scene.scene_number} audio")

    if failed:
        print(f"\n실패한 항목: {failed}")
        return 1
    print("\n모든 장면 생성 완료")
    return 0


if __name__ == "__main__":
    sys.exit(main())
