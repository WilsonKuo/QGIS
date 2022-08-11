#!/bin/python3.6

from __future__ import absolute_import

import os
import sys
import time
import datetime
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSettings, QTimer
import locale

# from radiobutton import RadioButton
from acsprism import rtdb_init
from mw2 import Ui_MainWindow
from tables import TTU_TABLE_SCHEMA as TABLE
from ttu_meter_mainwindow import MainWindow as MeterMainWindow
# from acstw.OracleInterface import OracleInterface


#B6228DB5132S01
__author__ = 'Wilson Kuo'

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, obj_name):
        super(MainWindow, self).__init__()
        self.obj_name = obj_name
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ##ui setting
        #self.ui.resulttableWidget.doubleClicked.connect(self.opendisplay)
        # self.ui.resultlineEdit.textChanged.connect(self.data_to_gui)
        self.ui.conditiontable.setText(self.obj_name)
        self.ui.resulttable.setText("CMP")
        self.ui.settings = QSettings('Wilson','CMP')
        print(self.ui.settings.fileName())
        self.setWindowTitle('CMP')


    # def _on_refresh(self):
    #     self.dataChanged.emit(
    #         self.index(0, 0),
    #         self.index(self.rowCount() - 1, self.columnCount() - 1))

        try:
            self.resize(self.ui.settings.value('window size'))
            self.move(self.ui.settings.value('window position'))
        except:
            pass
        

 
        self.tablecolumns = ['NAME', 'PA', 'PB', 'PC', 'QA', 'QB', 'QC']
        self.caltablecolumns = ['PA', 'PB', 'PC', 'QA', 'QB', 'QC']
        #self.tablecolumns = ['cmp_NAME', 'DISPLAY_NUMBER', 'P', 'Q', 'V', 'CAPACITY', 'USAGE_RATE', 'FLAG1', 'FLAG2', 'FLAG3', 'FLAG4']
        self.ui.resulttableWidget.setColumnCount(len(self.tablecolumns))
        self.ui.resulttableWidget.setHorizontalHeaderLabels(self.tablecolumns)
        self.ui.pushButton.clicked.connect(self.data_to_gui)
        locale.setlocale(locale.LC_ALL, "C")


    def data_to_gui(self):

        #1. QtWidgets.QTableWidgetItem(xxx) xxx must be string!
        #2. couldn't define setTextAlignment(QtCore.Qt.AlignCenter)) directly

        # MONTH
        datetime_object = datetime.datetime.strptime(str(self.ui.dateTimeEdit.date().month()), "%m")
        month_name = datetime_object.strftime("%b")
        full_month_name = datetime_object.strftime("%B")
        # MINUTE
        minute = self.ui.dateTimeEdit.time().minute()
        if minute >= 0 and minute < 15:
            minute = 0
        elif minute >= 15 and minute < 30:
            minute = 15
        elif minute >= 30 and minute < 45:
            minute = 30
        else:
            minute = 45
        # QUERY
        self.ui.resulttableWidget.clearContents()
        
        sourcedict = dict()
        targetdict = dict()
        namelist   = TABLE.get_cmp_name(self.obj_name).resultSet
        for name in namelist:
            sourcedict[name] = dict()
            targetdict[name] = dict()
            for col in self.caltablecolumns:
                sourcedict[name][col] = 0
                targetdict[name][col] = 0

        if self.ui.mdmscheckBox1.isChecked() or self.ui.mdmscheckBox2.isChecked():
            for record in TABLE.get_cmp_info('MDMS', self.obj_name, self.ui.dateTimeEdit.date().year(), full_month_name, self.ui.dateTimeEdit.date().day(), self.ui.dateTimeEdit.time().hour(), minute).resultSet:
                name = record['NAME']
                for col in self.caltablecolumns:
                    if col in record.keys():
                        if self.ui.mdmscheckBox1.isChecked():
                            sourcedict[name][col] += record[col] * self.ui.mdmsdoubleSpinBox1.value()
                        if self.ui.mdmscheckBox2.isChecked():
                            targetdict[name][col] += record[col] * self.ui.mdmsdoubleSpinBox2.value()
                    else:
                        pass

        if self.ui.ttucheckBox1.isChecked() or self.ui.ttucheckBox2.isChecked():
            for record in TABLE.get_cmp_info('TTU', self.obj_name, self.ui.dateTimeEdit.date().year(), full_month_name, self.ui.dateTimeEdit.date().day(), self.ui.dateTimeEdit.time().hour(), minute).resultSet:
                name = record['NAME']
                for col in self.caltablecolumns:
                    if col in record.keys():
                        if self.ui.ttucheckBox1.isChecked():
                            sourcedict[name][col] += record[col] * self.ui.ttudoubleSpinBox1.value()
                        if self.ui.ttucheckBox2.isChecked():
                            targetdict[name][col] += record[col] * self.ui.ttudoubleSpinBox2.value()
                    else:
                        pass

        if self.ui.dpfcheckBox1.isChecked() or self.ui.dpfcheckBox2.isChecked():
            for record in TABLE.get_cmp_info('DPF', self.obj_name, self.ui.dateTimeEdit.date().year(), full_month_name, self.ui.dateTimeEdit.date().day(), self.ui.dateTimeEdit.time().hour(), minute).resultSet:
                name = record['NAME']
                for col in self.caltablecolumns:
                    if col in record.keys():
                        if self.ui.dpfcheckBox1.isChecked():
                            sourcedict[name][col] += record[col] * self.ui.dpfdoubleSpinBox1.value()
                        if self.ui.dpfcheckBox2.isChecked():
                            targetdict[name][col] += record[col] * self.ui.dpfdoubleSpinBox2.value()
                    else:
                        pass




        newinfoSet = list()
        if len(self.ui.resultlineEdit.text()) == 0:
            for name in namelist:
                cmp = dict()
                cmp['NAME'] = name
                for col in self.caltablecolumns:
                    cmp[col]= round(targetdict[name][col] - sourcedict[name][col], 3)
                newinfoSet.append(cmp)
        else:
            for name in namelist:
                if self.ui.resultlineEdit.text() in name:
                    cmp = dict()
                    cmp['NAME'] = name
                    for col in self.caltablecolumns:
                        cmp[col]= round(targetdict[name][col] - sourcedict[name][col], 3)
                    newinfoSet.append(cmp)

        self.ui.resulttableWidget.setRowCount(len(newinfoSet))
        for row_num, cmp in enumerate(newinfoSet):
            for col_num, colname in enumerate(self.tablecolumns):
                item = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(cmp[colname])))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.resulttableWidget.setItem(row_num, col_num, item)
                self.ui.resulttableWidget.setColumnWidth(0, 160)


    def closeEvent(self, event):
        print('Save setting')
        self.ui.settings.setValue('window size', self.size())
        self.ui.settings.setValue('window position', self.pos())
        self.run = False

def main():
    rtdb_init()
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow("P8898GD94S4")
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()