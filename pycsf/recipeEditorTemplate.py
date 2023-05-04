# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recipeEditorTemplate.ui'
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

class Ui_recipeEditor(object):
    def setupUi(self, recipeEditor):
        recipeEditor.setObjectName(_fromUtf8("recipeEditor"))
        recipeEditor.resize(720, 442)
        self.gridLayout = QtWidgets.QGridLayout(recipeEditor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.showFormulaeCheck = QtWidgets.QCheckBox(recipeEditor)
        self.showFormulaeCheck.setObjectName(_fromUtf8("showFormulaeCheck"))
        self.horizontalLayout.addWidget(self.showFormulaeCheck)
        self.showMWCheck = QtWidgets.QCheckBox(recipeEditor)
        self.showMWCheck.setObjectName(_fromUtf8("showMWCheck"))
        self.horizontalLayout.addWidget(self.showMWCheck)
        self.showConcentrationCheck = QtWidgets.QCheckBox(recipeEditor)
        self.showConcentrationCheck.setObjectName(_fromUtf8("showConcentrationCheck"))
        self.horizontalLayout.addWidget(self.showConcentrationCheck)
        self.copyHtmlBtn = QtWidgets.QPushButton(recipeEditor)
        self.copyHtmlBtn.setObjectName(_fromUtf8("copyHtmlBtn"))
        self.horizontalLayout.addWidget(self.copyHtmlBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.hsplitter = QtWidgets.QSplitter(recipeEditor)
        self.hsplitter.setOrientation(QtCore.Qt.Horizontal)
        self.hsplitter.setObjectName(_fromUtf8("hsplitter"))
        self.recipeSetList = TreeWidget(self.hsplitter)
        self.recipeSetList.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.recipeSetList.setHeaderHidden(True)
        self.recipeSetList.setObjectName(_fromUtf8("recipeSetList"))
        self.recipeSetList.headerItem().setText(0, _fromUtf8("1"))
        self.vsplitter = QtWidgets.QSplitter(self.hsplitter)
        self.vsplitter.setOrientation(QtCore.Qt.Vertical)
        self.vsplitter.setObjectName(_fromUtf8("vsplitter"))
        self.recipeTable = QtWidgets.QTableWidget(self.vsplitter)
        self.recipeTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.recipeTable.setObjectName(_fromUtf8("recipeTable"))
        self.recipeTable.setColumnCount(0)
        self.recipeTable.setRowCount(0)
        self.notesTree = TreeWidget(self.vsplitter)
        self.notesTree.setObjectName(_fromUtf8("notesTree"))
        self.gridLayout.addWidget(self.hsplitter, 1, 0, 1, 1)

        self.retranslateUi(recipeEditor)
        QtCore.QMetaObject.connectSlotsByName(recipeEditor)

    def retranslateUi(self, recipeEditor):
        recipeEditor.setWindowTitle(_translate("recipeEditor", "Form", None))
        self.showFormulaeCheck.setText(_translate("recipeEditor", "Show formulae", None))
        self.showMWCheck.setText(_translate("recipeEditor", "Show molecular weights", None))
        self.showConcentrationCheck.setText(_translate("recipeEditor", "Show concentrations", None))
        self.copyHtmlBtn.setText(_translate("recipeEditor", "Copy HTML", None))
        self.notesTree.headerItem().setText(0, _translate("recipeEditor", "Notes", None))

from pyqtgraph import TreeWidget
