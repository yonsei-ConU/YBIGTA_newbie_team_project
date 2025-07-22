from review_analysis.preprocessing.base_processor import BaseDataProcessor
import pandas as pd
import re

class NaverPreprocessor(BaseDataProcessor):
    """
    Naver 영화 리뷰 데이터를 전처리하는 클래스.

    전처리 단계:
    1. 컬럼명 통일
    2. 결측치 제거
    3. 날짜 정제
    4. 평점 정제
    5. 리뷰 텍스트 정제
    6. 파생 변수 생성
    7. 감성 분석용 텍스트 정제
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

        # Step 5: 리뷰 정제
        print("[STEP 5] 리뷰 텍스트 정제 중...")
        df['review'] = df['review'].astype(str)
        before = len(df)
        df = df[df['review'].str.len().between(20, 1000)]
        print(f"[STEP 5] 길이 기준 필터링 제거: {before - len(df)}")

        def clean_text(text):
            """
            영어 텍스트에서 특수문자를 제거하고 소문자로 변환합니다.

            Args:
                text (str): 원본 텍스트

            Returns:
                str: 정제된 소문자 텍스트
            """
            text = re.sub(r'[^\w\s]', '', text)
            return text.lower().strip()

        df['cleaned_review'] = df['review'].apply(clean_text)

        # Step 6: 파생 변수 생성
        print("[STEP 6] 날짜 기반 파생 변수 생성 중...")
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['weekday'] = df['date'].dt.dayofweek

        # Step 7: 감성 분석용 정제
        print("[STEP 7] 감성 분석용 텍스트 정제 중 (한글 기준)...")

        def clean_korean_text(text):
            """
            한글 텍스트에서 특수문자, 숫자, 영어 등을 제거하고
            한글과 공백만 남깁니다. 다중 공백은 단일 공백으로 치환합니다.

            Args:
                text (str): 원본 텍스트

            Returns:
                str: 정제된 한글 텍스트
            """
            text = re.sub(r'[^가-힣\s]', '', text)
            return re.sub(r'\s+', ' ', text).strip()

        df['final_review'] = df['cleaned_review'].apply(clean_korean_text)

        self.data = df
        print(f"[DONE] 전처리 완료: 최종 {len(df)} rows")

    def feature_engineering(self):
        """(미사용)"""
        print("[FEATURE] 기능 엔지니어링 없음 (통과)")

    def save_to_database(self):
        """전처리 결과를 CSV로 저장"""
        output_path = f"{self.output_dir}/preprocessed_reviews_naver.csv"
        try:
            self.data.to_csv(output_path, index=False)
            print(f"[SAVE] 저장 완료 → {output_path}")
        except Exception as e:
            print(f"[ERROR] 저장 실패: {e}")
