#!/usr/bin/python3.6
# coding=utf-8

"""
:Copyright: © 2020 Advanced Control Systems, Inc. All Rights Reserved.
"""
__author__ = 'Darren Liang'


import sys
from core.QtCompat import QtWidgets, QtGui, QtCore, Slot, Qt


class CheckableComboBox(QtWidgets.QComboBox):
    def __init__(self, parent = None):
        super(CheckableComboBox, self).__init__(parent)
        self.setView(QtWidgets.QListView(self))
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))
        self.setMinimumWidth(parent.size().width())
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.setFont(font)

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def checkedItems(self):
        checkedItems = []
        for index in range(self.count()):
            item = self.model().item(index)
            if item.checkState() == QtCore.Qt.Checked:
                checkedItems.append(item)
        return checkedItems

    def checkedValues(self):
        checkedValues = []
        for index in range(self.count()):
            item = self.model().item(index)
            if item.checkState() == QtCore.Qt.Checked:
                value = str(item.text())
                if value != 'ALL':
                    checkedValues.append(value)
        return checkedValues
