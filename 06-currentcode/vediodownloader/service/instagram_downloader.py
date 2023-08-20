# -*- coding:utf-8 -*-  
from instascrape import Reel
import time
from service.common_downloader import *

# session id
SESSIONID = "Paste session Id Here"

class InstagramDownloader(CommonDownloader):

    def __init__(self, savePath, url, vedioName=None, threadCnt = default_thread_cnt, blockSize = BLOCK_SIZE):
         super(InstagramDownloader, self).__init__(savePath, url, vedioName, threadCnt, blockSize)

    def clear(self):
        return None

    def get_percent_current(self):
        fenMu = 1000000 if self.downTotal==0 else self.downTotal
        return int((self.downSuccess * 100) / fenMu)
  
    def get_metric(self):
        self.metricInfo.percentCurrent = self.get_percent_current()
        return self.metricInfo    


    def downLoad_start(self):

        self.init()
        insta_reel = Reel(self.url)
        self.downTotal = 1
		# Using scrape function and passing the headers
        insta_reel.scrape(headers=headers)
        current = 0
        while current < RETRY_TIME:
            try:   
                filePath = self.download_path / self.vedioName
                current = current + 1
                insta_reel.download(fp=filePath)
                self.downSuccess = self.downTotal
                logger.warn(f"the instagram: {self.url} download success")

                return True
            except Exception as e:
                logger.error(f"instagram downloader error:{current} time".format(str(e)).encode("utf-8"))
                logging.exception(e)

        return False 
