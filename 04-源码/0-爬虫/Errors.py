#coding=utf8

class BaseError: 
    def __init__(self, code, message): 
    	self.code = code 
    	self.message = message


    def getCode(self):
    	return self.code

    def getMessage(self):
    	return self.message

#----------------------------------------------------------
'''
  无前缀的错误码是通用错误码
'''

SUCCESS = BaseError("000000", "SUCCESS")
FAIL    = BaseError("111111", "FAIL")

#----------------------------------------------------------
'''
  客户端的错误码集合，都是以0c_ 开头 
'''
C_LoginFail       = BaseError("0c_0001", "客户端登陆失败！")
C_ErrorPasswdOrName = BaseError("0c_0002", "用户名或者密码错误")
C_Arrearage       = BaseError("0c_0003", "客户欠费")
C_InvalidUser     = BaseError("0c_0004", "无效的用户Id")
C_VersionTooLow   = BaseError("0c_0005", "客户端软件版本太低")


#----------------------------------------------------------
'''
  服务端的错误码集合，都是以 0s_ 开头
'''
S_DownLoadError   = BaseError("0s_0001", "服务端下载失败")
S_InvalidFileContent = BaseError("0s_0002", "下载的文件内容为空")
S_ParseFail       = BaseError("0s_0003", "服务端下载文件解析错误")
S_Forbidden       = BaseError("0s_0004", "该软件当前禁用!!")


