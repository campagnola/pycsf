from pyqtgraph.Qt import QtGui, QtCore
import re


class RichTextEdit(QtGui.QTextEdit):
    def __init__(self, *args):
        QtGui.QTextEdit.__init__(self, *args)
        self.setToolTip('Formatting keys:<br><b>bold: ctrl-b</b><br><i>italic: ctrl-i</i><br><span style="text-decoration: underline">underline: ctrl-u</span>')
        
    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_B and ev.modifiers() == QtCore.Qt.ControlModifier:
            if self.fontWeight() == QtGui.QFont.Normal:
                self.setFontWeight(QtGui.QFont.Bold)
            else:
                self.setFontWeight(QtGui.QFont.Normal)
        elif ev.key() == QtCore.Qt.Key_I and ev.modifiers() == QtCore.Qt.ControlModifier:
            self.setFontItalic(not self.fontItalic())
        elif ev.key() == QtCore.Qt.Key_U and ev.modifiers() == QtCore.Qt.ControlModifier:
            self.setFontUnderline(not self.fontUnderline())
        else:
            return QtGui.QTextEdit.keyPressEvent(self, ev)

    def toHtml(self):
        html = unicode(QtGui.QTextEdit.toHtml(self))
        
        # Strip off boilerplate html. This should make the JSON easier to
        # read without affecting the text.
        html = re.sub('.*<body [^>]+>', '', html.replace('\n', ''))
        html = re.sub('</body></html>', '', html)
        html = re.subn('</p>', '<br/>', html)[0]
        html = re.subn('<p [^>]+>', '', html)[0]
        
        return html.strip()
