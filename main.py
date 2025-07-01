# main.py
"""
主程序入口：
1. 调用爬虫收集URL
2. 针对每个URL调用各个漏洞扫描模块
3. 收集结果并生成 Excel 和 Markdown 报告
"""

import sys
import threading
from crawler import crawl_and_collect_urls
from reporter import generate_excel_report, generate_markdown_report

from scanner import sqli, xss, dirtrav, ssrf, cmdinj, cors, fuzz, deadjs
from utils.logger import log
from utils.config import HEADERS, COOKIES, PROXIES

results = []
lock = threading.Lock()

def scan_url(url):
    log(f"开始扫描: {url}")
    scan_result = {"url": url}

    for module in [sqli, xss, dirtrav, ssrf, cmdinj, cors, fuzz, deadjs]:
        name = module.__name__.split('.')[-1]
        result = module.scan(url, headers=HEADERS, cookies=COOKIES, proxies=PROXIES)
        scan_result[f"{name}_found"] = result['found']
        scan_result[f"{name}_request"] = result['request']
        scan_result[f"{name}_response"] = result['response']

    with lock:
        results.append(scan_result)

def main():
    if len(sys.argv) != 2:
        print("用法: python main.py http://example.com")
        sys.exit(1)

    target_url = sys.argv[1]
    urls = crawl_and_collect_urls(target_url, max_depth=2)
    log(f"共发现 {len(urls)} 个可扫描URL")

    threads = []
    for url in urls:
        t = threading.Thread(target=scan_url, args=(url,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    generate_excel_report(results)
    generate_markdown_report(results)
    log("所有报告生成完成")

if __name__ == '__main__':
    main()
