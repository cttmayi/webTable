import tornado.web
import conf

def th(name, field, width='*', editor='text', data=[]):
    list_data = []
    for d in data:
        list_data.append({ 'label': d, 'value': d })

    return {
        'name': name, 
        'field': field,
        'width': width, 
        'editor': editor, 
        'data': str(list_data)
    }

class VueTables:
    def __init__(self):
        pass


class VueTablesModule(tornado.web.UIModule):
    def __values(self, values):
        return values

    def render(self, name, p0, p1, values):
        return self.render_string(
            "modules/vuetables.html",
            name = name,
            p0 = p0,
            p1 = p1,
            values = self.__values(values),
            conf = conf,
        )


    # def css_files(self):
    #     return [
    #         "https://cdn.datatables.net/1.10.15/css/jquery.dataTables.min.css",
    #     ]

    # def javascript_files(self):
    #     return [
    #         "https://cdn.jsdelivr.net/npm/vue",
    #         "https://cdn.jsdelivr.net/npm/xe-utils",
    #         "https://cdn.jsdelivr.net/npm/vxe-table",
    #         "https://unpkg.com/axios/dist/axios.min.js",
    #     ]