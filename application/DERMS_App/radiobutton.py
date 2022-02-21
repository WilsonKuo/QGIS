#!/bin/python3.6
from PyQt5 import QtCore, QtWidgets

class RadioButton(object):
    def __init__(self, FLAG):
        super(RadioButton,self).__init__()
        self.FLAG = FLAG
        self.FLAGradioButton = QtWidgets.QRadioButton()
        self.FLAGradioButton.setObjectName("FLAG")
        self.FLAGradioButton.setChecked(True)
        self.FLAGradioButton.setDisabled(True)
        self.FLAGradioButton.setToolTip('???')
        if self.FLAG == 1:
            self.FLAGradioButton.setStyleSheet("""
                                               QRadioButton::indicator { width: 12px; height: 12px; border-radius: 7px; border: 1px solid black; font-size: 12pt; font-weight:bold; font-family: Arial;  }
                                               QRadioButton::indicator:checked { background-color: green; border: 2px solid white; } 
                                               """)
        elif self.FLAG == 0:
            self.FLAGradioButton.setStyleSheet("""
                                               QRadioButton::indicator { width: 12px; height: 12px; border-radius: 7px; border: 1px solid black; font-size: 12pt; font-weight:bold; font-family: Arial;  }
                                               QRadioButton::indicator:checked { background-color: red; border: 2px solid white; } 
                                               """)
        else:    
            self.FLAGradioButton.setStyleSheet("""
                                               QRadioButton::indicator { width: 12px; height: 12px; border-radius: 7px; border: 1px solid black; font-size: 12pt; font-weight:bold; font-family: Arial;  }
                                               QRadioButton::indicator:checked { background-color: white; border: 2px solid black; } 
                                               """)
        #### Align Center####            
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.FLAGradioButton)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setContentsMargins(0,0,0,0)
        self.widgets = QtWidgets.QTableWidget()
        self.widgets.setLayout(self.layout)