import pandas as pd

# 데이터 불러오기
df = pd.read_csv("database/preprocessed_reviews_rotten.csv")

# 1. 평균 평점
print("📌 평균 평점:", df['score'].mean())

# 2. 날짜별 리뷰 개수
print("\n📌 날짜별 리뷰 수:")
print(df['date'].value_counts().sort_index())

# 3. 요일별 리뷰 수 (weekday)
df['weekday'] = pd.to_datetime(df['date']).dt.day_name()
print("\n📌 요일별 리뷰 수:")
print(df['weekday'].value_counts())

# 4. 리뷰 길이별 평점 평균
df['review_length'] = df['review'].astype(str).apply(len)
print("\n📌 리뷰 길이 vs 점수 상관:")
print(df[['review_length', 'score']].corr())
