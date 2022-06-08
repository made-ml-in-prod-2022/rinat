import logging
import os
from typing import NoReturn, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


class DataPreprocessor:

    def __init__(self, file_path: str, shuffle: bool, test_size: float,
                 target: str) -> NoReturn:
        logger.info('Initializing data preprocessing}')
        self.file_path = file_path
        self.shuffle = shuffle
        self.test_size = test_size
        self.target = target

    def process(self):
        df = self.data_loader()
        train_df, valid_df = self.data_splitter(df)
        X_train, y_train, X_val, y_val = self.preprocessing(train_df, valid_df)
        return X_train, y_train, X_val, y_val

    def preprocessing(
        self, train_df: pd.DataFrame, valid_df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, np.ndarray, pd.DataFrame, np.ndarray]:
        X_train = train_df.drop(columns=self.target)
        y_train = np.array(train_df[self.target])
        X_val = valid_df.drop(columns=self.target)
        y_val = np.array(valid_df[self.target])
        return X_train, y_train, X_val, y_val

    def data_inference(self, df: pd.DataFrame):
        X = df.drop(columns=self.target)
        return X

    def inference_process(self):
        df = self.data_loader()
        X = self.data_inference(df)
        return X

    def data_loader(self) -> pd.DataFrame:
        logger.info(f'Reading data from {self.file_path}')
        df = pd.read_csv(self.file_path)
        logger.debug(f'Table has shape {df.shape}')
        return df

    def data_splitter(self,
                      df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        logger.info(
            f'Split dataset into train/test sizes: {1 - self.test_size}/{self.test_size}'
        )
        train_df, valid_df = train_test_split(df,
                                              test_size=self.test_size,
                                              shuffle=self.shuffle)
        dataset_path = os.path.join(os.path.join(os.getcwd(), "data"))
        if not os.path.exists(dataset_path):
            os.mkdir(dataset_path)
        train_df.to_csv(os.path.join(dataset_path, "train.csv"))
        valid_df.to_csv(os.path.join(dataset_path, "valid.csv"))
        logger.debug(f'Splitted datasets are save into {dataset_path}')
        return train_df, valid_df
