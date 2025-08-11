from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    '''
A class to represent the artifacts of data ingestion process.

This class stores the paths of the files generated during data ingestion,
including the training and testing datasets.
Attributes:
    trained_file_path (str): Path to the file containing the training dataset.
    test_file_path (str): Path to the file containing the testing dataset.
    '''
    trained_file_path:str 
    test_file_path:str

@dataclass
class DataValidationArtifact:
    """
    A class to represent the artifact of data validation process.
    
    This class stores the results of data validation including status,
    report file path, and any relevant messages.

    Attributes:
        validation_status (bool): The status of the validation (True if valid, False otherwise).
        validation_report_file_path (str): Path to the file containing the validation report.
        message (str): Additional information or messages related to the validation.
    """
    validation_status: bool
    validation_report_file_path: str
    message:str

@dataclass
class DataTransformationArtifact:
    """
    A class to represent the artifact of data transformation process.
    
    This class stores the paths of the transformed training and testing datasets,
    as well as the path to the preprocessing object file.

    Attributes:
        transformed_train_file_path (str): Path to the transformed training dataset.
        transformed_test_file_path (str): Path to the transformed testing dataset.
        preprocessing_object_file_path (str): Path to the file containing the preprocessing object.
    """
    transformed_train_file_path: str
    transformed_test_file_path: str
    preprocessing_object_file_path: str 
    