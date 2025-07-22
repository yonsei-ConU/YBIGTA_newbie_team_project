from abc import ABC, abstractmethod
import pandas as pd

class BaseDataProcessor:
    def __init__(self, input_path: str, output_dir: str):
        self.input_path = input_path
        self.output_dir = output_dir
        self.df = pd.read_csv(self.input_path)  
        
    
    @abstractmethod
    def preprocess(self):
        pass
    
    @abstractmethod
    def feature_engineering(self):
        pass

    @abstractmethod
    def save_to_database(self):
        
        pass
