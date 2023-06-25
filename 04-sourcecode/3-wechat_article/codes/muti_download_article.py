# -*- coding:utf-8 -*-
 
import json
import re
import time
from utils.mutithreadtask import MultiThreadHandler
from bs4 import BeautifulSoup
import requests
import os
from pathlib import Path, PurePath
import queue
import time

def save_html(url_content,htmlDir,file_name):
    filePath = htmlDir / (file_name + '.html')
    f = open(filePath, 'wb')
    f.write(url_content.content)  # save to page.html
    f.close()
    return url_content
 
 
def update_file(old, new,htmlDir, file_name):

    with open(htmlDir / (file_name + '.html'), encoding='utf-8') as f, open(htmlDir / (file_name + '_bak.html'), 'w',encoding='utf-8') as fw:  # 打开两个文件，原始文件用来读，另一个文件将修改的内容写入
        for line in f: 
            new_line = line.replace(old, new)  # 逐行替换
            new_line = new_line.replace("data-src", "src")
            fw.write(new_line)  # 写入新文件
    os.remove(htmlDir / (file_name + '.html')) 
    time.sleep(10)
    os.rename(htmlDir / (file_name + '_bak.html'), htmlDir / (file_name + '.html'))  #
    print('当前保存文件为：' + str(htmlDir / file_name) + '.html')
 

def save_file_to_local(htmlDir,targetDir,search_response,domain, file_name):
    obj = BeautifulSoup(save_html(search_response,htmlDir,file_name).content, 'lxml') 
    imgs = obj.find_all('img')
    urls = []
    for img in imgs:
        if 'data-src' in str(img):
            urls.append(img['data-src'])
        elif 'src=""' in str(img):
            pass
        elif "src" not in str(img):
            pass
        else:
            urls.append(img['src'])

    i = 0
    for each_url in urls:  
        if each_url.startswith('//'):
            new_url = 'https:' + each_url
            r_pic = requests.get(new_url)
        elif each_url.startswith('/') and each_url.endswith('gif'):
            new_url = domain + each_url
            r_pic = requests.get(new_url)
        elif each_url.endswith('png') or each_url.endswith('jpg') or each_url.endswith('gif') or each_url.endswith('jpeg'):
            r_pic = requests.get(each_url)
        t = targetDir / (str(i) + '.jpeg')
        print('当前保存图片为：' + str(t))
        fw = open(t, 'wb') 
        fw.write(r_pic.content) 
        i += 1
        update_file(each_url, str(t), htmlDir, file_name)  # 修改为本地的链接，这样本地打开整个页面就能访问
        fw.close()

def save(search_response,file_name):
    #Path.cwd() get current path
    htmlDir = Path.cwd() / file_name
    targetDir =  htmlDir / 'imgs1'  
    if not os.path.isdir(targetDir): 
        os.makedirs(targetDir)
    domain = 'https://mp.weixin.qq.com/s'
    save_html(search_response, htmlDir,file_name)
    save_file_to_local(htmlDir, targetDir, search_response, domain, file_name)


# 加载cookie
with open("cookies.txt", "r") as file:
    cookie = file.read()
cookies = json.loads(cookie)

url = "https://mp.weixin.qq.com"
response = requests.get(url, cookies=cookies)
token = re.findall(r'token=(\d+)', str(response.url))[0]
print(token)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    "Referer": "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token="+token+"&lang=zh_CN",
    "Host": "mp.weixin.qq.com",
}

class Item:
    def __init__(self, url, file_name, dir_name):
        self.url = url
        self.file_name = file_name
        self.dir_name = dir_name

def process(item, result_queue, cookies=cookies, headers=headers):
    search_response = requests.get(item.url, cookies=cookies, headers=headers)
    save(search_response,  item.file_name)
    result = f'{item.file_name} ------下载完毕：{item.dir_name}---------下载完毕：{item.url}'
    print(result)
    result_queue.put(result)
 

# 加载链接
f = open("article_link.txt", encoding='utf-8')  
line = f.readline()  

task_queue = queue.Queue()
out_queue = queue.Queue()

for line in open("article_link.txt", encoding='UTF-8'):
    new_line = line.strip()
    line_list = new_line.split("<=====>")
    file_name = line_list[0]
    dir_name = line_list[1]
    requestUrl = line_list[2]
    item = Item(requestUrl, file_name, dir_name)
    task_queue.put(item)

file.close()

MultiThreadHandler(task_queue, process, out_queue, 10).run(True)

print("finish download")

