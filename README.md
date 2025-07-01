# ycscan
## 用法
python main.py http://example.com

## 结构说明
漏扫工具:
</br>
├─ main.py</br>
├─ crawler.py         <-- 爬虫模块</br>
├─ scanner/           <-- 漏洞扫描模块</br>
│   ├─ __init__.py</br>
│   ├─ cmdinj.py      <-- 命令执行漏洞</br>
│   ├─ cors.py        <-- cors漏洞</br>
│   ├─ deadjs.py      <-- 死链扫描</br>
│   ├─ dirtrav.py     <-- 目录遍历</br>
│   ├─ fuzz.py        <-- fuzz模块</br>
│   ├─ sqli.py        <-- sql注入漏洞</br>
│   ├─ ssrf.py        <-- ssrf漏洞</br>
│   ├─ xss.py         <-- xss漏洞</br>
├─ utils/</br>
│   ├─ __init__.py</br>
│   ├─ requester.py   <-- 请求封装模块</br>
│   └─ logger.py      <-- 日志生成模块</br>
└─ reporter.py        <-- 报告生成模块</br>



## todo
1、fuzz、ssrf、cmdinj模块是ai直接生成的，逻辑存在问题，待优化</br>
2、增加其他漏洞扫描模块</br>
3、报告支持关键词高亮</br>
