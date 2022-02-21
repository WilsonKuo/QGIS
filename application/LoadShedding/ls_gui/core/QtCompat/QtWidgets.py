# coding=utf-8
"""
:Copyright: (c) 2016 Advanced Control Systems, Inc. All Rights Reserved.
"""
import os

__author__ = 'Sam Hartsfield'

if os.environ['QT_API'] == 'pyqt5':
    from PyQt5.QtWidgets import *

    # Override to improve compatibility.
    # PySide's versions always return the filter.
    if os.environ['QT_API'] == ('pyqt'):
        QFileDialog.getOpenFileName = \
            QFileDialog.getOpenFileNameAndFilter
        QFileDialog.getOpenFileNames = \
            QFileDialog.getOpenFileNamesAndFilter
        QFileDialog.getSaveFileName = \
            QFileDialog.getSaveFileNameAndFilter

elif os.environ['QT_API'] == 'pyside2':
    from PySide2.QtWidgets import *

elif os.environ['QT_API'] in ('pyqt', 'pyside'):
    # For now just make this an alias for QtGui
    from  core.QtCompat.QtGui import *
