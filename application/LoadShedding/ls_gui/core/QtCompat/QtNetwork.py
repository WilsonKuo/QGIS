# coding=utf-8
import os

__author__ = 'Sam Hartsfield'

if os.environ['QT_API'] == 'pyqt5':
    from PyQt5.QtNetwork import *
    from PyQt5 import QtNetwork as _Module
elif os.environ['QT_API'] == 'pyside2':
    from PySide2.QtNetwork import *
    from PySide2 import QtNetwork as _Module
elif os.environ['QT_API'] == 'pyside':
    from PySide.QtNetwork import *
    from PySide import QtNetwork as _Module
elif os.environ['QT_API'] == 'pyqt':
    from PyQt4.QtNetwork import *
    from PyQt4 import QtNetwork as _Module

# Appears to work well enough to get completion in PyCharm
__all__ = [x for x in dir(_Module) if not x.startswith('_')]
