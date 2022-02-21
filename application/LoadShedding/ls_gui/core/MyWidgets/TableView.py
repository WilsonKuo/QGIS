# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
__author__ = 'Darren Liang'
__date__   = '2021-11-24'


import os
import logging
import datetime
from  core.MyWidgets.TableModel  import HEADERS
from  core.QtCompat              import QtWidgets, QtGui, QtCore, Qt

logger = logging.getLogger(__name__)


class DeviceTableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super(DeviceTableView, self).__init__(parent)
        self.setMinimumSize(QtCore.QSize(0, 200))
        self.verticalHeader().hide()
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.horizontalHeader().setStyleSheet( 'QHeaderView::section{ background:LightSteelBlue;}')

        self.setFont(QtGui.QFont("Arial", 12, 50))
        self.horizontalHeader().setFont(QtGui.QFont("Arial", 11, 70))

    def setModel(self, model):
        """
        :type model: DeviceTableModel
        """
        # model.layoutAboutToBeChanged.connect(self._save_columns)
        # model.layoutChanged.connect(self._restore_columns)

        # model.modelAboutToBeReset.connect(self._save_columns)

        # Making this into a queued connection fixes the problem with restoring
        # header widths (presumably having something to do with the header view
        # not yet being updated), but creates a bad visual effect.
        # model.modelReset.connect(self._restore_columns)
        # model.modelReset.connect(
        #     self._restore_columns, Qt.QueuedConnection)
        # model.modelReset.connect(self._on_model_reset)
        super(DeviceTableView, self).setModel(model)


    def dasapp_model(self):
        """
        Use instead of model() for documentation of the expected type.
        If using a proxy model, return the source model.

        :rtype: DasAppTableModel
        """
        model = super(DeviceTableView, self).model()
        # if isinstance(model, QtCore.QSortFilterProxyModel):
        #     return model.sourceModel()
        return model
