#!/usr/bin/python3.6
# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""

from core.QtCompat import QtWidgets, QtGui, QtCore, Slot, Qt

class SpinBoxDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent, limits=None):
        QtWidgets.QItemDelegate.__init__(self, parent)
        self.limits = limits if limits is not None else (0,99999) 
        self.min    = self.limits[0] 
        self.max    = self.limits[1]   

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(self.min)
        editor.setMaximum(self.max)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setValue(int(value))

    def setModelData(self, editor, model, index):
        editor.interpretText()
        value = editor.value()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
    
    @QtCore.pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())


class DoubleSpinBoxDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent, limits=None, decimals=None):
        QtWidgets.QItemDelegate.__init__(self, parent)
        self.limits   = limits if limits is not None else (0,99999) 
        self.decimals = decimals if decimals is not None else 1
        self.min    = self.limits[0] 
        self.max    = self.limits[1]   

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(self.min)
        editor.setMaximum(self.max)
        editor.setDecimals(self.decimals)
        return editor

    def setEditorData(self, editor, index):
        # value = index.model().data(index)
        value = index.model().data(index, Qt.DisplayRole)
        editor.setValue(float(value))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.value(), QtCore.Qt.EditRole)
        # editor.interpretText()
        # value = editor.value()
        # model.setData(index, value, QtCore.Qt.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
    
    @QtCore.pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())

    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignCenter
        QtWidgets.QItemDelegate.paint(self, painter, option, index)
        