
# -*- coding:utf-8 -*-  
import os
import sys
import requests
import datetime

from Crypto.Cipher import AES #使用的是 pip install pycryptodome
from binascii import b2a_hex, a2b_hex

from concurrent.futures import ThreadPoolExecutor
import threading
import time
import urllib

# 用于显示进度条
from tqdm import tqdm
# 用于发起网络请求
import requests
# 用于多线程操作
import multitasking
import signal
# 导入 retry 库以方便进行下载出错重试
from retry import retry
signal.signal(signal.SIGINT, multitasking.killall)

#reload(sys)
#sys.setdefaultencoding('utf-8')

key = ""
download_path = ""
download_ts = ""
default_thread_cnt = 8
BLOCK_SIZE = 512 * 1024


'''
初始化函数，创建临时路径等
'''
def init():
    global download_path
    download_path = os.path.join(os.getcwd(), "download")
    if not os.path.exists(download_path):
        os.mkdir(download_path)
        
    #新建日期文件夹
    download_path = os.path.join(download_path, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    #print download_path
    os.mkdir(download_path)
    
    global download_ts
    download_ts = os.path.join(download_path, "tsfile")
    os.mkdir(download_ts)
       
def MapDownLoadTask(urlList, threadCnt = default_thread_cnt):
    threadCnt = len(urlList) if threadCnt > len(urlList) else threadCnt
    taskList = []
    totalFileSize = 0
    
    #print(f'urlList: {urlList}')
    for i in range(threadCnt):
        taskList.append({})
        
    for index, url in enumerate(urlList):  
        taskMapNum = index % threadCnt
        taskList[taskMapNum][index] = url
        #print("urlis :"+ url)
        '''
        response = requests.head(url)
        file_size = response.headers.get('Content-Length')
        if file_size is None:
           if raise_error is True:
               raise ValueError('该文件不支持多线程分段下载！')
           totalFileSize = totalFileSize +file_size
        '''
    #print(f'taskList: {taskList}')
        
    return threadCnt, len(urlList),taskList
    
    
def downloadTsFiles(urlList: list, retry_times: int = 3) -> None:

    print(f'一共待下载的ts文件数：{len(urlList)}')
    
    start = time.time()
    #先把任务分组
    threadCnt, totalFileCnt,taskList = MapDownLoadTask(urlList)

    '''
    根据文件直链和文件名下载文件
    Parameters
    ----------
    url : 文件直链
    file_name : 文件名
    retry_times: 可选的，每次连接失败重试次数
    Return
    ------
    None
    '''
    @retry(tries=retry_times)
    @multitasking.task
    def start_download(urlsMap) -> None:
 
        for index,url in urlsMap.items():
            #res = requests.get(url)
            urlfile = urllib.request.urlopen(url)
            cryptor = None
            if len(key): # AES 解密
               cryptor = AES.new(key, AES.MODE_CBC, key)
            
            tsName = os.path.join(download_ts, str(index) + ".ts")
            with open(tsName, 'ab') as tsFile:
                   #f.write(cryptor.decrypt(res.content))
                   #通过buffer控制每次读取的大小，防止内存爆掉
                while True:
                    buffer = urlfile.read(BLOCK_SIZE)
                    if not buffer:
                       # There is nothing more to read
                       break
                    content = buffer if cryptor == None else cryptor.decrypt(buffer)
                    tsFile.write(content)
                    tsFile.flush()
                bar.update(1)
                tsFile.close()
        
    
    # 创建进度条
    bar = tqdm(total=totalFileCnt, desc=f'下载文件总数：{len(urlList)}')
    
    for urlMap in taskList:
        start_download(urlMap)
    # 等待全部线程结束
    multitasking.wait_for_tasks()
    bar.close()
    
    totalCost = (time.time() - start) / 60
    print(f'下载任务结束，总计下载耗时:%.1f 分钟' % totalCost)
    
def mergeTs2MP4(mp4FileName:str)->None:

    '''
    把单个ts文件顺序写入到 mp4 文件中
    '''
    def ts2MP4(tsPath:str, mp4FileName:str)->bool:
        if not tsPath or not mp4FileName:
            return False  

        with open(tsPath, "rb") as tsf:
            '''
            while True:
                buffer = tsf.read(BLOCK_SIZE)
                if not buffer:
                  break
                  
                mp4f.write(buffer)
                mp4f.flush()
            '''
            mp4f.write(tsf.read())
            bar.update(1)#更新进度条
           
        return True
        
    #列举所有的ts文件，按文件标号排序，非字典序
    fs = os.listdir(download_ts)
    fs.sort(key= lambda x:int(x[:-3]))
    
    print(f'一共下载成功的ts文件数目是：{len(fs)}')
    
    mp4Name = os.path.join(download_path, mp4FileName + ".mp4")
    mp4f = open(mp4Name, "ab")
    
    # 创建进度条
    bar = tqdm(total=len(fs), desc=f'需转换的ts文件数：{len(fs)}')
    for f in fs:
        tmp = os.path.join(download_ts, f)
        if os.path.isfile(tmp):
           ret2 = ts2MP4(tmp, mp4FileName)
           if not ret2:
              print("ts2MP4 fail, filename:", tmp)
              continue

        elif os.path.isdir(tmp):
           func(tmp) # 递归去获取
        else:
           print('其他情况')
           
    mp4f.close()    
    bar.close()
    
    #清除临时的TS文件
    os.chdir(download_ts)
    os.system('del /Q *.ts')

 
def downLoadPrecess(url, mp4Name):

    #创建下载路径等准备
    init()
    
    all_content = requests.get(url).text  # 获取第一层M3U8文件内容
    m3u8File = download_path + "\site.m3u8"
    
    print(f'm3u8文件的保存路径： {m3u8File}')
    
    with open(m3u8File, "wb") as file:
         file.write(all_content.encode())
    
    if "#EXTM3U" not in all_content:
        raise BaseException("非M3U8的链接")
 
    unknow = True
    all_line = all_content.split("\n") 
    allTsFiles = []
    for index, line in enumerate(all_line): # 第二层
        if "#EXT-X-KEY" in line:  # 找解密Key
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]
            print("Decode Method：", method)
            
            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]
            
            key_url = key_path # 拼出key解密密钥URL
            
            res = requests.get(key_url)
            global key
            key = res.content
            print(f'ts文件的加密 key:{key}')
            
        if "#" not in line and 'http' in line: # 找ts地址并下载
            unknow = False
            pd_url = line # 拼出ts片段的URL
            allTsFiles.append(pd_url)
            
    if unknow:
        raise BaseException("未找到对应的TS文件URL")
    else:
        print("ts文件的URL解析完成")
    
    #多线程下载TS files
    downloadTsFiles(allTsFiles, 3)
    
    #把 TS files 合并为一个mp4文件
    mergeTs2MP4(mp4Name)
    
    
def merge_file(tsPath):
    os.chdir(tsPath)
    cmd = "copy /b * new.tmp"
    os.system(cmd)
    os.system('del /Q *.ts')
    os.system('del /Q *.mp4')
    os.rename("new.tmp", "new.mp4")
  
if __name__ == '__main__': 

    start = time.time()
    url = "https://long.lgtcpnb.cn/videos1/b379cf0988f4e9147efe341e8dc1b988/b379cf0988f4e9147efe341e8dc1b988.m3u8" 
    downLoadPrecess(url, "空姐")
    end = time.time()
    
    totalCost = (end - start) / 60
    
    print(f'线程数目:{default_thread_cnt}-总耗时:%.1f 分钟' % totalCost )
    
    #merge_file("E:\\sourcecode\\download\\20230114_212551\\tsfile")
