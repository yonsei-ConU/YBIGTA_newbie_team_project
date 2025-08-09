from typing import TypedDict, Literal, List, Optional, Dict, Any

Route = Literal["chat", "subject_info", "rag_review", "end"]

class State(TypedDict, total=False):
    """그래프 세션 상태 정의함. 메시지, 사용자 입력, 라우팅 결과, 검색 문서 등 저장함. 노드 간 공용으로 읽고 쓰게 됨."""
    messages: List[Dict[str, Any]]  # 대화 로그 저장용(역할/콘텐츠 등)
    user_input: str  # 최신 사용자 질문 텍스트
    route: Route  # 라우터가 결정한 다음 목적지 노드 이름
    subject_id: Optional[str]  # 주제/대상 선택됐을 때 식별자 저장
    retrieved_docs: List[Dict[str, Any]]  # RAG에서 찾은 문서들 메타 포함
    meta: Dict[str, Any]  # 기타 임시 상태 넣는 공간

def new_state() -> State:
    """초기 상태 객체 생성함. 시작 시 chat으로 라우팅하고 비어 있는 로그로 시작함."""
    return {"messages": [], "user_input": "", "route": "chat", "retrieved_docs": [], "meta": {}}
