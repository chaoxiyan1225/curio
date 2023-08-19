# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys, platform, random
from conf.pictures import *
import utils.useruitool as UserUITool
import utils.commontool as CommonTool
from service.system_control import *
from service.user_control import *
from service.downloader_control import *
import utils.logger as logger
import yt_dlp    


def my_hook(d):    
    if d['status'] == 'finished':
        pass

ydl_opts = {        
    'format':'bestvideo[height<=480]+bestaudio/best[height<=480]',
     'outtmpl': 'd:/',        
    # 'outtmpl': 'c:/images/%(id)s%(ext)s',        
    # 'cookiefile':'fbcookie.txt',        
    'postprocessors': [{                        
    'key': 'FFmpegVideoConvertor',                        
    'preferedformat': 'mp4'                        
    }],        
'logger': logger,        
'progress_hooks': [my_hook],    
}   
 
downloadCtrl = DownloadControl()
           
def downLoading(urls, savePath):
    try:
        downloadCtrl.downLoad_start(urls, savePath)
    except Exception as e1:
        logger.error(f"the input url:{urls} download fail, and error msg: {str(e1)}")
        messagebox.showinfo(title="严重", message="下载出现问题请稍后重试") 
        #self.is_need_stop = True
        logger.exception(e1)
        downloadCtrl.clear()
        
def inside_thread():
        while True:
            metricInfo = downloadCtrl.get_total_metrics()
            if metricInfo == None:
               time.sleep(5)
               continue
            
            logger.warn(f'the current percent: {metricInfo.currentMetricInfo.percentCurrent}')

            if metricInfo.totalVedioCnt > 0 and metricInfo.totalFailCnt + metricInfo.totalSuccessCnt >= metricInfo.totalVedioCnt:
               logger.warn(f"have  down load finish, {metricInfo.to_string()}")
               is_need_stop = True
               break
               
            if not downloadCtrl.downloading:
               logger.warn(f'the downloader finish')
               break
          
            time.sleep(10)
        
def main():

    urls = ["https://p8olrc.com/video/91141/"]
    savePath = "D:/"
    t = threading.Thread(target=downLoading, args=(urls, savePath))
    t2 = threading.Thread(target=inside_thread)
    t2.start()
    t.start()

   
if __name__ == "__main__":
    logger.warn('now start')
    try:
      main()
      
    except Exception as e:
      logger.error(f'the error happens: {str(e)}')
    
    logger.warn('end')
