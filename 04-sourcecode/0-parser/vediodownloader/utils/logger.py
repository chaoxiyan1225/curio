import logging 
import datetime   
              
def InitLogger(logFile, logLevel):    
    logger = logging.getLogger()      
    fileHandler = logging.FileHandler(logFile)        
    formatter = logging.Formatter(        
        "[%(asctime)s] [%(levelname)s]%(filename)s: %(lineno)s %(funcName)s %(message)s", "%Y-%m-%d %H:%M:%S"           
    )           
    fileHandler.setFormatter(formatter)        
    logger.addHandler(fileHandler)         
    logger.setLevel(logLevel)        
    return logger       
        
        
logger = InitLogger(       
    "vediodownloader_%s_%s_%s.log"         
    % (        
        datetime.datetime.now().year,          
        datetime.datetime.now().month,           
        datetime.datetime.now().day,          
    ),          
    logging.INFO,      
)        


'''

from loguru import logger
import datetime

logger.add(f'vedioDownLoader_{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}.log',rotation="100 MB", retention='10 days', format='{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} -{message}')
'''
def debug(msg)->None:
    logger.debug(msg)
 
def info(msg)->None:
    logger.info(msg)
    
def warn(msg)->None:
    logger.warn(msg)
    
def error(msg)->None:
    logger.error(msg)
    
