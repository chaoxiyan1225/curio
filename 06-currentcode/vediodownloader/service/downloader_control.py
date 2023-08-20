# -*- coding:utf-8 -*-  
import os, sys, time, signal, datetime
import requests, urllib, json
from Crypto.Cipher import AES #使用的是 pip install pycryptodome
from binascii import b2a_hex, a2b_hex
from concurrent.futures import ThreadPoolExecutor
from retry import retry# 导入 retry 库以方便进行下载出错重试
import conf.systemconf as SystemConf
import threading

#from aioVextractor.api import hybrid_worker
import aiohttp
import asyncio
from pprint import pprint

import utils.logger as logger
from service.facebook_downloader import * 
from service.instagram_downloader import * 
from service.youtobe_downloader import * 
from service.mp4_ts_downloader import *
from service.common_downloader import *


default_thread_cnt = 8
BLOCK_SIZE = 512 * 1024

metricMap = {}

class TotalMetricInfo:
    def __init__(self):
        self.totalVedioCnt = 0
        self.totalFailCnt = 0
        self.totalSuccessCnt = 0
        self.currentMetricInfo = None
        self.totalUrlCnt = 0
        self.currentUrl = 0 

class  DownloadControl:

    def __init__(self, threadCnt = default_thread_cnt, blockSize = BLOCK_SIZE):
        self.threadCnt = threadCnt
        self.blockSize = blockSize
        self.currentDownLoader = None
        self.totalMetricInfo = None
        self.vedioName = None
        self.download_path = None
        self.downloading = True
        self.lock = threading.Lock()
       
    '''
    初始化函数，创建临时路径等
    '''
    def init(self, savePath):
        logger.warn(f'------downloadContrl init:start-----------')
        
        self.totalMetricInfo = TotalMetricInfo()
    
        if savePath != None and savePath != "":
           self.download_path = savePath.replace("/", "\\")
        else:
           self.download_path = os.getcwd()
        
        logger.warn(f'------downloadContrl init:end-----------')

    def get_total_metrics(self):
    
        if self.currentDownLoader == None:
           return None
           
        self.lock.acquire()
        self.totalMetricInfo.currentMetricInfo = self.currentDownLoader.get_metric()
        self.lock.release()

        return self.totalMetricInfo    
    
    def update_total_metrics(self, url, metricInfo):
        self.lock.acquire()
        metricMap[url] = metricInfo
        self.lock.release()

    # def parse_all_vedios(self, urls):
    #     async def get_url_vedios(url):
    #         async with  aiohttp.ClientSession() as session:
    #             result = await hybrid_worker(
    #                 webpage_url=url,
    #                 session=session,
    #             )
    #             return result

    #     #url = "https://www.youtube.com/playlist?list=PLs54iBUqIopDv2wRhkqArl9AEV1PU-gmc"
    #     #https://juejin.cn/post/6844903988001767431
    #     for url in urls:
    #         print(asyncio.run(get_url_vedios(url=url)))
 
    def clear(self):
        self.downloading = False
        return None
    
    def get_downloader_by_url(self, url):
        if not url or url.strip() == "":
           logger.error("the url illegal!")
           return None
        
        if SystemConf.FACE_BOOK in url: 
            return FacebookDownloader(self.download_path, url, self.vedioName)
        elif SystemConf.YOUTOBE in url:
            return YoutubeDownloader(self.download_path, url, self.vedioName)
        elif SystemConf.INSTAGRAM in url:
            return InstagramDownloader(self.download_path, url, self.vedioName)
        else: 
            return MP4TSDownloader(self.download_path, url, self.vedioName)

    
    def downLoad_start(self, urls, savePath, mp4Name = None):
        self.init(savePath)

        # first parse all vedio url
        #self.parse_all_vedios(urls)
        count = 0

        for url in urls:
            count = count + 1
            self.vedioName = mp4Name
            self.currentDownLoader = self.get_downloader_by_url(url)
   
            self.totalMetricInfo.currentUrl = count
            self.totalMetricInfo.totalUrlCnt = len(urls)
            self.currentDownLoader.downLoad_start()
            self.update_total_metrics(url, self.currentDownLoader.get_metric())
              
        self.clear()
