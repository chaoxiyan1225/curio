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
import requests
from conf.systemconf import *
from urllib.parse import urlencode

from requests.auth import HTTPBasicAuth,HTTPDigestAuth
from requests_ntlm import HttpNtlmAuth



downloadCtrl = DownloadControl()


def gen_VedioInfos(url):
    
        logger.warn(f'需要解析视频名以及含有的视频信息')
        current = 0
        vedioName = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S')
        delay = 5
        resultM3u8 = set()
        resultMp4 = set()
        
        while current < RETRY_TIME:
            try: 
                current = current + 1
                response = requests.get(url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.text,'html.parser')
              
                response.close()
                pagetitle = soup.find("title")
                
                if pagetitle:
                   vedioName = str(pagetitle)[8:40].replace(" ", "")
                   for char in vedioName:
                        if char in sets:
                            vedioName = vedioName.replace(char, '')
                   
                invalidLink1='#'
                invalidLink2='javascript:void(0)'
           
                mycount=0
                for k in soup.find_all('a'):
                    #logger.warn(k)
                    link=k.get('href')
                    if(link is not None):
                        if link==invalidLink1:
                            pass
                        elif link==invalidLink2:
                            pass
                        elif link.find("javascript:")!=-1:
                            pass
                        else:
                            mycount=mycount+1
                        if '.m3u8' in link:
                            resultM3u8.add(link)
                        if '.mp4' in link:
                            resultMp4.add(link)
   
                if len(resultM3u8) == 0 and len(resultMp4) == 0: 
                    r=r'/http.*\.mp4' 
                    re_mp4=re.compile(r)  
                    mp4List=re.findall(re_mp4, response.text)  
                    for url in mp4List:  
                       resultMp4.add(url)
                      
                    r=r'/http.*\.m3u8'
                    re_m3u8=re.compile(r)  
                    m3u8List=re.findall(re_m3u8, response.text)  
                    for url in m3u8List:  
                       resultM3u8.add(url)
                   
                if  len(resultM3u8) == 0 and len(resultMp4) == 0:     
                    # 51网适配        
                    for k in soup.select('div[data-config]'):
                        jsonData = k.get('data-config')
                        if jsonData:
                           m3u8Json = json.loads(jsonData.strip('\t\n'))
                           vedio = m3u8Json['video']
                           if vedio:
                              url = vedio['url']
                              if url and  '.m3u8' in url:
                                 resultM3u8.add(url)
                                 
                              if url and  '.mp4' in url:
                                 resultMp4.add(url)
                             
                logger.warn(f'the vedioTile, the parse_subUrls {resultMp4}, {resultM3u8}')
                return vedioName, resultM3u8, resultMp4
     
            except Exception as e:
                logger.error(f" parse vedioinfo error, {url} {e}".encode("utf-8"))
                logging.exception(e)
                time.sleep(delay)
                delay *= 2
                
        logger.warn(f'the vedioTile:{vedioName}, the parse_subUrls {resultMp4}, {resultM3u8}')
        return vedioName, resultM3u8, resultMp4

           
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

    url = "https://motherless.com/7AF4696"
    
    gen_VedioInfos(url)
    
    ''' 
    savePath = "D:/"
    t = threading.Thread(target=downLoading, args=(urls, savePath))
    t2 = threading.Thread(target=inside_thread)
    t2.start()
    t.start()
    '''
   
   
   
def test2():
   content = 'data-mediabook="https://ev-ph.ypncdn.com/videos/202101/20/382104382/360P_360K_382104382_fb.mp4?rate=40k&amp;burst=1000k&amp;validfrom=1692791200&amp;validto=1692805600&amp;hash=QINisaB1Hh6wqdLvevUXfSVeXYQ%3D"'
   
   
   r=r'https?://.*\.(mp4|(mp4\?.*))'        
   re_mp4=re.compile(r)  
   
   for c in content.split("\""): 
      if re.match(re_mp4, c): 
         print(c)
   
   
   
if __name__ == "__main__":
    logger.warn('now start')
    try:
      #main()
            logger.warn(f'the vedio url')
            response = requests.head("https://ev-ph.ypncdn.com/videos/201509/09/56921831/191127_1058_360P_360K_56921831_fb.mp4?validfrom=1692968814&amp;validto=1692976014&amp;rate=40k&amp;burst=300k&amp;hash=YpVi43ukRa4I2HAUVRxVkibZ2Hw%3D ",auth=HTTPDigestAuth("youporntbag", "ycx/8520/8520-+"))
            file_size = response.headers.get('Content-Length')
            logger.warn(f'the response:{response.text},{response.headers} {file_size}')
      #print(urlencode("REAL mom son | MOTHERLESS.COM ™"))
      
    except Exception as e:
      logger.error(f'the error happens: {str(e)}')
    
    logger.warn('end')
