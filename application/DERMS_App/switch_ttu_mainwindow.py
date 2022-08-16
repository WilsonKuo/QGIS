#!/bin/python3.6

from __future__ import absolute_import

import os
import sys
import time
import threading
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSettings, QTimer

# from radiobutton import RadioButton
from acsprism import rtdb_init
from ttuinfo import TTUInfo
from mw import Ui_MainWindow
from tables import TTU_TABLE_SCHEMA as TABLE
from ttu_meter_mainwindow import MainWindow as MeterMainWindow
# from acstw.OracleInterface import OracleInterface


DPF_RATIO = 0.8
TTU_RATIO = 0.2

#B6228DB5132S01
__author__ = 'Wilson Kuo'

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, switch_name, device):
        super(MainWindow, self).__init__()
        self.switch_name = switch_name
        self.device = device
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ##ui setting
        #self.ui.resulttableWidget.doubleClicked.connect(self.opendisplay)
        self.ui.resultlineEdit.textChanged.connect(self.data_to_gui)
        self.ui.conditiontable.setText(self.switch_name)
        self.ui.resulttable.setText("TTU")
        self.ui.settings = QSettings('Wilson','SWITCH_TTU')
        print(self.ui.settings.fileName())
        self.setWindowTitle('SWITCH_TTU')


    # def _on_refresh(self):
    #     self.dataChanged.emit(
    #         self.index(0, 0),
    #         self.index(self.rowCount() - 1, self.columnCount() - 1))

        try:
            self.resize(self.ui.settings.value('window size'))
            self.move(self.ui.settings.value('window position'))
        except:
            pass
        
        self.ttuinfoSet = list()
        for record in TABLE.get_ttu_info(self.switch_name).resultSet:
            self.ttuinfoSet.append(TTUInfo(record))

        self.flag2codebook = {None: 'No flag', 0: 'Normal', 1: 'Steal'}
        self.flag3codebook = {None: 'No flag', 0: 'Normal', 1: 'Comm Off'}            
        self.flag4codebook = {None: 'No flag', 0: 'Normal', 1: 'Oper Off'}            

        self.existfile = list()
        for f in os.listdir("/home/acs/DB/SCREEN"):
            if 'BKG' in f:
                self.existfile.append(f)
        
        self.ttudisplaynumberdict = dict()
        for ttu in self.ttuinfoSet:
            self.ttudisplaynumberdict[ttu.name] = ttu.display_number
        #self.tablecolumns = ['TTU_NAME', 'DISPLAY_NUMBER', 'COMPARE_P', 'COMPARE_Q', 'TTU_P', 'TTU_Q', 'DPF_P', 'DPF_Q', 'MDMS_P', 'MDMS_Q', 'CAPACITY', 'USAGE_RATE', 'FLAG1', 'FLAG2', 'FLAG3', 'FLAG4']
        self.tablecolumns = ['TTU_NAME', 'DISPLAY_NUMBER', 'TTU_P', 'TTU_Q', 'CAPACITY', 'USAGE_RATE', 'FLAG1', 'FLAG2', 'FLAG3', 'FLAG4']
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
            for ttu in self.ttuinfoSet:
                newresultSet.append(ttu)
        else:
            for ttu in self.ttuinfoSet:
                if self.ui.resultlineEdit.text().upper() in ttu.name:
                    newresultSet.append(ttu)

        self.ui.resulttableWidget.setRowCount(len(newresultSet))
        for row, ttu in enumerate(newresultSet):
            item_name = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(ttu.name)))
            item_name.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.resulttableWidget.setItem(row, 0, item_name)
            self.ui.resulttableWidget.setColumnWidth(0,200)
        
            item_display_number = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(ttu.display_number)))
            item_display_number.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.resulttableWidget.setItem(row, 1, item_display_number)
            self.ui.resulttableWidget.setColumnWidth(1,150)

            # if (ttu.ttu_p * TTU_RATIO + ttu.dpf_p * DPF_RATIO) < ttu.mdms_p:
            #     item_compare_p = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(1)))
            # else:
            #     item_compare_p = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(0)))
            # item_compare_p.setTextAlignment(QtCore.Qt.AlignCenter)
            # item_compare_p.setToolTip(ttu.addrstring_ttu_p)
            # self.ui.resulttableWidget.setItem(row, 2, item_compare_p)

            # if (ttu.ttu_q * TTU_RATIO + ttu.dpf_q * DPF_RATIO) < ttu.mdms_q:
            #     item_compare_q = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(1)))
            # else:
            #     item_compare_q = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(0)))
            # item_compare_q.setTextAlignment(QtCore.Qt.AlignCenter)
            # item_compare_q.setToolTip(ttu.addrstring_ttu_q)
            # self.ui.resulttableWidget.setItem(row, 3, item_compare_q)

            item_ttu_p = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(ttu.ttu_p)))
            item_ttu_p.setTextAlignment(QtCore.Qt.AlignCenter)
            item_ttu_p.setToolTip(ttu.addrstring_ttu_p)
            self.ui.resulttableWidget.setItem(row, 2, item_ttu_p)

            item_ttu_q = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(ttu.ttu_q)))
            item_ttu_q.setTextAlignment(QtCore.Qt.AlignCenter)
            item_ttu_q.setToolTip(ttu.addrstring_ttu_q)
            self.ui.resulttableWidget.setItem(row, 3, item_ttu_q)

            # item_dpf_p = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(ttu.dpf_p)))
            # item_dpf_p.setTextAlignment(QtCore.Qt.AlignCenter)
            # self.ui.resulttableWidget.setItem(row, 6, item_dpf_p)

            # item_dpf_q = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(ttu.dpf_q)))
            # item_dpf_q.setTextAlignment(QtCore.Qt.AlignCenter)
            # self.ui.resulttableWidget.setItem(row, 7, item_dpf_q)

            # item_mdms_p = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(ttu.mdms_p)))
            # item_mdms_p.setTextAlignment(QtCore.Qt.AlignCenter)
            # self.ui.resulttableWidget.setItem(row, 8, item_mdms_p)

            # item_mdms_q = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(ttu.mdms_q)))
            # item_mdms_q.setTextAlignment(QtCore.Qt.AlignCenter)
            # self.ui.resulttableWidget.setItem(row, 9, item_mdms_q)

            item_capacity = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(ttu.capacity)))
            item_capacity.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.resulttableWidget.setItem(row, 4, item_capacity)

            item_usage_rate = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(ttu.usage_rate)))
            item_usage_rate.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.resulttableWidget.setItem(row, 5, item_usage_rate)

            #QtCore.Qt.DecorationRole
            # item_flag1 = RadioButton(ttu.flag1).widgets
            # self.ui.resulttableWidget.setCellWidget(row, 8, item_flag1)
            item_flag1 = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(str(ttu.flag1)))
            item_flag1.setTextAlignment(QtCore.Qt.AlignCenter)
            item_flag1.setToolTip(ttu.addrstring_flag1)
            self.ui.resulttableWidget.setItem(row, 6, item_flag1)

            # item_flag2 = RadioButton(ttu.flag2).widgets
            # self.ui.resulttableWidget.setCellWidget(row, 9, item_flag2)
            item_flag2 = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(self.flag2codebook[ttu.flag2]))
            item_flag2.setTextAlignment(QtCore.Qt.AlignCenter)
            item_flag2.setToolTip(ttu.addrstring_flag2)
            self.ui.resulttableWidget.setItem(row, 7, item_flag2)

            # item_flag3 = RadioButton(ttu.flag3).widgets
            # self.ui.resulttableWidget.setCellWidget(row, 10, item_flag3)
            item_flag3 = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(self.flag3codebook[ttu.flag3]))
            item_flag3.setTextAlignment(QtCore.Qt.AlignCenter)
            item_flag3.setToolTip(ttu.addrstring_flag3)
            self.ui.resulttableWidget.setItem(row, 8, item_flag3)

            # item_flag4 = RadioButton(ttu.flag4).widgets
            # self.ui.resulttableWidget.setCellWidget(row, 10, item_flag4)
            item_flag4 = QtWidgets.QTableWidgetItem(QtWidgets.QTableWidgetItem(self.flag4codebook[ttu.flag4]))
            item_flag4.setTextAlignment(QtCore.Qt.AlignCenter)
            item_flag4.setToolTip(ttu.addrstring_flag4)
            self.ui.resulttableWidget.setItem(row, 9, item_flag4)

            if 'BKG' + str(self.ttudisplaynumberdict[ttu.name]) + '.M' in self.existfile:
                for col in range(0,2):
                    self.ui.resulttableWidget.item(row, col).setBackground(QtGui.QColor(100,100,150))
    
    def contextMenuEvent(self, event):
        if self.ui.resulttableWidget.selectionModel().selection().indexes():
            for i in self.ui.resulttableWidget.selectionModel().selection().indexes():
                row, column = i.row(), i.column()
            menu = QtWidgets.QMenu()
            meterAction = menu.addAction("METER")
            oiAction = menu.addAction("TTU DISPLAY")
            action = menu.exec_(self.mapToGlobal(event.pos()))
            ttu_name = self.ui.resulttableWidget.item(row,0).text()
            if action == meterAction:
                ui = MeterMainWindow(ttu_name, self.device)
                ui.show()
            elif action== oiAction:
                current_display = self.ttudisplaynumberdict[ttu_name]
                #os.system('oiint {} -c display -fwin {}'.format(sys.argv[1], current_display))
                os.system('oiint {} -c display -fwin {}'.format(self.device, current_display))

    # def opendisplay(self):
    #     current_display = self.ttudisplaynumberdict[str(self.ui.resulttableWidget.item(self.ui.resulttableWidget.currentRow(),0).text())]
    #     #os.system('oiint {} -c display -fwin {}'.format(sys.argv[1], current_display))
    #     os.system('oiint {} -c display -fwin {}'.format(self.device, current_display))

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