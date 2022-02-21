# coding=utf-8
"""
:Copyright: © 2014 Advanced Control Systems, Inc. All Rights Reserved.
"""

from core.QtCompat.QtGui import QIcon
from core.QtCompat.QtWidgets import QAction
from pkg_resources import resource_filename

__author__ = 'Sam Hartsfield'


def create_action(
        self, text, slot=None, shortcut=None, icon=None,
        tip=None, checkable=False, signal='triggered'):

        action = QAction(text, self)

        if icon is not None:
            icon = resource_filename('acsQt.icon', icon)
            action.setIcon(QIcon(icon))

        if shortcut is not None:
            action.setShortcut(shortcut)

        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)

        if slot is not None:
            signal = getattr(action, signal)
            signal.connect(slot)

        if checkable:
            action.setCheckable(True)

        return action


def set_action_attributes(action, text=None, slot=None, shortcut=None, icon=None,
        tip=None, checkable=False, signal='triggered'):

    if text is not None:
        action.setTitle(text)

    if icon is not None:
        icon = resource_filename('acsQt.icon', icon)
        action.setIcon(QIcon(icon))

    if shortcut is not None:
        action.setShortcut(shortcut)

    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)

    if slot is not None:
        signal = getattr(action, signal)
        signal.connect(slot)

    if checkable:
        action.setCheckable(True)