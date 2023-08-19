import logging 
import datetime   
              
def InitLogger(logFile, logLevel):    
    logger = logging.getLogger()      
    fileHandler = logging.FileHandler(logFile)        
    formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(lineno)s \
      %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
      
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

def debug(msg)->None:
    logger.debug(msg)
 
def info(msg)->None:
    logger.info(msg)
    
def warn(msg)->None:
    logger.warn(msg)
    
def error(msg)->None:
    logger.error(msg)

    
