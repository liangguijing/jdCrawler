多线程爬取京东商品信息并储存到MySql DB

安装所需第三方库
```shell
pip install requests mysqlclient
```
windows安装mysqlclient:
下载对应版本的whl文件
[https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)
```shell
pip install mysqlclient-1.4.6-cp38-cp38-win32.whl
```

修改配置文件，运行crawler.py即可
