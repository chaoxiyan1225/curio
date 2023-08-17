import useruitool as UserUITool
import sys, platform, random

from service.systemcontrol import *
from service.usercontrol import *
from service.vediodownloadprocesser import *
from conf.pictures import *
import utils.useruitool as UserUITool
import utils.commontool as CommonTool
from service.system_control import *
from service.user_control import *
from service.downloader_control import *
import utils.logger as logger


downloadCtrl = DownloadControl()
           
def downLoading(urls, savePath):
    try:
        downloadCtrl.downLoad_start(urls, savePath)
    except Exception as e1:
        logger.error(f"the input url:{urls} download fail, and error msg: {str(e1)}")
        messagebox.showinfo(title="严重", message="下载出现问题请稍后重试") 
        #self.is_need_stop = True
        logger.exception(e1)
        self.downloadCtrl.clear()
        
def inside_thread(self):
        while True:
            metricInfo = downloadCtrl.get_total_metrics()
            if metricInfo == None:
               time.sleep(5)
               continue
            
            self.set_frame_view(metricInfo)

            if metricInfo.totalVedioCnt > 0 and metricInfo.totalFailCnt + metricInfo.totalSuccessCnt >= metricInfo.totalVedioCnt:
               logger.warn(f"have  down load finish, {metricInfo.to_string()}")
               self.is_need_stop = True
               break
               
            if not self.downloadCtrl.downloading:
               logger.warn(f'the downloader finish')
               break
          
            time.sleep(10)
        
def main():

    t = threading.Thread(target=downLoading, args=(urls, savePath))
    t2 = threading.Thread(target=self.inside_thread)
    t2.start()
    t.start()

   
if __name__ == "__main__":
    logger.warn('now start')
    try:
      main()
    except Exception as e:
      logger.error(f'the error happens: {str(e)}')
    
    logger.warn('end')
