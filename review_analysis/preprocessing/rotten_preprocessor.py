import pandas as pd
from datetime import datetime
from review_analysis.preprocessing.base_preprocessor import BaseDataProcessor
from sklearn.feature_extraction.text import TfidfVectorizer

class RottenTomatoesPreprocessor(BaseDataProcessor):
    def __init__(self, input_path: str, output_dir: str):
        super().__init__(input_path, output_dir)
        self.df = pd.read_csv(self.input_path)
        self.vectors = None  # 벡터는 생성하되 저장하지 않음

    def preprocess(self):
        # 점수 스케일 변환 (5점 → 10점)
        self.df["score"] = self.df["score"].astype(float) * 2

        # 날짜 형식 통일
        self.df["date"] = pd.to_datetime(
            self.df["date"], format="%b %d, %Y", errors="coerce"
        ).dt.strftime("%Y-%m-%d")

    def feature_engineering(self):
        # 날짜 기반 파생
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df["year"] = self.df["date"].dt.year
        self.df["month"] = self.df["date"].dt.month
        self.df["weekday"] = self.df["date"].dt.day_name()

        # 텍스트 정제
        self.df["final_review"] = (
            self.df["review"]
            .astype(str)
            .str.lower()
            .str.replace(r"[^a-z0-9\s]", "", regex=True)
            .str.strip()
        )

        # 열 이름 변경
        self.df.rename(columns={"score": "rating"}, inplace=True)

        # 벡터화 (벡터는 내부적으로만 생성하고 저장은 하지 않음)
        vectorizer = TfidfVectorizer(max_features=300)
        tfidf_matrix = vectorizer.fit_transform(self.df["final_review"])
        self.vectors = tfidf_matrix.toarray().tolist()

        # 저장 대상 컬럼만 유지
        self.df = self.df[["date", "rating", "review", "year", "month", "weekday", "final_review"]]

    def save_to_database(self):
        csv_path = f"{self.output_dir}/preprocessed_reviews_rotten.csv"
        self.df.to_csv(csv_path, index=False)
        print(f"✅ 전처리된 파일 저장 완료: {csv_path}")

        # ⚠️ vectors는 저장하지 않음!
