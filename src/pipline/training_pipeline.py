import sys
from src.exception import MyException
from src.components.data_ingestion import DataIngestion
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from src.utils import read_yaml_file,read_json_file
from src.logger import logging

class TrainingPipeline:
    def __init__(self):
       self.data_ingestion = DataIngestion() 
       self.data_validation = DataValidation()
       

    def start_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion process")
            logging.info(f"Data ingestion config: {self.data_ingestion.data_ingestion_config}")
            logging.info("gettig the data from mongo db")

            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion process completed successfully")
            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e, sys) 
        
    def start_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation process")
            logging.info(f"Data validation config: {self.data_validation.data_validation_config}")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation.data_validation_config)
            data_validation_artifact = data_validation.validate_data()
            logging.info("Data validation process completed successfully")
            return data_validation_artifact
        
        except Exception as e:
            raise MyException(e, sys)
        
    def run_pipeline(self):
            try:
                logging.info("Starting the training pipeline")
                data_ingestion_artifact = self.start_ingestion()
                logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
                logging.info("Training pipeline completed successfully")
                data_validation_artifact = self.start_validation(data_ingestion_artifact)
                logging.info(f"Data validation artifact: {data_validation_artifact}")
                
            except Exception as e:
                raise MyException(e, sys)