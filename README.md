# bilibili_meter
## B站数据采集监控工具

示例：https://gravitykey.top/bilibilimeter


###  简介
Flask + mysql 提供后台API，使用DBUtils连接池，自行魔改了廖雪峰的异步ORM，改为多线程可用，自行实现了简易雪花算法来生成数据ID。

手写爬虫，并且使用较简易的通信认证来确保安全性。

前端使用Vue + VueCli + Echarts + ElementUI 实现。


### 配置
#### pip安装依赖（略）

#### 生成初始化数据库的sql语句
```
python make_init_sql.py > sql.txt
```
然后执行此sql命令

#### 编辑配置文件
```
位置在 ./bilibili_meter/config.py
```

#### 新建管理员账户
```
python add_web_user.py -add [administrator_name] [youer_password]

然后提升权限

python add_web_user.py -setadmin [administrator_name] true
```

#### 配置Gunicorn，supervisor

示例文件见_gunicorn.conf，_supervisor.conf



#### 另：运行爬虫
```
python run_scraper.py
```
配置文件同在 `./bilibili_meter/config.py`，爬虫会自动轮询服务器并提交结果。


#### 前端工程路径

```
./vue-front/v01/
```
一些配置项
```
./vue-front/v01/src/config.js
```