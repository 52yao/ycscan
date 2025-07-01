# crawler.py
"""
爬虫模块：
- 递归爬取指定URL页面中所有链接
- 自动过滤静态资源（如 .css, .jpg 等）
- 只采集同源站点的链接
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from utils.logger import log
from utils.requester import get

# 要排除的静态资源后缀名
FILTER_EXT = (
    '.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
    '.woff', '.woff2', '.ttf', '.otf', '.eot', '.mp4', '.webm', '.webp',
    '.pdf', '.zip', '.tar', '.gz', '.rar'
)

def is_valid_url(url):
    """判断是否为有效URL，且不是静态资源"""
    if not url.startswith("http"):
        return False
    if any(url.lower().endswith(ext) for ext in FILTER_EXT):
        return False
    return True

def crawl_and_collect_urls(start_url, max_depth=2):
    visited = set()
    collected = set()
    base_domain = urlparse(start_url).netloc

    def crawl(url, depth):
        if depth > max_depth or url in visited:
            return
        visited.add(url)

        resp = get(url)
        if not resp or not resp.text:
            return

        try:
            soup = BeautifulSoup(resp.text, "html.parser")
        except Exception as e:
            log(f"[解析失败] {url} - {e}")
            return

        for tag in soup.find_all(["a", "link", "script", "iframe", "form"]):
            attr = "href" if tag.name != "script" else "src"
            link = tag.get(attr)
            if not link:
                continue
            abs_url = urljoin(url, link).split("#")[0].rstrip("/")
            domain = urlparse(abs_url).netloc
            if domain != base_domain:
                continue
            if is_valid_url(abs_url):
                collected.add(abs_url)
                crawl(abs_url, depth + 1)

    log(f"开始爬取: {start_url}")
    crawl(start_url, 0)

    return sorted(collected or [start_url])
