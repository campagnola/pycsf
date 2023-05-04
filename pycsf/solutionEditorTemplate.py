# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'solutionEditorTemplate.ui'
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

class Ui_solutionEditor(object):
    def setupUi(self, solutionEditor):
        solutionEditor.setObjectName(_fromUtf8("solutionEditor"))
        solutionEditor.resize(1139, 667)
        self.gridLayout_2 = QtWidgets.QGridLayout(solutionEditor)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.splitter_2 = QtWidgets.QSplitter(solutionEditor)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.solutionList = TreeWidget(self.splitter)
        self.solutionList.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.solutionList.setObjectName(_fromUtf8("solutionList"))
        item_0 = QtWidgets.QTreeWidgetItem(self.solutionList)
        item_0 = QtWidgets.QTreeWidgetItem(self.solutionList)
        item_0 = QtWidgets.QTreeWidgetItem(self.solutionList)
        item_0 = QtWidgets.QTreeWidgetItem(self.solutionList)
        item_0 = QtWidgets.QTreeWidgetItem(self.solutionList)
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.notesText = RichTextEdit(self.layoutWidget)
        self.notesText.setObjectName(_fromUtf8("notesText"))
        self.verticalLayout.addWidget(self.notesText)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.solutionTable = TreeWidget(self.layoutWidget1)
        self.solutionTable.setAlternatingRowColors(True)
        self.solutionTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.solutionTable.setAllColumnsShowFocus(False)
        self.solutionTable.setObjectName(_fromUtf8("solutionTable"))
        item_0 = QtWidgets.QTreeWidgetItem(self.solutionTable)
        item_0 = QtWidgets.QTreeWidgetItem(self.solutionTable)
        item_0 = QtWidgets.QTreeWidgetItem(self.solutionTable)
        item_0 = QtWidgets.QTreeWidgetItem(self.solutionTable)
        item_0 = QtWidgets.QTreeWidgetItem(self.solutionTable)
        item_0 = QtWidgets.QTreeWidgetItem(self.solutionTable)
        self.solutionTable.header().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.solutionTable)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.copyHtmlBtn = QtWidgets.QPushButton(self.layoutWidget1)
        self.copyHtmlBtn.setObjectName(_fromUtf8("copyHtmlBtn"))
        self.gridLayout.addWidget(self.copyHtmlBtn, 0, 3, 1, 1)
        self.reverseTempSpin = QtWidgets.QSpinBox(self.layoutWidget1)
        self.reverseTempSpin.setProperty("value", 34)
        self.reverseTempSpin.setObjectName(_fromUtf8("reverseTempSpin"))
        self.gridLayout.addWidget(self.reverseTempSpin, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.retranslateUi(solutionEditor)
        QtCore.QMetaObject.connectSlotsByName(solutionEditor)

    def retranslateUi(self, solutionEditor):
        solutionEditor.setWindowTitle(_translate("solutionEditor", "Form", None))
        self.solutionList.headerItem().setText(0, _translate("solutionEditor", "Solution", None))
        __sortingEnabled = self.solutionList.isSortingEnabled()
        self.solutionList.setSortingEnabled(False)
        self.solutionList.topLevelItem(0).setText(0, _translate("solutionEditor", "aCSF - Dissection", None))
        self.solutionList.topLevelItem(1).setText(0, _translate("solutionEditor", "aCSF - Holding", None))
        self.solutionList.topLevelItem(2).setText(0, _translate("solutionEditor", "aCSF - Recording", None))
        self.solutionList.topLevelItem(3).setText(0, _translate("solutionEditor", "Internal", None))
        self.solutionList.topLevelItem(4).setText(0, _translate("solutionEditor", "Misc", None))
        self.solutionList.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("solutionEditor", "Notes", None))
        __sortingEnabled = self.solutionTable.isSortingEnabled()
        self.solutionTable.setSortingEnabled(False)
        self.solutionTable.topLevelItem(0).setText(0, _translate("solutionEditor", "Concentrations (mM)", None))
        self.solutionTable.topLevelItem(1).setText(0, _translate("solutionEditor", "Ion Concentrations (estimated)", None))
        self.solutionTable.topLevelItem(2).setText(0, _translate("solutionEditor", "Ion Concentrations (measured)", None))
        self.solutionTable.topLevelItem(3).setText(0, _translate("solutionEditor", "Osmolarity (estimated)", None))
        self.solutionTable.topLevelItem(4).setText(0, _translate("solutionEditor", "Osmolarity (measured)", None))
        self.solutionTable.topLevelItem(5).setText(0, _translate("solutionEditor", "Reversal Potentials", None))
        self.solutionTable.setSortingEnabled(__sortingEnabled)
        self.label_4.setText(_translate("solutionEditor", "Reversal temperature", None))
        self.copyHtmlBtn.setText(_translate("solutionEditor", "Copy HTML", None))
        self.reverseTempSpin.setSuffix(_translate("solutionEditor", "C", None))

from .textEditor import RichTextEdit
from pyqtgraph import TreeWidget
