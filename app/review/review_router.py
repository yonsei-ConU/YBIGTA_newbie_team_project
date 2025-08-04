from fastapi import APIRouter, HTTPException
from database.mongodb_connection import get_reviews, replace_reviews
from review_analysis.preprocessing.letterboxd_preprocessor import LetterboxdPreprocessor
from review_analysis.preprocessing.naver_preprocessor import NaverPreprocessor
from review_analysis.preprocessing.rotten_preprocessor import RottenTomatoesPreprocessor

router = APIRouter()

@router.post("/preprocess/{site_name}")
def preprocess_reviews(site_name: str):
    reviews = get_reviews(site_name)

    if not reviews:
        raise HTTPException(status_code=404, detail=f"No data found for site: {site_name}")

    processor_map = {
        "letterboxd": LetterboxdPreprocessor(),
        "naver": NaverPreprocessor(),
        "rotten": RottenTomatoesPreprocessor()
    }

    processor = processor_map.get(site_name.lower())
    if processor is None:
        raise HTTPException(status_code=400, detail=f"Unsupported site_name: {site_name}")

    processed_reviews = processor.preprocess(reviews)

    replace_reviews(site_name, processed_reviews)

    return {
        "message": "Preprocessing completed",
        "site": site_name,
        "processed_count": len(processed_reviews)
    }
