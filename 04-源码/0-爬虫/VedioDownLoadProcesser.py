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

signal.signal(signal.SIGINT, multitasking.killall)

from loguru import logger

logger.add('LuPianShenQI_{time}.log',rotation="100 MB", retention='10 days')

#reload(sys)
#sys.setdefaultencoding('utf-8')

download_path = ""
download_ts = ""
default_thread_cnt = 8
BLOCK_SIZE = 512 * 1024

headers={
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
   

'''
   该类用来处理TS格式的视频文件下载
   支持多线程模式
'''
class  VedioDownLoadProcesser:

    def __init__(self, threadCnt = default_thread_cnt, blockSize = BLOCK_SIZE):
        self.threadCnt = threadCnt
        self.blockSize = blockSize
        self.key = None


    '''
    初始化函数，创建临时路径等
    '''
    def init(self):

        logger.warning(f'------初始化系统配置：start-----------')
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
        logger.warning(f'------初始化系统配置：end-----------')
    '''
    按线程数和下载列表去划分任务到多个线程中      
    '''
    def MapDownLoadTask(self, urlList):
        useThreadCnt = len(urlList) if self.threadCnt > len(urlList) else self.threadCnt
        taskList = []
        totalFileSize = 0
        
        for i in range(useThreadCnt):
            taskList.append({})
            
        for index, url in enumerate(urlList):  
            taskMapNum = index % useThreadCnt
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
            
        return useThreadCnt, len(urlList),taskList
        
    #多线程方式去下载TS文件
    def downloadTsFiles(self, urlList: list, retry_times: int = 3) -> None:

        logger.warning(f'一共待下载的ts文件数：{len(urlList)}')
        
        start = time.time()
        #先把任务分组
        useThreadCnt, totalFileCnt, taskList = self.MapDownLoadTask(urlList)

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
                req = urllib.request.Request(url, headers = headers)
                urlfile = urllib.request.urlopen(req)
                cryptor = None
                if len(self.key): # AES 解密
                   cryptor = AES.new(self.key, AES.MODE_CBC, self.key)
                
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
        multitasking.set_max_threads(useThreadCnt)
        
        for urlMap in taskList:
            start_download(urlMap)
        # 等待全部线程结束
        multitasking.wait_for_tasks()
        bar.close()
        
        totalCost = (time.time() - start) / 60
        logger.warning(f'下载任务结束，总计下载耗时:%.1f 分钟' % totalCost)
        
    def mergeTs2MP4(self, mp4FileName:str)->None:

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
        
        logger.warning(f'开始转为mp4，待转换TS文件数量：{len(fs)}')
        
        mp4Name = os.path.join(download_path, mp4FileName + ".mp4")
        mp4f = open(mp4Name, "ab")
        
        # 创建进度条
        bar = tqdm(total=len(fs), desc=f'需转换的ts文件数：{len(fs)}')
        for f in fs:
            tmp = os.path.join(download_ts, f)
            if os.path.isfile(tmp):
               ret2 = ts2MP4(tmp, mp4FileName)
               if not ret2:
                  logger.error("ts2MP4 fail, filename:", tmp)
                  continue

            elif os.path.isdir(tmp):
               func(tmp) # 递归去获取
            else:
               logger.warning('其他情况')
               
        mp4f.close()    
        bar.close()
        
        #清除临时的TS文件
        os.chdir(download_ts)
        os.system('del /Q *.ts')
        
        logger.warning('转换结束')


    #解析超链接打开页面后的子超链接
    def parseSubUrls(self, url):
  
        logger.warning(f'需要预解析URL：{url}')
        req = urllib.request.Request(url, headers = headers)
        webpage = urllib.request.urlopen(req)
        html = webpage.read()
        soup = BeautifulSoup(html, 'html.parser')   #文档对象
        invalidLink1='#'
        invalidLink2='javascript:void(0)'
        # 集合
        resultM3u8 = set()
        resultMp4 = set()
        # 计数器
        mycount=0
        #查找文档中所有a标签
        for k in soup.find_all('a'):
            #print(k)
            #查找href标签
            link=k.get('href')
            # 过滤没找到的
            if(link is not None):
                  #过滤非法链接
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
                       resultMp4.add(url)
                       
        # 这个是51吃瓜网的视频解析               
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
                     
        logger.warning('预解析结束')

        return resultM3u8, resultMp4

    
    def download1By1(self, url, mp4Name):
        
        all_content = requests.get(url, headers = headers).text  # 获取第一层M3U8文件内容
        m3u8File = download_path + "\site.m3u8"
        
        logger.warning(f'm3u8文件的保存路径： {m3u8File}')
        
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
                logger.warning("Decode Method：", method)
                
                if not self.key:
                   uri_pos = line.find("URI")
                   quotation_mark_pos = line.rfind('"')
                   key_path = line[uri_pos:quotation_mark_pos].split('"')[1]
                   key_url = key_path # 拼出key解密密钥URL
                   
                   res = requests.get(key_url)
                   self.key = res.content
                logger.warning(f'ts文件的加密 key:{self.key}')
                
            if "#" not in line and 'http' in line: # 找ts地址并下载
                unknow = False
                pd_url = line # 拼出ts片段的URL
                allTsFiles.append(pd_url)
                
        if unknow:
            logger.error('未来找到对于的TS文件URL，程序异常')
            raise BaseException("未找到对应的TS文件URL")
        else:
            logger.warning("ts文件的URL解析完成")
        
        #多线程下载TS files
        self.downloadTsFiles(allTsFiles, 3)
        
        #把 TS files 合并为一个mp4文件
        self.mergeTs2MP4(mp4Name)

     
    def downLoadStart(self, url, mp4Name):
        #创建下载路径等准备
        self.init()

        m3u8Ulrs = set()
        mp4Urls = set()
        if '.m3u8' in url:
           print(f'原始URL只含一个视频文件{url}')
           self.download1By1(url, f'{mp4Name}')
        else:
           m3u8Ulrs, mp4Urls = self.parseSubUrls(url)        
           if len(m3u8Ulrs) == 0 and len(mp4Urls) == 0:
             print(f'url{url},无法解析出 m3u8链接或者mp4链接')
             return
            
        print(f'the url:{url}，共含m3u8文件{len(m3u8Ulrs)}, mp4的文件个数{len(mp4Urls)}')
        #串行一一下载
        count = 0
        for url in m3u8Ulrs:
            count = count + 1
            self.download1By1(url, f'{mp4Name}_{count}')
    
    def merge_file(self, tsPath):
        os.chdir(tsPath)
        cmd = "copy /b * new.tmp"
        os.system(cmd)
        os.system('del /Q *.ts')
        os.system('del /Q *.mp4')
        os.rename("new.tmp", "new.mp4")

'''
if __name__ == '__main__': 

    start = time.time()
    downLoad = VedioDownLoadProces()
    url = "https://better.ccgg6.com/archives/19830/" 
    tsProcess.downLoadStart(url, "永赢基金-蔺抒涵")
    
    end = time.time()
    
    totalCost = (end - start) / 60
    
    print(f'线程数目:{default_thread_cnt}-总耗时:%.1f 分钟' % totalCost )
    
    #merge_file("E:\\sourcecode\\download\\20230114_212551\\tsfile")
'''
