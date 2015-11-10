#!/usr/bin/env python
# coding: UTF-8

from flask import render_template, flash, abort, redirect, session, url_for, request, make_response, g
from app import app
from app.weixin.Callback import Callback
from app.weixin.Call import Weixin
import json
import random
from datetime import datetime
from datetime import timedelta
import time
import requests


@app.route('/weixin/listUser')
def weixin_listUser():
    weixin = Weixin()
    ret = weixin.listUser()
    if ret['errcode'] != 0:
        abort(503)
    return json.dumps(ret)

@app.route('/weixin/listDepartment')
def weixin_listDepartment():
    weixin = Weixin()
    ret = weixin.listDepartment()
    if ret['errcode'] != 0:
        abort(503)
    return json.dumps(ret)

@app.route('/weixin/sendText/<userid>/<text>')
def weixin_sendText(userid, text):
    weixin = Weixin()
    ret=weixin.sendText(userid, text)
    return json.dumps(ret)

@app.route('/weixin/callback', methods=['GET', 'POST'])
def weixin_callback():

    msg_signature = request.args.get('msg_signature','')
    timestamp = request.args.get('timestamp','')
    nonce = request.args.get('nonce','')
    app.logger.debug("%s,%s,%s" % (msg_signature,timestamp,nonce))

    cb = Callback()

    # 在回调模式下，只有验证时的请求是GET，这时候只要返回echostr即可
    # 见 http://qydev.weixin.qq.com/wiki/index.php?title=%E5%9B%9E%E8%B0%83%E6%A8%A1%E5%BC%8F
    if request.method == 'GET':
        echostr = request.args.get('echostr','')
        app.logger.debug(echostr)
        ohcestr = cb.validate(msg_signature,timestamp,nonce,echostr)
        return render_template('weixin/echo.html', ohcestr=ohcestr), 200
    else:
        # POST请求，是微信回调(微信把用户的输入以及一些特定事件通过此方式通知企业），微信发来的消息是xml格式的，并且经过加密，需要用专用的解密算法解密
        # 见 http://qydev.weixin.qq.com/wiki/index.php?title=%E5%9B%9E%E8%B0%83%E6%A8%A1%E5%BC%8F
        body = request.get_data()
        msg = cb.decode(msg_signature,timestamp,nonce,body)
        app.logger.debug(msg)
        # 从消息中可以获取相关信息，我们包装了一小部分常用的，业务可以根据自己需要再继续封装
        msg_from = cb.getFromUser(msg)
        msg_type = cb.getMsgType(msg)
        if msg_type == 'text':
           text = cb.getText(msg)
           return make_response(cb.mkTextMsg(msg_from, text), 200)
        elif msg_type == 'event':
           event = cb.getEvent(msg)
           if event == 'enter_agent':
              news = [
                  {   'title':'API测试',
                      'description':'',
                      'picurl':'http://upload.univs.cn/2012/1120/thumb_940__1353374661982.jpg',
                      'url':''
                  },

                  {   'title':'获取用户列表',
                      'description':'',
                      'picurl':'http://v1.qzone.cc/pic/201507/12/16/16/55a22256bc474195.jpg%21600x600.jpg',
                      'url':url_for('weixin_listUser')
                  },

                  {   'title':'获取部门列表',
                      'description':'',
                      'picurl':'http://v1.qzone.cc/pic/201507/12/16/16/55a22256bc474195.jpg%21600x600.jpg',
                      'url':url_for('weixin_listDepartment')
                  }
              ]
              return make_response(cb.mkNewsMsg(msg_from, news), 200)
