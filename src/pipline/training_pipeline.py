import sys
from src.exception import MyException
from src.components.data_ingestion import DataIngestion
from src.entity.artifact_entity import DataIngestionArtifact
from src.logger import logging

class TrainingPipeline:
    def __init__(self):
       self.data_ingestion = DataIngestion()    

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
        
    def run_pipeline(self):
            try:
                logging.info("Starting the training pipeline")
                data_ingestion_artifact = self.start_ingestion()
                logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
                logging.info("Training pipeline completed successfully")
            except Exception as e:
                raise MyException(e, sys)