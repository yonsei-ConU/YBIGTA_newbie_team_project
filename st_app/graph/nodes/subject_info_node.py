"""
subject_info_node.py

리뷰 대상의 기본 정보를 반환하는 노드.
subjects.json 파일을 불러와 사용자 요청에 맞는 정보를 찾아 응답함.
"""

import json
from pathlib import Path
from st_app.utils.state import State

SUBJECTS_PATH = Path(__file__).parent.parent.parent / "db" / "subject_information" / "subjects.json"

def load_subjects() -> dict:
    """subjects.json 파일을 로드하여 딕셔너리로 반환함."""
    if SUBJECTS_PATH.exists():
        with open(SUBJECTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def subject_info_node(state: State) -> State:
    """
    user_input에서 주제를 추출하고, 해당 주제의 기본 정보를 찾아서 반환함.
    현재 버전은 단순 키워드 매칭 기반.
    """
    subjects = load_subjects()
    user_msg = state["user_input"]

    # 예시: 단순 매칭 (나중에 LLM으로 개선 가능)
    for key, info in subjects.items():
        if key.lower() in user_msg.lower():
            reply = f"[{key}] 정보:\n" + "\n".join(f"{k}: {v}" for k, v in info.items())
            state["messages"].append({"role": "assistant", "content": reply})
            return state

    # 매칭 실패 시
    state["messages"].append({"role": "assistant", "content": "죄송하지만 해당 대상의 정보를 찾지 못했습니다."})
    return state
