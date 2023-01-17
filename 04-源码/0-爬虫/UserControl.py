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

class UserInfo:
   def __init__(self, name = '', passwd = '', userId = '', isFree = False, start = '', end = '', isActive = False):
      self.name = name
      self.passwd = passwd
      self.isFree = isFree
      self.start = start
      self.end = end
      self.userId = userId
      self.isActive = isActive

class UserContrl:
   
   '''
     根据用户的登陆信息判断是否合法，包括使用软件的有效期限
   '''
   def CheckUserValid(self, userConf, userLogin):
      if not UserInfo or not userLogin:
         print(f'the userLogin is none or userConf is InValid.')
         return  False, Errors.C_LoginFail
      
      if userConf.name != userLogin.name or userConf.passwd != userLogin.passwd:
         return False, Errors.C_ErrorPasswdOrName
      
      nowStr = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))

      if userConf.isFree.lower() == 'false' and not ( nowStr <= userConf.end and userConf.start <= nowStr ):
         return False, Errors.C_Arrearage

      return True, Errors.SUCCESS


      
   def getUserConfFromGit(self, userId :str, projectZip = SystemConf.projectZip):
       
       status = ""
       try:
          ssl._create_default_https_context = ssl._create_unverified_context
          headers={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
          req = urllib.request.Request(SystemConf.projectZip, headers=headers)
          
          #print(f'print headers {headers}')
          userRead = urllib.request.urlopen(req)
          data = userRead.read()
          #print(f'data : {data}')
          zipFile = ZipFile(BytesIO(data))
          files = zipFile.namelist()         
          if not len(files):
             print(f'down load conf error!')

             status = ""
             return None, Errors.S_DownLoadError
          userConfFile = None
          
          for file in files:
              if SystemConf.userConf in file:
                 userConfFile = file
                 break     
     
          with zipFile.open(userConfFile, 'r') as userFile:
             jsonData = userFile.read()
             if not jsonData:
                print(f'the conf has no data.exit!')
                return None, Errors.S_InvalidFileContent
             
             parseData = json.loads(jsonData.decode().strip('\t\n'))
             userInfoJson = parseData[userId]
             if not userInfoJson:
                print(f'the user not register, contack XXX ') 
                return None, Errors.C_InvalidUser    
             
             userInfo = ParseJsonToObj(userInfoJson, UserInfo)
             return userInfo
          return None
       except Exception as e:
             print("parse userInfo fail ",  str(e))
             return None, Errors.S_ParseFail



userContrl = UserContrl()
userConf = userContrl.getUserConfFromGit("vip000001")
#userContrl.printSome("dddffd")
print(userConf.name)


userLogin = UserInfo("ycx", "123456", "vip000001")
ret,error = userContrl.CheckUserValid(userConf, userLogin)
print(f'the ret {ret}, and the meesage {error.getMessage()}')


