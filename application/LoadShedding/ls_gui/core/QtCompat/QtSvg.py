# coding=utf-8
import os

__author__ = 'Sam Hartsfield'

if os.environ['QT_API'] == 'pyqt5':
    from PyQt5.QtSvg import *
    from PyQt5 import QtSvg as _Module
elif os.environ['QT_API'] == 'pyside2':
    from PySide2.QtSvg import *
    from PySide2 import QtSvg as _Module
elif os.environ['QT_API'] == 'pyside':
    from PySide.QtSvg import *
    from PySide import QtSvg as _Module
elif os.environ['QT_API'] == 'pyqt':
    from PyQt4.QtSvg import *
    from PyQt4 import QtSvg as _Module

# Appears to work well enough to get completion in PyCharm
__all__ = [x for x in dir(_Module) if not x.startswith('_')]
