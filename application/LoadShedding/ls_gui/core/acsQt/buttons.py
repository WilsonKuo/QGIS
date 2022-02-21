# coding=utf-8
"""
:Copyright: © 2014 Advanced Control Systems, Inc. All Rights Reserved.
"""

from core.QtCompat import QtGui
from pkg_resources import resource_filename
__author__ = 'Sam Hartsfield'


def set_button_attributes(button, text=None, icon=None, tip=None, slot=None):
    if text is not None:
        button.setText(text)
    if icon is not None:
        icon = resource_filename('acsQt.icon', icon)
        button.setIcon(QtGui.QIcon(icon))
    if tip:
        button.setToolTip(tip)
        button.setStatusTip(tip)
    if slot is not None:
        button.clicked.connect(slot)


def create_pushbutton(text, icon=None, tip=None):
    button = QtGui.QPushButton()
    _set_button_attributes(button, text, icon, tip)
    return button


def create_tool_button(text=None, icon=None, tip=None):
    button = QtGui.QToolButton()
    _set_button_attributes(button, text, icon, tip)
    return button
