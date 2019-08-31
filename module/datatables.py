import tornado.web


class DataTablesModule(tornado.web.UIModule):
    def render(self, name, p0, datatables):
        return self.render_string(
            "modules/datatables.html",
            name = name,
            p0 = p0,
            datatables = datatables
        )

    def css_files(self):
        return [
            "https://cdn.datatables.net/1.10.15/css/jquery.dataTables.min.css",
        ]

    def javascript_files(self):
        return [
            "https://cdn.datatables.net/1.10.15/js/jquery.dataTables.min.js", 
            "/static/jeditable/jquery.jeditable.js",
        ]