#!/bin/python3.6
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mw.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(669, 616)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.conditiontable = QtWidgets.QLabel(self.centralwidget)
        self.conditiontable.setObjectName("conditiontable")
        self.horizontalLayout_7.addWidget(self.conditiontable)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.resulttable = QtWidgets.QLabel(self.centralwidget)
        self.resulttable.setObjectName("resulttable")
        self.horizontalLayout_6.addWidget(self.resulttable)
        self.resultlineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.resultlineEdit.setObjectName("resultlineEdit")
        self.horizontalLayout_6.addWidget(self.resultlineEdit)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.resulttableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.resulttableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.resulttableWidget.setColumnCount(0)
        self.resulttableWidget.setObjectName("resulttableWidget")
        self.resulttableWidget.setRowCount(0)
        self.horizontalLayout_4.addWidget(self.resulttableWidget)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 669, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuLanguage = QtWidgets.QMenu(self.menubar)
        self.menuLanguage.setObjectName("menuLanguage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionEnglish = QtWidgets.QAction(MainWindow)
        self.actionEnglish.setObjectName("actionEnglish")
        self.actionChinese = QtWidgets.QAction(MainWindow)
        self.actionChinese.setObjectName("actionChinese")
        self.menuFile.addAction(self.actionExit)
        self.menuLanguage.addAction(self.actionEnglish)
        self.menuLanguage.addAction(self.actionChinese)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.conditiontable.setText(_translate("MainWindow", "Condition"))
        self.resulttable.setText(_translate("MainWindow", "Result"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuLanguage.setTitle(_translate("MainWindow", "Language"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionEnglish.setText(_translate("MainWindow", "English"))
        self.actionChinese.setText(_translate("MainWindow", "Chinese"))
