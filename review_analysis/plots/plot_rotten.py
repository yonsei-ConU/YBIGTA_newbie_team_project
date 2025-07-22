import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 데이터 불러오기
df = pd.read_csv("database/preprocessed_reviews_rotten.csv")
df['date'] = pd.to_datetime(df['date'])
df['weekday'] = df['date'].dt.day_name()
df['review_length'] = df['review'].astype(str).apply(len)

# 저장 폴더 설정
output_dir = "review_analysis/plots"
os.makedirs(output_dir, exist_ok=True)


# 1. 날짜별 리뷰 수
plt.figure(figsize=(12, 4))
df['date'].value_counts().sort_index().plot(kind='line')
plt.title("Daily Review Count")
plt.xlabel("Date")
plt.ylabel("Review Count")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "daily_review_count.png"))
plt.close()


# 2. 요일별 리뷰 수
plt.figure(figsize=(8, 4))
sns.countplot(x="weekday", data=df, order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
plt.title("Review Count by Weekday")
plt.xlabel("Weekday")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "weekday_review_count.png"))
plt.close()


# 3. 리뷰 길이 vs 평점 스캐터
plt.figure(figsize=(8, 4))
sns.scatterplot(x="review_length", y="score", data=df, alpha=0.4)
plt.title("Review Length vs Score")
plt.xlabel("Review Length")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "length_vs_score.png"))
plt.close()
