from review_analysis.preprocessing.base_preprocessor import BaseDataProcessor
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import scipy.sparse
import numpy as np
import os

class NaverPreprocessor(BaseDataProcessor):
    """
    Naver 영화 리뷰 데이터를 전처리하는 클래스.

    전처리 단계:
    1. 컬럼명 통일
    2. 결측치 제거
    3. 날짜 정제
    4. 평점 정제
    5. 파생 변수 생성
    6. 리뷰 텍스트 정제 및 감성 분석용 정제
    """

    def __init__(self, input_path: str, output_dir: str):
        """
        Args:
            input_path (str): 입력 CSV 경로
            output_dir (str): 전처리 결과 저장 폴더 경로
        """
        print("[INIT] NaverPreprocessor 초기화됨")
        super().__init__(input_path, output_dir)
        self.data = None

    def preprocess(self):
        """전체 전처리 파이프라인 실행"""
        print("[PREPROCESS] 원본 데이터 로딩 중...")
        try:
            df = pd.read_csv(self.input_path)
        except Exception as e:
            print(f"[ERROR] CSV 로딩 실패: {e}")
            return
        print(f"[PREPROCESS] 데이터 로딩 완료: {len(df)} rows")

        # Step 1: 컬럼명 통일
        print("[STEP 1] 컬럼명 통일 중...")
        df.columns = ['date', 'rating', 'review']

        # Step 2: 결측치 제거
        print("[STEP 2] 결측치 제거 중...")
        before = len(df)
        df.dropna(subset=['date', 'rating', 'review'], inplace=True)
        print(f"[STEP 2] 제거된 행 수: {before - len(df)}")

        # Step 3: 날짜 정제
        print("[STEP 3] 날짜 포맷 정제 중...")
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        before = len(df)
        df.dropna(subset=['date'], inplace=True)
        print(f"[STEP 3] 제거된 잘못된 날짜 수: {before - len(df)}")

        # Step 4: 평점 정제
        print("[STEP 4] 평점 정제 중...")
        df['rating'] = df['rating'].astype(str).str.extract(r'(\d+)$')[0]
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        before = len(df)
        df.dropna(subset=['rating'], inplace=True)
        df = df[(df['rating'] >= 0) & (df['rating'] <= 10)]
        print(f"[STEP 4] 유효하지 않은 평점 제거: {before - len(df)}")

        # Step 5: 파생 변수 생성 (날짜 기반)
        print("[STEP 5] 날짜 기반 파생 변수 생성 중...")
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['weekday'] = df['date'].dt.dayofweek

        # Step 6: 리뷰 텍스트 정제 + 감성 분석용 정제
        print("[STEP 6] 리뷰 텍스트 정제 및 감성 분석용 정제 중...")
        df['review'] = df['review'].astype(str)
        before = len(df)
        df = df[df['review'].str.len().between(20, 1000)]
        print(f"[STEP 6] 길이 기준 필터링 제거: {before - len(df)}")

        def clean_korean_text(text: str) -> str:
            """
            리뷰에서 특수문자, 숫자, 영어 등을 제거하고
            한글과 공백만 남깁니다. 다중 공백은 단일 공백으로 치환합니다.

            Args:
                text (str): 원본 텍스트

            Returns:
                str: 정제된 한글 텍스트
            """
            text = re.sub(r'[^가-힣\s]', '', text)
            return re.sub(r'\s+', ' ', text).strip()

        df['final_review'] = df['review'].apply(clean_korean_text)
        print(f"[STEP 6] final_review 샘플 → {df['final_review'].iloc[0][:50]}...")

        self.data = df
        print(f"[DONE] 전처리 완료: 최종 {len(df)} rows")

    def feature_engineering(self):
        """
        전처리된 final_review 컬럼을 TF-IDF 벡터화하고,
        결과를 .npz 및 .npy 파일로 저장합니다.
        """
        print("[TF-IDF] 벡터화 시작")

        if self.data is None or 'final_review' not in self.data.columns:
            print("[TF-IDF] ⚠️ final_review가 존재하지 않습니다. 전처리 먼저 실행하세요.")
            return

        try:
            # 벡터화
            vectorizer = TfidfVectorizer(max_features=1000, min_df=2)
            X = vectorizer.fit_transform(self.data['final_review'])
            X = normalize(X)

            # 저장 경로
            matrix_path = os.path.join(self.output_dir, "vector_matrix_tfidf.npz")
            vocab_path = os.path.join(self.output_dir, "vocab_tfidf.npy")

            # 저장
            scipy.sparse.save_npz(matrix_path, X)
            np.save(vocab_path, vectorizer.get_feature_names_out())

            print(f"[TF-IDF] 벡터 행렬 저장 완료 → {matrix_path}")
            print(f"[TF-IDF] 단어 목록 저장 완료 → {vocab_path}")
            print(f"[TF-IDF] shape: {X.shape}")

        except Exception as e:
            print(f"[TF-IDF] ❌ 벡터화 실패: {e}")


    def save_to_database(self):
        """전처리 결과를 CSV로 저장"""
        output_path = f"{self.output_dir}/preprocessed_reviews_naver.csv"
        try:
            # 컬럼 순서 지정
            ordered_cols = ['date', 'rating', 'review', 'year', 'month', 'weekday', 'final_review']
            self.data[ordered_cols].to_csv(output_path, index=False)
            print(f"[SAVE] 저장 완료 → {output_path}")
        except Exception as e:
            print(f"[ERROR] 저장 실패: {e}")
