微信企业号对接代码-Python版
==============================

<strong><red>请注意，请先配置再运行！默认配置只是参考！</red></strong>

1. 系统要求
--------------

Python >=2.6

Flask 最新版

Flask-Session

requests[secure] （HTTPS支持）

__如果secure安装不成功（GFW，哈哈），请自行为app/weixin/Call.py中所有requests.get调用添加verify=True参数以略过SSL证书检查。__

推荐使用virtualenv以方便业务部署

2. 配置文件
--------------

config/default.py

参考[hustlzp的博客分享](http://www.hustlzp.com/post/2014/08/flask-config)以获取更多环境相关配置的方法



企业号接口文档：https://qy.weixin.qq.com/wiki/index.php?title=首页

企业体验号申请：https://qy.weixin.qq.com/try

<strong>如果需要获取通讯录信息或者通过程序管理企业号的通讯录，企业号需要开启回调模式，并新建管理组</strong>

3. 示例调用
--------------

app/views.py


4. 运行方式
--------------

debug模式: python run.py

daemon模式: ./control start|stop|restart
