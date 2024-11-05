from . import qt

Ui_constraintEditor = qt.importTemplate('.constraintEditorTemplate')


class ConstraintEditorWidget(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.ui = Ui_constraintEditor()
        self.ui.setupUi(self)
