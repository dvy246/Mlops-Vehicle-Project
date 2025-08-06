import logging
import os
from logging.handlers import RotatingFileHandler
import sys
from datetime import datetime
from from_root import from_root

#logging configuration

# Set the log file name and directory
log_file=f"{datetime.now().strftime('%Y-%m-%d')}.log"
log_dir='Logs'

MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 5  # Number of backup files to keep

LOG_DIR_PATH=os.path.join(from_root(), log_dir)
if not os.path.exists(LOG_DIR_PATH):
    os.makedirs(LOG_DIR_PATH,exist_ok=True)

LOG_FILE_PATH=os.path.join(LOG_DIR_PATH,log_file)

# Configure the logger
def configure_logger():
    """
    Configures the logger to log messages to both console and a file.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


configure_logger()