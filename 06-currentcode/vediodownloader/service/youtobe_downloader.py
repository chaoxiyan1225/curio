# -*- coding:utf-8 -*-  
import re
from pytube import YouTube
from pathlib import Path
from service.common_downloader import *

class YoutubeDownloader(CommonDownloader):

    def __init__(self, savePath, url, vedioName=None, threadCnt = default_thread_cnt, blockSize = BLOCK_SIZE):
         super(YoutubeDownloader, self).__init__(savePath, url, vedioName, threadCnt, blockSize)

    def clear(self):
        return
    
    def progress_set(stream = None, chunk = None, file_handle = None, remaining = None):
        filesize = chunk.filesize
        current = ((filesize - remaining)/filesize)
        percent = ('{0:.1f}').format(current*100)
        progress = int(50*current)
        
        self.downTotal = filesize
        self.downSuccess = filesize - remaining
       
    def get_percent_current(self):
        fenMu = 1000000 if self.downTotal==0 else self.downTotal
        return int((self.downSuccess * 100) / fenMu)
  
    def get_metric(self):
        self.metricInfo.percentCurrent = self.get_percent_current()
        return self.metricInfo    

    def downLoad_start(self):
        try:
            logger.warn(f"youtube downloader start download from  {self.url}")
            self.init()
            yt=YouTube(self.url, on_progress_callback = self.progress_set)
        except Exception as e:
            logger.error("[ERROR      ] {0}".format(str(e)).encode("utf-8"))
            return -1
        

        pattern = r'[\/.:*?"<>|]+'
        regex = re.compile(pattern)
        filename = regex.sub('',yt.title).\
                        replace('\'','').replace('\\','')+".mp4"
        
        self.vedioName = filename if filename else self.gen_vedio_name()

        p=Path(self.download_path)
        mp4Path = p / self.vedioName

        if mp4Path.exists():
            logger.warn("[SKIP]".format(mp4Path))
            return 0
        
        current = 0
        self.downTotal = 1
        self.totalVedioCnt = 1

        while current < RETRY_TIME:
            try:   
                logger.warn("youtube downloader [DOWNLOAD] {0}".format(self.vedioName))
                yt.streams.filter(subtype='mp4',progressive=True)\
                        .order_by('resolution')\
                        .desc()\
                        .first().download(mp4Path)
                
                current = current + 1 
                self.downSuccess = self.downTotal
                logger.warn("youtube download success".format(self.vedioName))
                self.successVedioCnt = 1                
                return True
            except Exception as e:
                logger.error(f"the youtube download error, {current} time".format(str(e)).encode("utf-8"))
                logging.exception(e)
                self.failVedioCnt = 1

        return False
