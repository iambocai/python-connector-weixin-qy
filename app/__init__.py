#!/usr/bin/env python
# coding: UTF-8

from flask import Flask
from flask.ext.session import Session

from config import load_config  # 绝对导入
from flask import current_app

import json


app = Flask(__name__)
config = load_config()
app.config.from_object(config)

sess = Session()

from app import views

