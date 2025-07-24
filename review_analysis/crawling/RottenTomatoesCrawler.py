from review_analysis.crawling.base_crawler import BaseCrawler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

class RottenTomatoesCrawler(BaseCrawler):
    """
    Selenium을 이용하여 Rotten Tomatoes 유저 리뷰를 500개 이상 수집하는 크롤러 클래스.
    영화의 유저 리뷰에서 평점(score), 날짜(date), 리뷰 내용(review)을 추출하여 CSV로 저장함.
    """

    def __init__(self, output_dir: str):
        """
        크롤러 초기화 함수. 출력 디렉토리 및 크롤링 대상 URL 설정.
        """
        super().__init__(output_dir)
        self.url = "https://www.rottentomatoes.com/m/mickey_17/reviews?type=user"
        self.driver = None
        self.reviews: list[tuple[str, str, str]] = []

    def start_browser(self):
        """
        Chrome WebDriver를 실행하여 대상 페이지 접속
        """
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # 필요 시 주석 해제
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get(self.url)

    def click_show_more(self, max_clicks=30):
        """
        "Load More" 버튼을 최대 max_clicks회 클릭하여 리뷰를 추가 로딩함.
        """
        print("\U0001f501 'Load More' 버튼 클릭 중...")
        for i in range(max_clicks):
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "rt-button[data-qa='load-more-btn']"))
                )
                self.driver.execute_script("""
                    const btn = document.querySelector("rt-button[data-qa='load-more-btn']");
                    if (btn) btn.click();
                """)
                print(f"👉 {i + 1}회 클릭")
                time.sleep(1.5)
            except Exception:
                print("\U0001f6d1 더 이상 버튼 없음 또는 실패")
                break

    def scrape_reviews(self):
        """
        브라우저를 시작하고 리뷰를 수집하며 리뷰 목록을 self.reviews에 저장
        """
        print("\U0001f345 Rotten Tomatoes 리뷰 수집 시작")
        self.start_browser()
        self.click_show_more(max_clicks=30)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        review_blocks = soup.select("div.audience-review-row")

        for block in review_blocks:
            try:
                score_tag = block.select_one("rating-stars-group")
                score = score_tag.get("score", "") if score_tag else ""

                date_tag = block.select_one("span.audience-reviews__duration")
                date = date_tag.text.strip() if date_tag else ""

                review_tag = block.select_one("p.audience-reviews__review")
                review = review_tag.text.strip() if review_tag else ""

                if review:
                    self.reviews.append((score, date, review))
            except Exception as e:
                print("⚠️ 리뷰 파싱 오류:", e)

        self.driver.quit()
        print(f"✅ 리뷰 수집 완료: 총 {len(self.reviews)}개")

    def save_to_database(self):
        """
        수집된 리뷰 데이터를 CSV 파일로 저장함.
        """
        df = pd.DataFrame(self.reviews, columns=["score", "date", "review"])
        os.makedirs(self.output_dir, exist_ok=True)
        save_path = os.path.join(self.output_dir, "reviews_rotten.csv")
        df.to_csv(save_path, index=False)
        print(f"💾 저장 완료: {save_path}")

    def crawl(self):
        """
        전체 크롤링 실행: 리뷰 수집 → 저장
        """
        self.scrape_reviews()
        self.save_to_database()