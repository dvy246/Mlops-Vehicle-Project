import sys
import os

from src.exception import MyException
from src.logger import logging

from pandas import DataFrame
import numpy as np
import yaml
import dill


def read_yaml_file(file_path: str) -> dict:
    logging.info(f"Reading YAML file from {file_path}...")
    """
    Reads a YAML file and returns its content as a dictionary.

    Parameters:
    ----------
    file_path : str
        Path to the YAML file.

    Returns:
    -------
    dict
        Content of the YAML file.
    """
    try:
        with open(file_path, 'rb') as file:
            content = yaml.safe_load(file)
        return content
    except Exception as e:
        raise MyException(e, sys)
    
def write_yaml_file(file_path: str, content:object,replace:bool=False) -> None:
    logging.info(f"Writing content to {file_path}")
    """
    Writes a dictionary to a YAML file.

    Parameters:
    ----------
    file_path : str
        Path to the YAML file.
    data : dict
        Dictionary to be written to the YAML file.
    """
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise MyException(e, sys)
    
def save_object(file_path: str, obj: object) -> None:
    logging.info(f"Saving object to {file_path}")
    """
    Saves an object to a file using dill.

    Parameters:
    ----------
    file_path : str
        Path to the file where the object will be saved.
    obj : object
        Object to be saved.
    """
    try:
        with open(file_path, 'wb') as file:
            dill.dump(obj, file)
    except Exception as e:
        raise MyException(e, sys)
    
def load_object(file_path: str) -> object:
    logging.info(f"Loading object from {file_path}")
    """
    Loads an object from a file using dill.

    Parameters:
    ----------
    file_path : str
        Path to the file from where the object will be loaded.

    Returns:
    -------
    object
        Loaded object.
    """
    try:
        with open(file_path, 'rb') as file:
            obj = dill.load(file)
        return obj
    except Exception as e:
        raise MyException(e, sys)
    
def save_numpy_array_data(file_path: str, array: np.ndarray) -> None:
    logging.info(f"Saving numpy array to {file_path}")
    """
    Saves a numpy array to a file.

    Parameters:
    ----------
    file_path : str
        Path to the file where the numpy array will be saved.
    array : np.ndarray
        Numpy array to be saved.
    """
    try:
        os.path.dirname(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, array)
    except Exception as e:
        raise MyException(e, sys)
    
def load_numpy_array_data(file_path: str) -> np.ndarray:
    logging.info(f"Loading numpy array from {file_path}")
    """
    Loads a numpy array from a file.

    Parameters:
    ----------
    file_path : str
        Path to the file from where the numpy array will be loaded.

    Returns:
    -------
    np.ndarray
        Loaded numpy array.
    """
    try:
        with open(file_path, 'rb') as file:
            array = np.load(file)
        return array
    except Exception as e:
        raise MyException(e, sys)
    
