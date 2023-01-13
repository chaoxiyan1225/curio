#coding=utf8
import sys, os
import requests, json
import urllib.request


from Crypto.Cipher import AES #使用的是 pip install pycryptodome

BLOCK_SIZE = 256 * 1024

def downLoadTs(siteFile, downloadPath, namePrefix):
    with open(siteFile, "r") as f:        
        count = 0 
        for line in f:
            if line.startswith("#"):
               continue

            line = line.strip()
            url = line 
            count = count + 1 
            tsDownload = None
            try:
                tsDownload = urllib.request.urlopen(url)
                with open(downloadPath + "/" + namePrefix + "-"+ count + ".ts", "wb") as tsFile:
                     #通过buffer控制每次读取的大小，防止内存爆掉
                     while True:
                          buffer = tsDownload.read(BLOCK_SIZE)
                          if not buffer:
                              # There is nothing more to read
                             break
                          tsFiles.write(buffer)
            except:
                print("down load error, url:", url, "status:", tsDownload)
                return False
        return True

      
def ts2MP4(tsPath, mp4Path):
   if tsPath == '' or  mp4path == '':
      return False  

   with open(mp4Path + ".mp4", "wb") as mp4f:
       with open(tsPath, "r") as tsf:
            mp4f.write(tsf)
   
   return True

def tsProcess(siteFile, downloadPath, namePrefix):
    newPath = downloadPath + "/" + namePrefix
    if not os.path.isdir(newPath):
       os.makedirs(newPath)

    ret = downLoadTs(siteFile, newPath, namePrefix)
    if not ret:
       return

    fs = os.listdir(downloadPath)
    for f in fs:
        tmp = os.path.join(downloadPath, f)
        if os.path.isfile(tmp):
           ret2 = ts2MP4(tmp, downloadPath + namePrefix)
           if not ret2:
              print("ts2MP4 fail, filename:", tmp)
              continue

        elif os.path.isdir(tmp):
           func(tmp) # 递归去获取
        else:
           print('其他情况')

if __name__ == '__main__':
   
   path = "/Users/chaoxi.ycx/ycx_work/sourecode/maotai"
   siteFile = "/Users/chaoxi.ycx/ycx_work/sourecode/maotai/视频链接地址.m3u8"   
   tsProcess(siteFile, path, "视频")
