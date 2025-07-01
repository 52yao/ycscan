# utils/logger.py
"""
日志模块：
- 输出彩色终端日志
- 同时保存到日志文件（scan.log）
"""

import datetime

LOG_FILE = "scan.log"

def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(f"\033[94m{formatted}\033[0m")  # 蓝色
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\\n")
