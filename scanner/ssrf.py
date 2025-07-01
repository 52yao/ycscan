# scanner/ssrf.py
"""
SSRF 检测模块（增强版）：
- 检查是否访问了内网地址
- 结合响应提示判断连接尝试
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from utils.requester import get

SSRF_TARGETS = [
    "http://127.0.0.1",
    "http://localhost",
    "http://10.0.0.1",
    "http://169.254.169.254/latest/meta-data/",
    "http://metadata.tencentyun.com/latest/meta-data",
    "http://metadata.google.internal/latest/meta-data",
    "http://100.100.100.200/latest/meta-data/"
]

SSRF_HINT_KEYWORDS = [
    "127.0.0.1", "localhost", "connection refused", "unable to connect",
    "timed out", "unreachable", "no route to host", "reset by peer",
    "refused to connect", "metadata", "hostname"
]

 # 返回错误关键词列表，为md报告高亮关键词
def get_keywords():
    return SSRF_HINT_KEYWORDS

def scan(url, headers, cookies, proxies):
    result = {"found": False, "request": "", "response": ""}
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    for param in query:
        for ssrf_url in SSRF_TARGETS:
            new_query = query.copy()
            new_query[param] = ssrf_url
            query_string = urlencode(new_query, doseq=True)
            test_url = urlunparse(parsed._replace(query=query_string))

            resp = get(test_url, headers=headers, cookies=cookies, proxies=proxies)
            if resp and any(kw in resp.text.lower() for kw in SSRF_HINT_KEYWORDS):
                result["found"] = True
                result["request"] = test_url
                result["response"] = resp.text[:5000]
                return result
    return result
