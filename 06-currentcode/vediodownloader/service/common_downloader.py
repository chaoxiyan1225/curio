# -*- coding:utf-8 -*-  
import os, sys, time, signal, datetime
import requests, urllib, json
from Crypto.Cipher import AES #使用的是 pip install pycryptodome
from binascii import b2a_hex, a2b_hex
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm # 用于显示进度条
import multitasking, threading # 用于多线程操作
from retry import retry# 导入 retry 库以方便进行下载出错重试
from bs4 import BeautifulSoup
import logging

import utils.logger as logger

signal.signal(signal.SIGINT, multitasking.killall)
from Crypto.Util.Padding import pad

from utils.commontool import *

#reload(sys)
#sys.setdefaultencoding('utf-8')

default_thread_cnt = 8
BLOCK_SIZE = 512 * 1024
RETRY_TIME = 3

MB = 1024**2

class MetricInfo(object):
    def __init__(self, totalVedioCnt=0, successVedioCnt=0, percentCurrent=0):
         self.totalVedioCnt = totalVedioCnt
         self.successVedioCnt = successVedioCnt
         self.percentCurrent = percentCurrent
         self.failVedioCnt = 0 
         
    def  to_string(self):
        return f"totalVedioCnt:{self.totalVedioCnt}, successVedioCnt:{self.successVedioCnt}, percentCurrent:{self.percentCurrent}, failVedioCnt:{self.failVedioCnt}"
'''
   该类用来处理TS格式的视频文件下载
   支持多线程模式
'''
class  CommonDownloader(object):

    def __init__(self, savePath, url, vedioName=None, threadCnt = default_thread_cnt, blockSize = BLOCK_SIZE):
        self.threadCnt = threadCnt
        self.blockSize = blockSize
        self.key = None
        self.downSuccess = 0
        self.downTotal = 0
        self.lock = threading.Lock()
        self.vedioName = vedioName
        self.download_path = savePath
        self.download_ts = ""
        self.url = url
        self.metricInfo = MetricInfo()

    def init(self):
        nameTitle, m3u8s, mp4s = self.gen_VedioInfos()
        if self.vedioName == None:
           self.vedioName = nameTitle
        
 
    def gen_VedioInfos(self):
    
        logger.warn(f'需要解析视频名以及含有的视频信息')
        current = 0
        vedioName = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S')
        delay = 5
        resultM3u8 = set()
        resultMp4 = set()
        
        while current < RETRY_TIME:
            try: 
                current = current + 1
                response = requests.get(self.url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text,'html.parser')
                response.close()
                pagetitle = soup.find("title")
                
                if pagetitle:
                   vedioName = str(pagetitle)[8:40].replace(" ", "")
                   
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
                             
                logger.warn(f'the vedioTile:{vedioName}, the parse_subUrls {resultMp4}, {resultM3u8}')
                return vedioName, resultM3u8, resultMp4
     
            except Exception as e:
                logger.error(f" parse vedioinfo error, {self.url} {e}".encode("utf-8"))
                logging.exception(e)
                time.sleep(delay)
                delay *= 2
                
        logger.warn(f'the vedioTile:{vedioName}, the parse_subUrls {resultMp4}, {resultM3u8}')
        return vedioName, resultM3u8, resultMp4
        
    def get_percent_current(self):
        pass
  
    def get_metric(self):
        self.metricInfo.percentCurrent = self.get_percent_current()
        return self.metricInfo    


    def map_download_task(self, urlList):
        useThreadCnt = len(urlList) if self.threadCnt > len(urlList) else self.threadCnt
        taskList = []

        for i in range(useThreadCnt):
            taskList.append({})
            
        for index, url in enumerate(urlList):  
            taskMapNum = index % useThreadCnt
            taskList[taskMapNum][index] = url
            #logger.warn("urlis :"+ url)
            
        return useThreadCnt, len(urlList),taskList
        
    def parse_subUrls(self, url):
        pass

    def clear(self):
        pass

    def parse_all_vedios(self, urls):
        pass


    def downLoad_start(self):
        pass
    
