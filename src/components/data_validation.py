import os
import pandas as pd
from src.constants import *

from src.utils.main_utils import read_yaml_file
from src.entity.config_entity import DataValidationConfig, DataIngestionConfig
from src.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from src.exception import MyException
from src.logger import logging
import json
import sys  


class DataValidation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
       '''constructor for DataValidation class.
       Args:
           data_ingestion_artifact (DataIngestionArtifact): Artifact from data ingestion process for validation.
           data_validation_config (DataValidationConfig): Configuration for data validation process.
       '''
       try:
           self.data_ingestion_artifact = data_ingestion_artifact
           self.data_validation_config = data_validation_config
           self.schema_config=read_yaml_file(file_path=SCHEMA_FILE_PATH)
       except Exception as e:
              raise MyException(e, sys) from e

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        '''Validates the number of columns in the dataframe against the schema.
        
        Args:
            dataframe (pd.DataFrame): Dataframe to validate.
        
        Returns:
            bool: True if the number of columns matches the schema, False otherwise.
        '''
        try:
            expected_columns = self.schema_config['columns']
            actual_columns = dataframe.columns.tolist()
            if len(expected_columns) != len(actual_columns):
                logging.info(f"Number of columns mismatch: Expected {len(expected_columns)}, Found {len(actual_columns)}")
                return False
            return True
        except Exception as e:
            logging.error(f"Error in validate_number_of_columns: {e}")
            raise MyException(e, sys) from e
         
    
    def is_column_exists(self,dataframe:pd.DataFrame)->bool:
        '''Checks if the required columns exist in the dataframe.
        Args:
            dataframe (pd.DataFrame): Dataframe to check for required columns.
        Returns:
            bool: True if all required columns exist, False otherwise.'''
        
        try:
            columns=dataframe.columns
            missing_categorical_columns=[]
            missing_numerical_columns=[]
            for col in self.schema_config['numerical_columns']:
                if col not in columns:
                    missing_numerical_columns.append(col)
            for col in self.schema_config['categorical_columns']:
                if col not in columns:
                    missing_categorical_columns.append(col)
            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")
                
            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical columns: {missing_categorical_columns}")
                
            return False if len(missing_numerical_columns) > 0 or len(missing_categorical_columns) > 0 else True
        except Exception as e:
            logging.error(f"Error in is_column_exists: {e}")
            raise MyException(e, sys) from e
        

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
            '''Reads data from a CSV file.
            
            Args:
                file_path (str): Path to the CSV file.
            
            Returns:
                pd.DataFrame: Dataframe containing the data from the CSV file.
            '''
            try:
                return pd.read_csv(file_path)
            except Exception as e:
                logging.error(f"Error reading data from {file_path}: {e}")
                raise MyException(e, sys) from e
            
    def initiate_data_validation(self) -> DataValidationArtifact:
        '''Initiates the data validation process.

        Returns:
            DataValidationArtifact: Artifact containing the validation results.
        '''
        try:
            error_msg=''
            logging.info("Starting data validation.")

            # Read training and testing data
            train_data,test_data=(DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                  DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))
            
            #validate number of columns
            status=self.validate_number_of_columns(dataframe=train_data)
            if not status:
                error_msg += f"Number of columns in training data does not match schema. Expected: {len(self.schema_config['columns'])}, Found: {len(train_data.columns)}\n"
            else:
                logging.info("Number of columns in training data matches schema.")

            #validate if required columns exist
            status=self.is_column_exists(dataframe=train_data)
            if not status:
                error_msg += "Required columns are missing in training data.\n"
            else:
                logging.info("All required columns exist in training data.")

            #validate number of columns in test data
            status=self.validate_number_of_columns(dataframe=test_data)
            if not status:
                error_msg += f"Number of columns in test data does not match schema. Expected: {len(self.schema_config['columns'])}, Found: {len(test_data.columns)}\n"
            else:
                logging.info("Number of columns in test data matches schema.")

            #validate if required columns exist in test data
            status=self.is_column_exists(dataframe=test_data)
            if not status:
                error_msg += "Required columns are missing in test data.\n"
            else:
                logging.info("All required columns exist in test data.")

            if len(error_msg) > 0:
                raise Exception(error_msg, sys)
            
            validation_status= True if len(error_msg) == 0 else False

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=error_msg,
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            
            )

            filepath=os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(filepath,exist_ok=True)

            validation_report={
                "validation_status":validation_status,
                "validation_message":error_msg.strip()}
            
            with open(self.data_validation_config.validation_report_file_path, 'w') as file:
                json.dump(validation_report, file)

            logging.info(f"Validation report saved at {self.data_validation_config.validation_report_file_path}")
            logging.info(f"Data validation artifact created: {data_validation_artifact}")
            logging.info(f"Data validation completed. Validation status: {data_validation_artifact.validation_status}")

            return data_validation_artifact
        except Exception as e:
            raise MyException(e, sys) from e
        