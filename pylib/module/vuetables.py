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
        if 'name' not in values:
            values['name'] = 'app' 

        if 'toolbar' not in values:
            values['toolbar'] = []

        if 'computed' in values:
            if 'name' not in values['computed']:
                values['computed']['name'] = ''

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