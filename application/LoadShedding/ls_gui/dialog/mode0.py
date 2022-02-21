# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
__author__ = 'Darren Liang'

from loadshedding  import loadshedding
from core.QtCompat      import QtWidgets, QtGui, QtCore, Slot, Qt


class mode0_ExecDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(mode0_ExecDialog, self).__init__(parent)
        self.setFixedSize(220,80)
        self.setWindowTitle("[Exec] Restore")
        self.args = None
   
        # decalre widget 
        self.label_groups = QtWidgets.QLabel("Groups")
        self.groups = QtWidgets.QLineEdit(self)
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)

        regexRule = QtCore.QRegExp("[0-9A-Za-z\,]+")
        validator = QtGui.QRegExpValidator(regexRule)
        self.groups.setValidator(validator)
        self.groups.setPlaceholderText("A,B,C")

        # set layout
        layout = QtWidgets.QFormLayout(self)
        layout.addRow(self.label_groups, self.groups)
        layout.addWidget(self.buttonBox)

        # set event
        self.buttonBox.accepted.connect(self.execute)
        self.buttonBox.rejected.connect(self.reject)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("Execute")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.execute)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)

        self.groups.textEdited.connect(self.to_upppercase)
        self.groups.textEdited.connect(self.verfy_content)
    
        # set font property
        self.font_setting(self.label_groups ,10)
        self.font_setting(self.groups       ,10)
        self.font_setting(self.buttonBox    ,10)
    
    def to_upppercase(self, text):
        self.groups.setText(str(text).upper())

    def verfy_content(self):
        cond = self.groups.text() != ''
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(cond)

    def execute(self):
        _groups = self.groups.text()
        args    = { "mode": "0", "group": _groups, }
        self.args = args
        self.accept()

    def font_setting(self, widget, size=None):
        size = 12 if size == None else size
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(size)
        widget.setFont(font)

class mode0_StopDialog(QtWidgets.QDialog):
    def __init__(self, parent, pool):
        super(mode0_StopDialog, self).__init__(parent)
        self.setFixedSize(220,80)
        self.setWindowTitle("[Stop] Restore")
        self.args  = None
        self.pool  = pool
        self.tasks = list(pool.keys())
        print(self.pool)
        # decalre widget 
        self.label     = QtWidgets.QLabel("Tasks")
        self.options   = QtWidgets.QComboBox(self)
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)

        # set layout
        layout = QtWidgets.QFormLayout(self)
        layout.addRow(self.label, self.options)
        layout.addWidget(self.buttonBox)

        # set event
        self.buttonBox.accepted.connect(self.execute)
        self.buttonBox.rejected.connect(self.reject)

        # self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("Ok")
        # self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.execute)
        # self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)
    
        # set font property
        self.font_setting(self.label     ,10)
        self.font_setting(self.options   ,10)
        self.font_setting(self.buttonBox ,10)

        self.options.addItems(self.tasks)

    def execute(self):
        options = self.options.currentText()
        args    = { "options": options, }
        self.args = args
        self.accept()

    def font_setting(self, widget, size=None):
        size = 12 if size == None else size
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(size)
        widget.setFont(font)

