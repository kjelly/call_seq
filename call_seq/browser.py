import sys
from PySide import QtGui, QtCore
import json
import os
import copy

from TextEdit import Editor


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.main_editor = Editor()
        self.setCentralWidget(self.main_editor)
        self.createDockWindows()
        self.createMenuBar()
        self.createContextMenu()

    def createContextMenu(self):
        self.context_menu = QtGui.QMenu(self.tr("Caller"), self)
        self.caller_action = self.context_menu.addAction(self.tr("Calle&r"))
        self.caller_action.triggered.connect(self.show_caller_code)
        self.callee_action = self.context_menu.addAction(self.tr("Calle&e"))
        self.callee_action.triggered.connect(self.show_callee_code)



    def createMenuBar(self):
        openAction = QtGui.QAction('&open', self)
        openAction.triggered.connect(self.openFile)

        exitAction = QtGui.QAction('&Exit', self)
        exitAction.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

    def createDockWindows(self):
        self.tree_docker = QtGui.QDockWidget("Call Sequence", self)
        self.tree_widget = QtGui.QTreeWidget(self.tree_docker)
        self.tree_widget.itemClicked.connect(self.show_caller_code)
        self.tree_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.on_custom_context_menu)
        self.tree_docker.setWidget(self.tree_widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                           self.tree_docker)

        self.info_docker = QtGui.QDockWidget("Info", self)
        self.info_widget = QtGui.QTextEdit(self.info_docker)
        self.info_docker.setWidget(self.info_widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                           self.info_docker)

    def openFile(self, file_name=None):
        if not file_name:
            file_name, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        if not file_name:
            return
        with open(file_name, 'r') as ftr:
            call_seq = json.load(ftr)
        self.init_tree_widget(call_seq)

    def init_tree_widget(self, data):
        item = QtGui.QTreeWidgetItem()
        item.setText(0, '<top>')
        self.build_tree(item, data)
        self.tree_widget.addTopLevelItem(item)

    def build_tree(self, top, data):
        for i in data['seq']:
            item = QtGui.QTreeWidgetItem(top)
            if i.get('name', None):
                item.setText(0, i['name'])
            else:
                item.setText(0, i['caller_code'])
            item.meta_data = i
            name = self.build_tree(item, i)
            top.addChild(item)

    def show_caller_code(self, *args):
        item = self.tree_widget.currentItem()
        meta_data = item.meta_data

        self.go_to_file_line(meta_data['caller_file_name'], meta_data['lineno'])
        self.show_infomation(item)
        return True

    def show_callee_code(self, *args):
        item = self.tree_widget.currentItem()
        meta_data = item.meta_data

        self.go_to_file_line(meta_data['callee_file_name'], meta_data['callee_first_line'])
        self.show_infomation(item)
        return True

    def show_infomation(self, item):

        info_data = copy.copy(item.meta_data)
        del info_data['seq']
        self.info_widget.setText(json.dumps(info_data,
                                            sort_keys=True,indent=4,
                                            separators=(',', ': ')))

    def go_to_file_line(self, file_name, lineno):
        if not os.path.exists(file_name):
            return
        self.main_editor.openFile(file_name)
        self.main_editor.gotoLine(lineno)


    def on_custom_context_menu(self, point):
        index = self.tree_widget.indexAt(point)
        if index.isValid():
            self.context_menu.exec_(self.tree_widget.mapToGlobal(point))



def main():
    import sys
    app = QtGui.QApplication(sys.argv)

    ex = MainWindow()
    ex.show()
    if len(sys.argv) > 1:
        ex.openFile(sys.argv[1])
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



