# scanner/fuzz.py
"""
Fuzz 模块（无害 Payload 版本）：
- 使用简单无害的 payload 避免被WAF拦截
- 依旧通过检测响应中的异常关键词判断漏洞可能
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from utils.requester import get

FUZZ_PAYLOADS = [
    "test123",
    "admin",
    "null",
    "true",
    "false",
    "1 OR 1=1",
    "1;--",
    "${7*7}",
    "$(echo 123)",
    "<test>",
    "0x414141",
    "../../etc/passwd",
    "admin' -- ",
    "admin\" -- ",
]

FUZZ_ERROR_KEYWORDS = [
    "error", "fail", "invalid", "denied", "unauthorized", "exception", "syntax", "timeout"
]

def get_keywords():
    return FUZZ_ERROR_KEYWORDS  # 返回错误关键词列表，为md报告高亮关键词

def scan(url, headers, cookies, proxies):
    result = {"found": False, "request": "", "response": ""}
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    for param in query:
        for payload in FUZZ_PAYLOADS:
            new_query = query.copy()
            new_query[param] = payload
            query_string = urlencode(new_query, doseq=True)
            test_url = urlunparse(parsed._replace(query=query_string))
            resp = get(test_url, headers=headers, cookies=cookies, proxies=proxies)
            if resp and any(keyword in resp.text.lower() for keyword in FUZZ_ERROR_KEYWORDS):
                result["found"] = True
                result["request"] = test_url
                result["response"] = resp.text[:5000]
                return result
    return result
