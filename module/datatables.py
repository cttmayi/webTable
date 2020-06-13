import tornado.web
import conf

def th(name, field, width='*', editor='text', data=[]):
    map_data = {}
    for d in data:
        map_data[d] = d

    return {
        'name': name, 
        'field': field,
        'width': width, 
        'editor': editor, 
        'data': str(map_data)}



class DataTablesModule(tornado.web.UIModule):
    def _datatables(self, datatables):
        if 'number' not in datatables.keys():
            datatables['number'] = False
        if 'order' in datatables.keys():
            datatables['order'] = str(datatables['order'])
        if 'th' not in datatables.keys() or len(datatables['th']) == 0:
            datatables['th'] = [th('ID', 'id')]
        if 'id' not in datatables.keys():
            datatables['id'] = datatables['th'][0]['field']
        return datatables

    def render(self, name, p0, datatables):
        return self.render_string(
            "modules/datatables.html",
            name = name,
            p0 = p0,
            datatables = self._datatables(datatables),
            conf = conf,
        )

    def css_files(self):
        return [
            "https://cdn.datatables.net/1.10.15/css/jquery.dataTables.min.css",
            #'https://cdn.datatables.net/buttons/1.5.6/css/buttons.dataTables.min.css',
        ]

    def javascript_files(self):
        return [
            "https://cdn.datatables.net/1.10.15/js/jquery.dataTables.min.js", 
            "https://cdn.bootcss.com/jeditable.js/2.0.13/jquery.jeditable.js",
            'https://cdn.datatables.net/buttons/1.5.6/js/dataTables.buttons.min.js',
            'https://cdn.datatables.net/buttons/1.5.6/js/buttons.flash.min.js',
            'https://cdn.datatables.net/buttons/1.5.6/js/buttons.html5.min.js',
            'https://cdn.datatables.net/buttons/1.5.6/js/buttons.print.min.js',
        ]