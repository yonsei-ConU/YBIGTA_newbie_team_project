"""
llm.py

Upstage Solar LLM 호출 함수.
"""

import streamlit as st
import requests

def call_llm(prompt: str) -> str:
    """
    프롬프트를 받아 Upstage Solar LLM 응답을 문자열로 반환함.
    """
    try:
        upstage_api_key = st.secrets["UPSTAGE_API_KEY"]
        if not upstage_api_key:
            raise ValueError("UPSTAGE_API_KEY가 비어있습니다")
    except KeyError:
        return "API 키가 설정되지 않았습니다."
    except Exception as e:
        return f"API 키 오류: {str(e)}"

    LLM_URL = "https://api.upstage.ai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {upstage_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "solar-1-mini-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    
    try:
        resp = requests.post(LLM_URL, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"API 호출 오류: {str(e)}"
    except Exception as e:
        return f"응답 처리 오류: {str(e)}"
