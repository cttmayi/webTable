# -*- coding: utf-8 -*-

import os.path
import json

import tornado.autoreload

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.template import Template
from tornado.escape import json_decode, json_encode

import pylib.module.datatables
import pylib.module.vuetables

from multiprocessing import Process, Queue

import conf
from tornado.options import define, options
define("port", default=conf.port, help="run on the given port", type=int)
define("debug", default=conf.debug, help="run on debug mode", type=bool)


# class BaseHandler(tornado.web.RequestHandler):
#     def __init__(self, *argc, **argkw):
#         super(BaseHandler, self).__init__(*argc, **argkw)
        
#     # 解决跨域问题
#     def set_default_headers(self):
#         print('set_default_headers')
#         self.set_header("Access-Control-Allow-Origin", "*")    # 这个地方可以写域名
#         self.set_header("Access-Control-Allow-Headers", "x-requested-with")
#         self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
#         self.set_header("Access-Control-Max-Age", 1000) 
#         self.set_header("Content-type", "application/json")


#     def options(self):
#         print('options')
#         self.set_status(204)
#         self.finish()
#         self.write('{"errorCode":"00","errorMessage","success"}')


class DefaultHandler(tornado.web.RequestHandler):
    def get(self, name, p0='_', p1='_'):
        page = pages[name]
        html = page.html(p0, p1)

        if 'template' in html.keys() and html['template'] is not None:
            template = html['template'] + '.html'
        else:
            template = 'default.html'

        self.render(template, name=name, p0=p0, p1=p1, html=html)


class QueryHandler(tornado.web.RequestHandler):
    def get(self, name, p0, p1):
        page = pages[name]
        out = page.query(p0, p1)
        self.write(json.dumps(out))


class UpdateHandler(tornado.web.RequestHandler):
    def post(self, name, p0, p1):
        page = pages[name]

        db_id = self.get_argument('id')
        field = self.get_argument('field')
        value = self.get_argument('value')

        is_ok = page.update(p0, p1, db_id, field, value)
        if is_ok:
            self.write(value)


class InsertHandler(tornado.web.RequestHandler):
    def get(self, name, p0, p1):
        page = pages[name]

        out = page.insert(p0, p1)
        self.write(json.dumps(out))

class DeleteHandler(tornado.web.RequestHandler):
    def post(self, name, p0, p1):
        page = pages[name]

        db_id = self.get_argument('id')
        db_id = page.delete(p0, p1, db_id)

        self.write(str(db_id))


def _update_process(q):
    # print('update_process ready!')
    while True:
        #if not q.empty():
        name, p0, p1, db_id, field, value = q.get(True)
        print('q:', name, p0, p1, db_id, field, value)
        page = __import__('pages.'+name, fromlist=[name])
        page.update_thread(p0, p1, db_id, field, value)

pages = {}

def init_page():
    name = 'example'
    pages[name] = __import__('pages.'+name, fromlist=[name])

if __name__ == "__main__":
    init_page()

    if conf.queue:
        q = Queue()
        conf.queue = q
        db_process = Process(target=_update_process, args=(q,))
        db_process.start()

    tornado.options.options.logging = "info"
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/" + conf.site + r"_query/(.+)/(.+)/(.+)", QueryHandler),
            (r"/" + conf.site + r"_update/(.+)/(.+)/(.+)", UpdateHandler),
            (r"/" + conf.site + r"_insert/(.+)/(.+)/(.+)", InsertHandler),
            (r"/" + conf.site + r"_delete/(.+)/(.+)/(.+)", DeleteHandler),
            (r"/" + conf.site + r"(.+)/(.+)/(.+)", DefaultHandler),
            (r"/" + conf.site + r"(.+)/(.+)", DefaultHandler),
            (r"/" + conf.site + r"(.+)", DefaultHandler),
        ],
        ui_modules={
            # 'DataTables': module.datatables.DataTablesModule,
            'VueTables': pylib.module.vuetables.VueTablesModule,
        },
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        debug = options.debug
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
