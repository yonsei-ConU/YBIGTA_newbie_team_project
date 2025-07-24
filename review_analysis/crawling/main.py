import sys
import os
from argparse import ArgumentParser
from typing import Dict, Type, Union

# 경로 설정: 프로젝트 루트로 이동
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 각 크롤러 import
from review_analysis.crawling.RottenTomatoesCrawler import RottenTomatoesCrawler
from review_analysis.crawling.naver_movie_crawler import NaverMovieCrawler
from review_analysis.crawling.letterboxd_crawler import LetterboxdCrawler

# 구체 크롤러 타입 명시 (BaseCrawler는 crawl 없음)
CrawlerType = Union[RottenTomatoesCrawler, NaverMovieCrawler, LetterboxdCrawler]

# 크롤러 선택지 등록
CRAWLER_CLASSES: Dict[str, Type[CrawlerType]] = {
    "rotten": RottenTomatoesCrawler,
    "naver": NaverMovieCrawler,
    "letterboxd": LetterboxdCrawler
}

# 명령줄 파서 함수
def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('-o', '--output_dir', type=str, required=True,
                        help="Output file directory. Example: ../../database")
    parser.add_argument('-c', '--crawler', type=str, required=False,
                        choices=CRAWLER_CLASSES.keys(),
                        help=f"Which crawler to use. Choices: {', '.join(CRAWLER_CLASSES.keys())}")
    parser.add_argument('-a', '--all', action='store_true',
                        help="Run all crawlers. Default to False.")
    return parser

# 메인 실행
if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    if args.all:
        for crawler_name in CRAWLER_CLASSES.keys():
            Crawler_class = CRAWLER_CLASSES[crawler_name]
            crawler = Crawler_class(args.output_dir)
            assert hasattr(crawler, "crawl")  # ✅ mypy-safe
            crawler.crawl()

    elif args.crawler:
        Crawler_class = CRAWLER_CLASSES[args.crawler]
        crawler = Crawler_class(args.output_dir)
        assert hasattr(crawler, "crawl")  # ✅ mypy-safe
        crawler.crawl()

    else:
        raise ValueError("No crawlers.")
