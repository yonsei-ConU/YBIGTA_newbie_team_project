# 👨‍💻 YBIGTA 27기 팀플 3조

안녕하세요! YBIGTA 27기 팀플 **3조**입니다!!

## 👤 자기소개
### 🙋‍♂️ 노유빈
- 이름: **노유빈**
- 학번: **22학번**
- 전공: **전기전자공학과**
- MBTI: **ESTP**

호기심 많고 도전적인 성격으로, 새로운 기술이나 프로젝트를 빠르게 습득하고 실전에서 적용하는 걸 좋아합니다.  
YBIGTA를 통해 함께 배우고 성장해나가고 싶습니다!

### 🙋‍♂️ 문영운
- 이름: **문영운**
- 학번: **20학번**
- 전공: **문헌정보학과**
- MBTI: **ISTP**

쉽게 넘기지 않고, 끝까지 파고드는 분석 습관이 저의 강점입니다.
함께 고민하며 성장하는 YBIGTA의 일원이 되고 싶습니다.


### 🙋‍♂️ 이재열
- 이름: **이재열**
- 학번: **24학번**
- 전공: **컴퓨터과학과**
- MBTI: **ISTP**

깊은 이론적 배경지식과 열정을 가지고 있습니다.
YBIGTA에서 하는 많은 프로젝트를 통해 성장하고 싶습니다.

<br> </br>

<details>
<summary> 🧩 Web 과제 - FastAPI 기반 사용자 관리 시스템 </summary>

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

## 💡 사이트별 크롤링 특징 및 데이터 소개

### 🍅 Rotten Tomatoes

- 🔗 [리뷰 페이지 링크](https://www.rottentomatoes.com/m/mickey_17/reviews?type=user)
- 🔁 `"Load More"` 버튼 최대 30회 클릭 자동화
- 🌐 미국 사이트 특성상 영어 리뷰가 다수
- ✅ 간결하고 깔끔한 HTML 구조
- 데이터 형식 `df.dtypes`
    | Column | Data Type |
    |--------|-----------|
    | scor   | float64     |
    | date   | object    |
    | review | object    |
- 데이터 개수 `df.shape` : (620, 3)

**출력 예시:**
```
score,date,review
3.5,"Jul 17, 2025","Amazing movie! Loved the cast..."
```

---

### 🎥 Naver Movie

- 🔗 [관람평 페이지 링크](https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=29816634&qvt=0&query=미키%2017%20관람평)
- 🔄 **최신순 + 공감순** 정렬 리뷰를 병합 수집
- 📜 **무한 스크롤** 방식 구현 (각 정렬 기준 최대 300개 수집)
- 🚫 중복 리뷰 자동 제거 포함
- ⚠️ HTML 구조가 자주 변경되므로 유지보수 필요

- 데이터 형식 `df.dtypes`
    | Column | Data Type |
    |--------|-----------|
    | star   | int64     |
    | date   | object    |
    | text   | object    |
- 데이터 개수 `df.shape` : (576, 3)


**출력 예시:**
```
date,rating,text
2025-02-28,10,"외계인 생물도 뻥카를 칠 수있다."
2025-03-01,8,"로버튼 패티슨의 1인 2역은 신의 한수다..."
```

---

### 📦 Letterboxd

- 🔗 [리뷰 페이지 링크](https://letterboxd.com/film/mickey-17/reviews/)
- ⭐ 별점 환산: ★ 개수와 ½ 문자를 파싱해 10점 만점 점수로 변환
- 🗓️ ISO 날짜 추출: <time datetime="…"> 속성에서 정확한 날짜 정보 획득
- 💾 CSV 저장: utf-8-sig 인코딩으로 reviews_letterboxd.csv 파일 생성 (pathlib 사용)
- 🕘 최신순 추출: 최신 리뷰 순서대로 추출
- 데이터 형식 `df.dtypes`
    | Column | Data Type |
    |--------|-----------|
    | star   | int64     |
    | date   | object    |
    | text   | object    |
- 데이터 개수 `df.shape` : (500, 3)

**출력 예시:**
```
star,date,text
6,2025-04-26,Cool concept and some funny moments but drags on WAYYYY too long
10,2025-07-23,The relationship between Nasha and the two Mickeys gave Challengers energy.
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
python -m review_analysis.preprocessing.main --all

# 특정 사이트만 실행 (예: Rotten Tomatoes)
python -m review_analysis.preprocessing.main -c reviews_rotten
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

## 🎥 Naver Movie

### 1️⃣ 일별 리뷰 수 추이  
![일별 리뷰 수 추이 (Naver)](review_analysis/plots/일별%20리뷰%20수%20추이%20(Naver).png)  
- 리뷰가 **짧은 기간에 집중**  
- **주말과 주초**에 급증하는 경향

### 2️⃣ 요일별 리뷰 수  
![요일별 리뷰 수 (Naver)](review_analysis/plots/요일별%20리뷰%20수%20(0=월요일%20~%206=일요일)%20(Naver).png)  
- **월·금·토·일**에 리뷰가 많음  
- **화~목**은 상대적으로 적음 → 감상 후 일정 지연 반영

### 3️⃣ 월별 리뷰 수  
![월별 리뷰 수 (Naver)](review_analysis/plots/월별%20리뷰%20수%20(Naver).png)  
- 리뷰가 **3~4월에 몰림**  
- 개봉 직후 반응 집중 현상

### 4️⃣ 평점 분포  
![평점 분포 (Naver)](review_analysis/plots/평점%20분포%20(Naver).png)  
- **8~10점**에 분포 집중 → 전반적으로 **긍정적 평가 우세**  
- 일부 **악평(0~3점)**도 존재

### 5️⃣ 리뷰 길이 vs 평점  
![리뷰 길이 vs 평점 (Naver)](review_analysis/plots/리뷰%20길이%20vs%20평점%20(Naver).png)  
- 상관계수 **+0.08** → **거의 무상관**  
- 긴 리뷰라고 해서 고평점인 것은 아님

### ✍️ 요약  
→ 리뷰는 **개봉 직후 + 주말 중심**으로 몰리며 전반적으로 **긍정적 평가가 많음**.  
리뷰 길이와 평점은 명확한 상관 없음.

---

## 🍅 Rotten Tomatoes

### 1️⃣ 일별 리뷰 수 추이  
![일별 리뷰 수 추이 (Rotten)](review_analysis/plots/일별%20리뷰%20수%20추이%20(Rotten).png)  
- **4월 초 집중**, **5~6월 재상승**  
- 개봉 초기 반응과 후속 관심 시점 존재

### 2️⃣ 요일별 리뷰 수  
![요일별 리뷰 수 (Rotten)](review_analysis/plots/요일별%20리뷰%20수%20(0=월요일%20~%206=일요일)%20(Rotten).png)  
- **월요일·일요일** 리뷰 집중  
- **금요일** 리뷰 수 가장 적음

### 3️⃣ 월별 리뷰 수  
![월별 리뷰 수 (Rotten)](review_analysis/plots/월별%20리뷰%20수%20(Rotten).png)  
- **4월 리뷰 집중**, 이후 점차 감소

### 4️⃣ 평점 분포  
![평점 분포 (Rotten)](review_analysis/plots/평점%20분포%20(Rotten).png)  
- **7~10점**이 우세하나  
- **저평점 분포도 존재** → **호불호 강한 영화로 해석 가능**

### 5️⃣ 리뷰 길이 vs 평점  
![리뷰 길이 vs 평점 (Rotten)](review_analysis/plots/리뷰%20길이%20vs%20평점%20(Rotten).png)  
- 상관계수 **+0.083** → **무상관**

### ✍️ 요약  
→ 개봉 후 특정 시점 반응 집중, **긍정 평가 우세하나 호불호 뚜렷**.  
리뷰 길이와 평점 관계는 없음.

---

## 📦 Letterboxd

### 1️⃣ 일별 리뷰 수 추이  
![일별 리뷰 수 추이 (Letterboxd)](review_analysis/plots/일별%20리뷰%20수%20추이%20(Letterboxd).png)  
- 리뷰 대부분 **7월 말 집중**  
- 수집 시점의 영향 반영

### 2️⃣ 요일별 리뷰 수  
![요일별 리뷰 수 (Letterboxd)](review_analysis/plots/요일별%20리뷰%20수%20(0=월요일%20~%206=일요일)%20(Letterboxd).png)  
- **월요일 리뷰 최다**  
- 수집 날짜와 겹칠 가능성

### 3️⃣ 월별 리뷰 수  
![월별 리뷰 수 (Letterboxd)](review_analysis/plots/월별%20리뷰%20수%20(Letterboxd).png)  
- 리뷰의 **7월 집중 현상** → 최신 리뷰 중심 수집 결과

### 4️⃣ 평점 분포  
![평점 분포 (Letterboxd)](review_analysis/plots/평점%20분포%20(Letterboxd).png)  
- **6~8점**에 집중 → **온건한 긍정 평가 경향**

### 5️⃣ 리뷰 길이 vs 평점  
![리뷰 길이 vs 평점 (Letterboxd)](review_analysis/plots/리뷰%20길이%20vs%20평점%20(Letterboxd).png)  
- 상관계수 **-0.021** → **무상관**

### ✍️ 요약  
→ 최근 리뷰 위주 수집으로 특정 시기 집중,  
전반적으로 **긍정적 평가** 비중 높고, 리뷰 길이와 평점 관계는 없음.

---

## 📊 사이트 간 리뷰 비교 분석

### 1️⃣ 일별 리뷰 수 비교  
![일별 리뷰 수 추이](review_analysis/plots/사이트%20간%20일별%20리뷰%20수%20비교.png)  
- Naver: **3~4월 집중**  
- Rotten: **4~5월 고르게 분포**  
- Letterboxd: **7월 급격한 증가**

### 2️⃣ 누적 리뷰 수 비교  
![누적 리뷰 수 추이](review_analysis/plots/사이트%20간%20누적%20리뷰%20수%20추이%20비교.png)  
- Naver: 빠른 초반 증가  
- Rotten: **전체 리뷰 수 가장 많음**  
- Letterboxd: **단기간 폭발적 증가**

> 📌 요약  
> 수집 시기와 크롤링 시점이 리뷰 수 추이에 큰 영향  
> 단순 비교보다는 **시계열 흐름 고려 필요**

### 3️⃣ 요일별 리뷰 수 비교  
![요일별 리뷰 수 비교](review_analysis/plots/사이트%20간%20요일별%20리뷰%20수%20비교.png)  
- Letterboxd: **화요일 집중 (수집일 영향)**  
- Naver: **주말 + 목요일 집중**  
- Rotten: **요일별 분산 뚜렷**

### 4️⃣ 평점 분포 비교  
![사이트 간 평점 분포 비교](review_analysis/plots/사이트%20간%20평점%20분포%20비교.png)  
- Naver: **긍정 평가 강함**  
- Letterboxd: **보통 이상 평가 중심**  
- Rotten: **고른 분포, 비판 성향 강함**

### 5️⃣ 리뷰 길이 분포 비교  
![사이트 간 리뷰 길이 분포 비교](review_analysis/plots/사이트%20간%20리뷰%20길이%20분포%20비교(20~1000자).png)  
- Rotten: **가장 긴 리뷰**  
- Naver: **가장 짧은 리뷰**  
→ **언어 및 플랫폼 문화에 따라 길이 차이 존재**

### 6️⃣ 평균 평점 및 분산 비교  
![사이트별 평균 평점 및 분산 비교](review_analysis/plots/사이트별%20평균%20평점%20및%20분산%20비교.png)

| 플랫폼         | 평균 평점 | 표준편차 |
|----------------|-----------|-----------|
| Letterboxd     | **7.29**  | **1.68**  |
| Naver          | 6.64      | 2.92      |
| Rotten         | 5.91      | 3.01      |

> ✍️ Letterboxd는 **일관된 긍정 평가**, Rotten은 **다양한 의견 분포**  
> 단순 평균보다는 **분산 포함 해석 필요**

---

## 🧠 플랫폼별 TF-IDF 키워드 분석

### 1️⃣ 플랫폼별 상위 TF-IDF 키워드 비교  
![플랫폼별 TF-IDF 키워드 비교](review_analysis/plots/플랫폼별%20TFIDF%20키워드비교.png)

| 플랫폼 | 주요 키워드 | 해석 |
|--------|--------------|------|
| **Letterboxd** | `robert`, `pattinson`, `filme`, `que`, `de`, `la` | 배우 중심, 비영어권 단어 혼재 |
| **Naver** | `너무`, `진짜`, `정말`, `봉준호`, `미키` | 감탄 표현 + 감독/배우 언급 |
| **Rotten** | `good`, `movie`, `film`, `great`, `story` | 전형적인 영어 리뷰 키워드 |

> ✍️ 플랫폼마다 **표현 방식과 감상 중심이 다름**  
> 감성적 서술 (Naver), 배우 중심 (Letterboxd), 평가 중심 (Rotten)

---

## 💬 감성 분석 기반 TF-IDF 키워드 비교

### 1️⃣ 감성 분포 요약  
![영문 플랫폼 감성 비율](review_analysis/plots/영문_플랫폼_감성비율.png)

| 플랫폼 | 긍정 | 중립 | 부정 |
|--------|------|------|------|
| Letterboxd | 약 40% | 약 50% | 약 10% |
| Rotten     | **약 70%** | 약 5% | 약 25% |

> Letterboxd는 **중립/긍정 혼합형 감성**,  
> Rotten은 **명확한 긍/부정 감성 판단**이 특징

### 2️⃣ 감성별 키워드 비교  
![감성별 키워드](review_analysis/plots/영문플랫폼_감성별_TFIDF.png)

| 플랫폼 | 감성 | 주요 키워드 |
|--------|------|-------------|
| Letterboxd | 긍정 | `love`, `good`, `robert`, `pattinson` |
| Letterboxd | 부정 | `long`, `bad`, `bit`, `trump`, `mickey` |
| Rotten     | 긍정 | `great`, `liked`, `fun`, `really` |
| Rotten     | 부정 | `boring`, `worst`, `terrible`, `bad` |

> ✍️ 감성별 키워드를 통해 플랫폼의 **표현 방식 + 리뷰 문화 차이**를 시각적으로 확인 가능

</details>


# docker hub 주소
https://hub.docker.com/repository/docker/nohyoobin/ybigta-app/general

# Trouble Shooting & 배운점

## ⚙️ Troubleshooting

### 1. EC2 + Docker + FastAPI 배포 이슈

- **ERR_CONNECTION_REFUSED 오류**
  - 원인: EC2 보안 그룹의 80번 포트 미개방
  - 해결: 인바운드 규칙에 80포트 (0.0.0.0/0) 허용 추가

- **FastAPI 내부 포트 불일치**
  - 원인: 도커 외부 80포트와 FastAPI 내부 8000포트 불일치
  - 해결: `--port 80`으로 uvicorn 실행 포트 통일

- **환경변수 미적용**
  - 원인: `--env-file .env` 옵션 누락
  - 해결: 옵션 추가하여 환경변수 적용

- **RDS 엔드포인트 오류**
  - 원인: 오타, 삭제, 퍼블릭 액세스 미허용
  - 해결: 퍼블릭 액세스=Yes, 엔드포인트 복사 확인

- **DB 스키마 불일치**
  - 원인: 코드에는 있으나 DB에 없는 컬럼 (예: password)
  - 해결: SQL로 직접 컬럼 추가

- **MySQL 접속 오류**
  - 원인: 비번 오타, DB명 오타, DB 미생성 등
  - 해결: 비밀번호 재설정, DB 생성 및 이름 규칙 준수

- **User Not Found (400/404)**
  - 원인: 실제 유저가 없는 경우로, 정상 동작임

### 2. MongoDB Atlas & 전처리 API 구현

- **데이터 덮어쓰기 오류**
  - 원인: 전처리 결과가 원본을 덮어씀 → 컬럼 수 mismatch
  - 해결: `{site_name}_preprocessed`에 별도 저장

- **Naver 리뷰 데이터 품질 문제**
  - 원인: 날짜/평점 형식이 통일되지 않음
  - 해결: 전처리 단계에서 정제 함수 추가

- **NLTK 의존성 제거**
  - 이유: 과도한 외부 의존성 제거

### 3. Docker 환경 이슈

- **requirements.txt 누락**
  - 원인: pandas, sklearn 등 빠짐
  - 해결: 의존성 재작성

- **환경변수 변경 후 미반영**
  - 원인: 컨테이너 재시작 미실행
  - 해결: 컨테이너 재시작으로 적용

### 4. 테스트 환경 문제

- **pytest 환경 불일치**
  - 원인: 기본 anaconda3 환경에서 실행
  - 해결: 가상환경(ybigta)에서 pytest 실행

### 🧠 개념 정리

- **MySQL vs MongoDB**
  - MySQL: 정형 데이터 (예: 유저 정보)
  - MongoDB: 비정형 문서 데이터 (예: 리뷰)

- **Docker**
  - 실행 환경을 통일하는 배포 도구

- **AWS 인프라**
  - EC2: 가상 서버
  - RDS: 관리형 MySQL
  - Security Group: 네트워크 접근 제어

- **환경변수 (.env)**
  - 민감정보 및 설정 일괄 관리

- **RESTful API & FastAPI**
  - HTTP 기반 API, JSON 입출력

- **데이터 전처리**
  - 정제, 형식 통일, 결측값 처리 등

- **테스트 자동화**
  - pytest로 CRUD 및 API 테스트 실행

## 📝 배운 점

### EC2 + Docker + FastAPI 배포

- 보안 그룹 인바운드 규칙 누락이 자주 발생한다.
- 포트 불일치 시 접속 안 된다. 실행 포트를 일치시켜야 한다
- `.env` 누락은 치명적이다. 적용 여부 확인 필수
- 도커 컨테이너가 잘 돌아가도 네트워크가 막히면 접속 안 된다

### RDS + MySQL 연동

- 엔드포인트는 항상 복붙. 오타 잦음
- 퍼블릭 액세스, 보안 그룹 설정 안 하면 연결 불가
- DB 필드와 코드가 다르면 장애 발생

### MongoDB Atlas + 리뷰 저장

- IP 허용 설정 안 하면 아무것도 안 됨
- 날짜, 평점 등 형식 불일치가 많아 정제가 필수
- 전처리 결과는 원본과 분리 저장이 안정적.
- NLTK 등 외부 의존성은 줄이는 게 좋음

### 테스트 및 개발 환경

- 가상환경과 테스트 환경이 다르면 깨짐
- `requirements.txt`는 전 환경을 커버해야 함
- 테스트는 버그 추적 속도를 크게 줄여준다
- `.env` 변경 시 컨테이너 재시작이 필수

### 전체 프로젝트 운영

- 에러 메시지가 유념해서 보기 + 공식문서와 로그 체크
- 단계를 쪼개서 점검하는 게 가장 빠르다.
- 로컬과 배포 환경은 다르다. 별개로 확인 필요