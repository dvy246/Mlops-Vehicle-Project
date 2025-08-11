import os
import pandas as pd
import numpy as np
import sys

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTEENN

from src.constants import *
from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact,DataIngestionArtifact
from src.utils.main_utils import save_numpy_array_data,load_numpy_array_data,read_yaml_file,save_object,load_object



class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)
        
    def get_transformation_object(self) -> Pipeline:
        '''
        Create a transformation pipeline with preprocessing steps.
        This method creates a pipeline that includes scaling and handling imbalanced data.
        Returns:
            Pipeline: A scikit-learn pipeline object containing the preprocessing steps.
        '''
        logging.info("Creating transformation object")
        try:
            sc=StandardScaler()
            minmax=MinMaxScaler()
            logging.info("Creating column transformer with standard and min-max scaling")
            numerical_cols=self._schema['num_features']
            mm_cols=self._schema['mm_features']

            # Create a column transformer to apply different transformations to different columns
            preprocessor=ColumnTransformer(transformers=[
                ('scaler',sc,numerical_cols),
                ('minmax_scaler',minmax,mm_cols)
            ],remainder='passthrough')
            logging.info("Column transformer created with specified transformations")
            logging.info('created a preprocessor to transform test and training data')
            # Create a pipeline that includes the preprocessor and an imbalanced data handler
            pipeline=Pipeline(steps=[
            ('preprocessor',preprocessor)
            ])
            logging.info("Created a pipeline with preprocessing steps")
            return pipeline
        except Exception as e:
            raise MyException(e,sys)
            
    def map_gender_columns(self,dataframe:pd.DataFrame) -> pd.DataFrame:
        '''
        Map gender columns to numerical values.
        This method maps the gender columns in the dataframe to numerical values.
        Args:
            dataframe (pd.DataFrame): The input dataframe containing gender columns.
        Returns:
            pd.DataFrame: The output dataframe with gender columns mapped to numerical values.
        '''
        try:
            logging.info('mapping gender columns to numerical values')
            dataframe['Gender']=dataframe['Gender'].map({'Male':1,'Female':0}).astype(int)
            return dataframe
        except Exception as e:
            raise MyException(e,sys)
        
    def create_dummy_columns(self,df:pd.DataFrame) -> pd.DataFrame:
        '''
        Create dummy columns for categorical variables.
        This method creates dummy columns for the categorical variables in the dataframe.
        Args:
            df (pd.DataFrame): The input dataframe containing categorical variables.
        Returns:
            pd.DataFrame: The output dataframe with dummy columns created.
        '''
        logging.info('creating dummy columns for categorical variables')
        df=pd.get_dummies(df,drop_first=True)
        return df
    
    def drop_id_column(self,df:pd.DataFrame) -> pd.DataFrame:
        '''
        Drop the 'id' column from the dataframe.
        This method drops the 'id' column from the input dataframe.
        Args:
            df (pd.DataFrame): The input dataframe containing an 'id' column.
        Returns:
            pd.DataFrame: The output dataframe with the 'id' column dropped.
        '''
        logging.info('dropping id column')
        id_column = self._schema['drop_columns']
        if id_column in df.columns:
            df = df.drop(columns=id_column, axis=1)
            logging.info('id column dropped')
        return df
    
    def rename_columns(self,df:pd.DataFrame) -> pd.DataFrame:
        '''
        Rename columns in the dataframe.
        This method renames the columns in the dataframe based on the schema.
        Args:
            df (pd.DataFrame): The input dataframe with columns to be renamed.
        Returns:
            pd.DataFrame: The output dataframe with renamed columns.
        '''
        logging.info('renaming columns')
        df.rename(columns={'Vehicle_Age<1 Year':'Vehicle_Age_lt_1_year','Vehicle_Age>2 Year':'Vehicle_Age_gt_2_year'},inplace=True)
        logging.info('columns renamed')
        renamed_columns=['Vehicle_Age_lt_1_year','Vehicle_Age_gt_2_year','Vehicle_Damage_Yes']
        for col in renamed_columns:
            if col in df.columns:
                df[col]=df[col].astype(int)
                logging.info('columns converted to int')

        return df
    
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        '''
        Read data from a file.
        This method reads data from a file and returns a pandas DataFrame.
        Args:
            file_path (str): The path to the file containing the data.
        Returns:
            pd.DataFrame: The data read from the file as a pandas DataFrame.
        '''
        python
 Copy
 Insert
 Export

@staticmethod
def read_data(file_path: str) -> pd.DataFrame:
    '''
    Read data from a file with proper error handling and validation.
    This method reads data from a file and returns a pandas DataFrame.
    Args:
        file_path (str): The path to the file containing the data.
    Returns:
        pd.DataFrame: The data read from the file as a pandas DataFrame.
    Raises:
        ValueError: If the file is empty or contains only headers.
        FileNotFoundError: If the file doesn't exist.
    '''
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at path: {file_path}")
            
        df = pd.read_csv(file_path)
        
        if df.empty:
            raise ValueError(f"File is empty: {file_path}")
            
        if len(df.columns) == 0:
            raise ValueError(f"File contains only headers: {file_path}")
            
        logging.info(f"Successfully read {len(df)} rows from {file_path}")
        return df
        
    except pd.errors.EmptyDataError:
        raise ValueError(f"File is empty or contains no data: {file_path}")
    except Exception as e:
        logging.error(f"Error reading data from {file_path}: {str(e)}")
        raise MyException(e, sys)
    
    def initalize_transformation(self) -> DataTransformationArtifact:
        '''
        Initialize the data transformation process.
        This method performs the data transformation steps and returns the artifact containing the transformed data paths.
        Returns:
            DataTransformationArtifact: An object containing the paths of the transformed training and testing datasets,
            as well as the path to the preprocessing object file.
        '''
        try:
            logging.info('Starting data transformation process')
            if not self.data_validation_artifact.validation_status:
                raise MyException("Data validation failed. Cannot proceed with data transformation.", sys)
            
            # Read training and testing data
            train_df = self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            logging.info('Data read successfully from ingestion artifact')
             
            #taking target and input columns from train and test dataframes
            input_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            input_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)

            target_train_df=train_df[TARGET_COLUMN]
            target_test_df=test_df[TARGET_COLUMN]
            logging.info('Input and target columns separated successfully')

            # Map gender column to numerical values
            input_train_df = self.map_gender_columns(input_train_df)
            input_test_df = self.map_gender_columns(input_test_df)

            # Create dummy columns for categorical variables
            input_train_df = self.create_dummy_columns(input_train_df)
            input_test_df = self.create_dummy_columns(input_test_df)

            # Drop id column
            input_train_df = self.drop_id_column(input_train_df)
            input_test_df = self.drop_id_column(input_test_df)

            # Rename columns
            input_train_df = self.rename_columns(input_train_df)
            input_test_df = self.rename_columns(input_test_df)
            logging.info('Data preprocessing steps completed successfully')

            # Return the transformed dataframes
            preprocess=self.get_transformation_object()
            logging.info('Transformation object created successfully')

            transformed_train_df = preprocess.fit_transform(input_train_df)
            transformed_test_df = preprocess.transform(input_test_df)
            logging.info('Data transformed successfully using the preprocessing object')

            #applying imbalance handling
            smote_enn = SMOTEENN(sampling_strategy='minority', random_state=42)
            final_input_train_df,final_target_train_df = smote_enn.fit_resample(transformed_train_df, target_train_df)
            final_input_test_df,final_target_test_df = smote_enn.fit_resample(transformed_test_df, target_test_df)
            logging.info('Imbalance handling applied successfully using SMOTEENN')

            train_array=np.c_[final_input_train_df,np.array(final_target_train_df)]
            test_array=np.c_[final_input_test_df,np.array(final_target_test_df)]
            logging.info('Data transformed successfully and arrays created and ready to be saved')

            # Save transformed data to disk
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocess)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_file_path_train, array=train_array)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_file_path_test, array=test_array)
            logging.info('Transformed data saved successfully to disk') 

            # Create and return the DataTransformationArtifact
            data_transformation_artifact = DataTransformationArtifact(transformed_train_file_path=self.data_transformation_config.transformed_file_path_train,
                                                                      transformed_test_file_path=self.data_transformation_config.transformed_file_path_test,
                                                                      preprocessing_object_file_path=self.data_transformation_config.transformed_object_file_path)
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        
        except Exception as e:
            raise MyException(e, sys)
