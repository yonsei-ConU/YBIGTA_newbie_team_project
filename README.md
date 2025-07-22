# 🎬 Rotten Tomatoes & Naver Movie Review Crawlers

이 프로젝트는 **Selenium**과 **BeautifulSoup**을 활용하여 영화 **"Mickey 17 (2025)"**에 대한 유저 리뷰를 수집하는 크롤러입니다.  
총 3개의 크롤러가 포함되어 있으며, 각각 Rotten Tomatoes와 Naver Movie, letterboxd의 유저 리뷰를 수집합니다.  
수집된 데이터는 평점, 날짜, 리뷰 내용이 포함된 **CSV 파일**로 저장됩니다.

---

## 🍅 Rotten Tomatoes Review Crawler

🔗 [크롤링 대상 링크](https://www.rottentomatoes.com/m/mickey_17/reviews?type=user)

### 📁 프로젝트 구조
```
review_analysis/
└── crawling/
    ├── RottenTomatoesCrawler.py
    ├── base_crawler.py
    └── main.py
database/
└── reviews_rotten.csv
```

### ⚙️ 설치 및 실행

```bash
# 필수 패키지 설치
pip install selenium webdriver-manager beautifulsoup4 pandas

# 실행 명령어
python review_analysis/crawling/main.py -o database -c rotten
```

### ✨ 주요 기능
- 🎞️ 대상 영화: **Mickey 17 (2025)**
- ✅ 최대 500개 이상의 유저 리뷰 자동 수집
- 🔁 `"Load More"` 버튼 자동 클릭 (최대 30회)
- 📄 `score`, `date`, `review` 컬럼 포함한 CSV 저장

### 📌 출력 예시
```
score,date,review
3.5,"Jul 17, 2025","Amazing movie! Loved the cast..."
```

---

## 🎥 Naver Movie Review Crawler

🔗 [크롤링 대상 링크](https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=29816634&qvt=0&query=미키%2017%20관람평)

### 📁 프로젝트 구조
```
review_analysis/
└── crawling/
    ├── naver_movie_crawler.py
    ├── base_crawler.py
    └── main.py
database/
└── reviews_naver.csv
```

### ⚙️ 설치 및 실행

```bash
# 필수 패키지 설치
pip install selenium webdriver-manager beautifulsoup4 pandas

# 실행 명령어
python review_analysis/crawling/main.py -o database -c naver
```

### ✨ 주요 기능
- 🎞️ 대상 영화: **미키 17 (2025)**
- 🔄 최신순 + 공감순 리뷰 모두 수집
- 📜 무한 스크롤 방식으로 리뷰 500개 이상 확보
- 📄 `score`, `date`, `review` 컬럼 포함된 CSV 저장
- 🚫 중복 리뷰 자동 제거

### 📌 출력 예시
```
date,rating,text
2025-02-28,10,"외계인 생물도 뻥카를 칠 수있다."
2025-03-01,8,"로버튼 패티슨의 1인 2역은 신의 한수다..."
```

## 📦 Letterboxd Review Crawler

🔗 [크롤링 대상 링크](<Letterboxd 영화 리뷰 페이지 링크>)

### 📁 프로젝트 구조
```
review_analysis/
└── crawling/
    ├── letterboxd_crawler.py
    ├── base_crawler.py
    └── main.py
database/
└── reviews_letterboxd.csv
```

### ⚙️ 설치 및 실행

```bash
# 필수 패키지 설치
pip install selenium webdriver-manager beautifulsoup4 pandas

# 실행 명령어
python review_analysis/crawling/main.py -o database -c letterboxd
```

### ✨ 주요 기능
- 🎞️ 대상 영화: **Mickey 17 (2025)**
- 🧭 유저 리뷰 500개 이상 자동 수집
- 🔁 페이지네이션 또는 무한 스크롤 처리
- 📄 `score`, `date`, `review` 컬럼 포함한 CSV 저장
- 🚫 중복 리뷰 자동 제거 (선택사항)

### 📌 출력 예시
```
date,rating,review
2025-03-02,4.0,"visually stunning and surprisingly emotional..."
2025-03-03,2.5,"not what I expected, but still enjoyable"
```
