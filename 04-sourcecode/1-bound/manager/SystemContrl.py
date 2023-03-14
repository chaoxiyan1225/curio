#coding=utf8
import sys, os
import requests, json
import urllib.request
import ssl
import base64 
from Crypto.Cipher import AES
from io import BytesIO

from zipfile import ZipFile
#import AesTool
import time
import config.SystemConf
import config.Errors
import utils.logger

logger = utils.logger
SystemConf = config.SystemConf
Errors = config.Errors
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
      self.versionsForbidden = []

   def toString(self):
      s = json.dumps(self.__dict__) 
      return s

class SoftWareContrl:

   def loadSoftWareInfoFromGit(self,  softwareConf = config.SystemConf.softwareConf, projectZip = config.SystemConf.projectZip):
       return self.loadJsonConfFromGit(softwareConf, projectZip, SofeWareInfo)

   def loadJsonConfFromGit(self, confFileName, gitZipFileName, jsonObject = None):

       try:
          ssl._create_default_https_context = ssl._create_unverified_context
          headers={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
          req = urllib.request.Request(gitZipFileName,headers=headers)
          
          #print(f'print headers {headers}')
          userRead = urllib.request.urlopen(req, timeout=15)
          data = userRead.read()
          #print(f'data : {data}')
          zipFile = ZipFile(BytesIO(data))
          files = zipFile.namelist()         
          if not len(files):
             logger.error(f'down load conf error! contack QQ :{SystemConf.contackQQ} or  {SystemConf.email} ')
             status = ""
             return None, Errors.S_InvalidFileContent
          confFile = None
          
          for file in files:
              if confFileName in file:
                 confFile = file
                 break     
          #print(f'the fils : {files}')

          with zipFile.open(confFile, 'r') as tmpFile:
             jsonData = tmpFile.read()
             if not jsonData:
                logger.error(f'the conf has no data.exit! , contack QQ :{SystemConf.contackQQ} or  {SystemConf.email} ')
                return None, Errors.S_InvalidFileContent

             confJson = json.loads(jsonData.decode().strip('\t\n'))
             if not confJson:
                logger.error(f'software conf load error, contack QQ :{SystemConf.contackQQ} or  {SystemConf.email} ')     
                return None, Errors.S_InvalidFileContent

             if jsonObject:
                jsonObject = ParseJsonToObj(confJson, jsonObject)
                return jsonObject, Errors.SUCCESS
             else:
                return confJson, Errors.SUCCESS
             
          return None, Errors.S_ParseFail
       except Exception as e:
             logger.error(f'parse software fail , exception : {str(e)} and contack QQ :{SystemConf.contackQQ} or  {SystemConf.email} ')
             return None, Errors.S_ParseFail

   '''
     加载软件的一些基本信息使用软件的有效期限
   '''
   def clientValid(self):
      softWareConf, error = self.loadSoftWareInfoFromGit()
      if not softWareConf or error != Errors.SUCCESS:
         logger.error('load conf from github fail')
         return error
      
      if softWareConf.isFree.lower() == 'true':
         logger.warning('the software isFree to use')
         return  Errors.S_ClientFreeUse

      if softWareConf.clientEnable.lower() == 'false':
         logger.error('all client cannot run, see software.conf for more info')
         return Errors.S_Forbidden

      if SystemConf.clientVersion in softWareConf.versionsForbidden:
         logger.error(f'the client verion not alow, client:{SystemConf.clientVersion}. and server version see software.conf')
         return Errors.C_VersionTooLow
      
      logger.warning('the client valid success')
      return Errors.SUCCESS
