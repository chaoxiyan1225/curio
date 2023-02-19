from loguru import logger

logger.add('LuPianShenQI_{time}.log',rotation="100 MB", retention='10 days')



logger.debug('this is a debug message')
logger.info('this is another debug message')
logger.warning('this is another debug message')
logger.error('this is another debug message')
logger.info('this is another debug message')
logger.success('this is success message!')
logger.critical('this is critical message!')
