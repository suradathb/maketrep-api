import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

# Create a global logger instance
logger = logging.getLogger(__name__)

# Create a FastAPI app instance
app = FastAPI()

# Define the log directory and log file name
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

def get_log_file_name():
    # Get the current date as a string in the format YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')
    # Define the log file name with the current date
    return os.path.join(log_dir, f'app_log_{current_date}.log')


# Create a custom handler for log rotation with custom file names
# class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
#     def getFilesToDelete(self):
#         # Override this method to customize log file names
#         dir_name, base_name = os.path.split(self.baseFilename)
#         file_names = os.listdir(dir_name)
#         result = []
#         prefix = base_name + "."
#         plen = len(prefix)
#         for fileName in file_names:
#             if fileName[:plen] == prefix:
#                 suffix = fileName[plen:]
#                 if self.extMatch.match(suffix):
#                     result.append(os.path.join(dir_name, fileName))
#         return result

# handler = CustomTimedRotatingFileHandler(
#     filename=log_file,
#     when='midnight',
#     interval=1,
#     backupCount=3650  # Keep up to 7 days of log files
# )

class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self):
        filename = get_log_file_name()
        super().__init__(
            filename= filename,
            when='midnight',
            interval=1,
            backupCount=3650
        )

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hendler = CustomTimedRotatingFileHandler()
hendler.setFormatter(formatter)
logger.addHandler(hendler)
logger.setLevel(logging.INFO)

# helpers.py
def logger_in(fun:str,ic_code:str,app_code:str,requst:Optional[str] = None):
    # Logic to retrieve Input information
    logger.info(f'{fun}("{ic_code}","{app_code}","{requst}")')


def logger_out(fun:str,ic_code:str,app_code:str,value_info:Optional[str] = None):
    # Logic to retrieve Returns information
    logger.info(f'{fun}("{ic_code}","{app_code}","{value_info}")')

def logger_error(fun:str,ic_code:str,app_code:str,errorvalue:Optional[str] = None):
    # Logic to retrieve Error information
    logger.info(f'{fun}("{ic_code}","{app_code}","{errorvalue}")')

def logger_body(fun:str,ic_code:str,app_code:str,value_info:Optional[str] = None,body_value:Optional[str] = None):
    # Logic to retrieve Error information
    logger.info(f'{fun}("{ic_code}","{app_code}","{value_info}","{body_value}")')

def logger_Trade(fun:str,ic_code:str,app_code:str,ord_no:str,value_info:Optional[str] = None,body_value:Optional[str] = None):
    # Logic to retrieve Error information
    logger.info(f'{fun}("{ic_code}","{app_code}","{ord_no}","{value_info}","{body_value}")')

def logger_Trade_error(fun:str,ic_code:str,app_code:str,ord_no:str,sendingHead:Optional[str],sendingBody:Optional[str],errorvalue:Optional[str] = None) ->None:
    # Logic to retrieve Error information
    logger.info(f'{fun}("{ic_code}","{app_code}","{ord_no}","{sendingHead}","{sendingBody}","{errorvalue}")')

def logger_in_Trade_report(fun:str,ic_code:str,app_code:str,ord_no:Optional[str] = None,url:Optional[str] = None):
    # Logic to retrieve Input information
    logger.info(f'{fun}("{ic_code}","{app_code}","{ord_no}","{url}")')



