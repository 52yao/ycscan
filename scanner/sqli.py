# scanner/sqli.py
"""
SQL 注入检测模块（增强版）：
- 尝试注入 payload 到 URL 参数中
- 检测返回内容中是否包含数据库错误信息
- 新增响应长度对比判断，提升绕过 WAF 检测能力
"""

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from utils.requester import get

SQL_PAYLOADS = [
    "'", "\"", "' OR '1'='1", "' AND 1=1--", "\" OR 1=1--",
    "1 OR 1=1", "1' OR '1'='1' -- ", "admin'-- ", "admin\"-- ",
    "1;WAITFOR DELAY '0:0:2'"
]

SQL_ERRORS = [
    "you have an error", "mysql", "syntax error", "warning",
    "unclosed quotation", "sql", "odbc", "database", "fail", "denied"
]

LENGTH_DIFF_THRESHOLD = 30  # 响应长度差异阈值

 # 返回错误关键词列表，为md报告高亮关键词
def get_keywords():
    return SQL_ERRORS 

def scan(url, headers, cookies, proxies):
    result = {"found": False, "request": "", "response": ""}
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    for param in query:
        # 1. 基于返回内容中的错误关键词判断
        for payload in SQL_PAYLOADS:
            new_query = query.copy()
            new_query[param] = payload
            query_string = urlencode(new_query, doseq=True)
            test_url = urlunparse(parsed._replace(query=query_string))

            resp = get(test_url, headers=headers, cookies=cookies, proxies=proxies)
            if resp and any(err in resp.text.lower() for err in SQL_ERRORS):
                result["found"] = True
                result["request"] = test_url
                result["response"] = resp.text[:5000]
                return result

        # 2. 响应长度差异判断：单引号 vs 双单引号
        for char in ["'", '"']:
            payload1 = query[param][0] + char
            payload2 = query[param][0] + (char * 2)

            for val, tag in [(payload1, "1个引号"), (payload2, "2个引号")]:
                new_query = query.copy()
                new_query[param] = val
                query_string = urlencode(new_query, doseq=True)
                test_url = urlunparse(parsed._replace(query=query_string))

                resp = get(test_url, headers=headers, cookies=cookies, proxies=proxies)
                if tag == "1个引号":
                    base_len = len(resp.text) if resp else 0
                    base_url = test_url
                    base_resp = resp.text[:5000] if resp else ""
                else:
                    double_len = len(resp.text) if resp else 0
                    diff = abs(double_len - base_len)

                    if diff > LENGTH_DIFF_THRESHOLD:
                        result["found"] = True
                        result["request"] = base_url + " ➔ " + test_url
                        result["response"] = f"响应长度差异: {diff}\n\n第一个返回片段:\n{base_resp}\n\n第二个返回片段:\n{resp.text[:5000]}"
                        return result

    return result
