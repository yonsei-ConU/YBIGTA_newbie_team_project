"""
rag_review_node.py

리뷰 검색 및 요약을 담당하는 노드.
FAISS 벡터 DB를 이용해 관련 문서를 검색하고,
LLM을 호출해 사용자 질문에 맞는 응답을 생성한다.
"""

import json
import faiss
import numpy as np
from pathlib import Path
from st_app.utils.state import State
from st_app.rag.embedder import get_embedding
from st_app.rag.llm import call_llm

# DB 경로
INDEX_PATH = Path("st_app/db/faiss_index/index.faiss")
META_PATH = Path("st_app/db/faiss_index/meta.json")

def load_faiss_index():
    """저장된 FAISS 인덱스 로드"""
    if not INDEX_PATH.exists():
        raise FileNotFoundError(f"FAISS index not found at {INDEX_PATH}")
    index = faiss.read_index(str(INDEX_PATH))
    return index

def load_meta():
    """메타데이터 로드"""
    if not META_PATH.exists():
        raise FileNotFoundError(f"Meta file not found at {META_PATH}")
    with open(META_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return meta

def search_reviews(query: str, top_k: int = 3):
    """
    쿼리를 임베딩 후 FAISS로 검색
    """
    index = load_faiss_index()
    meta = load_meta()
    query_vec = np.array([get_embedding(query)], dtype=np.float32)
    distances, ids = index.search(query_vec, top_k)

    results = []
    for idx in ids[0]:
        if idx < 0 or idx >= len(meta):
            continue
        results.append(meta[idx])
    return results

def rag_review_node(state: State) -> State:
    """
    리뷰 검색 후 LLM으로 최종 응답 생성
    """
    query = state["user_input"]
    try:
        docs = search_reviews(query, top_k=3)
    except Exception as e:
        state["messages"].append({
            "role": "assistant",
            "content": f"리뷰 검색 중 오류 발생: {e}"
        })
        return state

    state["retrieved_docs"] = docs

    # 검색 결과 텍스트 합치기
    context_text = "\n\n".join(
        f"[{d.get('date','')}] 평점 {d.get('rating','N/A')}/10\n{d.get('content','')}"
        for d in docs
    )

    # LLM 호출
    prompt = f"""다음은 사용자가 남긴 영화 리뷰입니다:
{context_text}

위 리뷰들을 참고해서 다음 질문에 답변해 주세요:
{query}
"""
    llm_response = call_llm(prompt)

    state["messages"].append({
        "role": "assistant",
        "content": llm_response
    })
    return state
