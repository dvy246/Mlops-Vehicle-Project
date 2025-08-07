import os 
import pymongo
from src.constants import DATABASE_NAME, COLLECTION_NAME, MONGODB_URL_KEY
from src.logger import logging
from src.exception import MyException
import sys
import certifi
from dotenv import load_dotenv
load_dotenv()

#this  is used to setup connection with MongoDB

ca=certifi.where()
class MongoDBConnection:
    client=None

    def __init__(self,database_name:str=DATABASE_NAME):
        try:
            if MongoDBConnection.client is None:
                try:
                    mongodb_url = os.getenv(mongodb_url)
                    if not mongodb_url:
                        raise ValueError(f"Environment variable '{MONGODB_URL_KEY}' is not set.")
                    
                    MongoDBConnection.client = pymongo.MongoClient(mongodb_url, tlsCAFile=ca)
                    logging.info(f"MongoDB client created with database: {database_name}")
                except Exception as e:
                    raise MyException(e, sys) from e

                self.client = MongoDBConnection.client
                self.database = self.client[database_name]  # Connect to the specified database
                self.database_name = database_name
                logging.info("MongoDB connection successful.")

        except Exception as e:
                raise MyException(e, sys) from e
    