from PySide import QtCore
import pyqode.python


# public API
from pyqode.python.bootstrapper import Bootstrapper
from pyqode.python.modes import PyAutoCompleteMode
from pyqode.python.modes import CalltipsMode
from pyqode.python.modes import CommentsMode
from pyqode.python.modes import PyCodeCompletionMode, JediCompletionProvider
from pyqode.python.modes import PEP8CheckerMode
from pyqode.python.modes import PyAutoIndentMode
from pyqode.python.modes import PyFlakesCheckerMode
from pyqode.python.modes import PyHighlighterMode
from pyqode.python.modes import PyIndenterMode
from pyqode.python.modes import DEFAULT_DARK_STYLES
from pyqode.python.modes import DEFAULT_LIGHT_STYLES
from pyqode.python.modes import GoToAssignmentsMode
from pyqode.python.modes import DocumentAnalyserMode
from pyqode.python.panels import PreLoadPanel
from pyqode.python.panels import SymbolBrowserPanel
from pyqode.python.panels import QuickDocPanel


class RichTextEdit(pyqode.core.QCodeEdit):
    def __init__(self):
        super(RichTextEdit, self).__init__()
        self.setLineWrapMode(self.NoWrap)
        self.installPanel(pyqode.core.LineNumberPanel(),
                          pyqode.core.PanelPosition.LEFT)
        self.installMode(pyqode.core.ZoomMode())
        #self.installMode(pyqode.core.FileWatcherMode())
        self.installMode(pyqode.core.SymbolMatcherMode())
        self.installMode(pyqode.core.WordClickMode())
        self.installMode(PyHighlighterMode(self.document()))
        self.installMode(PyAutoIndentMode())
        self.installMode(PyFlakesCheckerMode())
        self.installMode(PEP8CheckerMode())
        self.installMode(CalltipsMode())
        self.installMode(PyIndenterMode())
        self.installMode(GoToAssignmentsMode())
        self.installPanel(QuickDocPanel(), pyqode.core.PanelPosition.BOTTOM)
        self.installMode(CommentsMode())
        self.setReadOnly(True)
