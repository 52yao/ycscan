# scanner/cmdinj.py
"""
命令注入检测模块：
- 尝试注入命令执行符号 `; ping` `| whoami` 等
- 检查返回内容是否有系统命令执行痕迹
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from utils.requester import get

CMD_PAYLOADS = [";id", "|whoami", "&&dir", "||ls","&&echo test", "&&ping 127.0.0.1"],"`echo test`"

def scan(url, headers, cookies, proxies):
    result = {"found": False, "request": "", "response": ""}
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    for param in query:
        for payload in CMD_PAYLOADS:
            new_query = query.copy()
            new_query[param] = payload
            query_string = urlencode(new_query, doseq=True)
            test_url = urlunparse(parsed._replace(query=query_string))
            resp = get(test_url, headers=headers, cookies=cookies, proxies=proxies)
            if resp and ("uid=" in resp.text or "root" in resp.text or "administrator" in resp.text or "test" in resp.text):
                result["found"] = True
                result["request"] = test_url
                result["response"] = resp.text[:5000]
                return result
    return result
