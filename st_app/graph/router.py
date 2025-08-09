"""
router.py

이 모듈은 LangGraph의 라우팅 로직을 정의함.
사용자의 입력을 LLM 또는 간단한 규칙 기반으로 분류하여
적절한 노드(chat, subject, review)로 연결함.
"""

from langgraph.graph import StateGraph, END
from st_app.utils.state import State
from st_app.graph.nodes.chat_node import chat_node
from st_app.graph.nodes.subject_info_node import subject_info_node
from st_app.graph.nodes.rag_review_node import rag_review_node

def decide_route(state: State) -> str:
    """
    현재 상태에서 user_input을 확인하고 라우트 이름을 반환함.
    초기 버전은 키워드 매칭 기반이고, 나중에 LLM 호출로 대체 가능.
    """
    user_msg = state["user_input"].lower()
    if "리뷰" in user_msg or "후기" in user_msg:
        return "rag_review_node"
    elif "정보" in user_msg or "스펙" in user_msg:
        return "subject_info_node"
    else:
        return "chat_node"

def router_node(state: State) -> State:
    """
    라우터 노드: decide_route 실행 후 state['route']에 저장.
    """
    next_node = decide_route(state)
    state["route"] = next_node
    return state

def build_graph() -> StateGraph:
    """
    LangGraph 상태 그래프를 생성하고 노드 간 연결을 정의함.
    """
    workflow = StateGraph(State)

    # 노드 등록
    workflow.add_node("router", router_node)
    workflow.add_node("chat_node", chat_node)
    workflow.add_node("subject_info_node", subject_info_node)
    workflow.add_node("rag_review_node", rag_review_node)

    # 라우팅 연결 (state['route'] 값 사용)
    workflow.add_conditional_edges(
        source="router",
        path=lambda s: s["route"],
        path_map={
            "chat_node": "chat_node",
            "subject_info_node": "subject_info_node",
            "rag_review_node": "rag_review_node"
        }
    )

    # 각 노드에서 종료로 연결
    workflow.add_edge("chat_node", END)
    workflow.add_edge("subject_info_node", END)
    workflow.add_edge("rag_review_node", END)

    # 시작점
    workflow.set_entry_point("router")

    return workflow
