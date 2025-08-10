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
        st.error("⚠️ UPSTAGE_API_KEY가 Streamlit secrets에 설정되지 않았습니다.")
        st.info("💡 Streamlit Cloud의 Settings → Secrets에서 API 키를 설정해주세요.")
        return "API 키가 설정되지 않아 응답을 생성할 수 없습니다."
    except Exception as e:
        st.error(f"⚠️ API 키 설정 오류: {str(e)}")
        return "API 키 설정에 문제가 있어 응답을 생성할 수 없습니다."

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
        st.error(f"⚠️ API 호출 오류: {str(e)}")
        return "API 호출 중 오류가 발생했습니다."
    except Exception as e:
        st.error(f"⚠️ 응답 처리 오류: {str(e)}")
        return "응답 처리 중 오류가 발생했습니다."
