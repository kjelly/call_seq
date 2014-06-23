from PySide import QtCore, QtGui
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
from pyqode.core.modes import CaretLineHighlighterMode
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
        self.docPanel = QuickDocPanel()

        self.installPanel(self.docPanel, pyqode.core.PanelPosition.BOTTOM)
        self.installMode(CommentsMode())
        self.installMode(CaretLineHighlighterMode())
        self.saveOnFrameDeactivation = False

        self.hotkey_action_map = {
            '#': self.selectWordUnderCursorAndSearchBackward,
            'p': self.selectWordUnderCursorAndSearchBackward,
            '*': self.selectWordUnderCursorAndSearchForward,
            'n': self.selectWordUnderCursorAndSearchForward,
            'j': self.moveCursorDown,
            'k': self.moveCursorUp,
            'K': self.docPanel._onQuickDoc_triggered,
            'W': self.moveCursorWordLeft,
            'w': self.moveCursorWordRight,
        }

    def keyPressEvent(self, event):
        """
        Overrides the keyPressEvent to emit the keyPressed signal.

        Also takes care of indenting and handling smarter home key.

        :param event: QKeyEvent
        """
        self.hotkey_action_map.get(event.text(), self.doNothing)()
        # import pdb;pdb.set_trace()
        return True

    def keyReleaseEvent(self, event):
        """
        Overrides keyReleaseEvent to emit the keyReleased signal.

        :param event: QKeyEvent
        """
        return True

    def selectWordUnderCursorAndSearchForward(self):
        tc = self.selectWordUnderCursor(True)
        self.setTextCursor(tc)
        self.find(self.selectedText(), QtGui.QTextDocument.FindWholeWords)

    def selectWordUnderCursorAndSearchBackward(self):
        tc = self.selectWordUnderCursor(True)
        self.setTextCursor(tc)
        self.find(self.selectedText(), QtGui.QTextDocument.FindWholeWords |
                                       QtGui.QTextDocument.FindBackward)

    def doNothing(self):
        return True

    def moveCursorDown(self):
        self.moveCursor(QtGui.QTextCursor.Down)

    def moveCursorUp(self):
        self.moveCursor(QtGui.QTextCursor.Up)

    def moveCursorWordLeft(self):
        self.moveCursor(QtGui.QTextCursor.WordLeft)

    def moveCursorWordRight(self):
        self.moveCursor(QtGui.QTextCursor.WordRight)
