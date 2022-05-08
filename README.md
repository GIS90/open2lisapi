> ## 简介

![](https://img.shields.io/badge/Language-Python-red)
![](https://img.shields.io/badge/DevStructure-Flask-0000FF)
![](https://img.shields.io/badge/DB-Mysql-green)
![](https://img.shields.io/badge/Tool-Gunicorn-FFFF00)
![](https://img.shields.io/badge/Tool-Supervisor-FFFF00)

项目简称：**_open2lisapi_**  
Python3语言进行研发，是支撑***OPENTOOL-Z***项目的后端API。

前端 **_open2lbox_**：https://github.com/GIS90/open2lbox.git

### 平台地址

```
线上地址：http://tool.pygo2.top/  
测试账号：test  
密码：123456
```

### 项目架构

项目基于**python3+flask+mysql+gunicorn+supervisor**进行搭建的一个web服务项目，备具Restful API、验证session、模板开发等功能。  
上个版本的脚手架可以使用模板功能，这个open2lisapi主要用来做API对接，所以只保留了API接口功能，如果想使用前端模板功能，直接在deploy目录下的templates、static下写入html、js等文件即可。  
***git clone***之后修改配置即可运行，在此基础上可进行二次开发，可以前端/后台独立、也可以运用flask的jinja2模板。

  - python 开发语言，基于python3.7
  - flask python语言使用的web框架
  - mysql 数据库
  - gunicorn web服务与应用app之间的管理
  - supervisor 项目进程的启动、停止、重启等管理
  
项目可以运行于Linux、Windows、Macos等系统上，建议使用Centos7.5，支持性较好，默认端口9999（可以etc中的config.yaml配置中进行更改，配置有开发模式配置与线上配置，后面有详细介绍）。

### 开发进度记录

记录信息采用了腾讯共享文档的方式记录API接口、数据库模型、开发周期等信息。

- 开发周期记录  
  https://docs.qq.com/sheet/DZmJZUlBuS1dla0Vw?tab=BB08J2

- 数据模型说明  
  https://docs.qq.com/sheet/DZmtvY2xTUE9LdlND?tab=BB08J2

> ## 项目说明

### 配置说明

项目配置主要有2套，位于项目的根目录etc下
  - dev 测试环境
  - prod 线上环境

每套配置文件夹下有3个配置文件，config与gunicorn进行绑定：
  - config：项目的db、mail、log等项目开发用的所有配置，这里的log记录项目的log，关于项目相关的配置都可以在此文件进行配置
  - gunicorn：项目启动时所需要的IP、port、log、进程数量等配置
  - supervisor: 项目进程管理的配置信息

.yaml格式的配置文件是有deploy/config.py进行解析的，如果在config.yaml配置文件中添加配置信息，需要在此文件进行解析添加，**建议添加配置默认值**。

### 环境搭建

  - Centos7.5系统服务器
  - Python3、mysql、supervisor等基础环境安装。
  - 安装好数据库之后，执行dbsql>sql.sql文件，里面配置数据库名称、用户名、密码等（根据需求改成项目需要的）
  - git clone https://github.com/GIS90/open2lisapi.git
  - 安装项目运行的环境：python install_env.py，建立项目独立的运行环境，安装了virtualenv、python、gunicorn、packages等操作，了解具体详情请参考install_env.py代码
  - 更新web配置文件：etc/prod/config.yaml（线上）、etc/dev/config.yaml（测试），根据不同需求进行配置更改
  - cd 项目根目录：source .venv/bin/activate：激活项目环境
  - 启动项目：
    - 线上：gunicorn -c etc/prod/gunicorn.conf
    - 测试：gunicorn -c etc/dev/gunicorn.conf
    - **_手动启动：下面有介绍_**  
    如果是测试或者开发，建议使用手动启动项目，关于dev/prod中的config.yaml配置信息详情请参考配置解析说明部分
  - 选做：安装supervisor && 项目加入supervisor进行管理，项目包含了supervisord配置文件&&项目supervisorctl配置文件
  
### 手动安装包

  - pip install -r requirements.txt

此程序运行于python3，其中requirements.txt项目所需要的包，已固定版本，如果使用了***install_env.py***一键式部署，则无须单独安装包。

### 手动启动

1.项目根目录wsgi.py文件，开启app.run(host="0.0.0.0", port=9999, debug=True)  
2.安装好项目运行环境，***source .venv/bin/activate***启动项目运行python
3.执行sudo python wsgi.py，代码目前已写入，处于注释状态  
4.通过手动启动的项目为dev开发环境配置，可在deploy/config.py中进行默认调整（mode = os.environ.get('mode') or 'dev'）  
5.如果手动启动模式开启，在gunicorn进行启动，会error: [Errno 48] Address already in use.

注意：启动项目一定要用virtualenv安装的python环境进行启动（source .venv/bin/activate）

> ## 开发特定点

### Excel合并与拆分

文件：deploy/utils/excel_lib.py

在开发Excel功能上，使用了openpyxl、xlwt && xlrd，但是都一些小问题，如下：
- openpyxl: 不支持.xls（老版本excel）
- xlwt、xlrd: 表格行数限制65535
只好，根据操作Excel数据文件的格式进行判断，去执行指定的方法，如果操作的数据文件包含一个.xls文件，就用xlwt、xlrd去处理，否则就用openpyxl。

> ## 其他

### supervisor

管理项目进程的启动、停止、重启等操作
安装：pip install supervisor
配置：
  - dev：etc/dev/supervisor_open2lisapi.conf
  - prod：etc/prod/supervisor_open2lisapi.conf

把指定环境的supervisor_open2lisapi.conf cp到/etc/supervisord.d/include/*下。  
项目root根目录下有supervisord.conf文件，用来配置supervisord，放在/etc/supervisord.d目录下。

### gunicorn

负责web项目进程、服务

安装：pip install gunicorn

配置：
  - dev：etc/dev/gunicorn.conf
  - prod：etc/prod/gunicorn.conf

如需特别项目启动信息，可以加入gunicorn.conf或者更改命令行gunicorn启动方式加入参数即可

### sql

sql：dbsql>sql.sql，直接执行即可，包含创建数据库、用户、表、索引等

### crontab

里面包含crontab定时任务，具体任务列表如下：
- auto_clear_logs.sh：日志清除任务
- mysql_backup_task.sh：数据库备份任务

crontab简单功能：
- crontab -e 编辑
- crontab -l 查看

### qiniu对象存储

官网开发手册Python API：https://developer.qiniu.com/kodo/1242/python

### 其他

  - install_env.py项目一键式环境部署，前提服务器上有python3、pip，直接执行这个脚本即可
  - ~~bash_start.bash、bash_end.bash为手动方式进行项目启动与项目结束（已废弃）~~
  - deploy>utils>utils.py 为工具方法，任何python项目都适合使用


> ## 联系方式

* ***Github:*** https://github.com/GIS90
* ***Email:*** gaoming971366@163.com
* ***Blog:*** http://pygo2.top
* ***WeChat:*** PyGo90


Enjoy the good life everyday！！！
