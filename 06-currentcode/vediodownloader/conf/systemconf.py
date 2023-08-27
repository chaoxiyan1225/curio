#coding=utf8

#projectZip = 'https://github.com/chaoxiyan1225/vedioprocess/archive/refs/heads/main.zip'
import json

class VedioUrl:

   def __init__(self, id = '', name = '',url = '', country = '', descript = '', logo = ''):
        self.id = id 
        self.name = name
        self.url = url
        self.descript = descript
        self.country = country
        self.logo = logo

   def toString(self):
      s = json.dumps(self.__dict__)
      return s

projectZip =  'https://gitcode.net/ycx1225/videoconf/-/archive/master/videoconf-master.zip'
userConf = 'users.conf'
softwareConf = 'software.conf'
adviceurlConf = 'adviceurl.json'
contackQQ = '59478148'
email = 'chaoxiyan1225@163.com'
newSoftWareZip = ''
clientVersion = '1.0.6' # 客户端的版本号，随着时间递增，这个值会不断变化，不会超过服务端的值
emailFrom = email
emailPwd = 'VxqRl8Zr1ekcTvzxSndoUw=='
emailSender = 'SPEEEEEEED'
contackUs = f'QQ:{contackQQ} , email:{email}'

FACE_BOOK = "www.facebook.com"
YOUTOBE = "www.youtube.com"
INSTAGRAM = "www.instagram.com"

default_urls = [
                VedioUrl('66666', '我要吃瓜网','https://www.51cg4.com/', '中国', "我要吃瓜网最新网址", "https://gitcode.net/ycx1225/vediodownarchive/-/raw/master/logoimgs/51cg.png?inline=false"),
                
                VedioUrl('8888', '8x8x网','https://81xane.top/', '中国', "各种老电影", "https://gitcode.net/ycx1225/vediodownarchive/-/raw/master/logoimgs/51cg.png?inline=false"),
               ]
