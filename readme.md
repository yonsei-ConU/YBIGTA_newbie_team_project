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

2.설치 및 실행 방법

    a. 필요한 패키지 설치
        pip install selenium webdriver-manager beautifulsoup4 pandas

    b. 실행 명령어
        python review_analysis/crawling/main.py -o database -c rotten

3.기능
    -영화: Mickey 17 (2025)
    -유저 리뷰 최대 500개 이상 자동 수집
    -Load More 버튼 자동 클릭 (최대 30회)
    -score, date, review 컬럼 포함된 .csv 저장

4.출력 예시
    score,date,review
    3.5,"Jul 17, 2025","Amazing movie! Loved the cast..."