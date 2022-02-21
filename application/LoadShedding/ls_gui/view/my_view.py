# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""

__author__ = 'Darren Liang'

import logging
import os, datetime
from model.my_model import DEFAULT_HEADERS
from collections           import OrderedDict
from core.QtCompat import QtWidgets, QtGui, QtCore, Qt, Signal, Slot

logger = logging.getLogger(__name__)

class MyTableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super(MyTableView, self).__init__(parent)
        self.setAlternatingRowColors(True)
        self.verticalHeader().hide()
        self.setSortingEnabled(True)
        self.horizontalHeader().setSectionsMovable(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setStyleSheet('QHeaderView::section{ background:LightSteelBlue;}')

        self._user_changes  = OrderedDict()

        self._column_widths = {}
        self._column_settings_map = ColumnSettingsMap()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        self.set_font_size()
        
    def _column_settings(self):
        model = self.model()
        return self._column_settings_map.get()

    def set_font_size(self, size=None):
        size = size if size is not None else 12
        font = QtGui.QFont()
        font.setPointSize(size)
        # font.setBold(True)
        self.setFont(font)
    
    def setModel(self, model):
        """
        :type model: FeederTableModel
        """
        # model.layoutAboutToBeChanged.connect(self._save_columns)
        # model.layoutChanged.connect(self._restore_columns)

        model.modelAboutToBeReset.connect(self._save_columns)

        # Making this into a queued connection fixes the problem with restoring
        # header widths (presumably having something to do with the header view
        # not yet being updated), but creates a bad visual effect.
        # model.modelReset.connect(self._restore_columns)
        # model.modelReset.connect(
        #     self._restore_columns, Qt.QueuedConnection)
        model.modelReset.connect(self._on_model_reset)

        super(MyTableView, self).setModel(model)


    def model(self):
        """
        Use instead of model() for documentation of the expected type.
        If using a proxy model, return the source model.
        """
        model = super(MyTableView, self).model()
        # if isinstance(model, QtCore.QSortFilterProxyModel):
        #     return model.sourceModel()
        return model
    
    def _on_model_reset(self):
        """Called *after* the model has been reset"""
        self._restore_columns()

        tip = "RowCount" +': {:,}'.format(len(self.model().datas))
        self.setStatusTip(tip)
    
    @QtCore.pyqtSlot(QtCore.QPoint) 
    def _show_context_menu(self, position):
        # get cells which user selected 
        selected = self.selectedIndexes()
        # get column id from cell
        indexes  = list(set([idx.column() for idx in selected]))
        # QMenu settings
        menu = QtWidgets.QMenu() 
        action1 = menu.addAction("Action1") 
        action2 = menu.addAction("Action2")
        actions = menu.exec_(self.mapToGlobal(position)) 


    def restore_settings(self, settings):
        """
        :type settings: QtCore.QSettings
        """
        # TODO: unit test: make sure settings are restored before needed?
        # Or maybe just call _restore_columns at the end of this method?
        for column_key in DEFAULT_HEADERS:
            key = 'Col_%s' % column_key
            if settings.contains(key):
                width = int(settings.value(key))
                if width > 0:
                    self._column_widths[column_key] = width

        self._column_settings_map.restore_settings(settings)

        self._restore_columns()
        self._restroe_columns_orders()
    
    def _save_columns(self):
        model = self.model()

        column_settings = self._column_settings()
        column_settings.columns_visible.clear()
        columns = []
        

        for col in range(model.columnCount()):
            
            # If columns are movable, need to make sure to map to visual index
            # when getting column width.
            # Or not?
            # Do the column numbers for column width use the 'logical' or
            # 'visual' column number?
            # TODO: These are tricky to get right; add unit tests
            visual_col = self.horizontalHeader().visualIndex(col)
            # logger.debug(
            #     "logical %d -> visual %d; width=%d",
            #     col, visual_col, self.columnWidth(visual_col))
            # I think these will use the logical column number
            column_key = model.col_to_key(col)
            width = self.columnWidth(col)

            if width > 0:
                if column_key is not None:
                    logger.debug( "Saving width for %r (logical %d, visual %d): %d", column_key, col, visual_col, width)
                    self._column_widths[column_key] = width
            if not self.isColumnHidden(col):
                column_settings.columns_visible.append(column_key)

            columns.append((visual_col, model.col_to_key(col)))
        column_settings.columns_lastloc = [data[1] for data in sorted(columns, key=lambda tup: tup[0])]
        logger.debug(
            "Saved visible columns: %s", column_settings.columns_visible)

        self.horizontalHeader().saveState()
    
    def _restore_columns(self):
        m = self.model()
        # Resetting the header seems to fix the problem of losing the width
        # of certain columns. The visual effect is not  as bad as making it
        # a queued connection (presumably the same as using a zero timer,
        # in this case), but it is still there, so we might want to look
        # for an alternative (e.g. using multiple table views?).1
        # self.horizontalHeader().reset()
    
        for column_key in self._column_widths:
            col = m.col_from_key(column_key)
            if col is not None:
                visual_col = self.horizontalHeader().visualIndex(col)
                width = self._column_widths[column_key]
                header_name = m.headerData(col, Qt.Horizontal)
                if width > 0:
                    logger.debug("Restoring width for %s [%s] ""(logical %d, visual %d): %d", header_name, column_key, col, visual_col, width)
                    self.setColumnWidth(col, width)
        
        # Restore which columns are visible.
        # If visible columns haven't been set up yet, use the defaults.
        columns_visible = self._column_settings().columns_visible
        if not columns_visible:
            columns_visible = m.default_visible_columns()
        for col in range(m.columnCount()):
            column_key = m.col_to_key(col)
            hidden = column_key not in columns_visible
            self.setColumnHidden(col, hidden)

        self._reset_header_menu()
    
    def _restroe_columns_orders(self):
        m = self.model()
        s = self._column_settings()

        cond1 = m.header_keys is not None
        cond2 = s.columns_lastloc is not None
        if  cond1 and cond2 :
            headers = [ col for col in m.header_keys if col in s.columns_lastloc]
            if len(headers)>0:
                for nw_col in s.columns_lastloc:
                    nw_idx = s.columns_lastloc.index(nw_col)
                    if nw_col not in headers:
                        return
                    b4_idx = headers.index(nw_col)
                    if nw_idx != b4_idx:
                        headers[nw_idx], headers[b4_idx] = headers[b4_idx], headers[nw_idx]
                        self.horizontalHeader().swapSections(nw_idx,b4_idx)  

    def _reset_header_menu(self):
        header = self.horizontalHeader()

        # Add actions (context menu) to hide/show columns
        # First clear any existing actions
        for action in header.actions():
            header.removeAction(action)
        for column_index in range(header.count()):
            text = self.model().headerData(column_index, Qt.Horizontal, Qt.DisplayRole)
            action = QtWidgets.QAction(str(text), header)
            action.setCheckable(True)

            def toggle(checked, i=column_index):
                hidden = not checked
                # logger.debug("Setting column %d hidden: %s", i, hidden)
                self.setColumnHidden(i, hidden)
                if not hidden:
                    if self.columnWidth(i) == 0:
                        # Seems to happen after switching point type...
                        self.resizeColumnToContents(i)
                        logger.debug("Column %d resized; width=%d", i, self.columnWidth(i))
            action.setChecked(not self.isColumnHidden(column_index))
            action.toggled.connect(toggle)
            header.addAction(action)
        header.setContextMenuPolicy(Qt.ActionsContextMenu)

    def save_settings(self, settings):
        """
        Save settings for this point view.

        The number of attributes may change / be customized, so we need to
        save widths by column.
        We keep track of all attribute widths that we've ever seen, because
        they're probably not all currently visible.

        An alternative might be to always have all the columns, and hide the
        rest, if we could avoid updating hidden columns, and if that didn't
        add too much overhead.

        :type settings: QtCore.QSettings
        """
        self._save_columns()

        # print(settings)

        # Save "fixed" columns - those that are not RTDB attributes
        # TODO: should we save and restore header settings?
        # This could possibly be replaced by the header settings (which
        # would also store the position of any reordered columns). Not
        # sure if that should be global or per type/category.
        # print()
        for column_key, width in self._column_widths.items():
            key = 'Col_%s' % column_key
            settings.setValue(key, width)
        logger.debug("Column widths: %s", {
            k: w for k, w in self._column_widths.items()})
        self._column_settings_map.save_settings(settings)

class ColumnSettings(object):
    def __init__(self):
        self.columns_visible = []
        self.columns_lastloc = []

class ColumnSettingsMap(object):
    """
    Map of column settings for the different point type/category combinations
    we want to save.
    """
    def __init__(self):
        self._settings = {}
        self._category = 'tv_feeder'
        self._settings[self._category] = ColumnSettings()

    def get(self):
        """
        :rtype: ColumnSettings
        """
        return self._settings[self._category]

    @staticmethod
    def _key(colname):
        key = 'Columns_%s' % colname
        return key

    def save_settings(self, settings):
        """
        :type settings: QtCore.QSettings
        """
        # pass
        for colname in self._settings:
            key = self._key(colname)
            value = ' '.join(self.get().columns_visible)
            if value:
                settings.setValue(key, value)

            value2 = self.get().columns_lastloc           
            if value2:
                settings.setValue('headers', value2)


    def restore_settings(self, settings):
        """
        :type settings: QtCore.QSettings
        """
        for colname in self._settings:
            key = self._key(colname)
            column_settings = self.get()
            columns_visible = None
            value = settings.value(key)
            if value:
                columns_visible = value.strip().split()
            if columns_visible:
                column_settings.columns_visible = columns_visible

            columns_lastloc = settings.value('headers')
            if value:
                column_settings.columns_lastloc = columns_lastloc