"""
retriever.py

FAISS 인덱스를 사용하여 벡터 검색을 수행하는 리트리버 모듈.
"""

import os
import json
import faiss
import numpy as np
from typing import List, Dict, Any
from .embedder import get_embedding


class FAISSRetriever:
    """
    FAISS 인덱스를 사용한 벡터 검색 리트리버
    """
    
    def __init__(self, 
                 index_path: str = "st_app/db/faiss_index/index.faiss",
                 meta_path: str = "st_app/db/faiss_index/meta.json"):
        """
        FAISS 리트리버 초기화
        
        Args:
            index_path: FAISS 인덱스 파일 경로
            meta_path: 메타데이터 JSON 파일 경로
        """
        self.index_path = index_path
        self.meta_path = meta_path
        self.index = None
        self.metadata = None
        self._load_index()
    
    def _load_index(self):
        """FAISS 인덱스와 메타데이터 로드"""
        try:
            if (os.path.exists(self.index_path) and 
                    os.path.exists(self.meta_path)):
                self.index = faiss.read_index(self.index_path)
                with open(self.meta_path, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
                print(f"FAISS 인덱스 로드 완료: {len(self.metadata)}개 문서")
            else:
                print("FAISS 인덱스 파일을 찾을 수 없습니다. "
                      "빈 인덱스로 초기화합니다.")
                self.index = None
                self.metadata = []
        except Exception as e:
            print(f"FAISS 인덱스 로드 중 오류 발생: {e}")
            self.index = None
            self.metadata = []
    
    def search(self, query: str, top_k: int = 15) -> List[Dict[str, Any]]:
        """
        쿼리와 유사한 문서들을 검색
        
        Args:
            query: 검색 쿼리
            top_k: 반환할 상위 문서 수
            
        Returns:
            검색된 문서들의 리스트 (메타데이터 포함)
        """
        if not self.index or not self.metadata:
            return []
        
        try:
            # 쿼리 임베딩 생성
            query_embedding = get_embedding(query)
            if not query_embedding:
                return []
            
            # 벡터 검색 수행
            query_vector = np.array([query_embedding], dtype=np.float32)
            scores, indices = self.index.search(
                query_vector, min(top_k, len(self.metadata))
            )
            
            # 결과 반환
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.metadata):
                    doc = self.metadata[idx].copy()
                    doc['similarity_score'] = float(score)
                    results.append(doc)
            
            return results
            
        except Exception as e:
            print(f"검색 중 오류 발생: {e}")
            return []
    
    def search_by_site(self, query: str, site: str, 
                       top_k: int = 15) -> List[Dict[str, Any]]:
        """
        특정 사이트의 리뷰만 검색
        
        Args:
            query: 검색 쿼리
            site: 검색할 사이트 ('naver', 'rotten', 'letterboxd')
            top_k: 반환할 상위 문서 수
            
        Returns:
            검색된 문서들의 리스트
        """
        all_results = self.search(query, top_k * 3)
        
        # 사이트별 필터링
        site_mapping = {
            'naver': 'naver',
            'rotten': 'rotten', 
            'letterboxd': 'letterboxd'
        }
        
        target_site = site_mapping.get(site.lower(), site.lower())
        filtered_results = [
            doc for doc in all_results 
            if doc.get('site', '').lower() == target_site
        ]
        
        return filtered_results[:top_k]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        인덱스 통계 정보 반환
        
        Returns:
            인덱스 통계 정보 딕셔너리
        """
        if not self.index or not self.metadata:
            return {"total_documents": 0, "index_dimension": 0}
        
        stats = {
            "total_documents": len(self.metadata),
            "index_dimension": self.index.d,
            "sites": {}
        }
        
        # 사이트별 통계
        for doc in self.metadata:
            site = doc.get('site', 'unknown')
            if site not in stats['sites']:
                stats['sites'][site] = 0
            stats['sites'][site] += 1
        
        return stats


# 전역 리트리버 인스턴스
retriever = FAISSRetriever()
