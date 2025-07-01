# utils/markdown_utils.py

import re

def highlight_keywords(text, keywords):
    """
    将命中的关键词用 HTML span 红色标记，适用于 Markdown 报告。
    """
    for kw in keywords:
        if kw.lower() in text.lower():
            pattern = re.compile(re.escape(kw), re.IGNORECASE)
            text = pattern.sub(lambda m: f"<span style=\"color:red\">{m.group(0)}</span>", text)
    return text
