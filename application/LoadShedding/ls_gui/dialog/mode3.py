# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
__author__ = 'Darren Liang'

import os

from core.acsQt     import spinboxes
from core.QtCompat  import QtWidgets, QtGui, QtCore, Slot, Qt
from core.OracleInterface   import OracleInterface

USER  = os.getenv('ORACLE_USER', 'acs_qa')
PSWD  = os.getenv('ORACLE_PW'  , 'acs_qa')
TNS   = os.getenv('ORACLE_DBSTRING', 'emsa')
PRISMdb = OracleInterface(USER, PSWD, TNS)

class mode3_ExecDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(mode3_ExecDialog, self).__init__(parent)
        self.resize(250,120)
        self.setWindowTitle("UF")

        self.content     = self.get_table_content()
        self.subst_list  = list(set([ item[0] for item in self.content]))
        self.mtr_list    = [ item[1] for item in self.content]
        self.action_list = ["Add", "Delete"] 

        # decalre widget 
        self.label_mtr      = QtWidgets.QLabel("MTR")
        self.label_subst    = QtWidgets.QLabel("Subst")
        self.label_action   = QtWidgets.QLabel("Action")
        self.substation     = QtWidgets.QComboBox(self)
        self.maintrasformer = QtWidgets.QComboBox(self)
        self.action         = QtWidgets.QComboBox(self)
        buttonBox   = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)

        # set layout
        layout = QtWidgets.QFormLayout(self)
        layout.addRow(self.label_subst , self.substation)
        layout.addRow(self.label_mtr   , self.maintrasformer)
        layout.addRow(self.label_action, self.action)
        layout.addWidget(buttonBox)
                
        # set font property
        self.font_setting(self.label_mtr     ,10)
        self.font_setting(self.label_subst   ,10)
        self.font_setting(self.label_action  ,10)
        self.font_setting(self.substation    ,10)
        self.font_setting(self.maintrasformer,10)
        self.font_setting(self.action        ,10)
        self.font_setting(buttonBox          ,10)

        # add Items
        self.substation.addItems(self.subst_list)
        self.action.addItems(self.action_list)
        self._mtr_list = sorted(list(set(filter(lambda x: self.substation.currentText() in x, self.mtr_list))))
        self.maintrasformer.addItems(self._mtr_list)

        # set event
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.substation.currentIndexChanged.connect(self.subst_changed)

    def subst_changed(self):
        subst = self.substation.currentText()
        self.maintrasformer.clear()
        self._mtr_list = sorted(list(set(filter(lambda x: self.substation.currentText() in x, self.mtr_list))))
        self.maintrasformer.addItems(self._mtr_list)
    
    def get_table_content(self):
        query  = "select distinct substation, maintransformer from vw_ls_cfg where substation != 'None' order by 1"
        result = PRISMdb.ExecQuery(query)
        return result

    def font_setting(self, widget, size=None):
        size = 12 if size == None else size
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(size)
        widget.setFont(font)    


# class mode3_StopDialog(QtWidgets.QDialog):
#     def __init__(self, parent, pool):
#         super(mode3_StopDialog, self).__init__(parent)
#         self.setFixedSize(220,80)
#         self.setWindowTitle("[Stop] UF")
#         self.args  = None
#         self.pool  = pool
#         self.tasks = list(pool.keys())

#         # decalre widget 
#         self.label     = QtWidgets.QLabel("Tasks")
#         self.options   = QtWidgets.QComboBox(self)
#         self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)

#         # set layout
#         layout = QtWidgets.QFormLayout(self)
#         layout.addRow(self.label, self.options)
#         layout.addWidget(self.buttonBox)

#         # set event
#         self.buttonBox.accepted.connect(self.execute)
#         self.buttonBox.rejected.connect(self.reject)
    
#         # set font property
#         self.font_setting(self.label     ,10)
#         self.font_setting(self.options   ,10)
#         self.font_setting(self.buttonBox ,10)

#         self.options.addItems(self.tasks)

#     def execute(self):
#         options = self.options.currentText()
#         args    = { "options": options, }
#         self.args = args
#         self.accept()

#     def font_setting(self, widget, size=None):
#         size = 12 if size == None else size
#         font = QtGui.QFont()
#         font.setFamily("Arial")
#         font.setPointSize(size)
#         widget.setFont(font)
