"""
embedder.py

텍스트를 Upstage Embedding API를 사용해 벡터로 변환하는 함수.
"""

import streamlit as st
import requests

def get_embedding(text: str) -> list[float]:
    """
    주어진 텍스트를 임베딩 벡터로 변환함.
    """
    try:
        upstage_api_key = st.secrets["UPSTAGE_API_KEY"]
    except KeyError:
        raise ValueError("Streamlit secrets에서 UPSTAGE_API_KEY가 설정되지 않음")
    
    if not text.strip():
        return []

    EMBEDDING_URL = "https://api.upstage.ai/v1/embeddings"
    
    headers = {
        "Authorization": f"Bearer {upstage_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "embedding-passage",
        "input": text
    }
    resp = requests.post(EMBEDDING_URL, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["data"][0]["embedding"]
