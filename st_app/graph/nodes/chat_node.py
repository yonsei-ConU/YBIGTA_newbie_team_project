"""
chat_node.py

일반 대화를 처리하는 노드.
LLM을 호출하여 자연스러운 대화를 처리함.
"""

from st_app.utils.state import State
from st_app.rag.llm import call_llm
from st_app.rag.prompt import create_general_chat_prompt


def chat_node(state: State) -> State:
    """
    사용자 입력을 받아 LLM으로 자연스러운 응답을 생성하고 상태에 추가함.
    """
    user_msg = state["user_input"]
    
    # 이전 대화 맥락 구성 (최근 3개 메시지만 포함)
    conversation_context = ""
    if len(state["messages"]) > 0:
        recent_messages = state["messages"][-3:]  # 최근 3개 메시지만
        conversation_context = "\n\n**이전 대화 맥락:**\n"
        for msg in recent_messages:
            role = "사용자" if msg["role"] == "user" else "어시스턴트"
            conversation_context += f"{role}: {msg['content']}\n"
    
    # 프롬프트 템플릿을 사용하여 대화 응답 생성
    try:
        # 이전 대화 맥락을 포함한 프롬프트 생성
        if conversation_context:
            enhanced_prompt = (
                f"{conversation_context}\n\n**현재 사용자 질문:** "
                f"{user_msg}\n\n위 대화 맥락을 고려하여 연속성 있게 답변해주세요."
            )
        else:
            enhanced_prompt = create_general_chat_prompt(user_msg)
        
        reply = call_llm(enhanced_prompt)
    except Exception as e:
        reply = f"죄송합니다. 응답 생성 중 오류가 발생했습니다: {e}"

    # 대화 로그에 추가
    state["messages"].append({"role": "assistant", "content": reply})
    return state
