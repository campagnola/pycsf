try:
    import faulthandler
    faulthandler.enable()
except ImportError:
    pass

import sys
from pycsf import qt
from pycsf.editor import SolutionEditorWindow
from pycsf.core import SolutionDatabase

app = qt.QApplication([])

#import pyqtgraph as pg
#pg.dbg()
sysExcepthook = sys.excepthook
def handleException(*args):
    sysExcepthook(*args)
    qt.QMessageBox.warning(None, "Oops.", str(args[1]))
sys.excepthook = handleException    


db = SolutionDatabase()
w = SolutionEditorWindow(db=db)
if len(sys.argv) > 1:
    w.loadFile(sys.argv[1])
else:
    db.loadDefault()

w.show()
w.tabs.setCurrentIndex(2)

qt.QApplication.instance().exec_()
