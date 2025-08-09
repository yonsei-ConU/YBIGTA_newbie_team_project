"""
prompt.py

RAG 시스템에서 사용할 프롬프트 템플릿들을 정의합니다.
응답 품질과 일관성을 향상시키기 위한 구조화된 프롬프트를 제공합니다.
"""


def create_review_summary_prompt(query: str, context: str) -> str:
    """
    리뷰 요약을 위한 프롬프트 생성
    
    Args:
        query: 사용자 질문
        context: 검색된 리뷰 컨텍스트
    
    Returns:
        구조화된 프롬프트 문자열
    """
    return f"""당신은 영화 리뷰 분석 전문가입니다. 
다음은 사용자가 남긴 영화 리뷰들입니다:

{context}

사용자 질문: {query}

다음 형식으로 답변해주세요:

📽️ **영화 리뷰 분석 결과**

🔍 **검색된 리뷰 요약:**
- 총 {len(context.split('[')) - 1}개의 리뷰를 분석했습니다

⭐ **전체적인 평가:**
- 평점 분포와 주요 의견을 간단히 요약

💬 **주요 키워드:**
- 리뷰에서 자주 언급된 키워드 3-5개

📝 **상세 분석:**
- 사용자 질문에 맞는 구체적인 답변

답변은 친근하고 이해하기 쉽게 작성해주세요. 한국어로 답변해주세요."""


def create_movie_info_prompt(query: str, movie_info: dict) -> str:
    """
    영화 정보 제공을 위한 프롬프트 생성
    
    Args:
        query: 사용자 질문
        movie_info: 영화 정보 딕셔너리
    
    Returns:
        구조화된 프롬프트 문자열
    """
    return f"""당신은 영화 정보 전문가입니다.
다음 영화에 대한 정보를 제공해주세요:

🎬 **{movie_info.get('제목', '영화')} 정보**

📋 **기본 정보:**
- 감독: {movie_info.get('감독', 'N/A')}
- 출시연도: {movie_info.get('출시연도', 'N/A')}
- 장르: {movie_info.get('장르', 'N/A')}
- 주연: {movie_info.get('주연', 'N/A')}

✨ **특징:**
{movie_info.get('특징', 'N/A')}

📊 **평점:**
- 평점: {movie_info.get('평점', 'N/A')}
- 리뷰 수: {movie_info.get('리뷰수', 'N/A')}

사용자 질문: {query}

위 정보를 바탕으로 친근하고 유용한 답변을 제공해주세요."""


def create_general_chat_prompt(query: str) -> str:
    """
    일반적인 대화를 위한 프롬프트 생성
    
    Args:
        query: 사용자 질문
    
    Returns:
        친근한 대화형 프롬프트
    """
    return f"""안녕하세요! 저는 YBIGTA 영화 리뷰 AI 어시스턴트입니다. 

사용자: {query}

영화 리뷰나 영화 정보에 대해 질문해주시면 도움을 드릴 수 있어요!
예시:
- "액션 영화 리뷰 알려줘"
- "미키17 영화 정보 알려줘"
- "봉준호 감독 영화 추천해줘"

어떤 도움이 필요하신가요?"""
