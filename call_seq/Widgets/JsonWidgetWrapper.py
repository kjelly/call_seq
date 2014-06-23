from PySide import QtGui, QtCore


class JsonWidgetWrapper(QtCore.QObject):
    triggered = QtCore.Signal(str, str)

    def __init__(self, parent):
        super(JsonWidgetWrapper, self).__init__()

        self.widget = QtGui.QTreeWidget(parent)
        self.widget.setColumnCount(2)
        self.widget.setHeaderLabels(['key', 'value'])
        self.widget.itemActivated.connect(self.emit_triggered_signal)


    def set_data(self, data):
        item = QtGui.QTreeWidgetItem(self.widget)
        self.build_tree(item, data)
        self.widget.takeTopLevelItem(0)
        self.widget.addTopLevelItem(item)
        self.widget.expandAll()


    def build_tree(self, parent, data):
        if isinstance(data, list):
            parent.setText(1, 'list')
            self.build_tree_from_list(parent, data)
        elif isinstance(data, dict):
            parent.setText(1, 'dict')
            self.build_from_dict(parent, data)
        else:
            self.build_tree_from_obj(parent, data)

    def build_tree_from_obj(self, parent, data):
        parent.setText(1, '%s' % (str(data)))

    def build_from_dict(self, parent, data):
        for key in sorted(data.keys()):
            value = data[key]
            item = QtGui.QTreeWidgetItem(parent)
            item.setText(0, str(key))
            self.build_tree(item, value)
            parent.addChild(item)

    def build_tree_from_list(self, parent, data):
        for key, value in enumerate(data):
            item = QtGui.QTreeWidgetItem(parent)
            self.build_tree(item, value)
            parent.addChild(item)

    def emit_triggered_signal(self, item, column):
        self.triggered.emit(item.text(0), item.text(1))


def main():
    import sys
    app = QtGui.QApplication(sys.argv)

    wrapper = JsonWidgetWrapper(None)
    wrapper.set_data({'a': 1, 'b': 2, 'c': 3, 'd': 5})
    wrapper.widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
