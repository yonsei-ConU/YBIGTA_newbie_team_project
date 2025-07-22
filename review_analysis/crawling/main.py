from argparse import ArgumentParser
from typing import Dict, Type
from review_analysis.crawling.base_crawler import BaseCrawler
from review_analysis.crawling.RottenTomatoesCrawler import RottenTomatoesCrawler

CRAWLER_CLASSES: Dict[str, Type[BaseCrawler]] = {
    "rotten": RottenTomatoesCrawler,
}

def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("-o", "--output_dir", type=str, required=True, help="저장할 디렉토리 경로 (예: database)")
    parser.add_argument("-c", "--crawler", type=str, required=True, choices=CRAWLER_CLASSES.keys(), help="사용할 크롤러 이름 (예: rotten)")
    return parser

if __name__ == "__main__":
    args = create_parser().parse_args()

    CrawlerClass = CRAWLER_CLASSES[args.crawler]
    crawler = CrawlerClass(args.output_dir)
    crawler.scrape_reviews()
    crawler.save_to_database()
    print("리뷰 개수:", len(crawler.reviews))