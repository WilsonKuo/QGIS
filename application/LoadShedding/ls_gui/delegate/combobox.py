#!/usr/bin/python3.6
# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""

from core.QtCompat import QtWidgets, QtGui, QtCore, Slot, Qt

class ComboBoxDelegate(QtWidgets.QItemDelegate):
    """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent, items=None):
        QtWidgets.QItemDelegate.__init__(self, parent)
        self.mainwindow   = parent
        self.items = items if items is not None else []
        
    @QtCore.pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
    
    def setItems(self, items):
        self.items = items

    def createEditor(self, widget, option, index):
        editor = QtWidgets.QComboBox(widget)
        editor.addItems(self.items)
        
        item = editor.model().item(1)
        item.setData(QtGui.QColor('Green'), Qt.ForegroundRole)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setCurrentIndex(int(value))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentIndex(), QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        fgcolor = QtGui.QPen() if index.data(QtCore.Qt.ForegroundRole) is None else QtGui.QPen(index.data(QtCore.Qt.ForegroundRole))
        bgcolor = QtGui.QBrush() if index.data(QtCore.Qt.BackgroundRole) is None else QtGui.QBrush(index.data(QtCore.Qt.BackgroundRole))
        value   = index.model().data(index, role=Qt.DisplayRole)
        text    = self.items[int(value)]
        painter.setPen(fgcolor)
        painter.fillRect(option.rect, bgcolor)
        painter.drawText(option.rect, Qt.AlignCenter, text)
