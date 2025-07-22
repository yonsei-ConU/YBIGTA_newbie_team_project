import pandas as pd
from datetime import datetime
from review_analysis.preprocessing.base_processor import BaseDataProcessor


class RottenTomatoesProcessor(BaseDataProcessor):
    def __init__(self, input_path: str, output_dir: str):
        super().__init__(input_path, output_dir)
        self.df = pd.read_csv(self.input_path)  
        
    def preprocess(self):
        # 점수를 2배로 (5점 만점 → 10점 만점)
        self.df["score"] = self.df["score"].astype(float) * 2

        # 날짜를 YYYY-MM-DD 형식으로 변환
        self.df["date"] = pd.to_datetime(self.df["date"], format="%b %d, %Y", errors="coerce").dt.strftime("%Y-%m-%d")

    def feature_engineering(self):
        # 예시: 리뷰 길이 컬럼 추가
        self.df["review_length"] = self.df["review"].astype(str).apply(len)

    def save_to_database(self):
        save_path = "database/preprocessed_reviews_rotten.csv"
        self.df = self.df[["date", "score", "review"]]
        self.df.to_csv(save_path, index=False)
        print(f"✅ 전처리된 파일 저장 완료: {save_path}")
