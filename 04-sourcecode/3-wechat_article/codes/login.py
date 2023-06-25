# -!- coding: utf-8 -!-
from selenium import webdriver
import time
import json
 
#谷歌和火狐两种驱动人选一种即可
# 调用谷歌浏览器驱动   如果本地电脑未安装谷歌驱动，请网上下载
driver = webdriver.Chrome()
# 调用火狐浏览器驱动   如果本地电脑未安装火狐驱动，请网上下载
# driver = webdriver.Firefox()
driver.get("https://mp.weixin.qq.com/") # 微信公众平台网址
driver.find_element("link text", "使用帐号登录").click() # 此行代码为2020.10.10新增，因为微信公众号页码原来默认直接为登录框， 现在默认为二维码，此行代码可以将二维码切换到登录框页面
#driver.find_element_by_link_text("使用帐号登录").click() # 此行代码为2020.10.10新增，因为微信公众号页码原来默认直接为登录框， 现在默认为二维码，此行代码可以将二维码切换到登录框页面
driver.find_element("name", "account").clear()
driver.find_element("name","account").send_keys("chaoxiyan1225@163.com")  # 自己的微信公众号
time.sleep(2)
driver.find_element("name","password").clear()
driver.find_element("name","password").send_keys("ycx/8520/8520-+")  # 自己的微信公众号密码
driver.find_element("class name", "icon_checkbox").click()
 
time.sleep(2)
driver.find_element("class name", "btn_login").click()
time.sleep(15)
#此时会弹出扫码页面，需要微信扫码
cookies = driver.get_cookies()  # 获取登录后的cookies
print(cookies)
cookie = {}
for items in cookies:
    cookie[items.get("name")] = items.get("value")
# 将cookies写入到本地文件，供以后程序访问公众号时携带作为身份识别用
with open('cookies.txt', "w") as file:
    #  写入转成字符串的字典
    file.write(json.dumps(cookie))
