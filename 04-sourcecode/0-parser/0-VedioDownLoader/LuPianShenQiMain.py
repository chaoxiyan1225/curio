# -*- coding:utf-8 -*-  
import os, sys, time, signal, datetime
import requests, urllib, json

from VedioDownLoadProcesser import VedioDownLoadProcesser

from tqdm import tqdm # 用于显示进度条
import Errors

from loguru import logger
logger.add('LuPianShenQI_{time}.log',rotation="100 MB", retention='10 days')


headers={
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
   

'''
   该类用来处理TS/mp4格式的视频文件下载的控制类，包括权限验证
'''

class  LuPianShenQiMain:


    def __init__(self):
       self.userCtrl = UserControl()
       self.systemCtrl = SystemContrl()
    
    
    def beforeCheck(self):
        
        result = self.userCtrl.loginCheck()
        if result != Errors.SUCCESS:
           print(f'userLogin check fail {result.toString()}')
           return result;
           
        return self.systemCtrl.clientConfValid()

           
           
    def main(self):
        befCheckRet = selft.beforeCheck()
        


if __name__ == '__main__': 

    start = time.time()
    tsProcess = VedioDownLoadProcesser()
    url = "https://better.ccgg6.com/archives/19800/" 
    tsProcess.downLoadStart(url, "乱伦大战")
    
    end = time.time()
    
    totalCost = (end - start) / 60
    
    print(f'总耗时:%.1f 分钟' % totalCost )
    
    #merge_file("E:\\sourcecode\\download\\20230114_212551\\tsfile")
