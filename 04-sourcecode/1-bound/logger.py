from loguru import logger

logger.add('niuniufeitian_{time}.log',rotation="100 MB", retention='10 days')

def debug(msg)->None:
    logger.debug(msg)
 
def info(msg)->None:
    logger.info(msg)
    
def warning(msg)->None:
    logger.warning(msg)
    
def error(msg)->None:
    logger.error(msg)
