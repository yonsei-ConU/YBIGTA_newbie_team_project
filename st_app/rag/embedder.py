"""
embedder.py

텍스트를 Upstage Embedding API를 사용해 벡터로 변환하는 함수.
"""

import os
import requests

UPSTAGE_API_KEY = os.environ.get("UPSTAGE_API_KEY")
EMBEDDING_URL = "https://api.upstage.ai/v1/embeddings"

def get_embedding(text: str) -> list[float]:
    """
    주어진 텍스트를 임베딩 벡터로 변환함.
    """
    if not UPSTAGE_API_KEY:
        raise ValueError("환경 변수 UPSTAGE_API_KEY가 설정되지 않음")
    if not text.strip():
        return []

    headers = {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}",
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
