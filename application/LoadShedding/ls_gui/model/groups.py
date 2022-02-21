# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
__author__ = 'Darren Liang'


import os
import operator
import itertools
import datetime
import logging

from model.refresh_mixin   import RefreshMixin
from core.QtCompat                     import QtWidgets, QtGui, QtCore, Qt
from core.OracleInterface        import OracleInterface
from acstw.LinuxInterface         import LinuxInterface


logger  = logging.getLogger(__name__)

USER    = os.getenv('ORACLE_USER', 'acs_das')
PSWD    = os.getenv('ORACLE_PW'  , 'acs_das')
TNS     = os.getenv('ORACLE_DBSTRING', 'emsa')
PRISMdb = OracleInterface(USER, PSWD, TNS)
PRISM   = LinuxInterface()

# HEADERS = ("GROUPNAME", "AREA", "TOTAL")
HEADERS = ("GROUPNAME", "TOTAL")

# TODO: merge with common station view/model in acsprism package?
class GroupsTableModel(RefreshMixin, QtCore.QAbstractTableModel):
    # parent is required for models, otherwise you get spurious Qt warnings
    def __init__(self, parent):
        super(GroupsTableModel, self).__init__()

        # get data from sql
        self._datas  = []
        self.HEADERS = HEADERS

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
        # logger.info("Refreshing groups model")

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
        return ( super(GroupsTableModel, self).flags(index) | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def get_data(self):
        query = """
            SELECT  GROUPNAME,
                    STATION_PA, CATEGORY_PA, POINT_PA, RTDBTYPE_PA, ATTRIBUTE_PA, 
                    STATION_PB, POINT_PB,
                    STATION_PC, POINT_PC
            FROM    VIEW_LS_CFG
        """
        result = PRISMdb.ExecQuery(query)
        data   = [  (   group, 
                        self.read_rtdb_value(s1, c1, p1, t1, a1), 
                        self.read_rtdb_value(s2, c1, p2, t1, a1), 
                        self.read_rtdb_value(s3, c1, p3, t1, a1)
                    )
                    for (   group,
                            s1, c1, p1, t1, a1,
                            s2, p2,
                            s3, p3
                        ) in result 
                ]        

        return list(self.accumulate(data))
        # return []

    def read_rtdb_value(self, station, category, point, rtdbtype, attribute):

        if None in (station, category, point, rtdbtype, attribute):
            return 0.0
        rtdbvalue = PRISM.readrtdb(station, category, point, rtdbtype, attribute)
        return round(float(rtdbvalue),2)
    
    def accumulate(self, _list):
        it = itertools.groupby(_list, key=lambda d: (d[0], d[1]))
        for (group), subiter in it:
            yield group, round(sum(item[2]+item[3] for item in subiter),2)