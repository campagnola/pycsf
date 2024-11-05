import os
import pyqtgraph as pg
from . import qt
from .core import IONS
from .treeWidget import ItemDelegate, GroupItem, HtmlItem
from .format_float import formatFloat

Ui_solutionEditor = qt.importTemplate('.solutionEditorTemplate')


class SolutionEditorWidget(qt.QWidget):
    def __init__(self, db, parent=None):
        self.db = db
        self.selectedSolutions = []
        self.showAllReagents = False
        
        qt.QWidget.__init__(self, parent)
        self.ui = Ui_solutionEditor()
        self.ui.setupUi(self)
        
        self.ui.solutionList.setEditTriggers(qt.QAbstractItemView.EditKeyPressed | qt.QAbstractItemView.SelectedClicked)
        self.ui.solutionList.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.ui.solutionList.customContextMenuRequested.connect(self.solutionMenuRequested)

        self.addGroupItem = HtmlItem('+ <a href="/">add group</a>')
        self.ui.solutionList.addTopLevelItem(self.addGroupItem)
        self.addGroupItem.label.linkActivated.connect(lambda: self.addGroup('New Group'))
        
        self.ui.solutionTable.setSelectionBehavior(qt.QAbstractItemView.SelectItems)
        self.solnTableDelegate = ItemDelegate(self.ui.solutionTable)  # allow items to specify their own editors
        self.ui.solutionTable.setHeaderLabels([''])
        #self.ui.solutionTable.setUniformRowHeights(True)
        self.ui.solutionTable.clear()
        self.solnTreeItems = {}

        item = GroupItem('Concentrations (mM)', adder='show all reagents')
        self.solnTreeItems[str(item.text(0))] = item
        self.ui.solutionTable.addTopLevelItem(item)
        item.sigAddClicked.connect(self.showReagentsClicked)
        
        names = [
            'Ion Concentrations (estimated)',
            'Ion Concentrations (measured)',
            'Osmolarity (estimated)',
            'Osmolarity (measured)',
            'Reversal Potentials',
        ]
        for name in names:
            item = GroupItem(name)
            self.solnTreeItems[name] = item
            self.ui.solutionTable.addTopLevelItem(item)
            
        self.solutionTypeItem = SolutionTypeItem()
        self.reverseAgainstItem = ReverseAgainstItem()
        self.solnTreeItems['Reversal Potentials'].addChild(self.solutionTypeItem)
        self.solnTreeItems['Reversal Potentials'].addChild(self.reverseAgainstItem)
        
        self.estIonConcItems = {}
        self.measIonConcItems = {}
        self.ionReversalItems = {}
        for ion in IONS:
            item = qt.QTreeWidgetItem([ion])
            self.solnTreeItems['Ion Concentrations (estimated)'].addChild(item)
            self.estIonConcItems[ion] = item
            item = qt.QTreeWidgetItem([ion])
            self.solnTreeItems['Ion Concentrations (measured)'].addChild(item)
            self.measIonConcItems[ion] = item
            item = qt.QTreeWidgetItem([ion])
            self.solnTreeItems['Reversal Potentials'].addChild(item)
            self.ionReversalItems[ion] = item

        self.ui.splitter_2.setStretchFactor(0, 1)
        self.ui.splitter_2.setStretchFactor(1, 3)
        self.ui.splitter.setStretchFactor(0, 2)
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.solutionList.sigItemTextChanged.connect(self.solutionListTextChanged)
        self.ui.solutionList.sigItemCheckStateChanged.connect(self.solutionListCheckStateChanged)
        self.ui.solutionList.itemSelectionChanged.connect(self.solutionListSelectionChanged)
        self.ui.reverseTempSpin.valueChanged.connect(self.updateSolutionTree)
        self.solutionTypeItem.sigChanged.connect(self.recalculate)
        self.reverseAgainstItem.sigChanged.connect(self.recalculate)
        self.ui.notesText.textChanged.connect(self.notesTextChanged)
        self.ui.copyHtmlBtn.clicked.connect(self.copyHtml)

        self.ui.solutionTable.itemSelectionChanged.connect(self.selectionChanged)
        self.ui.solutionTable.itemClicked.connect(self.itemClicked)
        self.ui.solutionTable.resizeColumnToContents(0)

        self.db.solutions.solutionListChanged.connect(self.updateSolutionList)
        self.db.reagents.sigReagentListChanged.connect(self.updateSolutionTree)
        self.db.reagents.sigReagentDataChanged.connect(self.updateSolutionTree)
        self.db.reagents.sigReagentRenamed.connect(self.updateSolutionTree)

        self.updateSolutionList()

    def solutionMenuRequested(self, point):
        item = self.ui.solutionList.itemAt(point)
        item.showContextMenu(point)

    def solutionListSelectionChanged(self):
        items = self.ui.solutionList.selectedItems()
        self.ui.notesText.textChanged.disconnect(self.notesTextChanged)
        try:
            if len(items) == 0 or not isinstance(items[0], SolutionItem):
                self.ui.notesText.clear()
            else:
                soln = items[0].solution
                self.ui.notesText.setHtml(soln.notes)
        finally:
            self.ui.notesText.textChanged.connect(self.notesTextChanged)

    def notesTextChanged(self):
        items = self.ui.solutionList.selectedItems()
        if len(items) == 0:
            return
        item = items[0]
        item.solution.notes = str(self.ui.notesText.toHtml())
        
    def selectionChanged(self):
        selection = self.ui.solutionTable.selectionModel().selection().indexes()
        if len(selection) != 1:
            return
        item, col = self.ui.solutionTable.itemFromIndex(selection[0])
        if item.flags() & qt.Qt.ItemIsEditable == qt.Qt.ItemIsEditable:
            self.ui.solutionTable.editItem(item, col)

    def itemClicked(self, item, col):
        if hasattr(item, 'itemClicked'):
            item.itemClicked(col)

    def updateSolutionList(self):
        slist = self.ui.solutionList
        vpos = slist.verticalScrollBar().value()
        newSel = []
        for item in slist.topLevelItems():
            if item is not self.addGroupItem:
                slist.removeTopLevelItem(item)
        
        grpItems = {}
        for soln in self.db.solutions:
            item = SolutionItem(soln)
            item.setFlags(qt.Qt.ItemIsSelectable | qt.Qt.ItemIsEnabled | qt.Qt.ItemIsDragEnabled | qt.Qt.ItemIsEditable | qt.Qt.ItemIsUserCheckable)
            if soln in self.selectedSolutions:
                item.setCheckState(0, qt.Qt.Checked)
                newSel.append(soln)
            else:
                item.setCheckState(0, qt.Qt.Unchecked)
            item.solution = soln
            group = soln.group
            if group not in grpItems:
                grpItems[group] = self.addGroup(group)
            grpItem = grpItems[group]
            grpItem.addChild(item)
            
            item.sigCopyClicked.connect(self.copySolution)
            item.sigRemoveClicked.connect(self.removeSolution)

        slist.verticalScrollBar().setValue(vpos)
        self.selectedSolutions = newSel
        self.reverseAgainstItem.setAllSolutions(self.db.solutions)

    def copySolution(self, item):
        soln = item.solution.copy()
        names = [s.name for s in self.db.solutions]
        i = 0
        while True:
            name = soln.name + '_%d' % i
            if name not in names:
                break
            i += 1
        soln.setName(name)
        self.db.solutions.add(soln)
        
    def removeSolution(self, item):
        self.db.solutions.remove(item.solution)

    def addGroup(self, name):
        item = GroupItem(name, adder='add solution', editable=True, checkable=True)
        self.ui.solutionList.insertTopLevelItem(self.ui.solutionList.topLevelItemCount()-1, item)
        item.sigAddClicked.connect(self.addSolutionClicked)
        return item
            
    def solutionListCheckStateChanged(self, item, column):
        checked = item.isChecked(0)
        if isinstance(item, GroupItem):
            for child in item.childItems():
                child.setChecked(0, checked)
        else:
            selected = item.solution in self.selectedSolutions
            if checked and not selected:
                self.selectedSolutions.append(item.solution)
            elif not checked and selected:
                self.selectedSolutions.remove(item.solution)
        self.updateSolutionTree()

    def solutionListTextChanged(self, item, column):
        if isinstance(item, GroupItem):
            for child in item.childItems():
                child.solution.group = str(item.text(0))
        else:
            new = str(item.text(0))
            # Note: disconnect here prevents a segfault. Something to do with
            # removing an item during its own edit callback.
            try:
                self.db.solutions.solutionListChanged.disconnect(self.updateSolutionList)
                reconnect = True
            except TypeError:
                reconnect = False
                pass
                
            try:
                item.solution.setName(new)
            except Exception:
                item.resetText()
                raise
            finally:
                if reconnect:
                    self.db.solutions.solutionListChanged.connect(self.updateSolutionList)
            
            self.updateSolutionTree()
            # can't call updatesolutionlist from here--causes segv.
            self.reverseAgainstItem.setAllSolutions(self.db.solutions)
            
    def addSolutionClicked(self, item):
        basename = 'New Solution'
        name = basename
        count = 2
        while True:
            try:
                self.db.solutions.add(name=name, group=str(item.text(0)))
                break
            except NameError:
                name = basename + '%d'%count
                count += 1
        
    def showReagentsClicked(self, item, name):
        if self.showAllReagents:
            self.solnTreeItems['Concentrations (mM)'].addItem.setText('show all reagents')
        else:
            self.solnTreeItems['Concentrations (mM)'].addItem.setText('hide unused reagents')
        self.showAllReagents = not self.showAllReagents
        self.updateSolutionTree()

    def updateSolutionTree(self):
        table = self.ui.solutionTable
        vpos = table.verticalScrollBar().value()
        table.setColumnCount(len(self.selectedSolutions) + 1)
        table.setHeaderLabels([''] + [s.name for s in self.selectedSolutions])
        
        # collect a list of all reagents in all selected solutions
        reagentTree = self.solnTreeItems['Concentrations (mM)']
        reagentTree.clear()
        reagents = set()
        for soln in self.selectedSolutions:
            reagents = reagents | set(soln.reagentList())
        # check for unknown reagents
        allReagents = self.db.reagents.names()
        unknown = [r for r in reagents if r not in allReagents]
        # sort
        if self.showAllReagents:
            reagents = list(allReagents) + unknown
            showGroups = True
        else:
            reagents = [x for x in allReagents if x in reagents] + unknown
            showGroups = False
        
        # update reagent list
        self.reagentItems = {}
        grpItems = {}
        for reagent in reagents:
            #concs = ['%0.1f'%soln.reagents[reagent] if reagent in soln.reagents else '' for soln in self.selectedSolutions]
            #item = qt.QTreeWidgetItem([reagent] + concs)
            item = ReagentItem(reagent, self.selectedSolutions)
            item.sigChanged.connect(self.recalculate)
            self.reagentItems[reagent] = item
            if reagent in unknown:
                item.setForeground(0, qt.QColor(200, 0, 0))
                
            if showGroups:
                if reagent in unknown:
                    grp = 'Unknown reagents'
                else:
                    grp = self.db.reagents[reagent]['group']
                if grp in grpItems:
                    grpItems[grp].addChild(item)
                else:
                    grpItem = qt.QTreeWidgetItem([grp])
                    reagentTree.addChild(grpItem)
                    grpItems[grp] = grpItem
                    grpItem.addChild(item)
                    grpItem.setExpanded(True)
            else:
                reagentTree.addChild(item)

        # Set measured ion concentration values
        # (todo)
        self.solnTreeItems['Ion Concentrations (measured)'].setExpanded(False)
        
        # recalculate estimated ion concentrations, osmolartity, and reversals
        self.recalculate()
        
        # update reversal potential special fields
        self.solutionTypeItem.setSolutions(self.selectedSolutions)
        self.reverseAgainstItem.setSolutions(self.selectedSolutions)

        # resize columns
        for i in range(len(self.selectedSolutions)+1):
            table.resizeColumnToContents(i)

        table.verticalScrollBar().setValue(vpos)

    def recalculate(self):
        results = self.db.solutions.recalculate(self.selectedSolutions, self.ui.reverseTempSpin.value())
        for i, soln in enumerate(self.selectedSolutions):
            ions, osm, revs = results[soln.name]
            for ion in IONS:
                self.estIonConcItems[ion].setText(i+1, formatFloat(ions[ion]))
                if revs[ion] is None:
                    self.ionReversalItems[ion].setText(i+1, '')
                else:
                    self.ionReversalItems[ion].setText(i+1, formatFloat(revs[ion]))
                    
            self.solnTreeItems['Osmolarity (estimated)'].setText(i+1, formatFloat(osm))

    def copyHtml(self):
        txt = '<table>\n'
        txt += self._itemToHtml(self.ui.solutionTable, self.ui.solutionTable.headerItem())
        root = self.ui.solutionTable.invisibleRootItem()
        for i in range(root.childCount()):
            txt += self._itemToHtml(self.ui.solutionTable, root.child(i))
        txt += '</table>\n'

        # copy to clipboard
        if os.sys.platform in ['darwin']:
            qt.QApplication.clipboard().setText(txt)
        else:
            md = qt.QMimeData()
            md.setHtml(txt)
            qt.QApplication.clipboard().setMimeData(md)
        
    def _itemToHtml(self, tree, item):
        txt = "  <tr>\n"
        for i in range(tree.columnCount()):
            width = tree.header().sectionSize(i)
            t = str(item.text(i))
            bg = item.background(i)
            fg = item.foreground(i)
            style = ''
            if bg.isOpaque():
                style += 'background-color: %s; ' % bg.color().name()
            if fg.isOpaque():
                style += 'color: %s; ' % fg.color().name()
                
            txt += '    <td style="font-family: sans-serif; font-size: 10pt; vertical-align: middle; width: %dpx; %s">%s</td>\n' % (width, style, t)
        txt += "\n  </tr>\n"
        for i in range(item.childCount()):
            txt += self._itemToHtml(tree, item.child(i))
        return txt
        

class ReagentItem(pg.TreeWidgetItem):
    def __init__(self, name, solutions):
        class SigProxy(qt.QObject):
            sigChanged = qt.Signal(object)
        self._sigprox = SigProxy()
        self.sigChanged = self._sigprox.sigChanged

        self.name = name
        self.solutions = solutions
        pg.TreeWidgetItem.__init__(self, [name] + [formatFloat(sol[name]) if name in sol.reagentList() else '' for sol in solutions])
        self.setFlags(self.flags() | qt.Qt.ItemIsEditable)

    def createEditor(self, parent, option, col):
        if col == 0:
            return None
        return qt.QLineEdit(parent)
    
    def setEditorData(self, editor, col):
        editor.setText(self.text(col))
    
    def setModelData(self, editor, model, col):
        sol = self.solutions[col-1]
        t = str(editor.text())
        if t == '':
            sol[self.name] = None
        else:
            sol[self.name] = float(t)
        self.setText(col, editor.text())
        self.sigChanged.emit(self)


class SolutionItem(pg.TreeWidgetItem):
    def __init__(self, soln):
        class SigProxy(qt.QObject):
            sigCopyClicked = qt.Signal(object)
            sigRemoveClicked = qt.Signal(object)
        self.__sigprox = SigProxy()
        self.sigCopyClicked = self.__sigprox.sigCopyClicked
        self.sigRemoveClicked = self.__sigprox.sigRemoveClicked

        self.solution = soln
        pg.TreeWidgetItem.__init__(self, [soln.name])
        self.menu = qt.QMenu()
        self.menu.addAction('Copy', self.copyClicked)
        self.menu.addAction('Remove', self.removeClicked)
        
    def showContextMenu(self, point):
        tree = self.treeWidget()
        point = point + qt.QPoint(0, tree.header().height())
        pt = tree.mapToGlobal(point)
        self.menu.popup(pt)
        
    def copyClicked(self):
        self.sigCopyClicked.emit(self)
        
    def removeClicked(self):
        self.sigRemoveClicked.emit(self)
        
    def resetText(self):
        self.setText(0, self.solution.name)


class SolutionTypeItem(pg.TreeWidgetItem):
    def __init__(self):
        class SigProxy(qt.QObject):
            sigChanged = qt.Signal(object)
        self._sigprox = SigProxy()
        self.sigChanged = self._sigprox.sigChanged

        self.solutions = []
        pg.TreeWidgetItem.__init__(self, ['Solution type'])
        
    def setSolutions(self, solutions):
        self.solutions = solutions
        for i,sol in enumerate(solutions):
            self.setText(i+1, sol.type)
            
    def itemClicked(self, col):
        text = 'external' if str(self.text(col)) == 'internal' else 'internal'
        self.setText(col, text)
        self.solutions[col-1].type = text
        self.sigChanged.emit(self)
        return None


class ReverseAgainstItem(pg.TreeWidgetItem):
    def __init__(self):
        class SigProxy(qt.QObject):
            sigChanged = qt.Signal(object)
        self._sigprox = SigProxy()
        self.sigChanged = self._sigprox.sigChanged

        self.solutions = []
        pg.TreeWidgetItem.__init__(self, ['Reverse against'])
        self.internalMenu = qt.QMenu()
        self.externalMenu = qt.QMenu()
        
    def setSolutions(self, solutions):
        self.solutions = solutions
        for i,sol in enumerate(solutions):
            if sol.compareAgainst is None:
                #self.setText(i+1, '')
                pass
            else:
                self.setText(i+1, sol.compareAgainst)
            
    def setAllSolutions(self, solutions):
        for menu, soltyp in [(self.internalMenu, 'internal'), (self.externalMenu, 'external')]:
            menu.clear()
            grp = None
            for sol in solutions:
                if sol.type == soltyp:
                    continue
                if sol.group != grp:
                    grp = sol.group
                    label = qt.QLabel(grp)
                    font = label.font()
                    font.setWeight(font.Bold)
                    label.setFont(font)
                    act = qt.QWidgetAction(menu)
                    act.setDefaultWidget(label)
                    menu.addAction(act)
                menu.addAction("  " + sol.name, self.selectionChanged)
            
    def selectionChanged(self):
        action = self.treeWidget().sender()
        text = str(action.text()).strip()
        self.setText(self._activeColumn, text)
        self.solutions[self._activeColumn-1].compareAgainst = text
        self.sigChanged.emit(self)
            
    def itemClicked(self, col):
        tw = self.treeWidget()
        x = tw.header().sectionPosition(col)
        y = tw.header().height() + tw.visualItemRect(self).bottom()
        menu = self.internalMenu if self.solutions[col-1].type == 'internal' else self.externalMenu
        menu.popup(tw.mapToGlobal(qt.QPoint(x, y)))
        self._activeColumn = col
        return None


