import os
import sys
import pandas as pd

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import MyException
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.proj1_data import Proj1Data
from src.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self,data_ingestion_config: DataIngestionConfig=DataIngestionConfig()):

        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e,sys)
        
    #get the dataframe to the feature store
    def export_data_into_feature_store(self) -> DataFrame:
        try:
            logging.info("Exporting data into feature store")
            proj1_data = Proj1Data()
            dataframe=proj1_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(msg=f'shape of data frame is {dataframe.shape}')
            feature_store_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"saving the data at {feature_store_path}")
            dataframe.to_csv(feature_store_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise MyException(e, sys)

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        logging.info("Splitting data into train and test")
        try:
            train_data, test_data = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            logging.info(f"Train data shape: {train_data.shape}, Test data shape: {test_data.shape}")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving train data at {self.data_ingestion_config.training_file_path}")

            train_data.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_data.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info(f"Train and test data saved successfully at {self.data_ingestion_config.training_file_path} and {self.data_ingestion_config.testing_file_path}")
        except Exception as e:
            raise MyException(e, sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion process")
            dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info("Data ingestion process completed successfully")
            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e, sys)