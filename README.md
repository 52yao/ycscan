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

## 扫描逻辑
1、cors：构造恶意 Origin 头，检查响应中是否回显 Access-Control-Allow-Origin:</br>
2、死链：提取网页中引用的 JS 文件，检测是否存在无法访问的第三方 JS</br>
3、目录遍历：直接在url末尾怼关键词</br>
4、xss：构造无害但高识别度的 XSS payload，如【u】,【a】 (实际换成尖括号 )，检测返回包是否出现标识</br>
5、sql注入：注入 payload 到 URL 参数中，两个判断逻辑</br>
- 检测返回内容中是否包含数据库错误信息</br>
- 参数值后分别加上单引号、双引号，根据响应长度对比判断</br>

## todo
1、fuzz、ssrf、cmdinj模块是ai直接生成的，逻辑存在问题，待优化</br>
2、增加其他漏洞扫描模块</br>
3、报告支持关键词高亮</br>
4、开发图形化界面，支持傻瓜式操作，用户只需要输入待测试的url，点击开始，等待报告生成即可。</br>
</br>
本来想在国h前写一个“过的去”的扫描器，但是最后功能虽然越写越多，但是也越来越臃肿。只考虑能不能运行起来，别的方面啥也没管，一塌糊涂。</br>
最新版就不放出来了，这里是python写的第一版。</br>
后面用go重写，再放出来。如果没放就是又鸽了。</br>



