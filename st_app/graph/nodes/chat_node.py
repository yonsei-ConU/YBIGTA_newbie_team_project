"""
chat_node.py

일반 대화를 처리하는 노드.
나중에 LLM 호출을 붙여서 자유 대화를 처리할 수 있음.
"""

from st_app.utils.state import State

def chat_node(state: State) -> State:
    """
    사용자 입력을 받아 간단한 응답을 생성하고 상태에 추가함.
    초기 버전은 하드코딩된 간단한 답변을 사용.
    """
    user_msg = state["user_input"]
    reply = f"'{user_msg}' 라고 하셨군요. 저는 Chat Node입니다."

    # 대화 로그에 추가
    state["messages"].append({"role": "assistant", "content": reply})
    return state
