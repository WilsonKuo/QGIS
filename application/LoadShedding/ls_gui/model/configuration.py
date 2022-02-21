# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
__author__ = 'Darren Liang'


import os
import operator
import datetime
import logging

from model.refresh_mixin   import RefreshMixin
from core.QtCompat                     import QtWidgets, QtGui, QtCore, Qt
from core.OracleInterface        import OracleInterface


logger  = logging.getLogger(__name__)

USER    = os.getenv('ORACLE_USER', 'acs_das')
PSWD    = os.getenv('ORACLE_PW'  , 'acs_das')
TNS     = os.getenv('ORACLE_DBSTRING', 'emsa')
PRISMdb = OracleInterface(USER, PSWD, TNS)

HEADERS = ("NAME", "VALUE", "COMMENTS")


# TODO: merge with common station view/model in acsprism package?
class ConfigurationTableModel(RefreshMixin, QtCore.QAbstractTableModel):
    # parent is required for models, otherwise you get spurious Qt warnings
    def __init__(self, parent):
        super(ConfigurationTableModel, self).__init__()

        # get data from sql
        self._datas  = []
        self.HEADERS = HEADERS

        self._col_name  = HEADERS.index("NAME")
        self._col_value = HEADERS.index("VALUE")
        self.re_init()

    
    @property
    def datas(self):
        return self._datas

    def re_init(self):
        with self._pause_refresh():
            self.beginResetModel()
            self._datas = self.get_data()        
            self.endResetModel()
    
    def _on_refresh(self):
        self._datas = self.get_data()
        self.invalidate()
        # logger.info("Refreshing configuration model")

    def invalidate(self):
        # logger.debug("Refreshing")

        # Behavior of emitting with invalid indexes is not documented
        # self.dataChanged.emit(QModelIndex(), QModelIndex())

        # Indicate that all the attribute values changed, so the view
        # will re-read them.
        # Even though I give the column, it still seems to read all columns.
        # Indeed, even if I specify just one row, it still seems to read
        # all the visible rows and columns. I wonder what the point of the
        # arguments are anyway... am I doing it wrong?
        # May need to check Qt source code.
        self.dataChanged.emit(
            self.index(0, 0),
            self.index(self.rowCount() - 1, self.columnCount() - 1))

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.datas)

    def columnCount(self, index=QtCore.QModelIndex()):
        return len(self.HEADERS)

    def setData(self, index, value, role=Qt.EditRole):
        row  = index.row()
        col  = index.column()
        name = self._datas[row][self._col_name]

        if role == QtCore.Qt.EditRole:
            query = f"update ls_configuration set value = '{value}' where name='{name}'"
            PRISMdb.ExecNonQuery(query)
            self.dataChanged.emit(index, index)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        row = index.row()
        column = index.column()
        
        if role == QtCore.Qt.DisplayRole:
            value = self.datas[row][column]           
            return str(value)

        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return self.HEADERS[section]
        return int(section + 1)
    
    def flags(self, index):
        if index.column() == self._col_value:
            return (super(ConfigurationTableModel, self).flags(index) | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        else:
            return (super(ConfigurationTableModel, self).flags(index) | QtCore.Qt.ItemIsEnabled)

    def get_data(self):
        query = "select name, value, comments from ls_configuration"
        data  = list(map(list, PRISMdb.ExecQuery(query)))
        return data
        # return []