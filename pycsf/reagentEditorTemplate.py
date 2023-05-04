# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reagentEditorTemplate.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_reagentEditor(object):
    def setupUi(self, reagentEditor):
        reagentEditor.setObjectName(_fromUtf8("reagentEditor"))
        reagentEditor.resize(612, 466)
        self.gridLayout = QtWidgets.QGridLayout(reagentEditor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtWidgets.QSplitter(reagentEditor)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.reagentTree = TreeWidget(self.splitter)
        self.reagentTree.setAlternatingRowColors(True)
        self.reagentTree.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.reagentTree.setObjectName(_fromUtf8("reagentTree"))
        item_0 = QtWidgets.QTreeWidgetItem(self.reagentTree)
        item_0 = QtWidgets.QTreeWidgetItem(self.reagentTree)
        item_0 = QtWidgets.QTreeWidgetItem(self.reagentTree)
        item_0 = QtWidgets.QTreeWidgetItem(self.reagentTree)
        item_0 = QtWidgets.QTreeWidgetItem(self.reagentTree)
        item_0 = QtWidgets.QTreeWidgetItem(self.reagentTree)
        self.reagentNotes = RichTextEdit(self.splitter)
        self.reagentNotes.setObjectName(_fromUtf8("reagentNotes"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(reagentEditor)
        QtCore.QMetaObject.connectSlotsByName(reagentEditor)

    def retranslateUi(self, reagentEditor):
        reagentEditor.setWindowTitle(_translate("reagentEditor", "Form", None))
        self.reagentTree.headerItem().setText(0, _translate("reagentEditor", "Reagent", None))
        self.reagentTree.headerItem().setText(1, _translate("reagentEditor", "Formula", None))
        self.reagentTree.headerItem().setText(2, _translate("reagentEditor", "MW (g/mol)", None))
        self.reagentTree.headerItem().setText(3, _translate("reagentEditor", "Osmotic const.", None))
        self.reagentTree.headerItem().setText(4, _translate("reagentEditor", "Na", None))
        self.reagentTree.headerItem().setText(5, _translate("reagentEditor", "K", None))
        self.reagentTree.headerItem().setText(6, _translate("reagentEditor", "Cl", None))
        self.reagentTree.headerItem().setText(7, _translate("reagentEditor", "Ca", None))
        self.reagentTree.headerItem().setText(8, _translate("reagentEditor", "Mg", None))
        self.reagentTree.headerItem().setText(9, _translate("reagentEditor", "SO4", None))
        self.reagentTree.headerItem().setText(10, _translate("reagentEditor", "PO4", None))
        self.reagentTree.headerItem().setText(11, _translate("reagentEditor", "Cs", None))
        __sortingEnabled = self.reagentTree.isSortingEnabled()
        self.reagentTree.setSortingEnabled(False)
        self.reagentTree.topLevelItem(0).setText(0, _translate("reagentEditor", "Ions", None))
        self.reagentTree.topLevelItem(1).setText(0, _translate("reagentEditor", "pH Buffers", None))
        self.reagentTree.topLevelItem(2).setText(0, _translate("reagentEditor", "Metabolites", None))
        self.reagentTree.topLevelItem(3).setText(0, _translate("reagentEditor", "Antioxidants", None))
        self.reagentTree.topLevelItem(4).setText(0, _translate("reagentEditor", "Toxins", None))
        self.reagentTree.topLevelItem(5).setText(0, _translate("reagentEditor", "Markers", None))
        self.reagentTree.setSortingEnabled(__sortingEnabled)

from .textEditor import RichTextEdit
from pyqtgraph import TreeWidget
