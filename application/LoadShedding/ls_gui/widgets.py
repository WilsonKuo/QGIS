# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""

__author__ = 'Darren Liang'

import os
import logging

from collections   import OrderedDict 
from core.QtCompat      import QtWidgets, QtGui, QtCore, Signal, Slot, Qt
from core.acsQt         import actions

from core.OracleInterface import OracleInterface

logger  = logging.getLogger(__name__)
USER    = os.getenv('ORACLE_USER', 'acs_das')
PSWD    = os.getenv('ORACLE_PW'  , 'acs_das')
TNS     = os.getenv('ORACLE_DBSTRING', 'emsa')
PRISMdb = OracleInterface(USER, PSWD, TNS)

class DockWidget(QtWidgets.QDockWidget):
    def __init__(self, name):
        super(DockWidget, self).__init__()
        self.setObjectName(name)
        self.setWindowTitle(name)

        self.setStyleSheet("QDockWidget::title{ background : gainsboro;}")
        self.setFeatures(
            QtWidgets.QDockWidget.DockWidgetMovable   |
            QtWidgets.QDockWidget.DockWidgetFloatable |
            QtWidgets.QDockWidget.DockWidgetClosable)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.setFont(font)
    
class GroupsWidget(QtWidgets.QComboBox):
    """
    A combo box for selecting an Group.

    Groups are updated based on the ls_group table in DASDB.
    """
    group_changed = Signal(str)

    def __init__(self, short_names=False, parent=None):
        super(GroupsWidget, self).__init__(parent)
        self.setToolTip("Groups")
        self.setMinimumSize(QtCore.QSize(100, 25))
        self.setMaximumSize(QtCore.QSize(100, 16777215))
        self.currentIndexChanged.connect(self._group_changed)
        
        items = self.get_items_from_db()
        self.set_item(items)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.setFont(font)

    def set_item(self, items):
        self.clear()
        self.addItems(items)

    @Slot(int)
    def _group_changed(self, index):
        if index >= 0:
            category = str(self.itemText(index)[0])
            self.group_changed.emit(category)

    @property
    def group(self):
        if self.currentText():
            return str(self.currentText())

    @group.setter
    def group(self, group):
        if not group:
            return
        i = self.findText(group, Qt.MatchStartsWith)
        if i >= 0:
            self.setCurrentIndex(i)

    def get_items_from_db(self):
        query = "select groupname from ls_group order by gid"
        # return ['ALL'] + sorted([ str(record[0]) for record in PRISMdb.ExecQuery(query)])
        return []

class FeederWidget(QtWidgets.QLineEdit):
    feeder_changed = Signal(str)

    def __init__(self, parent=None):
        super(FeederWidget, self).__init__(parent)
        self.setToolTip("Feeder Search") 
        self.setMinimumSize(QtCore.QSize(150, 25))
        self.setMaximumSize(QtCore.QSize(150, 16777215))
        self.setPlaceholderText("Feeder Search")
        self.textEdited.connect(self._feeder_changed)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.setFont(font)

        regexRule = QtCore.QRegExp("[0-9A-Za-z\-\,]+")
        validator = QtGui.QRegExpValidator(regexRule)
        self.setValidator(validator)

    @Slot(str)
    def _feeder_changed(self, text):
        if len(text) >= 0:
            self.feeder_changed.emit(str(text))

    @property
    def feeder(self):
        if len(str(self.text()))>0:
            return str(self.text())

    @feeder.setter
    def feeder(self, text):
        if len(text) >= 0:
            self.setText(str(text))

class SubstationWidget(QtWidgets.QLineEdit):
    substation_changed = Signal(str)
    
    def __init__(self, parent=None):
        super(SubstationWidget, self).__init__(parent)
        self.setToolTip("Substation Search")   
        self.setMinimumSize(QtCore.QSize(150, 25))
        self.setMaximumSize(QtCore.QSize(150, 16777215))
        self.setPlaceholderText("Substation Search")
        self.textEdited.connect(self._substation_changed)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.setFont(font)

        regexRule = QtCore.QRegExp("[0-9A-Za-z\-\,]+")
        validator = QtGui.QRegExpValidator(regexRule)
        self.setValidator(validator)

    @Slot(str)
    def _substation_changed(self, text):
        if len(text) >= 0:
            self.substation_changed.emit(str(text))

    @property
    def substation(self):
        if len(str(self.text()))>0:
            return str(self.text())

    @substation.setter
    def substation(self, text):
        if len(text) >= 0:
            self.setText(str(text))

class FromDateWidget(QtWidgets.QDateTimeEdit):
    """
    A datetime edit for selecting an Log table From time.

    """
    time_changed = Signal(str)

    def __init__(self, parent=None):
        super(FromDateWidget, self).__init__(parent)
        self.setToolTip("Start time")
        self.setMinimumSize(QtCore.QSize(200, 0))
        self.setMaximumSize(QtCore.QSize(200, 16777215))
        self.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.setCalendarPopup(True)
        self.dateTimeChanged.connect(self._time_changed)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.setFont(font)
        
        self.set_init_datetime()

    def set_init_datetime(self):
        _nowtime = QtCore.QDateTime.currentDateTime()
        self.setDateTime(_nowtime.addDays(-1))
        self.setMaximumDate(_nowtime.date())

    @QtCore.pyqtSlot(QtCore.QDateTime)
    def _time_changed(self, dt):
        return dt

    @property
    def value(self):
        return str(self.dateTime().toString("yyyy-MM-dd hh:mm:ss"))

    @value.setter
    def value(self, value):
        if not value:
            return
        self.setDateTime(QtCore.QDateTime(value))

class ToDateWidget(QtWidgets.QDateTimeEdit):
    """
    A datetime edit for selecting an Log table To time.

    """
    time_changed = Signal(str)

    def __init__(self, parent=None):
        super(ToDateWidget, self).__init__(parent)
        self.setToolTip("End time")
        self.setMinimumSize(QtCore.QSize(200, 0))
        self.setMaximumSize(QtCore.QSize(200, 16777215))
        self.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.setCalendarPopup(True)
        self.dateTimeChanged.connect(self._time_changed)
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.setFont(font)
        
        self.set_init_datetime()

    def set_init_datetime(self):
        _nowtime = QtCore.QDateTime.currentDateTime()
        _nowdate = _nowtime.date()
        self.setDate(_nowdate.addDays(1))
        # self.setDateTime(_nowtime.addDays(1))
        # self.setMinimumDate(_nowtime.date().addDays(-1))

    @QtCore.pyqtSlot(QtCore.QDateTime)
    def _time_changed(self, dt):
        return dt

    @property
    def value(self):
        return str(self.dateTime().toString("yyyy-MM-dd hh:mm:ss"))

    @value.setter
    def value(self, value):
        if not value:
            return
        self.setDateTime(QtCore.QDateTime(value))

class ExecButtonWidget(QtWidgets.QPushButton):

    def __init__(self, name):
        super(ExecButtonWidget, self).__init__()
        self.setToolTip(name)
        self.setMinimumSize(QtCore.QSize(120, 25))
        self.setMaximumSize(QtCore.QSize(120, 16777215))
        self.setObjectName(name)
        self.setText(name)
        self.menu_setup()

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.setFont(font)
    
    def menu_setup(self):
        main_menu = QtWidgets.QMenu()
        self.action0 = main_menu.addAction('Restore')
        self.action1 = main_menu.addAction('ByDemand')
        self.action2 = main_menu.addAction('Rotating')
        self.action3 = main_menu.addAction('UF')

        self.font_setting(self.action0, 10)
        self.font_setting(self.action1, 10)
        self.font_setting(self.action2, 10)
        self.font_setting(self.action3, 10)
        self.setMenu(main_menu)

    def font_setting(self, widget, size=None):
        size = 12 if size == None else size
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(size)
        widget.setFont(font)

class StopButtonWidget(QtWidgets.QPushButton):

    def __init__(self, name):
        super(StopButtonWidget, self).__init__()
        self.setToolTip(name)
        self.setMinimumSize(QtCore.QSize(120, 25))
        self.setMaximumSize(QtCore.QSize(120, 16777215))
        self.setObjectName(name)
        self.setText(name)
        self.menu_setup()

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.setFont(font)
    
    def menu_setup(self):
        main_menu = QtWidgets.QMenu()
        self.action0 = main_menu.addAction('Restore')
        self.action1 = main_menu.addAction('ByDemand')
        self.action2 = main_menu.addAction('Rotating')
        self.action3 = main_menu.addAction('UF')

        self.action0.setEnabled(False)
        self.action1.setEnabled(False)
        self.action2.setEnabled(False)
        self.action3.setEnabled(False)

        self.font_setting(self.action0, 10)
        self.font_setting(self.action1, 10)
        self.font_setting(self.action2, 10)
        self.font_setting(self.action3, 10)
        self.setMenu(main_menu)

    def font_setting(self, widget, size=None):
        size = 12 if size == None else size
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(size)
        widget.setFont(font)


class LightWidget(QtWidgets.QRadioButton):
    def __init__(self, name):
        super(LightWidget, self).__init__()
        # self.setToolTip(name)
        self.setObjectName(name)
        self.setMinimumSize(QtCore.QSize(50, 20))
        self.setMaximumSize(QtCore.QSize(120, 16777215))
        self.setChecked(True)
        self.setEnabled(False)
        self.setAutoExclusive(False)
        self.setText(name)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setWeight(75)
        self.setFont(font)
        self.set_task_color("White")

    def set_task_tip(self, tasks):
        tasks = "\n".join([ f"{i}. {d}" for i, d in enumerate(tasks)])
        self.setToolTip(tasks)

    def set_task_color(self, color):
        css_code = """
            QRadioButton {
                color: #708090
            }
            QRadioButton::indicator { 
                width: 14px; 
                height: 14px; 
                border-radius: 8px;
                border-style: outset;
                border: 0.5px solid black; 
            }
            QRadioButton::indicator:checked { 
                border: 0.5px solid black;  
                border-style: outset;
                background-color: %s; 
            };

        """ % color
        self.setStyleSheet(css_code)
