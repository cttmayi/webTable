import tornado.web
import conf

def th(name, field, width='*', editor='text', data=[]):
    options = []
    for d in data:
        options.append({ 'label': d, 'value': d })

    return {
        'name': name,
        'field': field,
        'width': width,
        'editor': editor,
        'options': options
    }


class VueTablesModule(tornado.web.UIModule):
    def __get_values(self, values, key, def_value=None):
        if key in values:
            self.values[key] = values[key]
        elif def_value is not None:
            self.values[key] = def_value


    def __values(self, values):
        self.values = {}
        self.values['prop'] = {}

        self.__get_values(values, 'name', 'app')
        self.__get_values(values, 'id', '_id')
        self.__get_values(values, 'toolbar', [])
        self.__get_values(values, 'search', [])
        self.__get_values(values, 'height', 'auto')

        if 'computed' in values:
            if 'name' not in values['computed']:
                values['computed']['name'] = ''

        self.__get_values(values, 'computed')
        self.__get_values(values, 'summary')

        self.values['th'] = []
        self.values['search_fields'] = []


        for th in values['th']:
            if 'width' not in th:
                th['width'] = '*'

            if th['width'] == '*':
                if 'min-width' not in th:
                    th['min-width'] = '200'

            if 'editor' not in th:
                th['editor'] = 'text'

            if 'sortable' not in th:
                th['sortable'] = 'true'

            if 'options' in th:
                for i in range(len(th['options'])):
                    op = th['options'][i]
                    if isinstance(op, str):
                        th['options'][i] = { 'label': op, 'value': op }
            if 'tooltip' in th:
                self.values['tooltip'] = 'enable'

            if not ('search' in th and th['search'] == 'false'):
                if 'field' in th:
                    self.values['search_fields'].append(th['field'])

            self.values['th'].append(th)

        self.__get_values(values, 'row_style')
        self.__get_values(values, 'default_sort')
        self.__get_values(values, 'extend')

        return self.values


    def render(self, name, p0, p1, values):
        return self.render_string(
            "modules/vuetables.html",
            name = name,
            p0 = p0,
            p1 = p1,
            values = self.__values(values),
            conf = conf,
        )