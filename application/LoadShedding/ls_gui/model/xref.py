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
from core.LinuxInterface       import LinuxInterface

DEFAULT_HEADERS  = ['GROUPNAME','SUBSTATION', 'FEEDER'] 
# DEFAULT_HEADERS += ['LSPRIORITY', 'STATE', 'LSFDIDX','P'] 
DEFAULT_HEADERS += ['LSPRIORITY', 'STATE', 'LSFDIDX'] 
DEFAULT_HEADERS += ['LSACT', 'UPLINECOLORCODE', 'PA', 'PB', 'PC', 'STASTATUS', 'LSLOCKFLAG']
DEFAULT_HEADERS += ['LSACT_ADDR', 'UPLINECOLORCODE_ADDR', 'PA_ADDR', 'PB_ADDR', 'PC_ADDR', 'STASTATUS_ADDR', 'LSLOCKFLAG_ADDR']


USER    = os.getenv('ORACLE_USER', 'acs_das')
PSWD    = os.getenv('ORACLE_PW'  , 'acs_das')
TNS     = os.getenv('ORACLE_DBSTRING', 'emsa')
PRISMdb = OracleInterface(USER, PSWD, TNS)
PRISM   = LinuxInterface()

logger = logging.getLogger(__name__)


class XREFTableModel(RefreshMixin, QtCore.QAbstractTableModel):
    # For read-only: data, rowCount, columnCount, headerData
    # For write: flags, setData
    # parent is required for models, otherwise you get spurious Qt warnings
    def __init__(self, parent):
        super(XREFTableModel, self).__init__(parent)

        self.header_keys   =  DEFAULT_HEADERS
        self.header_values =  DEFAULT_HEADERS
        # self.header_values =  list(map(_,DEFAULT_HEADERS))
        self._datas   = []
        self._options = None
        self._user_changes = {}

        # column index 
        self._col_feeder       = DEFAULT_HEADERS.index("FEEDER")
        self._col_f_state      = DEFAULT_HEADERS.index("STATE")
        # self._col_p_value      = DEFAULT_HEADERS.index("P")
        self._col_pa_value     = DEFAULT_HEADERS.index("PA")
        self._col_pb_value     = DEFAULT_HEADERS.index("PB")
        self._col_pc_value     = DEFAULT_HEADERS.index("PC")
        self._col_st_value     = DEFAULT_HEADERS.index("STASTATUS")
        # self._col_falg_value   = DEFAULT_HEADERS.index("FLAG")
        self._col_lslockflag   = DEFAULT_HEADERS.index("LSLOCKFLAG")
        self._col_pa_address   = DEFAULT_HEADERS.index("PA_ADDR")
        self._col_pb_address   = DEFAULT_HEADERS.index("PB_ADDR")
        self._col_pc_address   = DEFAULT_HEADERS.index("PC_ADDR")
        self._col_st_address   = DEFAULT_HEADERS.index("STASTATUS_ADDR")
        self._col_flag_address = DEFAULT_HEADERS.index("LSLOCKFLAG_ADDR")


    @property
    def datas(self):
        return self._datas

    def get_feeder(self, row):
        return self._datas[row][self._col_feeder]
        # return self._datas[row][self._col_feeder]

    def get_lockflag_addr(self, row):
        return self._datas[row][self._col_flag_address]

    def re_init(self, options):
        self._options = options
        with self._pause_refresh():
            self.beginResetModel()      
            self._datas = self.get_data()
            self.endResetModel()

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
        # logger.info("Refreshing settings table")

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
            self.index(self.rowCount() - 1, self.columnCount() - 1)
            )
    
    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._datas)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(DEFAULT_HEADERS) #- 9

    def get_rtdb_point_address(self, s, c, p, t, a):
        return [s, c, p, t, a]

    def get_rtdb_point_value(self, s, c, p, t, a):
        # print(str(s)+","+str(c)+","+str(p)+","+str(t)+","+str(a))
        # return 0.0
        if None in (s, c, p, t, a):
            return 0.0 if str(t).upper()=='T' else 'X'
        rtdbvalue = PRISM.readrtdb(s, c, p, t, a)
        return round(float(rtdbvalue),2)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        :param index: the model index of the item
        :param role: what kind of information is required. 'Qt.DisplayRole' means that
            the data as displayed is wanted.
        """
        col     = index.column()
        row     = index.row()
        value   = self._datas[row][col]
        pa_val  = self._datas[row][self._col_pa_value]
        pb_val  = self._datas[row][self._col_pb_value]
        pc_val  = self._datas[row][self._col_pc_value]
        p_total = pa_val + pb_val + pc_val

        state   = self._datas[row][self._col_st_value]
        flag    = self._datas[row][self._col_lslockflag]
        pa_addr = self._datas[row][self._col_pa_address]
        pb_addr = self._datas[row][self._col_pb_address]
        pc_addr = self._datas[row][self._col_pc_address]
        st_addr = self._datas[row][self._col_st_address]
        fg_addr = self._datas[row][self._col_flag_address]


        if role == QtCore.Qt.DisplayRole:
            # if col == self._col_p_value: 
            #     self.datas[row][col] = p_total   
            #     return p_total

            if col == self._col_f_state:   
                self.datas[row][col] = state 
                return state

            if col == self._col_lslockflag: 
                self.datas[row][col] = flag
                return flag
            return str(value)

        elif role == Qt.DecorationRole:
            # color = QtGui.QColor()
            # return QtCore.QVariant(color)
            pass

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter | Qt.AlignVCenter
 
        elif role == QtCore.Qt.ToolTipRole:
            if col == self._col_f_state:    return "[%s]: %s" % (state, str(st_addr))
            if col == self._col_lslockflag: return "[%s]: %s" % (flag , str(fg_addr))
            # if col == self._col_p_value:   
            #     pa_tip = "PA [%s]: %s" % (pa_val, str(pa_addr))
            #     pb_tip = "PB [%s]: %s" % (pb_val, str(pb_addr))
            #     pc_tip = "PC [%s]: %s" % (pc_val, str(pc_addr))
            #     return f"{pa_tip}\n\n{pb_tip}\n\n{pc_tip}"

        elif role == QtCore.Qt.ForegroundRole:
            color = QtGui.QColor()

            if col == self._col_f_state:
                if state == 0: color = QtGui.QColor('Red')
                if state == 1: color = QtGui.QColor('Black')

            if col == self._col_lslockflag:
                if flag == 0: color = QtGui.QColor('Black')
                if flag == 1: color = QtGui.QColor('Green')
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
                    # return self.col_to_attr(section).name
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
        return ( super(XREFTableModel, self).flags(index) | 
                # QtCore.Qt.ItemIsEditable | 
                QtCore.Qt.ItemIsEnabled  | 
                QtCore.Qt.ItemIsSelectable)
    
    def setData(self, index, value, role=Qt.EditRole):
        row  = index.row()
        col  = index.column()
        name = self._datas[row][self._col_feeder]

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

        groups  = "" #if self._options['groups'] == 'ALL' else f" AND GROUPNAME = '{self._options['groups']}'"
        feeder  = "" #if self._options['feeder'] == None  else " AND REGEXP_LIKE (UPPER(FEEDER),  '(%s).*')"      %  '|'.join("%s" % f.upper() for f in self._options['feeder'].split(',') if f != '')
        subst   = "" #if self._options['subst']  == None  else " AND REGEXP_LIKE (UPPER(SUBSTATION),  '(%s).*')"  %  '|'.join("%s" % s.upper() for s in self._options['subst' ].split(',') if s != '')

        query = f"""
            SELECT  GROUPNAME
                    , SUBSTATION
                    , FEEDER
                    , LSFEEDER_PRIORITY
                    , 0 STATE
                    , LSFDIDX

                    , STATION_LSACT
                    , CATEGORY_LSACT
                    , POINT_LSACT
                    , RTDBTYPE_LSACT
                    , ATTRIBUTE_LSACT

                    , STATION_UPLINECOLORCODE
                    , CATEGORY_UPLINECOLORCODE
                    , POINT_UPLINECOLORCODE
                    , RTDBTYPE_UPLINECOLORCODE
                    , ATTRIBUTE_UPLINECOLORCODE

                    , STATION_STASTATUS
                    , CATEGORY_STASTATUS
                    , POINT_STASTATUS
                    , RTDBTYPE_STASTATUS
                    , ATTRIBUTE_STASTATUS

                    , STATION_LSLOCKFLAG
                    , CATEGORY_LSLOCKFLAG
                    , POINT_LSLOCKFLAG
                    , RTDBTYPE_LSLOCKFLAG
                    , ATTRIBUTE_LSLOCKFLAG

                    , STATION_PA
                    , CATEGORY_PA
                    , POINT_PA
                    , RTDBTYPE_PA
                    , ATTRIBUTE_PA

                    , STATION_PB
                    , CATEGORY_PB
                    , POINT_PB
                    , RTDBTYPE_PB
                    , ATTRIBUTE_PB

                    , STATION_PC
                    , CATEGORY_PC
                    , POINT_PC
                    , RTDBTYPE_PC
                    , ATTRIBUTE_PC
            FROM    VIEW_LS_CFG 
            WHERE   FEEDER IS NOT NULL {groups} {feeder} {subst}
            ORDER BY GROUPNAME, LSFEEDER_PRIORITY
        """
        # print(query)
        result = list(map(list, PRISMdb.ExecQuery(query)))
        data   = [  [   group, sub, fdr, pty, state, lsfdisx, 
                        self.get_rtdb_point_value(s1, c1, p1, t1, a1),   # lsaact value
                        self.get_rtdb_point_value(s2, c2, p2, t2, a2),   # uplinecolorcode value
                        self.get_rtdb_point_value(s5, c5, p5, t5, a5),   # pa value
                        self.get_rtdb_point_value(s6, c6, p6, t6, a6),   # pb value
                        self.get_rtdb_point_value(s7, c7, p7, t7, a7),   # pc value 
                        self.get_rtdb_point_value(s3, c3, p3, t3, a3),   # state value
                        self.get_rtdb_point_value(s4, c4, p4, t4, a4),   # flag value

                        self.get_rtdb_point_address(s1, c1, p1, t1, a1), # lsaact address
                        self.get_rtdb_point_address(s2, c2, p2, t2, a2), # uplinecolorcode address
                        self.get_rtdb_point_address(s5, c5, p5, t5, a5), # pa address
                        self.get_rtdb_point_address(s6, c6, p6, t6, a6), # pb address
                        self.get_rtdb_point_address(s7, c7, p7, t7, a7), # pc address
                        self.get_rtdb_point_address(s3, c3, p3, t3, a3), # state address
                        self.get_rtdb_point_address(s4, c4, p4, t4, a4)  # flag address
                    ]
                    for (   group, sub, fdr, pty, state, lsfdisx,
                            s1, c1, p1, t1, a1, #act
                            s2, c2, p2, t2, a2, #uplinecolorcode
                            s3, c3, p3, t3, a3, #stastatus
                            s4, c4, p4, t4, a4, #lslockflag
                            s5, c5, p5, t5, a5, #pa
                            s6, c6, p6, t6, a6, #pb
                            s7, c7, p7, t7, a7  #pc
                        ) in result 
                ]
        # print(data)
        return data
        # return []

    def set_dasdb_lockflag(self, feeders, state):
        _fdrs = ",".join(["'%s'" % f for f in feeders])
        query = f"update feederinput2 set lslockflag='{state}' where idx in (select idx from feederparam2 where name in ({_fdrs}))"
        PRISMdb.ExecNonQuery(query)
        self._on_refresh()

    def set_rtdb_lockflag(self, address, state):
        for addr in address :
            s, c , p, t, a = addr
            PRISM.writertdb(s, c , p, t, a, state)
            massage = "( %s ) -> %s" % (str(addr), state)
            logger.info(massage)
