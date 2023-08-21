#coding=utf8
import sys, os
import requests, json
import urllib.request
import ssl
import base64 
from Crypto.Cipher import AES
from io import BytesIO
from zipfile import ZipFile
import utils.commontool as CommonTool
import time
import conf.systemconf as SystemConf
import conf.errors as Errors

import utils.logger as  logger

def ParseJsonToObj(parseData, yourCls):
    result = yourCls()
    result.__dict__ = parseData
    return result

class UserInfo:
   def __init__(self, name = '', passwd = '', email = '', tel = '', 
      isFree = False, start = '', end = '', isActive = False):

      self.name = name
      self.passwd = passwd
      self.isFree = isFree
      self.start = start
      self.end = end
      self.email = email
      self.isActive = isActive
      self.tel = tel

   def toString(self):
      s = json.dumps(self.__dict__) 
      return s

class UserContrl:
   
   '''
     根据用户的登陆信息判断是否合法，包括使用软件的有效期限
   '''
   def CheckUserValid(self, userConf, userLogin = None):
      if not userConf:
         logger.warn(f'the userConf is InValid.')
         return  False, Errors.C_LoginFail
      
      #if userConf.name != userLogin.name or userConf.passwd != userLogin.passwd:
      #   return False, Errors.C_ErrorPasswdOrName
      
      nowStr = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))

      if userConf.isFree.lower() == 'false' and not ( nowStr <= userConf.end and userConf.start <= nowStr ):
         return False, Errors.C_Arrearage

      return True, Errors.SUCCESS


   # userId 就是本机的mac地址，原则上是一个账号就对应一个mac地址
   def getUserConfFromGit(self, userId :str, projectZip = SystemConf.projectZip):
       
       try:
          data = CommonTool.get_conf_data()
          if data == None:
             return None, Errors.S_DownLoadError
          
          #logger.warn(f'data : {data}')
          zipFile = ZipFile(BytesIO(data))
          files = zipFile.namelist()         
          if not len(files):
             logger.warn(f'down load conf error!')
             return None, Errors.S_DownLoadError

          userConfFile = None
          for file in files:
              if SystemConf.userConf in file:
                 userConfFile = file
                 break     
     
          with zipFile.open(userConfFile, 'r') as userFile:
             jsonData = userFile.read()
             if not jsonData:
                logger.warn(f'the conf has no data.exit!')
                return None, Errors.S_InvalidFileContent
             
             parseData = json.loads(jsonData.decode().strip('\t\n'))
             if userId not in parseData:
                logger.warn(f'the userId{userId} 不存在')
                return None, Errors.C_InvalidUser.append(f'userId{userId} 不存在')    

             userInfoJson = parseData[userId]
             if not userInfoJson:
                logger.warn(f'the user not register, contack XXX ') 
                return None, Errors.C_InvalidUser    
             
             userInfo = ParseJsonToObj(userInfoJson, UserInfo)
             return userInfo, Errors.SUCCESS

          return None, Errors.S_UnknowError

       except Exception as e:
          logger.warn("parse userInfo fail ",  str(e))
          return None, Errors.S_ParseFail.append(f'userId:[{userId}]')

   def LoginCheck(self, passwd = ''):

      retryCnt = 3 
      macId = CommonTool.get_mac_address()
      userInfo, error = self.getUserConfFromGit(macId)
       
      if error == Errors.C_InvalidUser:
          #CommonTool.sendRegisterMsg()
          logger.warn(f'客户端:[{macId}]未注册,请先注册再使用')
          return error

      while error == Errors.S_DownLoadError and retryCnt > 0:
           retryCnt = retryCnt - 1
           userInfo, error = self.getUserConfFromGit(macId)

           if error == Errors.SUCCESS:
              break

      if error != Errors.SUCCESS or not userInfo:
         logger.warn(f'请联系技术支持:{SystemConf.contackUs}, 并附加UserId:[{macId}]')
         CommonTool.sendClientLoginFailMsg(error.toString())
         return error

      error = self.CheckUserValid(userInfo)
       #欠费了
      if error == Errors.C_Arrearage:
         #需要给界面返回欠费信息
         logger.warn(f'当前欠费，请续费，续费操作请参考:')
         return error

      logger.warn(f'登陆成功，可以使用软件, {userInfo.toString()}')
      return Errors.SUCCESS

   def clickToRegister(self, email, tel = ''):

      if not email or CommonTool.emailRight(email) == False:
         logger.warn(f'输入的邮箱不正确或者格式错误：{email}')
         return Errors.C_EmailWrong
      
      success = CommonTool.sendRegisterMsg(email, tel) 
      if not success:
         logger.warn(f'第二次发送')
         sucess = CommonTool.sendRegisterMsg(email, tel)
      
      if not success:
         return Errors.C_SendEmailFail

      return  Errors.SUCCESS

'''
ctrl = UserContrl()
result = ctrl.LoginCheck()
if result == Errors.C_InvalidUser:
   ctrl.clickToRegister('594781478@qq.com')
'''
