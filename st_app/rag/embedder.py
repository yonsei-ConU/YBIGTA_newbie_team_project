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
        if not upstage_api_key:
            raise ValueError("UPSTAGE_API_KEY가 비어있습니다")
    except KeyError:
        st.error("⚠️ UPSTAGE_API_KEY가 Streamlit secrets에 설정되지 않았습니다.")
        st.info("💡 Streamlit Cloud의 Settings → Secrets에서 API 키를 설정해주세요.")
        return []
    except Exception as e:
        st.error(f"⚠️ API 키 설정 오류: {str(e)}")
        return []
    
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
    
    try:
        resp = requests.post(EMBEDDING_URL, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["data"][0]["embedding"]
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Embedding API 호출 오류: {str(e)}")
        return []
    except Exception as e:
        st.error(f"⚠️ Embedding 응답 처리 오류: {str(e)}")
        return []
