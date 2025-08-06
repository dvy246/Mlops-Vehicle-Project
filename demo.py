from src.logger import logging
from src.exception import MyException
import os,sys




logging.info("This is an info message from demo.py")


try:
    a=1+'a'
except Exception as e:
    logging.error("An error occurred in demo.py")
    raise MyException(e, sys) from e