"""
llm.py

Upstage Solar LLM 호출 함수.
"""

import os
import requests

UPSTAGE_API_KEY = os.environ.get("UPSTAGE_API_KEY")
LLM_URL = "https://api.upstage.ai/v1/chat/completions"

def call_llm(prompt: str) -> str:
    """
    프롬프트를 받아 Upstage Solar LLM 응답을 문자열로 반환함.
    """
    if not UPSTAGE_API_KEY:
        raise ValueError("환경 변수 UPSTAGE_API_KEY가 설정되지 않음")

    headers = {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "solar-1-mini-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    resp = requests.post(LLM_URL, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()
