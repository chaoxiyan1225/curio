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

import utils.logger as logger
import shutil

signal.signal(signal.SIGINT, multitasking.killall)
from Crypto.Util.Padding import pad

#reload(sys)
#sys.setdefaultencoding('utf-8')

default_thread_cnt = 8
BLOCK_SIZE = 512 * 1024

headers={
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

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

    def __init__(self, threadCnt = default_thread_cnt, blockSize = BLOCK_SIZE):
        self.threadCnt = threadCnt
        self.blockSize = blockSize
        self.key = None
        self.downSuccess = 0
        self.downTotal = 0
        self.lock = threading.Lock()
        self.name = None
        self.download_path = ""
        self.download_ts = ""
        self.metricInfo = MetricInfo()

    '''
      可能子下载器需要自己的init
    '''
    def init(self, savePath):
        pass


    def get_percent_current(self):
        pass
  
    def get_metric(self):
        self.metricInfo.percentCurrent = self.get_percent_current()
        return self.metricInfo    


    def map_download_task(self, urlList):
        useThreadCnt = len(urlList) if self.threadCnt > len(urlList) else self.threadCnt
        taskList = []
        totalFileSize = 0
        
        for i in range(useThreadCnt):
            taskList.append({})
            
        for index, url in enumerate(urlList):  
            taskMapNum = index % useThreadCnt
            taskList[taskMapNum][index] = url
            #logger.warn("urlis :"+ url)
            
        return useThreadCnt, len(urlList),taskList
        
    def parse_subUrls(self, url):
        pass


    def clear_file(self):
        pass

    def parse_all_vedios(self, urls):
        pass


    def downLoad_start(self, urls, savePath, mp4Name = None):
        pass
    
