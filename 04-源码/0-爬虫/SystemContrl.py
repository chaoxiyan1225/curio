#coding=utf8
import sys, os
import requests, json
import urllib.request
import ssl
import base64 
from Crypto.Cipher import AES
from io import BytesIO
from zipfile import ZipFile
import AesTool
import time
import SystemConf
import Errors


def ParseJsonToObj(parseData, yourCls):
    result = yourCls()
    result.__dict__ = parseData
    return result

class SofeWareInfo:
   def __init__(self, name = '', currentVersion = '', publishDate = '', isFree = 'False', isDemo = 'False', toatalSize = 0, author = '', clientEnable = 'False'):
      self.name = name
      self.currentVersion = currentVersion
      self.isFree = isFree
      self.isDemo = isDemo
      self.toatalSize = toatalSize
      self.author = author
      self.clientEnable = clientEnable

class SoftWareContrl:

   def loadSoftWareInfoFromGit(self,  softwareConf = SystemConf.softwareConf, projectZip = SystemConf.projectZip):

       try:
          ssl._create_default_https_context = ssl._create_unverified_context
          headers={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
          req = urllib.request.Request(SystemConf.projectZip,headers=headers)
          
          #print(f'print headers {headers}')
          userRead = urllib.request.urlopen(req)
          data = userRead.read()
          #print(f'data : {data}')
          zipFile = ZipFile(BytesIO(data))
          files = zipFile.namelist()         
          if not len(files):
             print(f'down load conf error! contack QQ :{SystemConf.contackQQ} or  {SystemConf.email} ')
             status = ""
             return None, Errors.S_InvalidFileContent
          softwareConfFile = None
          
          for file in files:
              if SystemConf.softwareConf in file:
                 softwareConfFile = file
                 break     
          #print(f'the fils : {files}')

          with zipFile.open(softwareConfFile, 'r') as tmpFile:
             jsonData = tmpFile.read()
             if not jsonData:
                print(f'the conf has no data.exit! , contack QQ :{SystemConf.contackQQ} or  {SystemConf.email} ')
                return None, Errors.S_InvalidFileContent

             softwareJson = json.loads(jsonData.decode().strip('\t\n'))
             if not softwareJson:
                print(f'software conf load error, contack QQ :{SystemConf.contackQQ} or  {SystemConf.email} ')     
                return None, Errors.S_InvalidFileContent
             softwareInfo = ParseJsonToObj(softwareJson, SofeWareInfo)

             return softwareInfo, Errors.SUCCESS
          return None, Errors.S_ParseFail
       except Exception as e:
             print(f'parse software fail , exception : {str(e)} and contack QQ :{SystemConf.contackQQ} or  {SystemConf.email} ')
             return None, Errors.S_ParseFail

   '''
     加载软件的一些基本信息使用软件的有效期限
   '''
   def clientValid(self):
      softWareConf, error = self.loadSoftWareInfoFromGit()
      if not softWareConf or error != Errors.SUCCESS:
         return False, error

      if softWareConf.clientEnable.lower() == 'false':
         return False, Errors.S_Forbidden

      if SystemConf.clientVersion <= softWareConf.currentVersion:
         print(f'the client verion is too low, client:{SystemConf.clientVersion}. and server version: {softWareConf.currentVersion}')
         return  False, Errors.C_VersionTooLow
      

      return True, Errors.SUCCESS
      


ctrl = SoftWareContrl()
ret, error = ctrl.clientValid()
print(f'the ret {ret}, and the message {error.getMessage()}')
