from review_analysis.preprocessing.base_preprocessor import BaseDataProcessor
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer

class LetterboxdPreprocessor(BaseDataProcessor):
    def __init__(self, input_path: str = None, output_path: str = None):
        super().__init__(input_path, output_path)

    def preprocess(self, reviews: list[dict]) -> list[dict]:
        # MongoDB에서 받은 데이터를 DataFrame으로 변환
        df = pd.DataFrame(reviews)
        
        # unify column names, order with other preprocessed CSVs
        df.columns = ['rating', 'date', 'review']
        df = df[['date', 'rating', 'review']]
        # convert date column to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        # trash any bad data
        df.dropna(subset=['date', 'rating', 'review'], inplace=True)
        # make derived variables
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['weekday'] = df['date'].dt.dayofweek
        
        def clean_text(text):
            """
            Simple text cleaning without NLTK stopwords.
            :param text: the text to be cleaned.
            :return: the cleaned text.
            """
            text = text.lower()
            text = re.sub(r'[^a-z0-9\s]', '', text)
            return text.strip()
            
        df['final_review'] = df['review'].astype(str).apply(clean_text)
        self.data = df
        
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
            output_path = f"{self.output_dir}/preprocessed_reviews_letterboxd.csv"
            try:
                self.data.to_csv(output_path, index=False)
            except Exception as e:
                print("Output file save failed")
