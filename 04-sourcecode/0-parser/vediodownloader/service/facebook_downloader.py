# -*- coding:utf-8 -*-  
from datetime import datetime
from tqdm import tqdm
import requests
import re
import os
from service.common_downloader import *

class FacebookDownloader(CommonDownloader):

    def __init__(self, savePath, url, vedioName=None, threadCnt = default_thread_cnt, blockSize = BLOCK_SIZE):
         super(FacebookDownloader, self).__init__(savePath, url, vedioName, threadCnt, blockSize)

    def init(self):
        self.gen_vedio_name()

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
                html = requests.get(self.url).content.decode('utf-8')
                logger.warn(f"facebook downloader the video in sd quality... \n")
                tmp_url = re.search(rf'sd_src:"(.+?)"', html) if re.search(rf'sd_src:"(.+?)"', html) != None else re.search(rf'hd_src:"(.+?)"', html)

                if tmp_url == None:
                    logger.error(f"facebookdown load error, the:{self.url}have no vedio ")
                    return False
                
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
                print(f"facebook  {self.url} download error :{current} time ".format(str(e)).encode("utf-8"))
                logging.exception(e)

        return False
