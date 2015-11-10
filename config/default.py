#!/usr/bin/env python

import os

class Config(object):
    DEBUG      =True
    BASE_DIR   = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    SESSION_TYPE	= 'filesystem'
    SESSION_FILE_DIR	= os.path.join(BASE_DIR,'tmp')
    SESSION_USE_SIGNER	= True

    WEIXIN_TOKEN	= 'FkiQyDiRNEAAAAAA'
    WEIXIN_AESKEY	= 'AAAAAAAAAAAAAAjKPVlZ51JOYpkijv6qIYWyuUmjD'
    WEIXIN_CORPID	= 'wxAAAAAAAAAA7278'
    WEIXIN_AGTID	= '4'
    WEIXIN_SECRET	= 'AHJHAJHOQUIUJJIJKKJKJKJKJKJKJKJKJKJKkHE_C51vEwnH1VeiI_2bYrVi'
