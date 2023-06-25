# -*- coding:utf-8 -*- 
import requests
import json
import re
import random
import time
 
with open("cookies.txt", "r") as file:
    cookie = file.read()
cookies = json.loads(cookie)
url = "https://mp.weixin.qq.com"
response = requests.get(url, cookies=cookies)
token = re.findall(r'token=(\d+)', str(response.url))[0]  # 从url中获取token
print(token)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    "Referer": "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token="+token+"&lang=zh_CN",
    "Host": "mp.weixin.qq.com",
}
# requestUrl = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
with open('article_link.txt', "w", encoding='utf-8') as file:
    for j in range(1, 48, 1):
        begin = (j-1)*5
        requestUrl = "https://mp.weixin.qq.com/cgi-bin/appmsg?token="+token+"&lang=zh_CN&f=json&ajax=1&random="+str(random.random())\
                     +"&action=list_ex&begin="+str(begin)+"&count=5&query=&fakeid=MzI1NjczMTU3Mg%3D%3D&type=9"
        search_response = requests.get(requestUrl, cookies=cookies, headers=headers)
        re_text = search_response.json()
        print(re_text)
        list = re_text.get("app_msg_list")
        for i in list:
            file.write(i["aid"]+"<=====>"+i["title"]+"<=====>"+i["link"] + "\n")
            print(i["aid"]+"<=====>"+i["title"]+"<=====>"+i["link"])
        time.sleep(20)

