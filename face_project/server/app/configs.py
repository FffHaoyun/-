# -*- coding: utf-8 -*-
import os
from app.ui.ui_page import PageUI

root_path = os.path.dirname(__file__)

# 公共配置
configs = dict(
    #加入xsrf跨站伪装登录保护，防止别人跨域请求
    xsrf_cookies = True,
    cookie_secret = '38980fc347fe412a8fd3f992132bb7e0',#使用uuid.uuid4().hex获取

    static_path=os.path.join(root_path, 'static'),
    template_path=os.path.join(root_path,'templates'),
    ui_modules=dict(
      page=PageUI
    ),
    debug=True  # True开启调试模式
)

# mongodb配置
mongodb_configs = dict(
    db_host='127.0.0.1',
    db_port=27017
)
