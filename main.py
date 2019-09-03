import os.path
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.template import Template
from tornado.escape import json_decode, json_encode

import module.datatables

from multiprocessing import Process, Queue

import conf
from tornado.options import define, options
define("port", default=conf.port, help="run on the given port", type=int)
define("debug", default=conf.debug, help="run on debug mode", type=bool)



class DefaultHandler(tornado.web.RequestHandler):
    def get(self, name, p0):
        page = __import__('pages.'+name, fromlist=[name])
        html = page.html(p0)

        if 'template' in html.keys() and html['template'] is not None:
            template = html['template'] + '.html'
        else:
            template = 'default.html'

        self.render(template, name=name, p0=p0, html=html)

class QueryHandler(tornado.web.RequestHandler):
    def get(self, name, p0):
        page = __import__('pages.'+name, fromlist=[name])
        out = page.query(p0)
        self.write(json.dumps(out))

class UpdateHandler(tornado.web.RequestHandler):
    def post(self, name, p0, field):
        page = __import__('pages.'+name, fromlist=[name])

        db_id = self.get_argument('id')
        value = self.get_argument('value')

        is_ok = page.update(p0, db_id, field, value)
        if is_ok:
            self.write(value)


def _update_process(q):
    print('update_process ready!')
    while True:
        #if not q.empty():
        name, p0, db_id, field, value = q.get(True)
        print('q:', name, p0, db_id, field, value)
        page = __import__('pages.'+name, fromlist=[name])
        page.update_thread(p0, db_id, field, value)


if __name__ == "__main__":
    if conf.queue:
        q = Queue()
        conf.queue = q
        db_process = Process(target=_update_process, args=(q,))
        db_process.start()

    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/" + conf.site + r"_query/(.+)/(.+)", QueryHandler),
            (r"/" + conf.site + r"_update/(.+)/(.+)/(.+)", UpdateHandler),
            (r"/" + conf.site + r"(.+)/(.+)", DefaultHandler),
        ],
        ui_modules={
            'DataTables': module.datatables.DataTablesModule
        },
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        debug = options.debug
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
