#coding=utf8

class BaseError: 
    def __init__(self, code, message): 
    	self.code = code 
    	self.message = message

    def getCode(self):
    	return self.code

    def getMessage(self):
    	return self.message

    def append(self, moreMsg):
    	self.message = f'{self.message},and {moreMsg}'

    	return self

    def toString(self):
    	return f'code:{self.code}, and message:{self.message}'

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
C_LoginFail         = BaseError("0c_0001", "客户端登陆失败！")
C_ErrorPasswdOrName = BaseError("0c_0002", "用户名或者密码错误")
C_Arrearage         = BaseError("0c_0004", "用户已欠费")
C_VersionTooLow     = BaseError("0c_0006", "email 信息错误")
C_SendEmailFail     = BaseError("0c_0007", "发送邮件错误")
C_InvalidUser       = BaseError("0c_0008", "无效的用户请注册")

#----------------------------------------------------------
'''
  服务端的错误码集合，都是以 0s_ 开头
'''
S_UnknowError        = BaseError("0s_0000", "服务端未知错误") 
S_DownLoadError      = BaseError("0s_0001", "服务端下载失败")
S_InvalidFileContent = BaseError("0s_0002", "下载的文件内容为空")
S_ParseFail          = BaseError("0s_0003", "服务端文件解析异常")
S_Forbidden          = BaseError("0s_0004", "该软件当前禁用!!")
S_NoAdviceUrl        = BaseError("0s_0005", "无建议的网址")

S_ClientFreeUse      = BaseError("1s_0001", "客户端免费试用")


