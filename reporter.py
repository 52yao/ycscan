# reporter.py
"""
报告模块（无 HTML）：
- 生成 Excel 和 Markdown 报告
- 报告保存到 report/ 文件夹中
"""

import os
import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

# 自动创建报告目录
REPORT_DIR = "report"
os.makedirs(REPORT_DIR, exist_ok=True)

# Excel 报告生成
def generate_excel_report(results):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(REPORT_DIR, f"report_{now}.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "漏洞报告"
    ws.append(["URL", "漏洞类型", "请求", "响应"])

    # 设置表头样式
    for row in ws.iter_rows(min_row=1, max_row=1):
        for cell in row:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center", vertical="center")

    for item in results:
        for key in item:
            if key.endswith("_found") and item[key]:
                prefix = key.replace("_found", "")
                ws.append([
                    item['url'],
                    prefix.upper(),
                    item.get(prefix + "_request", ""),
                    item.get(prefix + "_response", "")
                ])

    wb.save(filename)
    print(f"[✔] Excel 报告已保存: {filename}")


# Markdown 报告生成
def generate_markdown_report(results):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(REPORT_DIR, f"report_{now}.md")


    with open(filename, "w", encoding="utf-8") as f:
        f.write("# 漏洞扫描报告\n\n")

        for item in results:
            for key in item:
                if key.endswith("_found") and item[key]:
                    prefix = key.replace("_found", "")
                    f.write(f"## [{prefix.upper()}] {item['url']}\n\n")
                    f.write(f"**请求：**\n```\n{item.get(prefix + '_request','')}\n```\n")
                    f.write(f"**响应（截断）：**\n```\n{item.get(prefix + '_response','')}\n```\n\n")
    
    print(f"[✔] Markdown 报告已保存: {filename}")
