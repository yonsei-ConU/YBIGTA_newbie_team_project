import json
import faiss
import numpy as np
import pandas as pd
from st_app.rag.embedder import get_embedding
from pathlib import Path


def load_real_reviews():
    """실제 영화 리뷰 데이터 로드"""
    # 네이버 리뷰 데이터 로드
    naver_reviews = pd.read_csv("database/preprocessed_reviews_naver.csv")
    
    # 데이터 구조 변환
    reviews = []
    for _, row in naver_reviews.iterrows():
        review = {
            "date": row["date"],
            "rating": row["rating"],
            "content": row["final_review"],  # 전처리된 리뷰 텍스트 사용
            "source": "naver"
        }
        reviews.append(review)
    
    print(f"총 {len(reviews)}개의 네이버 리뷰 로드 완료")
    return reviews


def main():
    # 실제 리뷰 데이터 로드
    reviews = load_real_reviews()
    
    # 임베딩 생성 (처음 100개만 테스트)
    print("임베딩 생성 중...")
    sample_reviews = reviews[:100]  # 처음 100개만 사용 (테스트용)
    
    vectors = []
    valid_reviews = []
    
    for i, review in enumerate(sample_reviews):
        try:
            # 빈 내용 제외
            if review["content"] and len(review["content"].strip()) > 10:
                vector = get_embedding(review["content"])
                vectors.append(vector)
                valid_reviews.append(review)
                if (i + 1) % 10 == 0:
                    print(f"진행률: {i + 1}/{len(sample_reviews)}")
        except Exception as e:
            print(f"리뷰 {i} 임베딩 실패: {e}")
            continue
    
    print(f"성공적으로 임베딩 생성된 리뷰: {len(valid_reviews)}개")
    
    if not vectors:
        print("임베딩을 생성할 수 있는 리뷰가 없습니다.")
        return
    
    # FAISS 인덱스 생성
    vectors_np = np.array(vectors, dtype=np.float32)
    dim = len(vectors[0])
    
    print(f"벡터 차원: {dim}")
    print(f"벡터 개수: {len(vectors_np)}")
    
    # FAISS 인덱스 생성 (L2 거리 기반)
    index = faiss.IndexFlatL2(dim)
    index.add(vectors_np)
    
    # 저장
    output_dir = Path("st_app/db/faiss_index")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    faiss.write_index(index, str(output_dir / "index.faiss"))
    
    with open(output_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(valid_reviews, f, ensure_ascii=False, indent=2)
    
    print("FAISS 인덱스 및 메타 저장 완료")
    print(f"저장 위치: {output_dir}")
    print(f"인덱스 크기: {index.ntotal}")


if __name__ == "__main__":
    main()
