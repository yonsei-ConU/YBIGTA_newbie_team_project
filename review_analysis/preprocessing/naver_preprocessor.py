from review_analysis.preprocessing.base_preprocessor import BaseDataProcessor
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer

class NaverPreprocessor(BaseDataProcessor):
    def __init__(self, input_path: str = None, output_path: str = None):
        super().__init__(input_path, output_path)

    def preprocess(self, reviews: list[dict]) -> list[dict]:
        # MongoDB에서 받은 데이터를 DataFrame으로 변환
        df = pd.DataFrame(reviews)
        
        print(f"🔍 naver 전처리 시작: {len(df)}개 데이터")
        print(f"🔍 원본 컬럼: {list(df.columns)}")
        print(f"🔍 샘플 데이터: {df.iloc[0].to_dict() if len(df) > 0 else '데이터 없음'}")
        
        # 실제 데이터 구조에 맞게 컬럼명 매핑
        if 'text' in df.columns:
            df = df.rename(columns={'text': 'review'})
        
        # 컬럼 순서 통일
        if all(col in df.columns for col in ['date', 'rating', 'review']):
            df = df[['date', 'rating', 'review']]
        else:
            print(f"❌ 필요한 컬럼이 없습니다. 현재 컬럼: {list(df.columns)}")
            return []
        
        # 날짜 정제 및 변환
        def clean_date(date_str):
            """날짜 문자열 정제"""
            if pd.isna(date_str):
                return None
            date_str = str(date_str).strip()
            # 끝의 하이픈 제거
            if date_str.endswith('-'):
                date_str = date_str[:-1]
            return date_str
        
        df['date'] = df['date'].apply(clean_date)
        
        # 평점 정제 및 변환
        def clean_rating(rating):
            """평점 정제 및 숫자 변환"""
            if pd.isna(rating):
                return None
            rating_str = str(rating).strip()
            # 숫자만 추출
            numbers = re.findall(r'\d+', rating_str)
            if numbers:
                rating_num = int(numbers[0])
                # 10점 만점을 5점 만점으로 변환 (필요시)
                if rating_num > 5:
                    rating_num = rating_num / 2
                return rating_num
            return None
        
        df['rating'] = df['rating'].apply(clean_rating)
        
        print(f"🔍 데이터 정제 후 샘플: {df.iloc[0].to_dict() if len(df) > 0 else '데이터 없음'}")
        
        # convert date column to datetime with better error handling
        try:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            print(f"🔍 날짜 변환 후: {len(df)}개 데이터")
        except Exception as e:
            print(f"❌ 날짜 변환 오류: {e}")
            # 날짜 변환 실패 시 현재 날짜로 설정
            df['date'] = pd.Timestamp.now()
        
        # trash any bad data
        before_drop = len(df)
        df.dropna(subset=['date', 'rating', 'review'], inplace=True)
        after_drop = len(df)
        print(f"🔍 데이터 정제: {before_drop}개 → {after_drop}개")
        
        if len(df) == 0:
            print("❌ 전처리 후 데이터가 없습니다!")
            return []
        
        # make derived variables
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['weekday'] = df['date'].dt.dayofweek
        
        def clean_text(text):
            """
            Simple text cleaning for Korean text.
            :param text: the text to be cleaned.
            :return: the cleaned text.
            """
            text = re.sub(r'[^가-힣\s]', '', text)  # 한글과 공백만 유지
            return text.strip()
            
        df['final_review'] = df['review'].astype(str).apply(clean_text)
        self.data = df
        
        print(f"✅ naver 전처리 완료: {len(df)}개 데이터")
        
        # DataFrame을 dict 리스트로 변환하여 반환
        return df.to_dict('records')
    
    def feature_engineering(self):
        df = self.data
        # temporarily remove vectorization process
        """# tf-idf
        vectorizer = TfidfVectorizer(max_features=100)  # 최대 100개의 단어 선택
        tfidf_matrix = vectorizer.fit_transform(df['review'])
        df['vector'] = tfidf_matrix.toarray().tolist()"""
        self.data = df

    def save_to_database(self):
        if self.output_dir:
            output_path = f"{self.output_dir}/preprocessed_reviews_naver.csv"
            try:
                self.data.to_csv(output_path, index=False)
            except Exception as e:
                print("Output file save failed")
