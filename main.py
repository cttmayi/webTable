import os.path
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.template import Template
from tornado.escape import json_decode, json_encode

import module.datatables

from tornado.options import define, options
define("port", default=80, help="run on the given port", type=int)
define("debug", default=True, help="run on debug mode", type=bool)



class DefaultHandler(tornado.web.RequestHandler):
    def get(self, id, p0):
        page = __import__('pages.'+id, fromlist=[id])
        html = page.html(p0)

        if 'template' in html.keys() and html['template'] is not None:
            template = html['template'] + '.html'
        else:
            template = 'default.html'

        self.render(template, id=id, p0=p0, html=html)

class QueryHandler(tornado.web.RequestHandler):
    def get(self, id, p0):
        page = __import__('pages.'+id, fromlist=[id])
        out = page.query(p0)
        self.write(json.dumps(out))

class UpdateHandler(tornado.web.RequestHandler):
    def post(self, id, p0, field):
        page = __import__('pages.'+id, fromlist=[id])
        #data = json_decode(self.request.body)

        id = self.get_argument('id')
        value = self.get_argument('value')

        is_ok = page.update(p0, id, field, value)
        if is_ok:
            self.write(value)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/_query/(.+)/(.+)", QueryHandler),
            (r"/_update/(.+)/(.+)/(.+)", UpdateHandler),
            (r"/(.+)/(.+)", DefaultHandler),
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
