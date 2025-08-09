"""
rag_review_node.py

리뷰 검색 및 요약을 담당하는 노드.
FAISS 벡터 DB를 이용해 관련 문서를 검색하고,
LLM을 호출해 사용자 질문에 맞는 응답을 생성한다.
"""

from st_app.utils.state import State
from st_app.rag.retriever import retriever
from st_app.rag.llm import call_llm
from st_app.rag.prompt import create_review_summary_prompt


def rag_review_node(state: State) -> State:
    """
    리뷰 검색 후 LLM으로 최종 응답 생성
    """
    print("🚀 rag_review_node 시작!")
    query = state["user_input"]
    print(f"📝 사용자 질문: '{query}'")
    
    # 사용자 입력에서 검색할 리뷰 수 파악
    top_k = 15  # 기본값
    print(f"🔍 초기 top_k: {top_k}")
    
    # 특정 숫자가 언급된 경우 해당 숫자로 설정
    import re
    number_match = re.search(r'(\d+)개?\s*리뷰', query)
    if number_match:
        top_k = min(int(number_match.group(1)), 50)  # 최대 50개로 제한
        print(f"🔢 숫자 매칭: {number_match.group(1)}개 리뷰 요청")
    
    # "모든", "전체" 등의 키워드가 있으면 더 많이 검색
    if any(keyword in query for keyword in ['모든', '전체', '많이', 'all', 'many']):
        top_k = 30
        print(f"🔍 키워드 매칭: '모든/전체' 키워드 감지, top_k를 30으로 설정")
    
    print(f"🎯 최종 top_k: {top_k}")
    
    try:
        print("🔍 FAISS 검색 시작...")
        # 리트리버를 사용하여 관련 문서 검색
        docs = retriever.search(query, top_k=top_k)
        doc_count = len(docs) if docs else 0
        print(f"✅ FAISS 검색 완료! 검색된 문서 수: {doc_count}")
        
        if not docs:
            print("❌ 검색된 문서가 없음")
            state["messages"].append({
                "role": "assistant",
                "content": "죄송합니다. 관련된 리뷰를 찾을 수 없습니다. "
                           "다른 키워드로 검색해보시거나, "
                           "일반적인 대화를 시도해보세요."
            })
            return state
            
    except Exception as e:
        print(f"❌ FAISS 검색 중 오류 발생: {e}")
        state["messages"].append({
            "role": "assistant",
            "content": f"리뷰 검색 중 오류가 발생했습니다: {e}"
        })
        return state

    # 검색된 문서를 상태에 저장
    state["retrieved_docs"] = docs
    print(f"💾 검색된 문서를 state에 저장: {len(docs)}개")

    # 검색된 리뷰 수 정보 추가
    search_info = f"총 {len(docs)}개의 리뷰를 검색했습니다."
    print(f"📊 검색 정보: {search_info}")
    
    # 검색 결과를 텍스트로 변환
    print("📝 검색 결과를 텍스트로 변환 중...")
    context_text = "\n\n".join([
        f"[{doc.get('date', 'N/A')}] "
        f"평점 {doc.get('rating', 'N/A')}/10 "
        f"({doc.get('site', 'N/A')})\n"
        f"{doc.get('content', doc.get('review', 'N/A'))}"
        for doc in docs
    ])
    print(f"📄 변환된 컨텍스트 길이: {len(context_text)} 문자")
    print(f"📄 컨텍스트 미리보기: {context_text[:200]}...")

    # 프롬프트 생성 및 LLM 호출
    try:
        print("🤖 LLM 프롬프트 생성 중...")
        # 검색 정보를 포함한 프롬프트 생성
        enhanced_context = f"{search_info}\n\n{context_text}"
        prompt = create_review_summary_prompt(query, enhanced_context)
        print(f"📝 생성된 프롬프트 길이: {len(prompt)} 문자")
        print(f"📝 프롬프트 미리보기: {prompt[:300]}...")
        
        print("🤖 LLM 호출 중...")
        llm_response = call_llm(prompt)
        print(f"✅ LLM 응답 완료! 응답 길이: {len(llm_response)} 문자")
        print(f"📝 LLM 응답 미리보기: {llm_response[:200]}...")
        
    except Exception as e:
        print(f"❌ LLM 호출 중 오류 발생: {e}")
        llm_response = (
            f"리뷰 분석 중 오류가 발생했습니다: {e}\n\n"
            f"검색된 리뷰:\n{context_text}"
        )

    # 응답을 메시지에 추가
    print("💬 응답을 메시지에 추가 중...")
    state["messages"].append({
        "role": "assistant",
        "content": llm_response
    })
    
    print("✅ rag_review_node 완료!")
    return state
