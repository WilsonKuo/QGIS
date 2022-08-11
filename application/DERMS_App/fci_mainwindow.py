#!/bin/python3.6

from __future__ import absolute_import

import os
import sys
import time
import threading
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSettings, QTimer

from mw import Ui_MainWindow
from fci_ttu_info   import FCI_TTU_Info
from tables import TTU_TABLE_SCHEMA as TABLE
from acsprism import rtdb_init

__author__ = 'Wilson Kuo'
#B5934HE05T01
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, obj_name):
        super(MainWindow, self).__init__()
        self.obj_name = obj_name
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ##ui setting
        self.ui.resultlineEdit.textChanged.connect(self.data_to_gui)
        self.ui.conditiontable.setText(self.obj_name)
        self.ui.resulttable.setText("FCI")
        self.ui.settings = QSettings('Wilson','FCI')
        print(self.ui.settings.fileName())
        self.setWindowTitle('FCI')

        try:
            self.resize(self.ui.settings.value('window size'))
            self.move(self.ui.settings.value('window position'))
        except:
            pass

        self.fciInfoSet = list()
        for record in TABLE.get_fci_ttu_info(self.obj_name).resultSet:
            self.fciInfoSet.append(FCI_TTU_Info(record))

        
        # self.lockflag1codebook = {None: 'Online', 0: 'Offline', 1: 'Online'}
        # self.lockflag2codebook = {None: 'No Data', 0: 'Stock', 1: 'Installed', 2: 'Running'}
        # self.eflagcodebook = {0: 'No Data', 1001: 'Low Potential', 1002: 'Demand Overload', 1003: 'Demand Warning', 1004: 'Demand Reset', 1011: 'Cover Open', 1012: 'Cover Close', 1021: 'Primary Power Down', 1022: 'Primary Power Down', 1031: 'Over Voltage', 1032: 'Under Voltage'}
        #self.tablecolumns = ['fci_NAME', 'COMMUNICATION_STATUS', 'OPERATION_STATUS', 'LOAD_INFO', 'V', 'I', 'fci_EVENT']
        #self.tablecolumns = ['fci_NAME', 'OPERATION_STATUS', 'LOAD_INFO', 'V', 'I', 'fci_EVENT']
        self.tablecolumns = ["NAME", "AMPA", "AMPB", "AMPC", "FAULTFLAGA", "FAULTFLAGB", "FAULTFLAGC"]
        self.ui.resulttableWidget.setColumnCount(len(self.tablecolumns))
        self.ui.resulttableWidget.setHorizontalHeaderLabels(self.tablecolumns)
        self.qTimer = QTimer()
        self.qTimer.setInterval(1000) # 1000 ms = 1 s
        self.qTimer.timeout.connect(self.data_to_gui)
        # start timer
        self.qTimer.start()

        

    def data_to_gui(self):
        #1. QtWidgets.QTableWidgetItem(xxx) xxx must be string!
        #2. couldn't define setTextAlignment(QtCore.Qt.AlignCenter)) directly
        self.ui.resulttableWidget.clearContents()
        newresultSet = list()
        
        if len(self.ui.resultlineEdit.text()) == 0:
            for fci in self.fciInfoSet:
                newresultSet.append(fci)
        else:
            for fci in self.fciInfoSet:
                if self.ui.resultlineEdit.text().upper() in fci.name:
                    newresultSet.append(fci)

        self.ui.resulttableWidget.setRowCount(len(newresultSet))
        for row_num, fci in enumerate(newresultSet):
            for col_num, colname in enumerate(self.tablecolumns):
                item = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(getattr(fci, colname.lower()))))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if colname != "NAME":
                    item.setToolTip(getattr(fci, "addrstring_" + colname.lower()))
                self.ui.resulttableWidget.setItem(row_num, col_num, item)
                self.ui.resulttableWidget.setColumnWidth(0, 130)

    def closeEvent(self, event):
        print('Save setting')
        self.ui.settings.setValue('window size', self.size())
        self.ui.settings.setValue('window position', self.pos())
        self.run = False

def main():
    rtdb_init()
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow("N0711AE62S3")
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()