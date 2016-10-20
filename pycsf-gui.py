try:
    import faulthandler
    faulthandler.enable()
except ImportError:
    pass

import sys
from pyqtgraph import QtGui, QtCore
from pycsf.editor import SolutionEditorWindow
from pycsf.core import SolutionDatabase


app = QtGui.QApplication([])

db = SolutionDatabase()
if len(sys.argv) > 1:
    db.restore(sys.argv[1])
    
w = SolutionEditorWindow(db=db)
w.show()
w.tabs.setCurrentIndex(2)

QtGui.QApplication.instance().exec_()