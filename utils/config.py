# utils/config.py
"""
配置模块：
- 设置统一的请求头、Cookie 和代理
- 可供所有扫描模块导入使用
"""

# 自定义请求头（可添加常见字段伪装成浏览器）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept": "*/*",
}

# 自定义 Cookie（根据目标系统自行填写或动态导入）
COOKIES = {
    # "sessionid": "your-session-id"
}

# 代理设置（用于抓包或匿名访问）
# 示例格式: {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
PROXIES = {
    # "http": "http://127.0.0.1:8080",
    # "https": "http://127.0.0.1:8080"
}
