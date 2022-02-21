# coding=utf-8
"""
:Copyright: © 2014 Advanced Control Systems, Inc. All Rights Reserved.
"""

import os
import logging
import datetime
import operator

from model.refresh_mixin import RefreshMixin
from core.QtCompat                   import QtWidgets, QtGui, QtCore, Qt
from core.OracleInterface      import OracleInterface
from acstw.LinuxInterface       import LinuxInterface

DEFAULT_HEADERS  = ['NAME', 
                    'COLORCODE',
                    'STATION_STASTATUS',
                    'CATEGORY_STASTATUS',
                    'POINT_STASTATUS',
                    'RTDBTYPE_STASTATUS',
                    'ATTRIBUTE_STASTATUS',
                    'STATION_LOCKFLAG',
                    'CATEGORY_LOCKFLAG',
                    'POINT_LOCKFLAG',
                    'RTDBTYPE_LOCKFLAG',
                    'ATTRIBUTE_LOCKFLAG',
                    'STATE',
                    'LOCKFLAG'] 

# USER    = os.getenv('ORACLE_USER', 'acs_qa')
# PSWD    = os.getenv('ORACLE_PW'  , 'acs_qa')
# TNS     = os.getenv('ORACLE_DBSTRING', 'emsa')
USER    = os.getenv('ORACLE_USER', 'acs_das')
PSWD    = os.getenv('ORACLE_PW'  , 'acs_das')
TNS     = os.getenv('ORACLE_DBSTRING', 'emsa')
PRISMdb = OracleInterface(USER, PSWD, TNS)
PRISM   = LinuxInterface()

logger = logging.getLogger(__name__)


class UFTableModel(RefreshMixin, QtCore.QAbstractTableModel):
    # For read-only: data, rowCount, columnCount, headerData
    # For write: flags, setData
    # parent is required for models, otherwise you get spurious Qt warnings
    def __init__(self, parent):
        super(UFTableModel, self).__init__(parent)

        self.header_keys   =  DEFAULT_HEADERS
        self.header_values =  DEFAULT_HEADERS
        # self.header_values =  list(map(_,DEFAULT_HEADERS))
        self._datas   = []
        self._options = None
        self._user_changes = {}

        # column index 
        self._col_name      = DEFAULT_HEADERS.index("NAME")
        self._col_station_stastatus   = DEFAULT_HEADERS.index("STATION_STASTATUS")
        self._col_category_stastatus  = DEFAULT_HEADERS.index("CATEGORY_STASTATUS")
        self._col_point_stastatus     = DEFAULT_HEADERS.index("POINT_STASTATUS")
        self._col_rtdbtype_stastatus  = DEFAULT_HEADERS.index("RTDBTYPE_STASTATUS")
        self._col_attribute_stastatus = DEFAULT_HEADERS.index("ATTRIBUTE_STASTATUS")
        self._col_state     = DEFAULT_HEADERS.index("STATE")
        self._col_station_lockflag   = DEFAULT_HEADERS.index("STATION_LOCKFLAG")
        self._col_category_lockflag  = DEFAULT_HEADERS.index("CATEGORY_LOCKFLAG")
        self._col_point_lockflag     = DEFAULT_HEADERS.index("POINT_LOCKFLAG")
        self._col_rtdbtype_lockflag  = DEFAULT_HEADERS.index("RTDBTYPE_LOCKFLAG")
        self._col_attribute_lockfag = DEFAULT_HEADERS.index("ATTRIBUTE_LOCKFLAG")
        self._col_lockflag  = DEFAULT_HEADERS.index("LOCKFLAG")
        self.re_init()

    @property
    def datas(self):
        return self._datas

    def re_init(self):
        with self._pause_refresh():
            self.beginResetModel()      
            self._datas = self.get_data()
            self.endResetModel()

    def get_ufid(self, row):
        return self._datas[row][self._col_ufid]

    def col_from_key(self, column_key):
        """
        Get column index from key.
        """
        try:
            i = self.header_keys.index(column_key)
            return i
        except ValueError:
            return None

    def col_to_key(self, column_index):
        """
        Get column key from index.
        """
        try:
            return self.header_keys[column_index]
        except IndexError:
            return None

    def default_visible_columns(self):
        """
        Returns the column keys of the columns that should be visible by default
        """
        columns = set(self.header_keys)
        return columns

    def _on_refresh(self):
        self._datas = self.get_data()
        self.invalidate()
        # logger.info("Refreshing uf table")

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
    
    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._datas)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(DEFAULT_HEADERS) - 6 # (5+1)
    
    def get_u_rtdb_value(self, row):
        station   = self._datas[row][self._col_station_stastatus   ]
        category  = self._datas[row][self._col_category_stastatus  ]
        point     = self._datas[row][self._col_point_stastatus     ]
        rtdbtype  = self._datas[row][self._col_rtdbtype_stastatus  ]
        attribute = self._datas[row][self._col_attribute_stastatus]
        if None in (station, category, point, rtdbtype, attribute):
            return 'X'
        rtdbvalue = PRISM.readrtdb(station, category, point, rtdbtype, attribute)
        return float(rtdbvalue)
    
    def get_ulf_rtdb_value(self, row):
        station   = self._datas[row][self._col_station_lockflag   ]
        category  = self._datas[row][self._col_category_lockflag  ]
        point     = self._datas[row][self._col_point_lockflag     ]
        rtdbtype  = self._datas[row][self._col_rtdbtype_lockflag  ]
        attribute = self._datas[row][self._col_attribute_lockfag] #_col_attribute2
        if None in (station, category, point, rtdbtype, attribute):
            return 'X'
        rtdbvalue = PRISM.readrtdb(station, category, point, rtdbtype, attribute)
        return float(rtdbvalue)

    def get_u_rtdb_address(self, row):
        station   = self._datas[row][self._col_station_stastatus   ]
        category  = self._datas[row][self._col_category_stastatus  ]
        point     = self._datas[row][self._col_point_stastatus     ]
        rtdbtype  = self._datas[row][self._col_rtdbtype_stastatus  ]
        attribute = self._datas[row][self._col_attribute_stastatus]
        return [station, category, point, rtdbtype, attribute]   
    
    def get_lf_rtdb_address(self, row):
        station   = self._datas[row][self._col_station_lockflag   ]
        category  = self._datas[row][self._col_category_lockflag  ]
        point     = self._datas[row][self._col_point_lockflag     ]
        rtdbtype  = self._datas[row][self._col_rtdbtype_lockflag  ]
        attribute = self._datas[row][self._col_attribute_lockflag] #_col_attribute2
        return [station, category, point, rtdbtype, attribute]   

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        :param index: the model index of the item
        :param role: what kind of information is required. 'Qt.DisplayRole' means that
            the data as displayed is wanted.
        """
        col   = index.column()
        row   = index.row()
        # name  = self._datas[row][self._col_equip]
        value   = self._datas[row][col]
        u_val   = self.get_u_rtdb_value(row)
        ulf_val = self.get_ulf_rtdb_value(row)

        if role == QtCore.Qt.DisplayRole:
            if col == self._col_state:    return u_val
            if col == self._col_lockflag: return ulf_val
            return str(value)

        elif role == Qt.DecorationRole:
            # color = QtGui.QColor()
            # return QtCore.QVariant(color)
            pass

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter | Qt.AlignVCenter

        elif role == QtCore.Qt.ToolTipRole:
            if col == self._col_state :    return "(%s)" % ",".join(map(str,self.get_u_rtdb_address(row)))
            if col == self._col_lockflag : return "(%s)" % ",".join(map(str,self.get_lf_rtdb_address(row)))

        elif role == QtCore.Qt.ForegroundRole:
            color = QtGui.QColor()

            if col == self._col_state:
                if u_val == 0: color = QtGui.QColor('Red')
                if u_val == 1: color = QtGui.QColor('Black')

            if col == self._col_lockflag:
                if ulf_val== 0: color = QtGui.QColor('Black')
                if ulf_val== 1: color = QtGui.QColor('Green')
            return color

        elif role == QtCore.Qt.BackgroundRole:
            # color = QtGui.QColor(240,230,140)
            # return QtCore.QVariant(color)
            pass
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                try:
                    return self.header_values[section]
                except IndexError:
                    pass
            return int(section + 1)
    
    def sort(self, col, order):
        if self._datas and self._datas[0]:
            self.layoutAboutToBeChanged.emit()
            if isinstance(self._datas[0][col], str):
                sortkey = lambda row: row[col].lower()
            else:
                sortkey = operator.itemgetter(col)

            self._datas = sorted(
                self._datas, key=sortkey,
                reverse=(order != Qt.DescendingOrder))
            self.layoutChanged.emit()

    def flags(self, index):
        return ( super(UFTableModel, self).flags(index) | 
                # QtCore.Qt.ItemIsEditable | 
                QtCore.Qt.ItemIsEnabled  | 
                QtCore.Qt.ItemIsSelectable)
    
    def setData(self, index, value, role=Qt.EditRole):
        row  = index.row()
        col  = index.column()
        name = self._datas[row][self._col_name]

        # if role == QtCore.Qt.EditRole:
        #     if self._datas[row][col] != value: # valueChanged
        #         self.user_changes.setdefault(name, {})
        #         self.user_changes.get(name).update({str(col):value, "data":self._datas[row]})
        #         self.dataChanged.emit(index, index)
        #     elif self.user_changes.__contains__(name) and self._datas[row][col] == value:
        #         self.user_changes.get(name).pop(str(col), None)
        #         self.user_changes.get(name).pop('data',   None)
        #         self.dataChanged.emit(index, index)
        #         if len(self.user_changes.get(name))==0: 
        #             self.user_changes.pop(name, None)
        #             self.dataChanged.emit(index, index)
        #     elif self.user_changes.__contains__(name) and self.user_changes.get(name).get(str(col)) != value:
        #         self.user_changes.get(name).update({str(col):value, "data":self._datas[row]})
        #         self.dataChanged.emit(index, index)

    def get_data(self):
        query = f"""
            SELECT  NAME, 
                    COLORCODE,
                    STATION_STASTATUS,
                    CATEGORY_STASTATUS,
                    POINT_STASTATUS,
                    RTDBTYPE_STASTATUS,
                    ATTRIBUTE_STASTATUS,
                    STATION_LOCKFLAG,
                    CATEGORY_LOCKFLAG,
                    POINT_LOCKFLAG,
                    RTDBTYPE_LOCKFLAG,
                    ATTRIBUTE_LOCKFLAG
            FROM    VIEW_UF_CFG
            WHERE STATION_STASTATUS IS NOT NULL
            ORDER BY NAME
        """
        data = list(map(list, PRISMdb.ExecQuery(query)))
        return data
        # return []
    
    def set_dasdb_lockflag(self, indexes, state):
        index = ",".join(map(str,indexes))
        query = f"update ufparam set lockflag='{state}' where ufid in ({index})"
        PRISMdb.ExecNonQuery(query)
        self.re_init()

    def set_rtdb_lockflag(self, address, state):
        for addr in address :
            st, ca, pt, tp, at = addr
            PRISM.writertdb(st, ca, pt, tp, at, state)
            massage = "( %s ) -> %s" % (", ".join(map(str,[st, ca, pt, tp, at])), state)
            logger.info(massage)