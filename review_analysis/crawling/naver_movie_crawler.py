import os
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from review_analysis.crawling.base_crawler import BaseCrawler

class NaverMovieCrawler(BaseCrawler):
    """
    네이버 영화 '미키 17'의 관람평 데이터를 크롤링하는 크롤러 클래스.

    Attributes:
        url (str): 크롤링 대상 URL.
        reviews (list): 크롤링한 리뷰 데이터 (date, score, text) 리스트.
    """
    def __init__(self, output_dir):
"""
        NaverMovieCrawler 객체를 초기화한다.

        Args:
            output_dir (str): 크롤링 결과 파일을 저장할 디렉터리 경로.
        """
        super().__init__(output_dir)
        self.url = "https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bkEw&pkid=68&os=29816634&qvt=0&query=미키%2017%20관람평"
        self.reviews = []

    def start_browser(self):
        """
        셀레니움 WebDriver(Chrome)를 초기화한다.
        """
        options = Options()
        # options.add_argument("--headless")  # 필요 시 주석 해제
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scroll_down(self, min_reviews=500):
        """
        동적 로딩 방식의 리뷰 페이지를 지정한 개수만큼 스크롤하여 더 많은 데이터를 로드한다.

        Args:
            min_reviews (int): 최소 크롤링할 리뷰 개수.
        """
        print("🔽 스크롤을 내리며 리뷰를 수집 중...")
        scroll_area = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.lego_review_list._scroller"))
        )

        prev_count = 0
        same_count_times = 0

        while True:
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_area)
            time.sleep(1.5)
            current_count = len(self.driver.find_elements(By.CSS_SELECTOR, "li.area_card._item"))

            if current_count >= min_reviews:
                break
            if current_count == prev_count:
                same_count_times += 1
                if same_count_times >= 3:
                    print("⚠️ 더 이상 로드되지 않아 스크롤 종료")
                    break
            else:
                same_count_times = 0

            prev_count = current_count

    def parse_reviews(self):
        """
        현재 페이지에서 HTML을 파싱하여 리뷰 정보를 추출한다.

        Returns:
            list: 추출된 리뷰 리스트. 각 리뷰는 (date, score, text) 형태의 튜플.
        """
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        blocks = soup.select("li.area_card._item")

        reviews = []
        for block in blocks:
            score_tag = block.select_one(".area_text_box")
            review_tag = block.select_one("span.desc._text")
            date_tag = block.select_one("dd.this_text_normal")

            score = score_tag.get_text(strip=True) if score_tag else ""
            review = review_tag.get_text(strip=True) if review_tag else ""
            date = date_tag.get_text(strip=True).split()[0].replace(".", "-") if date_tag else ""

            if score and review and date:
                reviews.append((date, score, review))
        return reviews

    def scrape_reviews(self, tab_name="공감순"):
        """
        지정된 탭(공감순 또는 최신순)의 리뷰를 수집한다.

        Args:
            tab_name (str): 크롤링할 탭의 이름 ("공감순" 또는 "최신순").

        Returns:
            list: 해당 탭에서 수집한 리뷰 리스트.
        """
        self.driver.get(self.url)
        time.sleep(2)
        if tab_name == "최신순":
            try:
                latest_tab = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[text()="최신순"]'))
                )
                latest_tab.click()
                print("🆕 '최신순' 탭 클릭 완료")
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ '최신순' 탭 클릭 실패: {e}")

        self.scroll_down(min_reviews=500)
        html_path = os.path.join(self.output_dir, f"naver_raw_{tab_name}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        print(f"✅ HTML 저장 완료: {html_path}")

        return self.parse_reviews()

    def save_to_database(self, reviews):
        """
        수집한 리뷰를 중복 제거 후 CSV 파일로 저장한다.

        Args:
            reviews (list): (date, score, text) 형태의 리뷰 리스트.
        """
        deduplicated = list({(d, s, r) for d, s, r in reviews})
        output_path = os.path.join(self.output_dir, "reviews_naver.csv")
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "rating", "text"])
            writer.writerows(deduplicated)
        print(f"✅ 중복 제거 후 {len(deduplicated)}개 리뷰 저장 완료: {output_path}")

    def crawl(self):
        """
        전체 크롤링 파이프라인을 실행한다.
        공감순과 최신순 탭에서 리뷰를 각각 수집하고, 중복을 제거한 뒤 저장한다.
        """
        self.start_browser()
        try:
            sympathy = self.scrape_reviews("공감순")
            latest = self.scrape_reviews("최신순")
            combined = sympathy + latest
            self.save_to_database(combined)
        finally:
            self.driver.quit()
            print("🔚 브라우저 종료")