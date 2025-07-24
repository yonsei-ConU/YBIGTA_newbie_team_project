# 👨‍💻 YBIGTA 27기 팀플 3조

안녕하세요! YBIGTA 27기 팀플 **3조**입니다!!

---

## 👤 자기소개

### 🙋‍♂️ 노유빈
- 이름: **노유빈**
- 학번: **22학번**
- 전공: **연세대학교 전기전자공학과**
- MBTI: **ESTP**

호기심 많고 도전적인 성격으로, 새로운 기술이나 프로젝트를 빠르게 습득하고 실전에서 적용하는 걸 좋아합니다.  
YBIGTA를 통해 함께 배우고 성장해나가고 싶습니다!

---

### 🙋‍♂️ 문영운
- 이름: **문영운**
- 학번: **20학번**
- 전공: **문헌정보학과**
- MBTI: **ISTP**

분석적이고 실용적인 사고를 바탕으로, 팀에 조용한 추진력을 더하는 스타일입니다.  
꾸준히 성장하는 개발자가 되기 위해 노력하고 있습니다.

---

### 🙋‍♂️ 이재열
- 이름: **이재열**
- 학번: **24학번**
- 전공: **컴퓨터과학과**
- MBTI: **????**

차분한 에너지로 팀워크에 기여하며, 컴퓨터과학에 대한 깊은 관심을 가지고 있는 팀원입니다.

# 🧩 Web 과제 - FastAPI 기반 사용자 관리 시스템

이 프로젝트는 FastAPI를 기반으로 한 사용자 로그인/회원가입 시스템입니다.  
MVC 패턴을 적용하여 구조를 나누었고, HTML 인터페이스를 포함해 실제 사용 가능한 미니 웹 서비스를 구현했습니다.

### 📁 프로젝트 구조
```
YBIGTA_newbie_team_project/
├── app/
│ ├── main.py # FastAPI 실행 엔트리포인트
│ ├── static/index.html # 사용자 인터페이스 (디자인 포함)
│ ├── user/
│ │ ├── user_router.py # Controller 역할
│ │ ├── user_service.py # Service 역할
│ │ ├── user_repository.py # Repository 역할
│ │ └── user_schema.py # DTO (Pydantic models)
│ └── responses/base_response.py
├── database/users.json # 가상의 유저 DB
├── tests/ # pytest 기반 테스트
│ ├── test_user_router.py
│ └── test_user_service.py
├── requirements.txt
```

## 🎨 index.html 꾸민 내용

- YBIGTA 로고 및 전체 UI 디자인 추가
- 로그인/회원가입 폼 스타일 개선
- 배경 그라데이션, 버튼 스타일, 사용자 환영 메시지 구현
- 비밀번호 변경 및 계정 삭제 인터페이스 구현

---
## 🚀 코드 실행 방법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. FastAPI 서버 실행
```bash
uvicorn app.main:app --reload
```

### 3. 접속 확인
- http://localhost:8000  
- Swagger 문서: http://localhost:8000/docs


# 🎬 YBIGTA 27기 팀플 3조 – Movie Review Crawlers

안녕하세요! YBIGTA 27기 팀플 **3조**입니다!  
이 프로젝트는 영화 **"Mickey 17 (2025)"**에 대한 유저 리뷰를 수집하는 **웹 크롤러 구현 과제**입니다.  
총 3개의 사이트 **(Rotten Tomatoes, Naver Movie, Letterboxd)** 를 대상으로  
**Selenium**과 **BeautifulSoup**을 활용하여 리뷰를 수집하며,  
수집된 리뷰는 `score`, `date`, `review` 컬럼을 포함한 **CSV 파일**로 저장됩니다.

---

## 📁 디렉토리 구조

```
review_analysis/
└── crawling/
    ├── RottenTomatoesCrawler.py
    ├── naver_movie_crawler.py
    ├── letterboxd_crawler.py
    ├── base_crawler.py
    └── main.py

database/
├── reviews_rotten.csv
├── reviews_naver.csv
└── reviews_letterboxd.csv
```

---

## ⚙️ 설치 및 실행 방법

### 1️⃣ 필수 패키지 설치
```bash
pip install selenium webdriver-manager beautifulsoup4 pandas
```

※ `nltk`가 필요한 경우:
```bash
pip install nltk
python -m nltk.downloader stopwords
```

---

### 2️⃣ 단일 크롤러 실행 예시
```bash
# Rotten Tomatoes
python review_analysis/crawling/main.py -o database -c rotten

# Naver Movie
python review_analysis/crawling/main.py -o database -c naver

# Letterboxd
python review_analysis/crawling/main.py -o database -c letterboxd
```

---

### 3️⃣ 전체 크롤러 실행
```bash
python review_analysis/crawling/main.py -o database --all
```

---

## ✨ 기능 요약

- 🎞️ 대상 영화: **Mickey 17 (2025)**
- ✅ 각 사이트에서 유저 리뷰 **500개 이상** 수집
- 🔁 Load More 버튼 클릭, 무한 스크롤, 페이지네이션 등 자동화 처리
- 📄 `score`, `date`, `review` 컬럼 포함된 CSV 저장
- 🚫 중복 리뷰 자동 제거 (사이트에 따라 적용)

----------------------------------------------------------------------------------------

# 전처리

## 🧪 Rotten Tomatoes 리뷰 전처리 

### EDA: 개별 사이트 리뷰의 시각화 및 특성 설명

---

📈 **일별 리뷰 수 추이**  
![Daily Review Count](https://raw.githubusercontent.com/yonsei-ConU/YBIGTA_newbie_team_project/master/review_analysis/plots/daily_review_count.png)  
- 초기 집중: 4월 초부터 리뷰 수가 급증하며 최대 23개 기록  
- 후기 감소: 5월 중순 이후 일평균 리뷰 수가 5개 이하로 급감  
- 활성 기간: 대체로 4월 초~중순이 가장 활발하게 작성됨

---

📊 **요일별 리뷰 수**  
![Review Count by Weekday](https://raw.githubusercontent.com/yonsei-ConU/YBIGTA_newbie_team_project/master/review_analysis/plots/weekday_review_count.png)  
- 최다 요일: 월요일과 일요일이 각 106건으로 가장 많음  
- 최소 요일: 금요일이 가장 적은 74건  
- 영화 리뷰 작성이 주말과 주 초에 집중되는 경향이 있음

---

📉 **리뷰 길이 vs 평점**  
![Review Length vs Score](https://raw.githubusercontent.com/yonsei-ConU/YBIGTA_newbie_team_project/master/review_analysis/plots/length_vs_score.png)  
- 상관관계: 약 0.084로 매우 약한 양의 상관관계  
- 특이사항: 짧은 리뷰에도 높은 점수가 많은 등, 리뷰 길이와 평점은 밀접하지 않음

### 전처리 및 Feature Engineering 설명
```
    📂 대상 파일 
    - `database/reviews_rotten.csv`  
    - `database/preprocessed_reviews_rotten.csv`

    ⚙️ 전처리 과정  
    - 점수 변환:  
    - 기존 5점 만점 → 10점 만점으로 스케일 변경 (`x2`)
    - 날짜 변환:  
    - `"Jul 21, 2025"` → `"2025-07-21"` 형식으로 변환 
    - 텍스트 정리:  
    - 불필요한 공백 제거 및 결측값 자동 처리

    🧠 Feature Engineering  
    - `review_length` 컬럼 추가  
    - 각 리뷰의 길이 (문자 수)를 정수형으로 저장
    - 추후 분석(군집, 감정 등)에 활용 가능
```

### 비교 분석: 텍스트 통계 기반 분석 결과
```
    📌 주요 지표  
    - 평균 평점: `5.91점`  
    - 전체 수집 기간: `2025-03-31 ~ 2025-07-21 (총 110일)`  
    - 요일별 리뷰 분포:  
    - `월, 일` 최다  
    - `금` 최저  

    📌 상관 분석 
    - 리뷰 길이 vs 점수: `0.084 (양의 상관관계이지만 매우 약함)`  
    - → 평점은 길이와 거의 무관하며, 간단한 리뷰에도 높은 점수가 다수 있음
```

### 실행 방법 요약
```
    a. 크롤링
        python review_analysis/crawling/main.py -o database -c rotten
    b. 전처리 및 FE
        python -m review_analysis.preprocessing.main -c reviews_rotten
    c. 비교분석 결과 출력
        python review_analysis/comparison/compare_rotten.py
    d. 시각화 이미지 생성
        python review_analysis/plots/plot_rotten.py
```

### 결과파일
```
    📄 전처리된 데이터: 
        database/preprocessed_reviews_rotten.csv
    🖼️ 시각화 이미지:
        daily_review_count.png
        length_vs_score.png
        weekday_review_count.png
```


# 분석