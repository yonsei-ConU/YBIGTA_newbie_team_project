# review_analysis/crawling/letterboxd_mickey17.py
from review_analysis.crawling.base_crawler import BaseCrawler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

class LetterboxdCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.base_url = 'https://letterboxd.com/film/mickey-17/reviews/'

    def start_browser(self):
        opts = webdriver.ChromeOptions()
        # opts.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=opts)
        print("Chrome browser started")

    def scrape_reviews(self):
        reviews, page = [], 1
        wait = WebDriverWait(self.driver, 10)

        while len(reviews) < 500:
            url = self.base_url if page == 1 else f"{self.base_url}/page/{page}/"
            print(f"Fetching {url}")
            self.driver.get(url)

            # 1) Wait for at least one review article
            try:
                wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "article.production-viewing")
                ))
            except Exception as e:
                print("Done")
                break

            # 2) Parse
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            items = soup.select("article.production-viewing")
            for it in items:
                star_el = it.select_one("span.rating")
                date_el = it.select_one("time.timestamp")
                text_el = it.select_one("div.body-text")

                if not (star_el and date_el and text_el):
                    continue

                reviews.append({
                    "star": self._to_float(star_el.get_text(strip=True)),
                    "date": date_el.get("datetime"),
                    "text": text_el.get_text(" ", strip=True),
                })

                if len(reviews) >= 500:
                    break

            page += 1

        self.reviews = reviews
        print(f"Collected {len(reviews)} reviews")

    def save_to_database(self):
        out = Path(self.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(self.reviews)
        df.to_csv(out / "reviews_letterboxd.csv", index=False, encoding="utf-8-sig")
        print("Saved CSV → %s", out)

    @staticmethod
    def _to_float(star_str: str) -> float:
        assert star_str
        half = "½" in star_str
        full = star_str.count("★")
        return full * 2 + half
    
    def crawl(self):
        self.start_browser()
        try:
            self.scrape_reviews()
            self.save_to_database()
        finally:
            self.driver.quit()
            print("Browser closed")
