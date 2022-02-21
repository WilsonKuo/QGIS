# coding=utf-8
"""
:Copyright: © 2017 Advanced Control Systems, Inc. All Rights Reserved.
"""
import logging
import os
from  core.QtCompat import QtWidgets, QtGui, QtCore
from  core.QtCompat.QtWidgets import QAction
from pkg_resources import resource_string
import sys

__author__ = 'Sam Hartsfield'

logger = logging.getLogger(__name__)


def Base64ToBytes(filename):
    image = QtGui.QImage(filename)
    ba64  = QtCore.QByteArray()
    buff  = QtCore.QBuffer(ba64)
    image.save(buff, "PNG")
    return ba64.toBase64().data()

def iconFromBase64(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon

def create_q_application(title, icon=None, gui=True):
    if gui:
        # Make sure we don't create a QApplication if one already exists.
        # startingUp() returns true if an application object has not been
        # created yet.
        if QtWidgets.QApplication.startingUp():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        if icon is None:
            # Use default icon
            # filename = "acs_icon.png"
            # png_bytes = QtCore.QByteArray(resource_string('assets', filename))
            # buf = QtCore.QBuffer(png_bytes)
            # q_icon = read_icon(buf)
            q_icon = read_icon(None)
            print()
        else:
            q_icon = read_icon(icon)
        app.setWindowIcon(q_icon)
    else:
        if QtCore.QCoreApplication.startingUp():
            app = QtCore.QCoreApplication(sys.argv)
        else:
            app = QtCore.QCoreApplication.instance()
    app.setOrganizationName("ACS")
    app.setOrganizationDomain("acspower.com")
    app.setApplicationName(title)
    return app


def read_icon(icon):
    """
    Normally QIcon doesn't read all the possible sizes from an "ico" file.
    This function will.

    Suggestion came from https://qt-project.org/forums/viewthread/14470
    """
    # Pass through
    if isinstance(icon, QtGui.QIcon):
        return icon
    elif isinstance(icon, QtGui.QPixmap):
        return QtGui.QIcon(icon)
    reader = QtGui.QImageReader(icon)
    q_icon = QtGui.QIcon()
    if reader.canRead():
        while True:
            # The documentation seems to suggest that "read" will jump to
            # the next image, but when tested, it did not.
            image = reader.read()
            if not image:
                logger.error(
                    "Error reading icon file '%s': %s",
                    icon, reader.errorString())
                break
            q_icon.addPixmap(QtGui.QPixmap.fromImage(image))
            if not reader.jumpToNextImage():
                break
    else:
        logger.error(
            "Cannot read icon from file '%s': %s", icon, reader.errorString())
    return q_icon


