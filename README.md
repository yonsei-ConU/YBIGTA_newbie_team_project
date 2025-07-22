Rotten Tomatoes Review Crawler

    Selenium을 활용해 Rotten Tomatoes에서 특정 영화의 유저 리뷰를 크롤링하고, 평점(score), 날짜(date), 리뷰 내용(review)을 추출해 CSV 파일로 저장하는 프로젝트입니다.
    크롤링한 사이트의 링크는 다음과 같습니다.
    https://www.rottentomatoes.com/m/mickey_17/reviews?type=user

1.프로젝트 구조
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