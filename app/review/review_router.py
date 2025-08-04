from fastapi import APIRouter, HTTPException
from database.mongodb_connection import get_reviews, save_preprocessed_reviews
from review_analysis.preprocessing.letterboxd_preprocessor import (
    LetterboxdPreprocessor
)
from review_analysis.preprocessing.naver_preprocessor import NaverPreprocessor
from review_analysis.preprocessing.rotten_preprocessor import (
    RottenTomatoesPreprocessor
)

router = APIRouter(prefix="/review")


@router.post("/preprocess/{site_name}")
def preprocess_reviews(site_name: str):
    print(f"✅ 들어온 요청 site_name: {site_name}")

    reviews = get_reviews(site_name)

    if not reviews:
        raise HTTPException(
            status_code=404, 
            detail=f"No data found for site: {site_name}"
        )

    processor_map = {
        "letterboxd": LetterboxdPreprocessor(),
        "naver": NaverPreprocessor(),
        "rotten": RottenTomatoesPreprocessor()
    }

    if site_name not in processor_map:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported site: {site_name}"
        )

    processor = processor_map[site_name]
    processed_reviews = processor.preprocess(reviews)

    # 전처리된 데이터를 별도 컬렉션에 저장 (원본 덮어쓰지 않음)
    preprocessed_collection_name = save_preprocessed_reviews(
        site_name, processed_reviews
    )

    return {
        "message": "Preprocessing completed",
        "site": site_name,
        "processed_count": len(processed_reviews),
        "saved_to_collection": preprocessed_collection_name
    }
