import os
import glob
from argparse import ArgumentParser
from typing import Dict, Type
from review_analysis.preprocessing.base_processor import BaseDataProcessor
from review_analysis.preprocessing.naver_preprocessor import NaverPreprocessor
from review_analysis.preprocessing.rotten_processor import RottenTomatoesProcessor

# 모든 preprocessing 클래스를 예시 형식으로 적어주세요. 
# key는 "reviews_사이트이름"으로, value는 해당 처리를 위한 클래스
PREPROCESS_CLASSES: Dict[str, Type[BaseDataProcessor]] = {
    "reviews_rotten": RottenTomatoesProcessor,
    "reviews_naver": NaverPreprocessor
    # 필요 시 다른 processor도 여기에 추가
}

# key는 크롤링한 csv파일 이름으로 적어주세요! ex. reviews_naver.csv -> reviews_naver
REVIEW_COLLECTIONS = glob.glob(os.path.join("database", "reviews_*.csv"))

def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('-o', '--output_dir', type=str, required=False, default="database", help="Output file dir.")
    parser.add_argument('-c', '--preprocessor', type=str, required=False, choices=PREPROCESS_CLASSES.keys(),
                        help=f"Which processor to use. Choices: {', '.join(PREPROCESS_CLASSES.keys())}")
    parser.add_argument('-a', '--all', action='store_true', help="Run all data preprocessors.")
    return parser

if __name__ == "__main__":
    print("[MAIN] main.py 실행 시작됨")
    parser = create_parser()
    args = parser.parse_args()
    print(f"[MAIN] args.preprocessor = {args.preprocessor}, args.all = {args.all}")

    os.makedirs(args.output_dir, exist_ok=True)

    if args.all:
        print("[MAIN] --all 옵션 실행")
        for csv_file in REVIEW_COLLECTIONS:
            print(f"[MAIN] 대상 파일: {csv_file}")
            base_name = os.path.splitext(os.path.basename(csv_file))[0]
            print(f"[MAIN] base_name = {base_name}")
            if base_name in PREPROCESS_CLASSES:
                print(f"[MAIN] 클래스 매칭됨: {base_name}")
                preprocessor_class = PREPROCESS_CLASSES[base_name]
                preprocessor = preprocessor_class(csv_file, args.output_dir)
                preprocessor.preprocess()
                preprocessor.feature_engineering()
                preprocessor.save_to_database()
            else:
                print(f"[MAIN] 해당 이름의 클래스 없음: {base_name}")

    elif args.preprocessor:
        base_name = args.preprocessor
        print(f"[MAIN] 단일 실행 요청: {base_name}")

        if base_name in PREPROCESS_CLASSES:
            input_path = os.path.join(args.output_dir, f"{base_name}.csv")
            print(f"[MAIN] input_path = {input_path}")
            print(f"[MAIN] PREPROCESS_CLASSES = {list(PREPROCESS_CLASSES.keys())}")
            preprocessor_class = PREPROCESS_CLASSES[base_name]
            preprocessor = preprocessor_class(input_path, args.output_dir)
            preprocessor.preprocess()
            preprocessor.feature_engineering()
            preprocessor.save_to_database()
        else:
            print(f"[ERROR] {base_name} 클래스가 PREPROCESS_CLASSES에 없습니다.")
    else:
        print("[ERROR] 실행할 preprocessor가 지정되지 않았습니다.")
