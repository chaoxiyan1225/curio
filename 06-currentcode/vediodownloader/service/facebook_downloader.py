# -*- coding:utf-8 -*-  
from datetime import datetime
from tqdm import tqdm
import requests
import re
import os
from service.common_downloader import *
from bs4 import BeautifulSoup

class FacebookDownloader(CommonDownloader):

    def __init__(self, savePath, url, vedioName=None, threadCnt = default_thread_cnt, blockSize = BLOCK_SIZE):
         super(FacebookDownloader, self).__init__(savePath, url, vedioName, threadCnt, blockSize)


    def clear(self):
        return

    def get_percent_current(self):
        fenMu = 1000000 if self.downTotal==0 else self.downTotal
        return int((self.downSuccess * 100) / fenMu)
  
    def get_metric(self):
        self.metricInfo.percentCurrent = self.get_percent_current()
        return self.metricInfo    

    def downLoad_start(self):

        current = 0
        while current < RETRY_TIME:
            try:
                self.init()
               
                current = current + 1
                response = requests.get(self.url, headers=headers)
                soup = BeautifulSoup(response.text,'html.parser')
                logger.warn(f"facebook downloader the video ... \n")
                logger.warn(soup)
                
                soup.find("aa")
                vedio_url = None
                if vedio_url == None:
                    logger.error(f"facebookdown load error, the:{self.url} have no vedio ")
                    return False
                    
                logger.warn(f'the url:{vedio_url}')
                
                video_url =  tmp_url.group(1)
                file_size_request = requests.get(video_url, stream=True)
                self.downTotal = int(file_size_request.headers['Content-Length'])
                filename = self.download_path / self.vedioName

                with open(filename + '.mp4', 'wb') as f:
                    for data in file_size_request.iter_content(BLOCK_SIZE):
                        self.downSuccess = self.downSuccess + BLOCK_SIZE
                        f.write(data)

                logger.warn(f"the facebook : {self.url} download success")
                return True

            except Exception as e:
                logger.error(f"facebook  {self.url} download error :{current} time ".format(str(e)).encode("utf-8"))
                logging.exception(e)

        return False
