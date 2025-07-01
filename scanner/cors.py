# scanner/cors.py
"""
CORS 配置错误检测模块：
- 构造恶意 Origin 头
- 检查响应中是否回显 Access-Control-Allow-Origin: *
"""

from utils.requester import get

def scan(url, headers, cookies, proxies):
    result = {"found": False, "request": "", "response": ""}
    evil_headers = headers.copy()
    evil_headers["Origin"] = "http://evil.com"

    resp = get(url, headers=evil_headers, cookies=cookies, proxies=proxies)
    if resp and "Access-Control-Allow-Origin" in resp.headers:
        if resp.headers.get("Access-Control-Allow-Origin") in ["*", "http://evil.com"]:
            result["found"] = True
            result["request"] = url
            result["response"] = str(resp.headers)
    return result
