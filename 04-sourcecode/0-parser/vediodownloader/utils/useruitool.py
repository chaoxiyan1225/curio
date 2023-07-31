#coding=utf8
import sys, os
import requests, json
import uuid
import base64

import conf.systemconf as SystemConf
import re

def IsValidUrl(url:str )->bool:

    if not url:
        return False

    url = url.strip()
    if re.match(r'^https?:/{2}\w.+$', url):
        return True
    else:
        return False


def IsValidEmail(email:str)->bool:
    if not email:
       return False

    email = email.strip()
    result = re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email)

    if result:
       return True
    else:
       return False

def IsValidTel(tel:str)->bool:

    if not tel:
       return False

    pattern = re.compile(r'^(13[0-9]|14[0|5|6|7|9]|15[0|1|2|3|5|6|7|8|9]|'
                         r'16[2|5|6|7]|17[0|1|2|3|5|6|7|8]|18[0-9]|'
                         r'19[1|3|5|6|7|8|9])\d{8}$')

    if pattern.search(tel):
       return True

    return False
