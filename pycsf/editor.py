import os, json
from pyqtgraph.Qt import QtGui, QtCore
from .core import SolutionDatabase
from .reagentEditor import ReagentEditorWidget
from .solutionEditor import SolutionEditorWidget
from .recipeEditor import RecipeEditorWidget
from .constraintEditor import ConstraintEditorWidget


class SolutionEditorWindow(QtGui.QMainWindow):
    def __init__(self, db=None):
        if db is None:
            db = SolutionDatabase()
        self.db = db
        
        self.currentFile = None
        
        QtGui.QMainWindow.__init__(self)
        
        icon = os.path.join(os.path.dirname(__file__), 'flask.png')
        if os.path.isfile(icon):
            self.setWindowIcon(QtGui.QIcon(icon))
        
        self.resize(1200, 800)
        self.tabs = QtGui.QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.reagentEditor = ReagentEditorWidget(self.db)
        self.tabs.addTab(self.reagentEditor, 'Reagents')
        
        self.solutionEditor = SolutionEditorWidget(self.db)
        self.tabs.addTab(self.solutionEditor, 'Solutions')
        
        self.recipeEditor = RecipeEditorWidget(self.db)
        self.tabs.addTab(self.recipeEditor, 'Recipes')
        
        self.constraintEditor = ConstraintEditorWidget()
        self.tabs.addTab(self.constraintEditor, 'Constraints')
        self.tabs.setCurrentWidget(self.solutionEditor)

        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction('Open', self.loadFile)
        self.fileMenu.addAction('Save', self.save)
        self.fileMenu.addAction('Save As', self.saveAs)

    def loadReagents(self, data):
        self.reagents.restore(data)
        self.reagentEditor.updateReagentList()
        
    def save(self):
        # clear focus to trigger any pending editor updates
        fw = QtGui.QApplication.focusWidget()
        if fw is not None:
            fw.clearFocus()
        
        if self.currentFile is None:
            self.saveAs()
        else:
            self.db.saveFile(self.currentFile)
        
    def saveAs(self):
        fname = QtGui.QFileDialog.getSaveFileName()
        if fname is not None:
            self.currentFile = fname
            self.setWindowTitle('Solution Editor: ' + fname)
            self.save()
        
    def loadFile(self, fname=None):
        if fname is None:
            fname = str(QtGui.QFileDialog.getOpenFileName())
            if fname == '':
                return
        self.db.loadFile(fname)
        self.currentFile = fname
        self.setWindowTitle('Solution Editor: ' + fname)
        self.reagentEditor.updateReagentList()
        self.solutionEditor.updateSolutionList()
        self.solutionEditor.updateSolutionTree()
        