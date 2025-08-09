import json
import faiss
import numpy as np
from st_app.rag.embedder import get_embedding
from pathlib import Path

# 예시 리뷰 데이터
reviews = [
    {"date": "2024-01-01", "rating": 8, "content": "재밌고 감동적인 영화였다."},
    {"date": "2024-02-01", "rating": 5, "content": "스토리가 지루했다."},
    {"date": "2024-03-01", "rating": 9, "content": "연출과 배우 연기가 최고였다."}
]

# 임베딩 생성
vectors = [get_embedding(r["content"]) for r in reviews]
vectors_np = np.array(vectors, dtype=np.float32)

# FAISS 인덱스 생성
dim = len(vectors[0])
index = faiss.IndexFlatL2(dim)
index.add(vectors_np)

# 저장
Path("st_app/db/faiss_index").mkdir(parents=True, exist_ok=True)
faiss.write_index(index, "st_app/db/faiss_index/index.faiss")
with open("st_app/db/faiss_index/meta.json", "w", encoding="utf-8") as f:
    json.dump(reviews, f, ensure_ascii=False, indent=2)

print("FAISS 인덱스 및 메타 저장 완료")
