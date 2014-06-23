from PySide import QtGui, QtCore
from .JsonWidgetWrapper import JsonWidgetWrapper


class InfoWidgetWrapper(object):
    def __init__(self, parent, go_to_line_func=None):
        super(InfoWidgetWrapper, self).__init__()
        self.data = None
        self.go_to_line_func = go_to_line_func

        self.json_widget_wrapper = JsonWidgetWrapper(parent)
        self.widget = self.json_widget_wrapper.widget
        self.json_widget_wrapper.triggered.connect(self.handle_info_widget_item_click)

    @QtCore.Slot(int, int)
    def handle_info_widget_item_click(self, key, value):
        if key in ['return_lineno', 'return']:
            self.go_to_line_func(self.data['callee_file_name'], self.data['return_lineno'])
        elif key in ['callee_first_line', 'name', 'arguments', 'callee_file_name']:
            self.go_to_line_func(self.data['callee_file_name'], self.data['callee_first_line'])
        elif key in ['caller_code', 'caller_file_name', 'lineno']:
            self.go_to_line_func(self.data['caller_file_name'], self.data['lineno'])


    def set_data(self, data):
        self.data = data
        self.json_widget_wrapper.set_data(data)
