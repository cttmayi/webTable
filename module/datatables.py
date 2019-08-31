import tornado.web


class DataTablesModule(tornado.web.UIModule):
    def render(self, id, p0, datatables):
        return self.render_string(
            "modules/datatables.html",
            id = id,
            p0 = p0,
            datatables = datatables
        )

    #def html_body(self):
    #    return "<div class=\"addition\"><p>html_body()</p></div>"

    #def embedded_javascript(self):
    #    return "document.write(\"<p>embedded_javascript()</p>\")"

    #def embedded_css(self):
    #    return ".addition {color: #A1CAF1}"

    def css_files(self):
        return [
            "https://cdn.datatables.net/1.10.15/css/jquery.dataTables.min.css",
        ]

    def javascript_files(self):
        return [
            "https://cdn.datatables.net/1.10.15/js/jquery.dataTables.min.js", 
            "/static/jeditable/jquery.jeditable.js",
        ]