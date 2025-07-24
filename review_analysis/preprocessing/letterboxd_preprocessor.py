from review_analysis.preprocessing.base_preprocessor import BaseDataProcessor
import pandas
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# run this only once to download the stopwords
# if you haven't downloaded the stopwords yet, uncomment the next two lines
# import nltk
# nltk.download('stopwords', quiet=True)

class LetterboxdPreprocessor(BaseDataProcessor):
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.stop_words = set(stopwords.words('english'))

    def preprocess(self):
        # load csv
        try:
            df = pandas.read_csv(self.input_path)
        except Exception as e:
            print("CSV load failed:", e)
            return
        # unify column names, order with other preprocessed CSVs
        df.columns = ['rating', 'date', 'review']
        df = df[['date', 'rating', 'review']]
        # convert date column to datetime
        df['date'] = pandas.to_datetime(df['date'], errors='coerce')
        # trash any bad data
        df.dropna(subset=['date', 'rating', 'review'], inplace=True)

        def clean_text(text):
            """
            removes special characters or stop words.
            :param text: the text to be cleaned.
            :return: the text after removing special characters or stop words.
            """
            text = text.lower()
            text = re.sub(r'[^a-z0-9\s]', '', text)
            return ' '.join([word for word in text.split() if word not in self.stop_words])

        df['final_review'] = df['review'].astype(str).apply(clean_text)
        self.data = df
    
    def feature_engineering(self):
        # make derived variables
        df = self.data
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['weekday'] = df['date'].dt.dayofweek
        # temporarily remove vectorization process
        """# tf-idf
        vectorizer = TfidfVectorizer(max_features=100)  # 최대 100개의 단어 선택
        tfidf_matrix = vectorizer.fit_transform(df['review'])
        df['vector'] = tfidf_matrix.toarray().tolist()"""
        self.data = df

    def save_to_database(self):
        output_path = f"{self.output_dir}/preprocessed_reviews_letterboxd.csv"
        try:
            self.data.to_csv(output_path, index=False)
        except Exception as e:
            print("Output file save failed")
