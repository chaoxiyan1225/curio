# -*- coding:utf-8 -*-  
import os, sys, time, signal, datetime
import requests, urllib3, json
from Crypto.Cipher import AES #使用的是 pip install pycryptodome
from binascii import b2a_hex, a2b_hex
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm # 用于显示进度条
import multitasking, threading # 用于多线程操作
from retry import retry# 导入 retry 库以方便进行下载出错重试
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth


from utils.logger import *
import utils.commontool as CommonTool
import shutil

from service.common_downloader import *
signal.signal(signal.SIGINT, multitasking.killall)
from Crypto.Util.Padding import pad
#import pycurl

http = urllib3.PoolManager(block=True)

#reload(sys)
#sys.setdefaultencoding('utf-8')

class  MP4TSDownloader(CommonDownloader):

    def __init__(self, savePath, url, vedioName=None, threadCnt = default_thread_cnt, blockSize = BLOCK_SIZE):
         super(MP4TSDownloader, self).__init__(savePath, url, vedioName, threadCnt, blockSize)

    def init(self):

        logger.warning(f'------init start-----------')
        self.m3u8Urls = set()  # total vedios
        self.mp4Urls = set()   # total vedios
        
        nameTitle, m3u8s, mp4s = self.gen_vedioInfos_v1()
        for url in m3u8s:
            self.m3u8Urls.add(url)
            
        for url in mp4s:
            self.mp4Urls.add(url)
        
        
        if self.vedioName == None:
           self.vedioName = nameTitle
        logger.warning(f'------init mp4 ts end-----------')


    def get_percent_current(self):
        fenMu = 1000000 if self.downTotal==0 else self.downTotal
        #self.downSuccess = self.curlDownloader.getinfo(self.curlDownloader.SIZE_DOWNLOAD)  #下载数据包的大小
        return int((self.downSuccess * 100) / fenMu)
  
    def get_metric(self):
        self.metricInfo.percentCurrent = self.get_percent_current() if self.get_percent_current() > 0 else 1
        return self.metricInfo    


    class Mp4DownLoader:

        def __init__(self, vedioDownLoader, savePath):
            self.vedioDownLoader = vedioDownLoader
            self.vedioDownLoader.lock.acquire()
            self.vedioDownLoader.downSuccess = 0
            self.vedioDownLoader.downTotal = 0
            self.vedioDownLoader.lock.release()
            self.download_path = savePath
            #self.curlDownloader = None

        def split(self, start: int, end: int, step: int) -> list[tuple[int, int]]:
            parts = [(start, min(start+step-1, end-1))
                     for start in range(0, end, step)]
            self.vedioDownLoader.lock.acquire()
            self.vedioDownLoader.downTotal = len(parts)
            self.vedioDownLoader.lock.release()
            return parts

        def get_file_size(self, url: str, raise_error: bool = False) -> int:
        
            logger.warning(f'the vedio url {url}')
            response = requests.head(url,auth=HTTPBasicAuth("youporntbag", "ycx/8520/8520-+"))
            logger.warning(f'the response:{response.text}')
            file_size = response.headers.get('Content-Length')
            if file_size is None:
                if raise_error is True:
                    raise ValueError('该文件不支持多线程分段下载！')
                return file_size
            return int(file_size)
       
        def download(self, url: str, file_name: str, retry_times: int = 3, each_size=2*MB):
            mp4Name = os.path.join(self.download_path, file_name + ".mp4")
            f = open(mp4Name, 'ab')
            file_size = self.get_file_size(url)
            
            if file_size < 1*MB:
                logger.warning(f'the url:{url} may be ads vedio size :{file_size}')
                return "adsVedio"
            
            logger.warning(f'the file_size:{file_size}')

            @retry(tries=retry_times)
            @multitasking.task
            def start_download(start: int, end: int) -> None:
                _headers = headers.copy()
                _headers['Range'] = f'bytes={start}-{end}'
                logger.info(f'download bytes={start}-{end} start')
                response = http.request("GET", url, headers=_headers)
                
                f.seek(start)
                f.write(response.data)
                
                logger.info(f'download bytes={start}-{end} success')
                
                self.vedioDownLoader.lock.acquire()
                self.vedioDownLoader.downSuccess = self.vedioDownLoader.downSuccess + end - start + 1
                self.vedioDownLoader.lock.release()
               

                '''
                chunk_size = 128
        
                chunks = []
                for chunk in response.iter_content(chunk_size=chunk_size):
                    chunks.append(chunk)
                    ##bar.update(chunk_size)
                    self.vedioDownLoader.lock.acquire()
                    self.vedioDownLoader.downSuccess = self.vedioDownLoader.downSuccess + chunk_size
                    self.vedioDownLoader.lock.release()

                f.seek(start)
                for chunk in chunks:
                    f.write(chunk)
            
                del chunks
                '''

            session = requests.Session()
            each_size = min(each_size, file_size)
            parts = self.split(0, file_size, each_size)
            logger.warning(f'共切分数：{len(parts)}, {parts}')
            
            self.vedioDownLoader.downTotal = file_size
         
            ##bar = tqdm(total=file_size, desc=f'下载文件：{file_name}')
            for part in parts:
                start, end = part
                start_download(start, end)
          
            multitasking.wait_for_tasks()
            f.close()
            
            return "success"
            ##bar.close()

    def download_tsFiles(self, urlList: list, retry_times: int = 3) -> None:

        logger.warning(f'一共待下载的ts文件数：{len(urlList)}')
        self.downTotal = len(urlList)
       
        start = time.time()
        #先把任务分组
        useThreadCnt, totalFileCnt, taskList = self.map_download_task(urlList)

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
        logger.warning(f'下载任务结束，总计下载耗时:%.1f 分钟' % totalCost)


    def mp4_download_1By1(self, url, mp4FileName):
        mp4Down = self.Mp4DownLoader(self, self.download_path)
        return mp4Down.download(url, mp4FileName)

    
    def ts_download_1By1(self, url, mp4Name):
    
        addPath = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                
        self.download_ts = os.path.join(self.download_path, f"tsfile_{addPath}")
        os.mkdir(self.download_ts)
        
        all_content = requests.get(url, headers = headers).text
        
        
        father = os.path.join(self.download_ts, os.pardir)
        m3u8File = father+ f"\site.m3u8" 
        
        logger.warning(f'm3u8save path: {m3u8File}')
        
        with open(m3u8File, "wb") as file:
             file.write(all_content.encode())
        
        if "#EXTM3U" not in all_content:   
            raise BaseException("非M3U8的链接")
     
        logger.warning(f'start decode ts files')
        unknow = True
        all_line = all_content.split("\n") 
        allTsFiles = []
        for index, line in enumerate(all_line): # 第二层
            if "#EXT-X-KEY" in line:  # 找解密Key
                method_pos = line.find("METHOD")
                comma_pos = line.find(",")
                method = line[method_pos:comma_pos].split('=')[1]
                logger.warning(f"Decode Method：{method}")

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
            logger.error('not find ts ，程序异常')

        else:
            logger.warning("ts文件的URL解析完成")
        
        #mutilthread TS files
        self.download_tsFiles(allTsFiles, 3)
        
        #把 TS files 合并为一个mp4文件
        if len(allTsFiles) > 0:
           self.merge_ts_2_mp4(mp4Name)
         
        
    def merge_ts_2_mp4(self, mp4FileName:str)->None:
        def ts2MP4(tsPath:str, mp4FileName:str)->bool:
            if not tsPath or not mp4FileName:
                return False  

            with open(tsPath, "rb") as tsf:
                mp4f.write(tsf.read())
                ##bar.update(1)#更新进度条
               
            return True
            
        
        fs = os.listdir(self.download_ts)
        fs.sort(key= lambda x:int(x[:-3]))
        
        logger.warning(f'compaction to mp4，TS cnt：{len(fs)}')
        
        mp4Name = os.path.join(self.download_path, mp4FileName + ".mp4")
        mp4f = open(mp4Name, "ab")
        
        ##bar = tqdm(total=len(fs), desc=f'需转换的ts文件数：{len(fs)}')
        for f in fs:
            tmp = os.path.join(self.download_ts, f)
            if os.path.isfile(tmp):
               ret2 = ts2MP4(tmp, mp4FileName)
               if not ret2:
                  logger.error("ts2MP4 fail, filename:", tmp)
                  continue
            else:
               logger.warning('other error')
               
        mp4f.close()
        ##bar.close()
        os.chdir(self.download_ts)
        os.system('del /Q *.ts')
        
        logger.warning('compaction to mp4 finished')
        time.sleep(4)
        
        father = os.path.join(self.download_ts, os.pardir)
        os.chdir(father)
        os.system('del /Q *.m3u8')
        
        
    def clear(self):
        #os.rmdir(self.download_ts)
        shutil.rmtree(self.download_ts)
        os.chdir(os.path.join(os.path.join(self.download_ts, os.pardir), os.pardir))
       
    def parse_all_vedios(self, url):
        logger.warning(f'the input urls:{url}')

        url = url.strip()
        if url == None or url == "" or "http" not in url:
            return 
        
        if '.m3u8' in url:
            logger.warning(f'input:{url} only one m3u8 file')
            self.m3u8Urls.add(url)
        elif '.mp4' in url:
            logger.warning(f'input:{url} only one mp4 file')
            self.mp4Urls.add(url)

    def downLoad_start(self):
        self.init()
        self.downSuccess = 0 # to single vedio
        self.downTotal = 0   # to single vedio
        # first parse all vedio url
        self.parse_all_vedios(self.url)
        self.metricInfo.totalVedioCnt = len(self.m3u8Urls) + len(self.mp4Urls)
           
        logger.warning(f'the url:{self.url} m3u8 cnt:{len(self.m3u8Urls)}, mp4 cnt:{len(self.mp4Urls)}, the vedioname: {self.vedioName}')
        
        logger.debug(f'the m3u8urls:{self.m3u8Urls}')
        logger.debug(f'the mp4ulrs:{self.mp4Urls}')        
       
        count = 0
        for m3u8Url in self.m3u8Urls:
            self.downSuccess = 0
            self.downTotal = 0
            count = count + 1
            self.key = None
            self.ts_download_1By1(m3u8Url, f'{self.vedioName}_{count}')
            time.sleep(15)  
            self.clear()
            
            if self.downSuccess != self.downTotal:
               self.metricInfo.failVedioCnt = self.metricInfo.failVedioCnt + 1 
            else:
               self.metricInfo.successVedioCnt = self.metricInfo.successVedioCnt + 1

        for mp4Url in self.mp4Urls:
            self.downSuccess = 0 
            self.downTotal = 0
            count = count + 1
            result = self.mp4_download_1By1(mp4Url, f'{self.vedioName}_{count}')  
            time.sleep(15)            

            if self.downSuccess != self.downTotal:
               self.metricInfo.failVedioCnt = self.metricInfo.failVedioCnt + 1
            else: 
               if self.downTotal != 0:
                  self.metricInfo.successVedioCnt = self.metricInfo.successVedioCnt + 1

   
        return True


if __name__ == '__main__': 

    logger.warning(f'start----download')
    start = time.time()
    downLoad = MP4TSDownloader()
    url = "https://cgcg1.com/archives/60127/" 
    downLoad.downLoad_start(url, "wewewewe")
    
    end = time.time()
    
    totalCost = (end - start) / 60
    
    logger.warning(f'线程数目:{default_thread_cnt}-总耗时:%.1f 分钟' % totalCost )
    
    #merge_file("E:\\sourcecode\\download\\20230114_212551\\tsfile")
    
    

