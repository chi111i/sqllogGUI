sql盲注日志分析工具GUI版本

tshark -r blindsql.pcapng   -Y  "http.request.line" >1.txt
导出sql日志后，选择合适正则分析即可。

[参考项目](https://github.com/sqlsec/Sqlmap_Plaintext)

![demo](./demo.png)
