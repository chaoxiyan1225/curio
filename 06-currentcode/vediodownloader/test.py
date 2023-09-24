# -*- coding:utf-8 -*-  
from __future__ import unicode_literals
import sys, platform, random
from conf.pictures import *
import utils.useruitool as UserUITool
import utils.commontool as CommonTool
from service.system_control import *
from service.user_control import *
from service.downloader_control import *
from utils.logger import *
from yt_dlp import YoutubeDL
import requests
from conf.systemconf import *
from urllib.parse import urlencode
import logging

from pytube import YouTube
import random

from requests.auth import HTTPBasicAuth,HTTPDigestAuth
from requests_ntlm import HttpNtlmAuth



downloadCtrl = DownloadControl()


def gen_VedioInfos(url):
    
        logger.warning(f'需要解析视频名以及含有的视频信息')
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
                    #logger.warning(k)
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
                             
                logger.warning(f'the vedioTile, the parse_subUrls {resultMp4}, {resultM3u8}')
                return vedioName, resultM3u8, resultMp4
     
            except Exception as e:
                logger.error(f" parse vedioinfo error, {url} {e}".encode("utf-8"))
                logging.exception(e)
                time.sleep(delay)
                delay *= 2
                
        logger.warning(f'the vedioTile:{vedioName}, the parse_subUrls {resultMp4}, {resultM3u8}')
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
            
            logger.warning(f'the current percent: {metricInfo.currentMetricInfo.percentCurrent}')

            if metricInfo.totalVedioCnt > 0 and metricInfo.totalFailCnt + metricInfo.totalSuccessCnt >= metricInfo.totalVedioCnt:
               logger.warning(f"have  down load finish, {metricInfo.to_string()}")
               is_need_stop = True
               break
               
            if not downloadCtrl.downloading:
               logger.warning(f'the downloader finish')
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
   


def downLoader_ytb(link):
        yt = None
        try:
            logger.warning(f"youtube downloader start download from  {link}")
            yt=YouTube(link, use_oauth=True, allow_oauth_cache=False)
        except Exception as e:
            logger.error("[ERROR] {0}".format(str(e)).encode("utf-8"))
            return -1
        
        pattern = r'[\/.:*?"<>|]+'
        regex = re.compile(pattern)
        #filename = regex.sub('',yt.title).\
        #                replace('\'','').replace('\\','')+".mp4"
        
       
        mp4Path = "E:\sourcecode\download"
        
        logger.warning(f"the path {mp4Path}")

        
        current = 0
      
        while current < 1:
            try:   
                logger.warning("youtube downloader [DOWNLOAD] {0}")
                yt.streams.filter(subtype='mp4',progressive=True)\
                        .order_by('resolution')\
                        .desc()\
                        .first().download(mp4Path)
                
                current = current + 1 
              
                logger.warning("youtube download success")
                
                return True
            except Exception as e:
                logger.error(f"the youtube download error, {current} time".format(str(e)).encode("utf-8"))
                logging.exception(e)


        return False

'''
 |  progress_hooks:    A list of functions that get called on download
 |                     progress, with a dictionary with the entries
 |                     * status: One of "downloading", "error", or "finished".
 |                               Check this first and ignore unknown values.
 |                     * info_dict: The extracted info_dict
 |
 |                     If status is one of "downloading", or "finished", the
 |                     following properties may also be present:
 |                     * filename: The final filename (always present)
 |                     * tmpfilename: The filename we're currently writing to
 |                     * downloaded_bytes: Bytes on disk
 |                     * total_bytes: Size of the whole file, None if unknown
 |                     * total_bytes_estimate: Guess of the eventual file size,
 |                                             None if unavailable.
 |                     * elapsed: The number of seconds since download started.
 |                     * eta: The estimated time in seconds, None if unknown
 |                     * speed: The download speed in bytes/second, None if
 |                              unknown
 |                     * fragment_index: The counter of the currently
 |                                       downloaded video fragment.
 |                     * fragment_count: The number of fragments (= individual
 |                                       files that will be merged)
 |
 |                     Progress hooks are guaranteed to be called at least once
 |                     (with status "finished") if the download is successful.

''' 

def my_hook(d):
    if d['status'] == 'finished':
        logger.warning('Done downloading, now post-processing ...')
        
    if d['status'] == 'downloading':
       p = d['downloaded_bytes']/d['total_bytes']
       logger.warning(f'the current progress:{p}')
    
       
def down_ydl(link):
    URLS = [link]
    cnt = 0 
    ydl_opts = {
    'logger': logger,
    'progress_hooks': [my_hook],
    'outtmpl': 'C:\\Users\\orange\\gitproject\\curio\\06-currentcode\\'+f'%(title)s.%(ext)s',
    }

    with YoutubeDL(ydl_opts) as ydl:
        while cnt < 3:
            try:
              cnt = cnt + 1
              logger.warning(f"start: {cnt}")
              ydl.download(URLS)
              logger.warning("finish")
              return
            except Exception as e:
              logger.error(str(e))
          
if __name__ == "__main__":

    logger.warning('now start')
    down_ydl("https://www.youtube.com/watch?v=-fopYsgFdzc")

    logger.warning('end')
