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
- MBTI: **ISTP**

깊은 이론적 배경지식과 열정을 가지고 있습니다.
YBIGTA에서 하는 많은 프로젝트를 통해 성장하고 싶습니다.

<br> </br>


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

<br> </br>



# 🎬 Mickey 17 (2025) Review Crawlers

**Selenium + BeautifulSoup** 기반 크롤러 3종을 통해  
**Rotten Tomatoes, Naver Movie, Letterboxd**의 유저 리뷰 데이터를 수집합니다.

---

## 📌 공통 기능

- 🎞️ 대상 영화: **Mickey 17 (2025)**
- 📦 사용 기술: `Selenium`, `BeautifulSoup`, `pandas`, `webdriver-manager`
- ✅ 각 사이트별 리뷰 **500개 이상 자동 수집**
- 💾 출력 형식: `score`, `date`, `review` 컬럼을 포함한 **CSV 파일** 저장  
- 📁 저장 위치: `database/reviews_사이트이름.csv`
- 🛠️ 실행 방식:

    ```bash
    # 필수 패키지 설치
    pip install selenium webdriver-manager beautifulsoup4 pandas

    # 크롤링 명령어
    python review_analysis/crawling/main.py -o database -c [사이트이름]
    ```

    예시:
    ```bash
    python review_analysis/crawling/main.py -o database -c rotten
    python review_analysis/crawling/main.py -o database -c naver
    python review_analysis/crawling/main.py -o database -c letterboxd
    ```

---

## 💡 사이트별 크롤링 특징

### 🍅 Rotten Tomatoes

- 🔗 [리뷰 페이지 링크](https://www.rottentomatoes.com/m/mickey_17/reviews?type=user)
- 🔁 `"Load More"` 버튼 최대 30회 클릭 자동화
- 🌐 미국 사이트 특성상 영어 리뷰가 다수
- ✅ 간결하고 깔끔한 HTML 구조

**출력 예시:**
```
score,date,review
3.5,"Jul 17, 2025","Amazing movie! Loved the cast..."
```

---

### 🎥 Naver Movie

- 🔗 [관람평 페이지 링크](https://search.naver.com/search.naver?...query=미키%2017%20관람평)
- 🔄 **최신순 + 공감순** 정렬 리뷰를 병합 수집
- 📜 **무한 스크롤** 방식 구현 (각 정렬 기준 최대 300개 수집)
- 🚫 중복 리뷰 자동 제거 포함
- ⚠️ HTML 구조가 자주 변경되므로 유지보수 필요

**출력 예시:**
```
date,rating,text
2025-02-28,10,"외계인 생물도 뻥카를 칠 수있다."
2025-03-01,8,"로버튼 패티슨의 1인 2역은 신의 한수다..."
```

---

### 📦 Letterboxd

- 🔗 [리뷰 페이지 링크](*링크 입력 필요*)
- 🔄 **무한 스크롤 또는 페이지네이션** 자동 처리
- 🚫 중복 리뷰 제거 여부는 선택사항 (기본 OFF)
- 📝 리뷰 포맷이 자유롭고 캐주얼한 경향

**출력 예시:**
```
date,rating,review
2025-03-02,4.0,"visually stunning and surprisingly emotional..."
2025-03-03,2.5,"not what I expected, but still enjoyable"
```

---

## 📂 관련 디렉토리 구조

```text
review_analysis/
└── crawling/
    ├── base_crawler.py              # 크롤러 상속 기반 클래스
    ├── RottenTomatoesCrawler.py     # Rotten Tomatoes 크롤러
    ├── naver_movie_crawler.py       # Naver Movie 크롤러
    ├── letterboxd_crawler.py        # Letterboxd 크롤러
    └── main.py                      # 크롤링 실행 진입점
database/
    ├── reviews_rotten.csv
    ├── reviews_naver.csv
    └── reviews_letterboxd.csv
```


<br> </br>

# 🧪 Mickey 17 (2025) Review Preprocessing

**세 리뷰 사이트(Rotten Tomatoes, Naver Movie, Letterboxd)**로부터 수집한 데이터를 통일된 형식으로 전처리하고,  
텍스트 정제 및 날짜 기반 피처 엔지니어링을 수행하여 분석 가능한 형태의 CSV 파일로 저장합니다.

---

## 📌 공통 처리 내용

- 📄 컬럼 통일: `date`, `rating`, `review` 순으로 정렬  
- 🗓️ 날짜 형식 정제: 다양한 형식을 `YYYY-MM-DD`로 통일  
- 🧹 텍스트 정제: 소문자화, 특수문자 제거, 불용어 제거 등 사이트별 최적화 처리  
- 🧠 파생 변수 생성: `year`, `month`, `weekday`, `final_review` 컬럼 추가  
- 💾 전처리된 CSV 파일은 `database/preprocessed_reviews_사이트이름.csv`로 저장됨

---

## 💡 사이트별 전처리 차이점

### 🍅 Rotten Tomatoes
- `score` 컬럼을 **5점 만점 → 10점 만점**으로 환산  
- 날짜 형식 `"Jul 21, 2025"` → `"2025-07-21"`로 변환  
- 영어 텍스트를 소문자 처리 + 특수문자 제거  
- TF-IDF 벡터화 수행 (단, **벡터 저장은 생략**)

### 🎥 Naver Movie
- `rating` 컬럼에서 숫자 추출 및 유효 범위(0~10) 내 정제  
- 리뷰 길이가 **20~1000자 사이인 데이터만 유지**  
- 한글 리뷰에서 **특수문자/영어 제거** 및 **다중 공백 제거**  
- TF-IDF 벡터화 결과를 `.npz`, `.npy` 파일로 저장 (**실행 시 생성됨**)

### 📦 Letterboxd
- 영어 리뷰를 소문자 처리 후 특수문자 제거  
- 불용어(stopwords) 제거로 텍스트 정제  
- TF-IDF는 임시 비활성화 (필요시 주석 해제 가능)

---

## 🛠️ 실행 방법

```bash
# 모든 사이트 전처리 일괄 실행
python review_analysis/preprocessing/main.py --all

# 특정 사이트만 실행 (예: Rotten Tomatoes)
python review_analysis/preprocessing/main.py -c reviews_rotten

# 출력 경로 지정 가능 (기본값은 database/)
python review_analysis/preprocessing/main.py -o custom_dir -c reviews_naver
```

---

## 📂 전처리 파일 구조

```text
review_analysis/
└── preprocessing/
    ├── base_preprocessor.py            # 공통 추상 클래스
    ├── rotten_preprocessor.py          # Rotten 리뷰 전처리
    ├── naver_preprocessor.py           # Naver 리뷰 전처리
    ├── letterboxd_preprocessor.py      # Letterboxd 리뷰 전처리
    └── main.py                         # 전처리 실행용 진입점
database/
    ├── preprocessed_reviews_rotten.csv
    ├── preprocessed_reviews_naver.csv
    ├── preprocessed_reviews_letterboxd.csv
    ├── vector_matrix_tfidf.npz         # 🔄 (Naver 전처리 실행 시 자동 생성)
    └── vocab_tfidf.npy                 # 🔄 (Naver 전처리 실행 시 자동 생성)
```

> ⚠️ `.npz`, `.npy` 파일은 GitHub에 포함되어 있지 않으며,  
> `NaverPreprocessor`를 실행하면 자동 생성됩니다.


# 📊 EDA
## 📊 사이트별 리뷰 EDA

---

### 🎥 Naver Movie

#### 1️⃣ 일별 리뷰 수 추이  
![일별 리뷰 수 추이 (Naver)](review_analysis/plots/일별%20리뷰%20수%20추이%20(Naver).png)  
- 리뷰가 **짧은 기간에 집중됨**
- 특히 **주말과 주초에 급증**

#### 2️⃣ 요일별 리뷰 수  
![요일별 리뷰 수 (Naver)](review_analysis/plots/요일별%20리뷰%20수%20(0=월요일%20~%206=일요일)%20(Naver).png)  
- **월·금·토·일** 리뷰 많음  
- **화~목**은 상대적으로 적음 → 감상 패턴과 일치

#### 3️⃣ 월별 리뷰 수  
![월별 리뷰 수 (Naver)](review_analysis/plots/월별%20리뷰%20수%20(Naver).png)  
- 대부분 **3~4월**에 몰림  
- 영화 개봉 및 초기 반응 집중 추정

#### 4️⃣ 평점 분포  
![평점 분포 (Naver)](review_analysis/plots/평점%20분포%20(Naver).png)  
- **8~10점**에 다수 분포 → **긍정적 평가 중심**
- **0~3점** 악평도 일부 존재

#### 5️⃣ 리뷰 길이 vs 평점  
![리뷰 길이 vs 평점 (Naver)](review_analysis/plots/리뷰%20길이%20vs%20평점%20(Naver).png)  
- 상관계수 **+0.08** → **거의 무상관**
- 긴 리뷰가 반드시 고평점은 아님

✍️ **요약**  
→ 리뷰 수와 평점 모두 긍정적인 경향이며,  
작성 시점은 **개봉 초기 + 주말 중심**.  
리뷰 길이와 평점은 큰 관계 없음.

---

### 🍅 Rotten Tomatoes

#### 1️⃣ 일별 리뷰 수 추이  
![일별 리뷰 수 추이 (Rotten)](review_analysis/plots/일별%20리뷰%20수%20추이%20(Rotten).png)  
- **4월 초 집중**, **5월 말~6월 초 재상승**
- 개봉 초기 + 후속 반응 구간 존재

#### 2️⃣ 요일별 리뷰 수  
![요일별 리뷰 수 (Rotten)](review_analysis/plots/요일별%20리뷰%20수%20(0=월요일%20~%206=일요일)%20(Rotten).png)  
- **월요일·일요일**에 가장 많음  
- **금요일**은 리뷰 가장 적음

#### 3️⃣ 월별 리뷰 수  
![월별 리뷰 수 (Rotten)](review_analysis/plots/월별%20리뷰%20수%20(Rotten).png)  
- **4월 리뷰 집중**, 이후 점차 감소  
- 개봉 후 짧은 기간 반응 쏠림

#### 4️⃣ 평점 분포  
![평점 분포 (Rotten)](review_analysis/plots/평점%20분포%20(Rotten).png)  
- **7~10점** 우세하지만  
- **낮은 평점도 일정 비중 존재** → 호불호 강함

#### 5️⃣ 리뷰 길이 vs 평점  
![리뷰 길이 vs 평점 (Rotten)](review_analysis/plots/리뷰%20길이%20vs%20평점%20(Rotten).png)  
- 상관계수 **+0.083** → **거의 무상관**

✍️ **요약**  
→ 개봉 초기 및 특정 시점에 반응 집중.  
**긍정 평가 우세하나**, **호불호가 갈리는 분포**.  
리뷰 길이와 평점은 상관 거의 없음.

---

### 📦 Letterboxd

#### 1️⃣ 일별 리뷰 수 추이  
![일별 리뷰 수 추이 (Letterboxd)](review_analysis/plots/일별%20리뷰%20수%20추이%20(Letterboxd).png)  
- 리뷰 대부분 **7월 말에 집중**  
- 최근 리뷰 중심으로 수집된 것으로 추정

#### 2️⃣ 요일별 리뷰 수  
![요일별 리뷰 수 (Letterboxd)](review_analysis/plots/요일별%20리뷰%20수%20(0=월요일%20~%206=일요일)%20(Letterboxd).png)  
- **월요일 리뷰 최다**  
- 수집 시점의 영향일 가능성 있음

#### 3️⃣ 월별 리뷰 수  
![월별 리뷰 수 (Letterboxd)](review_analysis/plots/월별%20리뷰%20수%20(Letterboxd).png)  
- **7월에 몰림**  
- 크롤링 방식에 따라 발생한 쏠림 현상

#### 4️⃣ 평점 분포  
![평점 분포 (Letterboxd)](review_analysis/plots/평점%20분포%20(Letterboxd).png)  
- **6~8점** 집중 → 비교적 **보통 이상 평가**
- **5점 이하**는 적음 → 악평 드묾

#### 5️⃣ 리뷰 길이 vs 평점  
![리뷰 길이 vs 평점 (Letterboxd)](review_analysis/plots/리뷰%20길이%20vs%20평점%20(Letterboxd).png)  
- 상관계수 **-0.021** → **무상관**

✍️ **요약**  
→ 최신 리뷰 위주로 수집되어 시기 집중 현상 있음.  
전반적으로 **온건한 긍정 평가**,  
리뷰 길이와 평점의 관계는 없음.
