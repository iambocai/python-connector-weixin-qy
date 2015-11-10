#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# Author: iambocai
# Created Time: Thu 11 Sep 2015 03:55:41 PM CST
# File Name: Callback.py
# Description: 主动调用微信接口
#########################################################################

from flask import current_app
from flask import render_template
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import requests
import time
import json


class AccessToken:
    def __init__(self,sCorpID,sSecrect):
        self.access_token = None
        self.expires_in = 0
        self.timestamp = 0
        if not self.refreshToken(sCorpID,sSecrect):
            raise ValueError,'access_token not initaled, please check you config first !!'

    def refreshToken(self,sCorpID,sSecrect):
        currtime = time.time()
        if currtime - self.timestamp >= self.expires_in :
            url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' %(sCorpID,sSecrect)
            ret = json.loads(requests.get(url).content)
            if ret.has_key('access_token'):
                self.access_token = ret['access_token']
                self.expires_in = ret['expires_in']
                self.timestamp = currtime
                urrent_app.logger.debug('new access_token:'+self.access_token)
                return True
            else:
                current_app.logger.debug('get ak failed:'+json.dumps(ret))
                return False
        else:
            current_app.logger.debug('old access_token:'+self.access_token)
            return True
 

class Weixin:

    def __init__(self):
        config = current_app.config
        self.corpid = config.get('WEIXIN_CORPID');
        self.secrect= config.get('WEIXIN_SECRET');
        self.agentid= config.get('WEIXIN_AGTID');
        access = AccessToken(self.corpid, self.secrect)
        self.access_token = access.access_token

    def sendMsg(self, arrMsg):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % (self.access_token)
        return json.loads(requests.post(url, data=arrMsg).content)

    def sendText(self,sToUser,sText):
        postdata = { 
            "touser": sToUser,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": sText
            },
            "safe":"1"
        }
        #current_app.logger.debug('sendText:'+json.dumps(postdata))
        return self.sendMsg(json.dumps(postdata))

    def listDepartment(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token=%s' % (self.access_token)
        return json.loads(requests.get(url).content)


    def listUser(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token=%s&department_id=1&fetch_child=1&status=0' % (self.access_token)
        return json.loads(requests.get(url).content)
