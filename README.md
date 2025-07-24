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

차분한 에너지로 팀워크에 기여하며, 컴퓨터과학에 대한 깊은 관심을 가지고 있는 팀원입니다.

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


# 리뷰 사이트별 EDA
## 🧪 Naver 리뷰 EDA

### 1️⃣ 일별 리뷰 수 추이  
![일별 리뷰 수 추이 (Naver)](review_analysis/plots/일별%20리뷰%20수%20추이%20(Naver).png)  
- 리뷰가 특정 **주말과 주초**에 집중되며 **짧은 기간에 몰림** 현상 보임  
- 일평균 리뷰 수는 **5~10개 수준**

### 2️⃣ 요일별 리뷰 수  
![요일별 리뷰 수 (Naver)](review_analysis/plots/요일별%20리뷰%20수%20(0=월요일%20~%206=일요일)%20(Naver).png)  
- **주말(토~일)**과 **금요일, 월요일**에 리뷰 수가 높음  
- **주중(화~목)**은 상대적으로 낮은 활동량  
- 영화 감상 패턴과 연계된 작성 습관 가능성

### 3️⃣ 월별 리뷰 수  
![월별 리뷰 수 (Naver)](review_analysis/plots/월별%20리뷰%20수%20(Naver).png)  
- 대부분의 리뷰는 **한 달(3~4월)** 사이에 집중  
- 특정 기간에 이슈나 홍보 요인이 있었을 가능성

### 4️⃣ 평점 분포  
![평점 분포 (Naver)](review_analysis/plots/평점%20분포%20(Naver).png)  
- **8~10점에 몰림** → **긍정적인 평가**가 많음  
- **0~3점** 분포도 일부 존재 → **악평도 존재**

### 5️⃣ 리뷰 길이 vs 평점  
![리뷰 길이 vs 평점 (Naver)](review_analysis/plots/리뷰%20길이%20vs%20평점%20(Naver).png)  
- 상관계수 **+0.08**로, **매우 약한 양의 상관관계**  
- 길이가 길다고 해서 무조건 높은 평점을 주는 건 아님  
- **짧은 리뷰에도 긍정/부정 표현 충분히 가능**

---

✍️ **요약**  
네이버 리뷰는 **특정 시기에 몰려 있는 경향**이 있고,  
**전반적으로 긍정적 평가가 많은 편**이며  
**리뷰 길이와 평점 사이의 뚜렷한 관계는 없음**.


## 🍅 Rotten Tomatoes 리뷰 EDA
### 📌 **1. 일별 리뷰 수 추이 (Rotten)**  
![일별 리뷰 수 추이 (Rotten)](review_analysis/plots/일별%20리뷰%20수%20추이%20(Rotten).png)  
- 4월 초~중순에 리뷰 수 급증, 이후 점차 감소하다가 5월 말~6월 초, 6월 중순에 리뷰 증가
- 개봉 초기 이외에도 **5월 말~6월 초 집중**이 특징  

### 📌 **2. 요일별 리뷰 수 (Rotten)**  
![요일별 리뷰 수 (0=월요일 ~ 6=일요일) (Rotten)](review_analysis/plots/요일별%20리뷰%20수%20(0=월요일%20~%206=일요일)%20(Rotten).png)  
- 최다 요일: 월요일과 일요일이 각 106건으로 가장 많음
- 최소 요일: 금요일이 가장 적은 74건
- 영화 리뷰 작성이 주말과 주 초에 집중되는 경향이 있음

### 📌 **3. 월별 리뷰 수 (Rotten)**  
![월별 리뷰 수 (Rotten)](review_analysis/plots/월별%20리뷰%20수%20(Rotten).png)  
- 리뷰의 대부분이 4월에 집중  
- 해당 시기에 **개봉 또는 홍보**가 있었을 가능성 있음  

### 📌 **4. 평점 분포 (Rotten)**  
![평점 분포 (Rotten)](review_analysis/plots/평점%20분포%20(Rotten).png)  
- **7~10점 분포가 우세**하여 긍정적인 평가 비중 높음  
- 다만 전반적으로 고루 분포하여, 호불호가 갈리는 영화임을 보여줌

📌 **5. 리뷰 길이 vs 평점 (Rotten)**  
![리뷰 길이 vs 평점 (Rotten)](review_analysis/plots/리뷰%20길이%20vs%20평점%20(Rotten).png)  
- 🔍 리뷰 길이와 평점의 상관계수: **+0.083**  
- **매우 약한 양의 상관관계** → 길이가 평가에 큰 영향 없음  


> ✍️ 전반적으로 Rotten 리뷰는 개봉 초기 집중되며,  
> **긍정적 평가가 다소 강한 편**이나 부정적 평가도 존재하는 호불호가 강한 영화로 판단됨


## 🎬 Letterboxd 리뷰 EDA

### 📌 **1. 일별 리뷰 수 추이 (Letterboxd)**  
![일별 리뷰 수 추이 (Letterboxd)](review_analysis/plots/일별%20리뷰%20수%20추이%20(Letterboxd).png)  
- 리뷰는 7월 말에 집중적으로 작성된 것으로 보임
- 크롤링을 하는 과정에서 최신 작성된 리뷰 500여개를 수집한 것으로 추정

### 📌 **2. 요일별 리뷰 수 (Letterboxd)**  
![요일별 리뷰 수 (0=월요일 ~ 6=일요일) (Letterboxd)](review_analysis/plots/요일별%20리뷰%20수%20(0=월요일%20~%206=일요일)%20(Letterboxd).png)  
- 월요일에 작성된 리뷰가 가장 많음
- 월요일에 크롤링을 진행했으리라 추정

### 📌 **3. 월별 리뷰 수 (Letterboxd)**  
![월별 리뷰 수 (Letterboxd)](review_analysis/plots/월별%20리뷰%20수%20(Letterboxd).png)  
- 월별 리뷰 수는 7월에 밀집되어 있음  

### 📌 **4. 평점 분포 (Letterboxd)**  
![평점 분포 (Letterboxd)](review_analysis/plots/평점%20분포%20(Letterboxd).png)  
- **6~8점에 가장 많이 분포**  
- 5점 이하도 드물며, **대체로 긍정적인 평가**  

### 📌 **5. 리뷰 길이 vs 평점 (Letterboxd)**  
![리뷰 길이 vs 평점 (Letterboxd)](review_analysis/plots/리뷰%20길이%20vs%20평점%20(Letterboxd).png)  
- 🔍 리뷰 길이와 평점의 상관계수: **-0.021**  
- **거의 무상관** → 리뷰 길이와 평점 사이 관련성 없음  

---

> ✍️ **요약**  
> Letterboxd 리뷰는 최근 7월 중순~말경에 데이터가 집중적으로 수집되었으며 
> **대체로 긍정 평가가 나타나는** 경향을 보임.  
> 리뷰 길이와 평점은 **거의 관계가 없는 것**으로 분석됨.


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

