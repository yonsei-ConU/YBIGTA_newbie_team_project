import streamlit as st
from st_app.graph.router import build_graph
from st_app.utils.state import new_state

# 페이지 기본 설정
st.set_page_config(page_title="YBIGTA RAG-Agent Demo", layout="centered")

# 세션 상태 초기화
if "graph" not in st.session_state:
    st.session_state.graph = build_graph().compile()
if "state" not in st.session_state:
    st.session_state.state = new_state()
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 YBIGTA RAG-Agent Chatbot")

# 이전 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력
if user_input := st.chat_input("메시지를 입력하세요..."):
    # 유저 메시지 상태에 저장
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.state["user_input"] = user_input

    # 그래프 실행
    result_state = st.session_state.graph.invoke(st.session_state.state)

    # 어시스턴트 응답 저장
    if result_state["messages"]:
        assistant_reply = result_state["messages"][-1]["content"]
    else:
        assistant_reply = "응답이 없습니다."

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    # 화면 갱신
    st.rerun()
