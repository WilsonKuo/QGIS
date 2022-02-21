# coding=utf-8
"""
:Copyright: © 2014 Advanced Control Systems, Inc. All Rights Reserved.
"""

from core.QtCompat import QtGui
from pkg_resources import resource_filename

__author__ = 'Darren'

def set_label_attributes(label, text=None, icon=None, tip=None):
    if text is not None:
        label.setText(text)
    if icon is not None:
        files = resource_filename('acsQt.icon', icon)
        image = QtGui.QPixmap.fromImage(QtGui.QImage(files))
        minWidth  = label.minimumWidth()
        minHeight = label.minimumHeight()
        label.setPixmap(image.scaled(minWidth, minHeight))
    if tip:
        label.setToolTip(tip)
        label.setStatusTip(tip)

