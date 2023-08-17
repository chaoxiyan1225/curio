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
class  VedioDownLoadProcesser:

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
    初始化函数，创建临时路径等
    '''
    def init(self, savePath):

        self.downSuccess = 0
        self.downTotal = 0
        logger.warn(f'------初始化系统配置：start-----------')
        
        if savePath != None and savePath != "":
           self.download_path = savePath.replace("/", "\\")
        
        else:
           self.download_path = os.getcwd()
        
        #新建日期文件夹
        addPath = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.download_path = os.path.join(self.download_path, addPath)
        #logger.warning self.download_path
        os.mkdir(self.download_path)
        
        
        self.download_ts = os.path.join(self.download_path, "tsfile")
        os.mkdir(self.download_ts)
        logger.warn(f'------初始化系统配置：end-----------')

    class Mp4DownLoader:

        def __init__(self, vedioDownLoader):
            self.vedioDownLoader = vedioDownLoader
            self.vedioDownLoader.lock.acquire()
            self.vedioDownLoader.downSuccess = 0
            self.vedioDownLoader.downTotal = 0
            self.vedioDownLoader.lock.release()

        def split(self, start: int, end: int, step: int) -> list[tuple[int, int]]:
            parts = [(start, min(start+step, end))
                     for start in range(0, end, step)]
            self.vedioDownLoader.lock.acquire()
            self.vedioDownLoader.downTotal = len(parts)
            self.vedioDownLoader.lock.release()
            return parts

        def get_file_size(self, url: str, raise_error: bool = False) -> int:
            response = requests.head(url)
            file_size = response.headers.get('Content-Length')
            if file_size is None:
                if raise_error is True:
                    raise ValueError('该文件不支持多线程分段下载！')
                return file_size
            return int(file_size)

        def download(self, url: str, file_name: str, retry_times: int = 3, each_size=16*MB) -> None:
            mp4Name = os.path.join(self.download_path, file_name + ".mp4")
            f = open(mp4Name, 'ab')
            file_size = self.get_file_size(url)

            @retry(tries=retry_times)
            @multitasking.task
            def start_download(start: int, end: int) -> None:
                _headers = headers.copy()
                _headers['Range'] = f'bytes={start}-{end}'
                response = session.get(url, headers=_headers, stream=True)
                chunk_size = 128
        
                chunks = []
                for chunk in response.iter_content(chunk_size=chunk_size):
                    chunks.append(chunk)
                    ##bar.update(chunk_size)
                    self.vedioDownLoader.lock.acquire()
                    self.vedioDownLoader.downSuccess = self.vedioDownLoader.downSuccess + 1
                    self.vedioDownLoader.lock.release()

                f.seek(start)
                for chunk in chunks:
                    f.write(chunk)
            
                del chunks

            session = requests.Session()
            each_size = min(each_size, file_size)
            parts = self.split(0, file_size, each_size)
            logger.warn(f'分块数：{len(parts)}')
         
            ##bar = tqdm(total=file_size, desc=f'下载文件：{file_name}')
            for part in parts:
                start, end = part
                start_download(start, end)
          
            multitasking.wait_for_tasks()
            f.close()
            ##bar.close()

    def get_percent_current(self):
        fenMu = 1000000 if self.downTotal==0 else self.downTotal
        return int((self.downSuccess * 100) / fenMu)
  
    def get_metric(self):
        self.metricInfo.percentCurrent = self.get_percent_current()
        return self.metricInfo    

    '''
    按线程数和下载列表去划分任务到多个线程中      
    '''
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
            '''
            response = requests.head(url)
            file_size = response.headers.get('Content-Length')
            if file_size is None:
               if raise_error is True:
                   raise ValueError('该文件不支持多线程分段下载！')
               totalFileSize = totalFileSize +file_size
            '''
        #logger.warn(f'taskList: {taskList}')
            
        return useThreadCnt, len(urlList),taskList
        
    #多线程方式去下载TS文件
    def download_tsFiles(self, urlList: list, retry_times: int = 3) -> None:

        logger.warn(f'一共待下载的ts文件数：{len(urlList)}')
        self.downTotal = len(urlList)
        
        start = time.time()
        #先把任务分组
        useThreadCnt, totalFileCnt, taskList = self.map_download_task(urlList)

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
                
                tsName = os.path.join(self.download_ts, str(index) + ".ts")
                with open(tsName, 'ab') as tsFile:
                       #f.write(cryptor.decrypt(res.content))
                    while True:
                        buffer = urlfile.read(BLOCK_SIZE)
                        if not buffer:
                           # There is nothing more to read
                           break
                           
                        encrypted_data_len = len(buffer)
                        if encrypted_data_len % 16 != 0:
                            # print(encrypted_data_len)
                            # 变为16的倍数
                            buffer = pad(buffer, 16)
                        
                        content = buffer if cryptor == None else cryptor.decrypt(buffer)
                        tsFile.write(content)
                        tsFile.flush()
                    ##bar.update(1)
                    self.lock.acquire()
                    self.downSuccess = self.downSuccess + 1
                    self.lock.release()
                    tsFile.close()
            
        ##bar = tqdm(total=totalFileCnt, desc=f'下载文件总数：{len(urlList)}')
        multitasking.set_max_threads(useThreadCnt)
        
        for urlMap in taskList:
            start_download(urlMap)
        multitasking.wait_for_tasks()
        ##bar.close()
        
        totalCost = (time.time() - start) / 60
        logger.warn(f'下载任务结束，总计下载耗时:%.1f 分钟' % totalCost)

    def parse_subUrls(self, url):
  
        logger.warn(f'需要预解析URL：{url}')
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
            #logger.warn(k)
            #查找href标签
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
                    resultMp4.add(url)
                       
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
                     
        logger.warn('预解析结束')
        return resultM3u8, resultMp4


    # 如果是Mp4格式的视频，可能要切分片去下载
    def mp4_download_1By1(self, url, mp4FileName):
        mp4Down = self.Mp4DownLoader(self)
        mp4Down.download(url, mp4FileName)

    
    def ts_download_1By1(self, url, mp4Name):
        
        all_content = requests.get(url, headers = headers).text  # 获取第一层M3U8文件内容
        m3u8File = self.download_path + "\site.m3u8"
        logger.warn(f'm3u8save pth： {m3u8File}')
        
        with open(m3u8File, "wb") as file:
             file.write(all_content.encode())
        
        if "#EXTM3U" not in all_content:   
            raise BaseException("非M3U8的链接")
     
        logger.warn(f'start decode ts files')
        unknow = True
        all_line = all_content.split("\n") 
        allTsFiles = []
        for index, line in enumerate(all_line): # 第二层
            if "#EXT-X-KEY" in line:  # 找解密Key
                method_pos = line.find("METHOD")
                comma_pos = line.find(",")
                method = line[method_pos:comma_pos].split('=')[1]
                logger.warn(f"Decode Method：{method}")

                if not self.key:
                   uri_pos = line.find("URI")
                   quotation_mark_pos = line.rfind('"')
                   key_path = line[uri_pos:quotation_mark_pos].split('"')[1]
                   key_url = key_path # 拼出key解密密钥URL
                  
                   res = requests.get(key_url)
                   self.key = res.content
                   
                logger.warn(f'ts文件的加密 key:{self.key}')
                
            if "#" not in line and 'http' in line: # 找ts地址并下载
                unknow = False
                pd_url = line # 拼出ts片段的URL
                allTsFiles.append(pd_url)

        if unknow:
            logger.error('未来找到对于的TS文件URL，程序异常')
            raise BaseException("未找到对应的TS文件URL")
        else:
            logger.warn("ts文件的URL解析完成")
        
        #多线程下载TS files
        self.download_tsFiles(allTsFiles, 3)
        
        #把 TS files 合并为一个mp4文件
        self.merge_ts_2_mp4(mp4Name)
         
    
    def merge_file(self, tsPath):
        os.chdir(tsPath)
        cmd = "copy /b * new.tmp"
        os.system(cmd)
        os.system('del /Q *.ts')
        os.system('del /Q *.mp4')
        os.rename("new.tmp", "new.mp4")
        
    def merge_ts_2_mp4(self, mp4FileName:str)->None:

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
                ##bar.update(1)#更新进度条
               
            return True
            
        #列举所有的ts文件，按文件标号排序，非字典序
        fs = os.listdir(self.download_ts)
        fs.sort(key= lambda x:int(x[:-3]))
        
        logger.warn(f'开始转为mp4，待转换TS文件数量：{len(fs)}')
        
        mp4Name = os.path.join(self.download_path, mp4FileName + ".mp4")
        mp4f = open(mp4Name, "ab")
        
        # 创建进度条
        ##bar = tqdm(total=len(fs), desc=f'需转换的ts文件数：{len(fs)}')
        for f in fs:
            tmp = os.path.join(self.download_ts, f)
            if os.path.isfile(tmp):
               ret2 = ts2MP4(tmp, mp4FileName)
               if not ret2:
                  logger.error("ts2MP4 fail, filename:", tmp)
                  continue
            else:
               logger.warn('其他情况')
               
        mp4f.close()
        ##bar.close()
        os.chdir(self.download_ts)
        os.system('del /Q *.ts')
        
        logger.warn('转换结束')
        time.sleep(4)
        
        father = os.path.join(self.download_ts, os.pardir)
        os.chdir(father)
        os.system('del /Q *.m3u8')
        
    def clear_file(self):
        #os.rmdir(self.download_ts)
        shutil.rmtree(self.download_ts)
        os.chdir(os.path.join(father, os.pardir))
       

    def parse_all_vedios(self, urls):
        logger.warn(f'the input urls:{urls}')
        for u in urls:
            url = u.strip()
            
            if url == None or url == "" or "http" not in url:
               continue
            
            if '.m3u8' in url:
                logger.warn(f'原始URL只含一个视频文件{url}')
                self.m3u8Ulrs.add(url)
            elif '.mp4' in url:
                logger.warn(f'原始URL只含一个mp4视频文件{url}')
                self.mp4Urls.add(url)
            else:
                logger.warn(f'需要解析含有的视频信息')
                m3u8Tmps, mp4Tmps = self.parse_subUrls(url)        
                if len(m3u8Tmps) == 0 and len(mp4Tmps) == 0:
                    logger.warn(f'url{url},无法解析出 m3u8链接或者mp4链接')
                    return
                
                for url in m3u8Tmps:
                    self.m3u8Ulrs.add(url)
                    
                for url in mp4Tmps:
                    self.mp4Urls.add(url)

    def downLoad_start(self, urls, savePath, mp4Name = None):
        self.init(savePath)
        self.downSuccess = 0 # to single vedio
        self.downTotal = 0   # to single vedio
        self.name = mp4Name if mp4Name != None else "随机名" 
        self.m3u8Ulrs = set()  # total vedios
        self.mp4Urls = set()   # total vedios
        # first parse all vedio url
        self.parse_all_vedios(urls)
        self.metricInfo.totalVedioCnt = len(self.m3u8Ulrs) + len(self.mp4Urls)
           
        logger.warn(f'the url:{urls},共含m3u8文件{len(self.m3u8Ulrs)}, mp4的文件个数{len(self.mp4Urls)}')
        
        count = 0
        for m3u8Url in self.m3u8Ulrs:
            self.downSuccess = 0
            self.downTotal = 0
            count = count + 1
            self.ts_download_1By1(m3u8Url, f'{self.name}_{count}')
            
            if self.downSuccess != self.downTotal:
               self.metricInfo.failVedioCnt = self.metricInfo.failVedioCnt + 1 
            else:
               self.metricInfo.successVedioCnt = self.metricInfo.successVedioCnt + 1

        for mp4Url in self.mp4Urls:
            self.downSuccess = 0 
            self.downTotal = 0
            count = count + 1
            self.mp4_download_1By1(mp4Url, f'{self.name}_{count}')   

            if self.downSuccess != self.downTotal:
               self.metricInfo.failVedioCnt = self.metricInfo.failVedioCnt + 1
            else:
               self.metricInfo.successVedioCnt = self.metricInfo.successVedioCnt + 1
               
        

if __name__ == '__main__': 

    logger.warn(f'start----download')
    start = time.time()
    downLoad = VedioDownLoadProcesser()
    url = "https://cgcg1.com/archives/60127/" 
    downLoad.downLoad_start(url, "wewewewe")
    
    end = time.time()
    
    totalCost = (end - start) / 60
    
    logger.warn(f'线程数目:{default_thread_cnt}-总耗时:%.1f 分钟' % totalCost )
    
    #merge_file("E:\\sourcecode\\download\\20230114_212551\\tsfile")
