#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 使用百度语音库 把文字转为语音。使用场景是读书会等，估计微信的公众号的文章朗读也是基于此做的。
'''

import requests
import json
import sys
import base64
import time
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
timer = time.perf_counter

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#填写百度控制台中相关开通了“语音合成”接口的应用的的API_KEY及SECRET_KEY
API_KEY = 'Wawo2qzX1ezgVGkOQ6h4O9gg'
SECRET_KEY = 'YEyL2DMnubp9KsvE9ABECSDGz0gd1Lwr'

urlCreate = 'https://aip.baidubce.com/rpc/2.0/tts/v1/create'  #创建长文本语音合成任务请求地址

urlQuery = 'https://aip.baidubce.com/rpc/2.0/tts/v1/query'  #查询长文本语音合成任务结果请求地址

"""  获取请求TOKEN start 通过开通语音合成接口的百度应用的API_KEY及SECRET_KEY获取请求token"""

class DemoError(Exception):
    pass

TOKEN_URL = 'https://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选

def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}

    post_data = urlencode(params)
    post_data = post_data.encode( 'utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
 
        result_str =  result_str.decode()

#    print(result_str)
    result = json.loads(result_str)
#    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
#        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

"""  获取鉴权结束，TOKEN end """

"""  发送语音合成请求 """

#待进行合成的文本，需要为UTF-8编码；输入多段文本时，文本间会插入1s长度的空白间

# token = {"access_token":"24.19fd456ac888cb1d1cdef56fcb1b567a.2592000.1579157900.282828-11778899"}

token = {"access_token":fetch_token()}

def createTask():
    headers = {'content-type': "application/json"}
    text = [

    "本博客是关于一个在IT以及分布式领域深耕多年的程序员的故事!"

    "2005年入川读书，一直在电子科技大学通信学院直到硕士毕业进入社会。",

    "2012年硕士毕业入职华为公司，当时入职的部门是云计算下面的分布式存储。之后一直在做分布式存储相关的业务，直到2020年决定离开。",

    "2020年2月加入阿里巴巴-阿里云，现在主攻数据湖方向。更详细的介绍请参考CSDN神技圈子的平台"
    ]

    body = {
    "text": text,
    "format": "mp3-16k",        #音频格式，支持"mp3-16k","mp3-48k", "wav", "pcm-8k","pcm-16k"
    "voice": 1,        #音库，度小宇=1，度小美=0，度逍遥（基础）=3，度丫丫=4；度逍遥（精品）=5003，度小鹿=5118，度博文=106，度小童=110，度小萌=111，度米朵=103，度小娇=5
    "lang": "zh"       #语言选择,目前只有中英文混合模式，填写固定值"zh"
    }
    response = requests.post(urlCreate,params=token,data = json.dumps(body), headers = headers)
    # 返回请求结果信息，获得task_id，通过长文本语音合成查询接口，获取合成结果

    respJson = response.json()

    if respJson['task_id'] is not None:
        return respJson['task_id'] 

    print(f'create task error , the code:{respJson}')
    return None


def queryTask(taskIds):
    body = {
        "task_ids": taskIds
    }

    headers = {'content-type': "application/json"}

    response = requests.post(urlQuery,params=token,data = json.dumps(body), headers = headers)

    respJson = response.json()

    for task in respJson['tasks_info']:
        if task['task_status'] != 'Success' and task['task_status'] == 'Running':
           print(f'翻译ing： {task}')

        else:
           downUrl = task['task_result']['speech_url']
           taskID = task['task_id']
           print(f'taskId:{taskID},下载地址为;{downUrl}')


# step1 
# 
#taskID = createTask()
taskID = '6458be8ae4a4240001e99f25'
tasks = []
if taskID != None:
   tasks.append(taskID)
   queryTask(tasks)

    




