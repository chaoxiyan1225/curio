# -*- coding:utf-8 -*-  
import re
from pytube import YouTube
from pathlib import Path
from service.common_downloader import *
from yt_dlp import YoutubeDL

class YoutubeDownloader(CommonDownloader):

    def __init__(self, savePath, url, vedioName=None, threadCnt = default_thread_cnt, blockSize = BLOCK_SIZE):
         super(YoutubeDownloader, self).__init__(savePath, url, vedioName, threadCnt, blockSize)

    def clear(self):
        return
    
    def get_metric(self):
        return self.metricInfo  

    def ydl_hook(self, d):
        #logger.warning(d)
        if d['status'] == 'finished':
           self.metricInfo.percentCurrent = 100
            
        if d['status'] == 'downloading':
           totalSize = 1
           
           if 'total_bytes' in d:
               totalSize = d['total_bytes']
           elif 'total_bytes_estimate' in d:
               totalSize = d['total_bytes_estimate']
               
           p = d['downloaded_bytes']/ totalSize
           self.metricInfo.percentCurrent = (int)(p * 100)
     
    def downLoad_start(self):
        URLS = [self.url]
        ydl_opts = {
        'logger': logger,
        'progress_hooks': [self.ydl_hook],
        'outtmpl': self.download_path + '\\'+f'%(title)s.%(ext)s',
        }
        
        logger.warning(f"youtube downloader start download from:{self.url}, and the opts:{ydl_opts}")
        current = 0 
        with YoutubeDL(ydl_opts) as ydl:
            while current < RETRY_TIME:
                try:
                    logger.warning(f"[DOWNLOAD]:{current}")
                    current = current + 1 
                    ydl.download(URLS)
                    logger.warning("finish")
                    logger.warning("youtube download success".format(self.vedioName))           
                    return True
                except Exception as e:
                    logger.error(f"the youtube download error, {current} time".format(str(e)).encode("utf-8"))
                    logging.exception(e)
                    self.failVedioCnt = 1

        return False
