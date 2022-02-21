# coding=utf-8
"""
:Copyright: © 2014 Advanced Control Systems, Inc. All Rights Reserved.
"""

from core.QtCompat import QtGui

__author__ = 'Darrne Liang'


def set_spinbox_attributes(spinbox, value=None, maximum=None, minimum=None, limit=None, step=None, tip=None):
    if value is not None:
        spinbox.setValue(value)

    if maximum is not None:
        spinbox.setMaximum(maximum)

    if minimum is not None:
        spinbox.setMinimum(minimum)

    if limit is not None:
        spinbox.setRange(limit[0], limit[1])
    
    if step is not None:
        spinbox.singleStep(step)

    if tip:
        spinbox.setToolTip(tip)
        spinbox.setStatusTip(tip)