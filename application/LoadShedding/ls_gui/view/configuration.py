# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
import os
import logging
import datetime
from core.QtCompat    import QtWidgets, QtGui, QtCore, Qt

__author__ = 'Darren Liang'

logger = logging.getLogger(__name__)


class ConfigurationTableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super(ConfigurationTableView, self).__init__(parent)
        # self.setMinimumSize(QtCore.QSize(0, 200))
        self.verticalHeader().hide()
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.horizontalHeader().setStyleSheet('QHeaderView::section{ background:LightSteelBlue;}')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.horizontalHeader().setFont(font)

    def setModel(self, model):
        """
        :type model: ConfigurationTableView
        """

        # Making this into a queued connection fixes the problem with restoring
        # header widths (presumably having something to do with the header view
        # not yet being updated), but creates a bad visual effect.

        super(ConfigurationTableView, self).setModel(model)

    def _on_model_reset(self):
        tip = "RowCount" +': {:,}'.format(len(self.model().datas))
        self.setStatusTip(tip)

    def model(self):
        """
        Use instead of model() for documentation of the expected type.
        If using a proxy model, return the source model.

        :rtype: ConfigurationTableView
        """
        model = super(ConfigurationTableView, self).model()
        # if isinstance(model, QtCore.QSortFilterProxyModel):
        #     return model.sourceModel()
        return model

