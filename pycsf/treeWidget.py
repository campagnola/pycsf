import pyqtgraph as pg
from . import qt


class ItemDelegate(qt.QItemDelegate):
    """Delegate that allows tree items to create their own per-column editors.
    """
    def __init__(self, tree):
        qt.QItemDelegate.__init__(self, tree)
        self.tree = tree
        tree.setItemDelegate(self)
        
    def createEditor(self, parent, option, index):
        item, col = self.tree.itemFromIndex(index)
        if hasattr(item, 'createEditor'):
            return item.createEditor(parent, option, col)
        else:
            return None
    
    def setEditorData(self, editor, index):
        item, col = self.tree.itemFromIndex(index)
        return item.setEditorData(editor, col)
        
    def setModelData(self, editor, model, index):
        item, col = self.tree.itemFromIndex(index)
        return item.setModelData(editor, model, col)


class LabeledWidget(qt.QWidget):
    def __init__(self, text, widget):
        qt.QWidget.__init__(self)
        self.widget = widget
        self.layout = qt.QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = qt.QLabel(text)
        self.label.setFixedWidth(100)
        self.layout.addWidget(self.label)
        self.layout.addWidget(widget)


class HtmlItem(pg.TreeWidgetItem):
    def __init__(self, text):
        pg.TreeWidgetItem.__init__(self)
        self.label = qt.QLabel(text)
        self.label.setTextInteractionFlags(qt.Qt.TextBrowserInteraction)
        self.setWidget(0, self.label)


class GroupItem(pg.TreeWidgetItem):
    def __init__(self, name, adder=None, editable=False, checkable=False, addList=None):
        class SigProxy(qt.QObject):
            sigAddClicked = qt.Signal(object, object)
        self._sigprox = SigProxy()
        self.sigAddClicked = self._sigprox.sigAddClicked
            
        pg.TreeWidgetItem.__init__(self, [name])
        font = qt.QFont()
        font.setWeight(qt.QFont.Bold)
        self.setFont(0, font)
        self.setForeground(0, pg.mkBrush(255, 255, 255))
        self.setBackground(0, pg.mkBrush(180, 180, 200))
        #self.setFirstColumnSpanned(True)
        self.setExpanded(True)
        if editable:
            self.setFlags(self.flags() | qt.Qt.ItemIsEditable)
        if checkable:
            self.setFlags(self.flags() | qt.Qt.ItemIsUserCheckable)
            self.setChecked(0, False)
        
        if adder is None:
            self.addItem = None
        else:
            self.addItem = AdderItem(adder, addList=addList)
            pg.TreeWidgetItem.addChild(self, self.addItem)
            self.addItem.clicked.connect(self.addClicked)

    def addChild(self, item):
        if self.addItem is None:
            pg.TreeWidgetItem.addChild(self, item)
        else:
            self.insertChild(self.childCount()-1, item)

    def addClicked(self, item, val):
        self.sigAddClicked.emit(self, val)

    def childItems(self):
        items = pg.TreeWidgetItem.childItems(self)
        if self.addItem is not None:
            items.remove(self.addItem)
        return items
    
    def clear(self):
        for item in self.childItems():
            self.removeChild(item)

    def setAddList(self, l):
        self.addItem.setAddList(l)


class AdderItem(pg.TreeWidgetItem):
    def __init__(self, text, addList=None):
        class SigProxy(qt.QObject):
            clicked = qt.Signal(object, object)  # self, value
        self._sigproxy = SigProxy()
        self.clicked = self._sigproxy.clicked
        
        pg.TreeWidgetItem.__init__(self)
        self.setFlags(self.flags() | qt.Qt.ItemIsEditable)
        self.label = qt.QLabel()
        self.setText(text)
        self.label.setTextInteractionFlags(qt.Qt.TextBrowserInteraction)
        self.label.linkActivated.connect(self.labelClicked)
        self.setWidget(0, self.label)
        
        self.addListPopup = qt.QMenu(self.label)
        self.addListPopup.triggered.connect(self.addSelected)
        
        self.setAddList(addList)

    def setText(self, col, text=None):
        if text is None:
            text = '+ <a href="/">%s</a>' % col
            self.label.setText(text)
        else:
            pg.TreeWidgetItem.setText(self, col, text)
        
    def setAddList(self, addList):
        self.addList = addList
        if addList is not None:
            w = self.addListPopup
            w.clear()
            for item in self.addList:
                if item.startswith('__'):
                    # secret code for adding non-interactive labels
                    l = qt.QLabel(item[2:])
                    f = l.font()
                    f.setWeight(f.Bold)
                    l.setFont(f)
                    a = qt.QWidgetAction(w)
                    a.setDefaultWidget(l)
                    w.addAction(a)
                else:
                    w.addAction(item)
        
    def labelClicked(self):
        if self.addList is None:
            self.clicked.emit(self, None)
        else:
            w = self.addListPopup
            pt = self.label.mapToGlobal(qt.QPoint(15, self.label.height()))
            w.popup(pt)
        
    def addSelected(self, action):
        self.clicked.emit(self, str(action.text()))
        
        

