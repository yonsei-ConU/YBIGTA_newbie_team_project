import os
import requests
import json
import csv
import time
from review_analysis.crawling.base_crawler import BaseCrawler

class WatchaAPICrawler(BaseCrawler):
    def __init__(self, output_dir):
        super().__init__(output_dir)
        self.url = "https://pedia.watcha.com/api/contents/md7Ypo1/comments?filter=all&order=recommended"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Accept": "application/vnd.frograms+json;version=2.1.0",
            "Referer": "https://pedia.watcha.com/ko-KR/contents/md7Ypo1/comments?order=recommended",
            "Origin": "https://pedia.watcha.com",
            "Cookie": "_c_pdi=web-_Je6hmEjdjlqDUa3RG-U11Fu3cAHan; _gid=GA1.2.1953845667.1753115477; _ga_1PYHGTCRYW=GS2.1.s1753158378$o5$g0$t1753158378$j60$l0$h0; _ga_S4YE5E5P6R=GS2.1.s1753158378$o5$g0$t1753158378$j60$l0$h0; _ga=GA1.1.923485025.1752716719",
            "x-frograms-app-code": "Galaxy",
            "x-frograms-client": "Galaxy-Web-App",
            "x-frograms-client-language": "ko",
            "x-frograms-client-region": "KR",
            "x-frograms-client-version": "2.1.0",
            "x-frograms-device-identifier": "web-_Je6hmEjdjlqDUa3RG-U11Fu3cAHan",
            "x-frograms-galaxy-language": "ko",
            "x-frograms-galaxy-region": "KR",
            "x-frograms-version": "2.1.0"
        }

    def start_browser(self):
        pass  # API 방식이므로 필요 없음

    def scrape_reviews(self):
        all_reviews = []
        next_url = self.url
        page = 1

        while True:
            print(f"📦 Fetching page {page}...")
            response = requests.get(next_url, headers=self.headers)

            if response.status_code != 200:
                print(f"❌ 요청 실패: {response.status_code}")
                break

            data = response.json()
            result_block = data.get("result", {})
            comments = result_block.get("result", [])

            if not comments:
                break

            for item in comments:
                text = item.get("text", "").strip().replace("\n", " ")
                rating = item.get("user_content_action", {}).get("rating")
                date = item.get("created_at")
                all_reviews.append([date, rating, text])

                if len(all_reviews) >= 500:
                    break

            next_uri = result_block.get("next_uri")
            if not next_uri or len(all_reviews) >= 500:
                break

            next_url = "https://pedia.watcha.com" + next_uri
            time.sleep(0.3)
            page += 1

        self.reviews = all_reviews

    def save_to_database(self):
        output_path = os.path.join(self.output_dir, "reviews_watcha_api.csv")
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "rating", "text"])
            writer.writerows(self.reviews)

        print(f"✅ {len(self.reviews)}개 리뷰 저장 완료: {output_path}")

    def crawl(self):
        self.scrape_reviews()
        self.save_to_database()
