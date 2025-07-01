# utils/requester.py
"""
请求封装模块：
- 统一处理 requests.get/post 请求
- 支持传入代理、headers、cookies
- 忽略 SSL 警告
"""

import requests
import urllib3
from utils.logger import log

# 忽略不安全 HTTPS 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get(url, headers=None, cookies=None, proxies=None, timeout=6):
    try:
        resp = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, timeout=timeout, verify=False)
        log(f"[GET] {url} - {resp.status_code}")
        return resp
    except Exception as e:
        log(f"[请求失败] {url} - {e}")
        return None

def post(url, data=None, headers=None, cookies=None, proxies=None, timeout=6):
    try:
        resp = requests.post(url, data=data, headers=headers, cookies=cookies, proxies=proxies, timeout=timeout, verify=False)
        log(f"[POST] {url} - {resp.status_code}")
        return resp
    except Exception as e:
        log(f"[请求失败] {url} - {e}")
        return None
