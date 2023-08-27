#coding=utf8
import sys, os, time
import requests, json
import urllib.request
import ssl
import uuid
import base64 
from Crypto.Cipher import AES

# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header
import conf.systemconf as SystemConf
import re
import utils.logger as logger

last_time = 0
zip_data = None

iv =  '5947814788888888'
default_key = 'vedioprocesskey6'
data = 'hello world'




#coding=utf8
import sys, os, time,random
import requests, json
import urllib.request
import ssl
import uuid
import base64 
from Crypto.Cipher import AES

# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header
import conf.systemconf as SystemConf
import re
import utils.logger as logger
RETRY_TIME = 3
import logging


iv =  '5947814788888888'
default_key = 'vedioprocesskey6'
data = 'hello world'

pictures = ['ab.png','dl.png','buy.png','dq.png','fund.png','icon.png','rg.png','stock.png', 'weixin.png', 'zhifubao.png']


proxies = {
        'http': '127.0.0.1:1212',
        'https': '127.0.0.1:1212'
    }
        
headers_list = [
    {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666'
    }, {
        'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320'
    }, {
        'user-agent': 'Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+'
    }, {
        'user-agent': 'Mozilla/5.0 (PlayBook; U; RIM Tablet OS 2.1.0; en-US) AppleWebKit/536.2+ (KHTML like Gecko) Version/7.2.1.0 Safari/536.2+'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G965U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; SM-T837A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; U; en-us; KFAPWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.13 Safari/535.19 Silk-Accelerated=true'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LGMS323 Build/KOT49I.MS32310c) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 550) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/14.14263'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 10 Build/MOB31T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR4.170623.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 6 Build/N6F26U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Nexus 6P Build/OPP3.170518.006) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)'
    }, {
        'user-agent': 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebKit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 3 Build/PQ1A.181105.017.A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36'
    }, {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
    }, {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }, {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
    }
]

headers = random.choice(headers_list)

SESSION_TIMEOUT = 5 * 60

def get_conf_data():
    current = time.time() 
    global zip_data
    global last_time
    if current - last_time < SESSION_TIMEOUT and zip_data == None:
          return zip_data
            
    current = 0
    delay = 5
    while current < RETRY_TIME:
        try: 
            current = current + 1
            ssl._create_default_https_context = ssl._create_unverified_context
            headers={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
            req = urllib.request.Request(SystemConf.projectZip, headers=headers)

            userRead = urllib.request.urlopen(req, timeout=15)
            data = userRead.read()
            zip_data = data
            last_time = time.time()

            return zip_data
          
        except Exception as e:
            logger.error(f" send request error, {SystemConf.projectZip} {e}".encode("utf-8"))
            logging.exception(e)
            time.sleep(delay)
            delay *= 2

    return None

def picToPythonFile(picture_names, path ,py_name):
    """
    将图像文件转换为py文件
    :param picture_name:
    :return:
    """
    write_data = []
    for picture_name in picture_names:
        filename = picture_name.replace('.', '_')
        open_pic = open("%s/%s" % (path, picture_name), 'rb')
        b64str = base64.b64encode(open_pic.read())
        open_pic.close()
        # 注意这边b64str一定要加上.decode()
        #write_data.append('%s = b\'%s\'\n' % (filename, b64str.decode()))
        write_data.append('%s = %s \n' % (filename, b64str))

    f = open('%s.py' % py_name, 'w+')
    for data in write_data:
        f.write(data)
    f.close()

def picToBytePythonFile(picture_names, path ,py_name):
    """
    将图像文件转换为py文件
    :param picture_name:
    :return:
    """
    write_data = []
    for picture_name in picture_names:
        filename = picture_name.replace('.', '_')
        open_pic = open("%s/%s" % (path, picture_name), 'rb')
        #b64str = base64.b64encode(open_pic.read())
        bytes =  open_pic.read()
        open_pic.close()
        # 注意这边b64str一定要加上.decode()
        #write_data.append('%s = b\'%s\'\n' % (filename, b64str.decode()))
        write_data.append('%s = %s \n' % (filename, bytes))

    f = open('%s.py' % py_name, 'w+')
    for data in write_data:
        f.write(data)
    f.close()

def convert_pathPic_pyFile(path = "imgs", pyfileName = "pictures{_v2}"):

    walks  = os.walk(path)
    picNames = []
    for path, dir_list,file_list in walks:
        for fileName in file_list:
            picNames.append(fileName)

    picToBytePythonFile(picNames, path, pyfileName)

# aes key must 16byte
def AES_Encode(data, key = default_key):
   
    if len(data) < 16:
        data = pad(data)
   
    AES_obj = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    AES_en_str = AES_obj.encrypt(data.encode("utf-8"))
    AES_en_str = base64.b64encode(AES_en_str)
    AES_en_str = AES_en_str.decode("utf-8")

    return AES_en_str

def AES_Decode(data, key = default_key):
    data = data.encode("utf-8")
    data = base64.b64decode(data)
    AES_de_obj = AES.new(key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8"))
    AES_de_str = AES_de_obj.decrypt(data)
    #去掉之前补齐的空格
    AES_de_str = AES_de_str.strip()
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


def sendMailByWangyi(subject:str, content:str, From = SystemConf.emailFrom, To =  SystemConf.emailFrom) -> bool:
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
        print(f'发送邮件成功: {To}！！')
        ret = True
    except smtplib.SMTPException as e:
        print(f"无法发送邮件{To}: str{e}")
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
    
def send_getRequest(url):
    current = 0
    delay = 5
    while current < RETRY_TIME:
        try: 
            current = current + 1
            response = requests.get(url, headers=headers)
            
            return response
          
        except Exception as e:
            logger.error(f" send request error, {url} {e}".encode("utf-8"))
            logging.exception(e)
            time.sleep(delay)
            delay *= 2

    return None

if __name__ == '__main__':
    #sendRegisterMsg('')
    print(get_mac_address())
