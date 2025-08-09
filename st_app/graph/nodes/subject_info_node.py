"""
subject_info_node.py

리뷰 대상의 기본 정보를 반환하는 노드.
subjects.json 파일을 불러와 사용자 요청에 맞는 정보를 찾아 응답함.
"""

import json
from pathlib import Path
from st_app.utils.state import State
from st_app.rag.llm import call_llm
from st_app.rag.prompt import create_movie_info_prompt


SUBJECTS_PATH = (Path(__file__).parent.parent.parent / 
                 "db" / "subject_information" / "subjects.json")


def load_subjects() -> dict:
    """subjects.json 파일을 로드하여 딕셔너리로 반환함."""
    if SUBJECTS_PATH.exists():
        with open(SUBJECTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def subject_info_node(state: State) -> State:
    """
    user_input에서 주제를 추출하고, 해당 주제의 기본 정보를 찾아서 LLM으로 자연스럽게 응답함.
    """
    subjects = load_subjects()
    user_msg = state["user_input"]

    # 사용자 질문에서 주제 추출 및 정보 검색
    found_info = None
    found_key = None
    
    for key, info in subjects.items():
        if key.lower() in user_msg.lower():
            found_info = info
            found_key = key
            break

    if found_info:
        # 프롬프트 템플릿을 사용하여 정보 제공
        try:
            prompt = create_movie_info_prompt(user_msg, found_info)
            reply = call_llm(prompt)
        except Exception:
            # LLM 호출 실패 시 기본 정보만 제공
            info_text = "\n".join(f"{k}: {v}" for k, v in found_info.items())
            reply = f"[{found_key}] 정보:\n{info_text}"
    else:
        # 매칭 실패 시 LLM에게 도움 요청
        prompt = f"""사용자가 다음 질문을 했습니다: {user_msg}

사용자가 찾고 있는 정보가 subjects.json에 없는 것 같습니다.
사용자에게 친절하게 안내해주세요."""
        
        try:
            reply = call_llm(prompt)
        except Exception:
            reply = "죄송하지만 해당 대상의 정보를 찾지 못했습니다."

    state["messages"].append({"role": "assistant", "content": reply})
    return state
