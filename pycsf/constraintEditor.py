from pyqtgraph.Qt import QtWidgets, QtCore
from .constraintEditorTemplate import Ui_constraintEditor


class ConstraintEditorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_constraintEditor()
        self.ui.setupUi(self)
