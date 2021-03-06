# weiboCrawl

#### 介绍
微博爬虫保存到mysql并使用flask展示

#### 软件架构
软件架构说明


#### 安装教程

server 端:(flask)
1.  mysql创建数据库和用户

    ```
    create database weibo;
    create user 'webuser'@'localhost' identified by '123456';
    ```
    授权用户
    ```
    grant all privileges on weibo.* to 'webuser'@'localhost';
    ```

2.  mysql恢复数据

    恢复mysql: ```mysql -uwebuser -p weibo < weibo_db.sql``` 密码:123456

3.  配置flask运行环境

    进入webServer文件夹

    ```
    pipenv install
    ```
    
    **如果提示没有pipenv**

    可以使用```pip install pipenv```来安装

    然后使用```pipenv shell```进入虚拟环境

    **flask 版本必须小于2.0 falsk-migrate 必须小于3.0**
4.  启动web服务

    ```python run app.py```
    访问http://localhost:5001可以查看项目

#### 使用说明

1.  xxxx
2.  xxxx
3.  xxxx

#### 数据备份恢复

    进入webServer

    备份mysql: ```mysqldump -uwebuser -p weibo > weibo_db.sql``` 密码:123456

    恢复mysql: ```mysql -uwebuser -p weibo < weibo_db.sql``` 密码:123456


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
