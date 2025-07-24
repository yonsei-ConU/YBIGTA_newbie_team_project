import pandas as pd
from datetime import datetime
from review_analysis.preprocessing.base_processor import BaseDataProcessor

class RottenTomatoesProcessor(BaseDataProcessor):
    def __init__(self, input_path: str, output_dir: str):
        super().__init__(input_path, output_dir)
        self.df = pd.read_csv(self.input_path)

    def preprocess(self):
        # ✅ 점수 스케일 변환 (5점 만점 → 10점 만점)
        self.df["score"] = self.df["score"].astype(float) * 2

        # ✅ 날짜 형식 통일 (e.g., Jul 21, 2025 → 2025-07-21)
        self.df["date"] = pd.to_datetime(
            self.df["date"], format="%b %d, %Y", errors="coerce"
        ).dt.strftime("%Y-%m-%d")

    def feature_engineering(self):
        # ✅ 날짜 파생 변수
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df["year"] = self.df["date"].dt.year
        self.df["month"] = self.df["date"].dt.month
        self.df["weekday"] = self.df["date"].dt.day_name()

        # ✅ 간단 텍스트 정제본
        self.df["final_review"] = (
            self.df["review"]
            .astype(str)
            .str.lower()
            .str.replace(r"[^a-z0-9\s]", "", regex=True)
            .str.strip()
        )

        # ✅ 열 이름 바꾸기: score → rating
        self.df.rename(columns={
            "score": "rating"
        }, inplace=True)

        # ✅ 최종 열 순서 및 필터링
        self.df = self.df[["date", "rating", "review", "year", "month", "weekday", "final_review"]]

    def save_to_database(self):
        save_path = "database/preprocessed_reviews_rotten.csv"
        self.df.to_csv(save_path, index=False)
        print(f"✅ 전처리된 파일 저장 완료: {save_path}")
