#coding=utf8
import sys, os
import requests, json
import urllib.request
import ssl
import uuid
import base64 
from Crypto.Cipher import AES

import utils.logger as logger

# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header
import config.SystemConf
import re

iv =  '5947814788888888'
default_key = 'vedioprocesskey6'
data = 'hello world'

pictures = ['ab.png','dl.png','buy.png','dq.png','fund.png','icon.png','rg.png','stock.png', 'weixin.png', 'zhifubao.png']


def picToPythonFile(picture_names, py_name):
    """
    将图像文件转换为py文件
    :param picture_name:
    :return:
    """
    write_data = []
    for picture_name in picture_names:
        filename = picture_name.replace('.', '_')
        open_pic = open("%s" % picture_name, 'rb')
        b64str = base64.b64encode(open_pic.read())
        open_pic.close()
        # 注意这边b64str一定要加上.decode()
        write_data.append('%s = "%s"\n' % (filename, b64str.decode()))

    f = open('%s.py' % py_name, 'w+')
    for data in write_data:
        f.write(data)
    f.close()

# aes 加密 要求key要16byte
def AES_Encode(data, key = default_key):
   # 将长度不足16字节的字符串补齐
    if len(data) < 16:
        data = pad(data)
    # 创建加密对象
    AES_obj = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    # 完成加密
    AES_en_str = AES_obj.encrypt(data.encode("utf-8"))
    # 用base64编码一下
    AES_en_str = base64.b64encode(AES_en_str)
    # 最后将密文转化成字符串
    AES_en_str = AES_en_str.decode("utf-8")
    return AES_en_str

# aes解密 要求key要16byte
def AES_Decode(data, key = default_key):
    # 解密过程逆着加密过程写
    # 将密文字符串重新编码成二进制形式
    data = data.encode("utf-8")
    # 将base64的编码解开
    data = base64.b64decode(data)
    # 创建解密对象
    AES_de_obj = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    # 完成解密
    AES_de_str = AES_de_obj.decrypt(data)
    # 去掉补上的空格
    AES_de_str = AES_de_str.strip()
    # 对明文解码
    AES_de_str = AES_de_str.decode("utf-8")
    return AES_de_str

# 将原始的明文用空格填充到16字节
def pad(data):
    pad_data = data
    for i in range(0,16-len(data)):
        pad_data = pad_data + ' '
    return pad_data

# 获取本机mac地址
def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

def sendMonitorMsg(toEmail:str, subject, content):
    return sendMailByWangyi(subject, content, To = toEmail)

def sendRegisterMsg(email:str = '', tel:str = ''):
    mac = get_mac_address()
    subject = f'【撸片神器注册消息】来自:[{mac}]'
    content = f'【1】当前用户发起新注册请求，请及时处理。\n   (1)对端的邮箱:{email}  \n   (2)对端手机号:{tel} \n   (3)mac 地址[{mac}]'
    return sendMailByWangyi(subject, content)


def sendClientLoginFailMsg(errorMsg:str, email:str = ''):
    mac = get_mac_address()
    subject = f'【撸片神器客户端错误】来自:[{mac}]'
    content = f'当前用户登陆遇到连续错误对端的邮箱:{email} \nmac 地址[{mac}]'
    return sendMailByWangyi(subject, content)


def sendMailByWangyi(subject:str, content:str, From = config.SystemConf.emailFrom, To =  config.SystemConf.emailFrom) -> bool:
    message = MIMEText(content, "plain", "utf-8")
    message["Accept-Language"]="zh-CN"
    message["Accept-Charset"]="ISO-8859-1,utf-8"
    message['Subject'] = subject  # 邮件标题
    message['To'] =  To  # 收件人
    message['From'] =  From  # 发件人

    ret = False
    try:
        smtp = smtplib.SMTP_SSL("smtp.163.com", 994)  
        smtp.login(SystemConf.emailFrom, AES_Decode(SystemConf.emailPwd))
        smtp.sendmail(SystemConf.emailFrom, [To], message.as_string())
        logger.warning(f'发送邮件成功: {To}！！')
        ret = True
    except smtplib.SMTPException as e:
        logger.error(f"无法发送邮件{To}: str{e}")
    finally:
        smtp.quit()
        return ret


#校验邮箱格式是否正确
def emailRight(email:str) -> bool:
    if not email:
       return False

    reg_str = r'(^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$)'
    mod = re.compile(reg_str)
    tems = mod.findall(email)
     
    if not tems:
        return False

    return True


#picToPythonFile(pictures, 'pictures')
#print('转换成功')
