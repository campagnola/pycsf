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

#import pyqtgraph as pg
#pg.dbg()


db = SolutionDatabase()
w = SolutionEditorWindow(db=db)
if len(sys.argv) > 1:
    w.loadFile(sys.argv[1])

w.show()
w.tabs.setCurrentIndex(2)

QtGui.QApplication.instance().exec_()