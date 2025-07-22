import pandas as pd
from preprocessing.base_processor import BaseDataProcessor

class NaverDataProcessor(BaseDataProcessor):
    """
    네이버 영화 리뷰 데이터를 전처리하는 클래스입니다.

    BaseDataProcessor를 상속받아 전처리, 특징 생성, 결과 저장 메서드를 구현합니다.

    Attributes:
        input_path (str): 원본 CSV 파일 경로
        output_dir (str): 전처리된 파일을 저장할 디렉토리
        df (pd.DataFrame): 처리 중인 데이터프레임
    """

    def __init__(self, input_path: str, output_dir: str):
        """
        NaverDataProcessor의 생성자.

        Args:
            input_path (str): 입력 CSV 파일 경로
            output_dir (str): 출력 파일 저장 디렉토리
        """
        super().__init__(input_path, output_dir)
        self.df = None

    def preprocess(self):
        """
        Step 1. 원본 데이터를 불러오고, 컬럼명을 통일합니다.

        - CSV 파일 로드
        - 컬럼명을 ['date', 'rating', 'review']로 변경
        - 변경된 컬럼명을 출력
        """
        print("🚿 Step 1: 파일 불러오기 & 컬럼명 통일")

        df = pd.read_csv(self.input_path)
        print("기존 컬럼명:", df.columns.tolist())

        df.columns = ['date', 'rating', 'review']
        print("변경 후 컬럼명:", df.columns.tolist())

        self.df = df

    def feature_engineering(self):
        """
        추후 구현 예정: 날짜 파생 변수, 텍스트 벡터화 등.
        """
        pass

    def save_to_database(self):
        """
        추후 구현 예정: 최종 결과를 CSV로 저장.
        """
        pass
