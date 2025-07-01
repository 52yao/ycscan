# scanner/deadjs.py
"""
死链扫描模块：
- 提取网页中引用的 JS 文件
- 检测是否存在无法访问的第三方 JS（死链）
- 如果站点失效，可能存在被第三方接管的风险
"""

import re
from urllib.parse import urlparse, urljoin
from utils.requester import get

def scan(url, headers, cookies, proxies):
    result = {"found": False, "request": "", "response": ""}
    third_party_js = []

    # 获取网页内容
    resp = get(url, headers=headers, cookies=cookies, proxies=proxies)
    if not resp or not resp.text:
        return result

    # 提取所有 script src 链接
    scripts = re.findall(r'<script[^>]+src=[\'"]?([^\'"\s>]+)', resp.text, re.IGNORECASE)
    parsed_url = urlparse(url)
    domain = parsed_url.hostname

    for src in scripts:
        full_url = urljoin(url, src)
        parsed_src = urlparse(full_url)

        # 忽略自身域名
        if parsed_src.hostname and parsed_src.hostname != domain:
            js_resp = get(full_url, headers=headers, cookies=cookies, proxies=proxies)
            if not js_resp or js_resp.status_code >= 400:
                third_party_js.append({
                    "src": full_url,
                    "status": js_resp.status_code if js_resp else "连接失败"
                })

    if third_party_js:
        result["found"] = True
        result["request"] = f"引用 JS 检测来源：{url}"
        result["response"] = "\n".join([f"{item['src']} ➜ {item['status']}" for item in third_party_js])

    return result
