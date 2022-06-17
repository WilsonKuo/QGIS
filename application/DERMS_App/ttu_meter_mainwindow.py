#!/bin/python3.6

from __future__ import absolute_import

import os
import sys
import time
import threading
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSettings

from mw import Ui_MainWindow
from tables import TTU_TABLE_SCHEMA as TABLE


__author__ = 'Wilson Kuo'
#B5934HE05T01
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ttu_name, device):
        super(MainWindow, self).__init__()
        self.ttu_name = ttu_name
        self.device = device
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ##ui setting
        self.ui.resultlineEdit.textChanged.connect(self.data_to_gui)
        self.ui.conditiontable.setText(self.ttu_name)
        self.ui.resulttable.setText("METER")
        self.ui.settings = QSettings('Wilson','TTU_METER')
        print(self.ui.settings.fileName())
        self.setWindowTitle('TTU_METER')

        try:
            self.resize(self.ui.settings.value('window size'))
            self.move(self.ui.settings.value('window position'))
        except:
            pass

        self.meterInfoSet = list()
        for record in TABLE.get_meter_data(self.ttu_name).resultSet:
            self.meterInfoSet.append(record)
        
        self.lockflag1codebook = {None: 'Online', 0: 'Offline', 1: 'Online'}
        self.lockflag2codebook = {None: 'No Data', 0: 'Stock', 1: 'Installed', 2: 'Running'}
        self.eflagcodebook = {0: 'No Data', 1001: 'Low Potential', 1002: 'Demand Overload', 1003: 'Demand Warning', 1004: 'Demand Reset', 1011: 'Cover Open', 1012: 'Cover Close', 1021: 'Primary Power Down', 1022: 'Primary Power Down', 1031: 'Over Voltage', 1032: 'Under Voltage'}
        #self.tablecolumns = ['METER_NAME', 'COMMUNICATION_STATUS', 'OPERATION_STATUS', 'LOAD_INFO', 'V', 'I', 'METER_EVENT']
        self.tablecolumns = ['METER_NAME', 'OPERATION_STATUS', 'LOAD_INFO', 'V', 'I', 'METER_EVENT']
        self.ui.resulttableWidget.setColumnCount(len(self.tablecolumns))
        self.ui.resulttableWidget.setHorizontalHeaderLabels(self.tablecolumns)
        self.data_to_gui()

        self.interval = 5
        self.run = True
        self.thread = threading.Thread(target = self.update_resultSet)
        self.thread.start()


    def update_resultSet(self):
        tmp_interval = self.interval
        while self.run:
            tmp_interval -= 1
            if tmp_interval == 0:
                sys.stdout.write('\rRefresh Table in {0} second(s)'.format(tmp_interval))
                sys.stdout.flush()
                # print('no need to update resultSet')
                self.meterInfoSet *= 0
                for record in TABLE.get_meter_data(self.ttu_name).resultSet:
                    self.meterInfoSet.append(record)
                self.data_to_gui()
                print('\nRefresh Table Successfully')
                tmp_interval = self.interval
            time.sleep(1)
            sys.stdout.write('\rRefresh Table in {0} second(s)'.format(tmp_interval))
            sys.stdout.flush()
    def data_to_gui(self):
        #1. QtWidgets.QTableWidgetItem(xxx) xxx must be string!
        #2. couldn't define setTextAlignment(QtCore.Qt.AlignCenter)) directly
        newresultSet = list()
        if len(self.ui.resultlineEdit.text()) == 0:
            for meter in self.meterInfoSet:
                newresultSet.append(meter)
        else:
            for meter in self.meterInfoSet:
                if self.ui.resultlineEdit.text() in meter['METER_NAME']:
                    newresultSet.append(meter)

        self.ui.resulttableWidget.setRowCount(len(newresultSet))
        for row, meter in enumerate(newresultSet):
            item_name = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str( meter['METER_NAME'])))
            item_name.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.resulttableWidget.setItem(row, 0, item_name)
            self.ui.resulttableWidget.setColumnWidth(0, 130)
        
            # item_lockflag1 = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(self.lockflag1codebook[meter.lockflag1])))
            # item_lockflag1.setTextAlignment(QtCore.Qt.AlignCenter)
            # item_lockflag1.setToolTip(meter.addrstring_lockflag1)
            # self.ui.resulttableWidget.setItem(row, 1, item_lockflag1)
            
            item_lockflag2 = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(self.lockflag2codebook[meter['LOCKFLAG2']])))
            item_lockflag2.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.resulttableWidget.setItem(row, 2 - 1, item_lockflag2)
            self.ui.resulttableWidget.setColumnWidth(2 - 1, 180)

            item_p = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(meter['PA'])))
            item_p.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.resulttableWidget.setItem(row, 3 - 1, item_p)

            # item_v = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(meter.v)))
            # item_v.setTextAlignment(QtCore.Qt.AlignCenter)
            # item_v.setToolTip(meter.addrstring_v)
            # self.ui.resulttableWidget.setItem(row, 4 - 1, item_v)

            item_i = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(round(meter['AMPA'], 3))))
            item_i.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.resulttableWidget.setItem(row, 5 - 1, item_i)

            item_eflag = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(self.eflagcodebook[meter['EFLAG']])))
            item_eflag.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.resulttableWidget.setItem(row, 6 - 1, item_eflag)
            self.ui.resulttableWidget.setColumnWidth(6 - 1, 200)

    def closeEvent(self, event):
        print('Save setting')
        self.ui.settings.setValue('window size', self.size())
        self.ui.settings.setValue('window position', self.pos())
        self.run = False

def main():
    rtdb_init()
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()