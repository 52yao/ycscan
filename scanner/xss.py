# scanner/xss.py
"""
XSS 检测模块（增强版）：
- 注入多个无害但高识别度的 XSS payload
- 检测返回包是否出现特殊标识（如 65535src）
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from utils.requester import get

# 多种无害、唯一标记型 XSS payload
XSS_PAYLOADS = [
    "<u>65535src</u>",
    "<b id=65535src></b>",
    "<div class=65535src></div>",
    "<a href='javascript:65535src'>click</a>",
    "<img src=x onerror=65535src>",  # 低风险 onerror
]

UNIQUE_MARK = "65535src"  # 用于回显检测的唯一标记

 # 返回错误关键词列表，为md报告高亮关键词
def get_keywords():
    return UNIQUE_MARK

def scan(url, headers, cookies, proxies):
    result = {"found": False, "request": "", "response": ""}
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    for param in query:
        for payload in XSS_PAYLOADS:
            new_query = query.copy()
            new_query[param] = payload
            query_string = urlencode(new_query, doseq=True)
            test_url = urlunparse(parsed._replace(query=query_string))
            resp = get(test_url, headers=headers, cookies=cookies, proxies=proxies)

            if resp and UNIQUE_MARK.lower() in resp.text.lower():
                result["found"] = True
                result["request"] = test_url
                result["response"] = resp.text[:5000]
                return result

    return result
