# -*- coding: utf-8 -*-
import json
import tornado.gen
import tornado.concurrent
from app.api.views_common import CommonHandler


class IndexHandler(CommonHandler):
    # 定义一个GET请求方法
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.get_response()


    #让阻塞的代码在线程池里运行
    @tornado.concurrent.run_on_executor()
    def get_response(self):
        # self.write("<h1 style='color:blue'>这是一个API接口</h1>")
        # self.write("<h1 style='color:red'>{}</h1>".format(str(self.md)))
        self.write(self.common_params) #字典默认转化为json响应给浏览器端


