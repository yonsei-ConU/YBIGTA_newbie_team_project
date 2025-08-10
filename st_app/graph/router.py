"""
router.py

이 모듈은 LangGraph의 라우팅 로직을 정의함.
사용자의 입력을 분석하여 적절한 노드(chat, subject, review)로 연결함.
LLM이 판단하여 유동적으로 조건부 라우팅을 진행함.
"""

from langgraph.graph import StateGraph, END
from st_app.utils.state import State
from st_app.graph.nodes.chat_node import chat_node
from st_app.graph.nodes.subject_info_node import subject_info_node
from st_app.graph.nodes.rag_review_node import rag_review_node
from st_app.rag.llm import call_llm
import streamlit as st


def decide_route(state: State) -> str:
    """
    사용자 입력을 분석하여 적절한 노드로 라우팅함.
    LLM이 판단하여 유동적으로 조건부 라우팅을 진행함.
    """
    user_msg = state["user_input"]
    
    print(f"🔍 라우팅 분석 중: '{user_msg}'")
    
    # 라우팅 정보를 Streamlit에 표시
    st.info(f"🔍 라우팅 분석 중: '{user_msg}'")
    
    # LLM 기반 라우팅을 위한 프롬프트
    routing_prompt = f"""
당신은 사용자의 질문을 분석하여 적절한 노드로 라우팅하는 AI 어시스턴트입니다.

사용자 질문: "{user_msg}"

다음 세 가지 노드 중 하나를 선택하세요:

1. chat_node: 일반적인 대화, 인사, 감사, 기타 질문
2. subject_info_node: 영화/제품의 정보, 줄거리, 감독, 출연진, 장르, 개봉일 등에 대한 질문
3. rag_review_node: 리뷰, 후기, 평가, 사용자 경험, 추천 등에 대한 질문

응답은 반드시 다음 중 하나만 출력하세요 (하이픈이나 다른 문자 없이):
chat_node
subject_info_node
rag_review_node

추가 설명이나 다른 텍스트는 포함하지 마세요.
"""
    
    try:
        print("🤖 LLM에게 라우팅 결정 요청 중...")
        # LLM을 호출하여 라우팅 결정
        route_decision = call_llm(routing_prompt).strip().lower()
        print(f"📝 LLM 응답: '{route_decision}'")
        
        # 응답 검증 및 정규화
        if "chat" in route_decision:
            print("✅ chat_node로 라우팅")
            st.success("✅ chat_node로 라우팅됨")
            return "chat_node"
        elif "subject" in route_decision or "info" in route_decision:
            print("✅ subject_info_node로 라우팅")
            st.success("✅ subject_info_node로 라우팅됨")
            return "subject_info_node"
        elif "rag" in route_decision or "review" in route_decision:
            print("✅ rag_review_node로 라우팅")
            st.success("✅ rag_review_node로 라우팅됨")
            return "rag_review_node"
        else:
            print(f"⚠️ 예상치 못한 응답: '{route_decision}' -> chat_node로 기본 라우팅")
            st.warning(f"⚠️ 예상치 못한 응답: '{route_decision}' -> chat_node로 기본 라우팅")
            # 기본값으로 일반 대화 노드
            return "chat_node"
            
    except Exception as e:
        print(f"❌ 라우팅 결정 중 오류 발생: {e}")
        st.error(f"❌ 라우팅 결정 중 오류 발생: {e}")
        # 오류 발생 시 기본값으로 일반 대화 노드
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
    각 노드 처리 후 자동으로 Chat Node로 복귀하는 구조.
    """
    workflow = StateGraph(State)

    # 노드 등록
    workflow.add_node("router", router_node)
    workflow.add_node("chat_node", chat_node)
    workflow.add_node("subject_info_node", subject_info_node)
    workflow.add_node("rag_review_node", rag_review_node)

    # 초기 라우팅 연결
    workflow.add_conditional_edges(
        source="router",
        path=lambda s: s["route"],
        path_map={
            "chat_node": "chat_node",
            "subject_info_node": "subject_info_node",
            "rag_review_node": "rag_review_node"
        }
    )

    # 각 노드 처리 후 Chat Node로 복귀
    workflow.add_edge("chat_node", END)
    workflow.add_edge("subject_info_node", END)
    workflow.add_edge("rag_review_node", END)

    # 시작점 설정
    workflow.set_entry_point("router")

    return workflow
