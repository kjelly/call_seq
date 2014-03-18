import sys
from PySide import QtGui, QtCore
import json
import os

from TextEdit import Editor


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.main_editor = Editor()
        self.setCentralWidget(self.main_editor)
        self.createDockWindows()
        self.createMenuBar()

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
        self.tree_widget.itemClicked.connect(self.item_clicked)
        self.tree_docker.setWidget(self.tree_widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                           self.tree_docker)

        self.info_docker = QtGui.QDockWidget("Info", self)
        self.info_widget = QtGui.QTextEdit(self.info_docker)
        self.info_docker.setWidget(self.info_widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                           self.info_docker)

    def openFile(self):
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
            item.setText(0, i['code'])
            item.meta_data = i
            self.build_tree(item, i)
            top.addChild(item)
        return top

    def item_clicked(self, item, column):
        meta_data = item.meta_data
        file_name = meta_data['file_name']
        if not os.path.exists(file_name):
            return
        self.main_editor.openFile(file_name)
        self.main_editor.gotoLine(meta_data['lineno'])
        #with open(file_name, 'r') as ftr:
        #    self.main_editor.setText(ftr.read())

        info = ''
        format = '%s: %s\n' + '-' * 10 + '\n'
        for i in meta_data:
            if i == 'seq':
                continue
            info += format % (i, meta_data[i])
        self.info_widget.setText(info)


def main():
    app = QtGui.QApplication(sys.argv)

    ex = MainWindow()
    ex.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
