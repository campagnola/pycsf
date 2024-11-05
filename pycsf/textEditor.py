import re
from . import qt


class RichTextEdit(qt.QTextEdit):
    def __init__(self, *args):
        qt.QTextEdit.__init__(self, *args)
        self.setToolTip('Formatting keys:<br><b>bold: ctrl-b</b><br><i>italic: ctrl-i</i><br><span style="text-decoration: underline">underline: ctrl-u</span>')
        
    def keyPressEvent(self, ev):
        if ev.key() == qt.Qt.Key_B and ev.modifiers() == qt.Qt.ControlModifier:
            if self.fontWeight() == qt.QFont.Normal:
                self.setFontWeight(qt.QFont.Bold)
            else:
                self.setFontWeight(qt.QFont.Normal)
        elif ev.key() == qt.Qt.Key_I and ev.modifiers() == qt.Qt.ControlModifier:
            self.setFontItalic(not self.fontItalic())
        elif ev.key() == qt.Qt.Key_U and ev.modifiers() == qt.Qt.ControlModifier:
            self.setFontUnderline(not self.fontUnderline())
        else:
            return qt.QTextEdit.keyPressEvent(self, ev)

    def toHtml(self):
        html = str(qt.QTextEdit.toHtml(self))
        
        # Strip off boilerplate html. This should make the JSON easier to
        # read without affecting the text.
        html = re.sub('.*<body [^>]+>', '', html.replace('\n', ''))
        html = re.sub('</body></html>', '', html)
        html = re.subn('</p>', '<br/>', html)[0]
        html = re.subn('<p [^>]+>', '', html)[0]
        
        return html.strip()
