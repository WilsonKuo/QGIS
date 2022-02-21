"""
This module attempts to resolve the major problems of allowing this program
to use either PySide or PyQt4 without any code/import changes.

Alternatively, there is a package "pyqode.qt",
which provides compatibility with PyQt5, PyQt4, and PySide, using the
PyQt5 layout (there are also some other similar packages, e.g. QtPy).


I started with something I found in a web search, but it used a dynamic import
method that causes problems with code completion.

Reference (add others as found; some found with search on
"pyside qt_compat.py"):

* http://qt-project.org/wiki/Differences_Between_PySide_and_PyQt

  - https://github.com/ros-visualization/python_qt_binding

* http://askubuntu.com/questions/140740/should-i-use-pyqt-or-pyside-for-a-new-qt-project
* https://github.com/epage/PythonUtils/blob/master/util/qt_compat.py
* https://pypi.python.org/pypi/pyqode.qt


:author: Sam Hartsfield
"""
import logging
import os

__author__ = 'Sam Hartsfield'

logger = logging.getLogger(__name__)

_TRY_PYSIDE = True

# Note: TraitsUI (and maybe other libraries as well) reads the "QT_API"
# environment variable, and expects certain values.
# The "pyqode.qt" shim also writes this variable.
API_VAR = 'QT_API'


def set_sip_api_v2():
    # PySide is only compatible with PyQt4's API version 2.
    import sip
    sip.setapi('QDate', 2)
    sip.setapi('QDateTime', 2)
    sip.setapi('QString', 2)
    sip.setapi('QTextStream', 2)
    sip.setapi('QTime', 2)
    sip.setapi('QUrl', 2)
    sip.setapi('QVariant', 2)


if API_VAR in os.environ:
    if os.environ[API_VAR].lower() == 'pyqt5':
        import PyQt5
        os.environ[API_VAR] = 'pyqt5'
    elif os.environ[API_VAR].lower() == 'pyside2':
        import PySide2
        os.environ[API_VAR] = 'pyside2'
    elif os.environ[API_VAR].lower() == 'pyqt4':
        set_sip_api_v2()
        import PyQt4
        os.environ[API_VAR] = 'pyqt'
    elif os.environ[API_VAR].lower() == 'pyside':
        import PySide
        os.environ[API_VAR] = 'pyside'
else:
    try:
        if not _TRY_PYSIDE:
            raise ImportError()
        import PySide
        # TODO: should we set sys.modules['PyQt4'] to point to PySide?
        os.environ[API_VAR] = 'pyside'
    except ImportError:
        try:
            import PyQt5
            os.environ[API_VAR] = 'pyqt5'
        except ImportError:
            # PySide2 doesn't seem to be ready yet.
            # import PySide2
            # os.environ[API_VAR] = 'pyside2'

            # PySide is only compatible with PyQt4's API version 2.
            set_sip_api_v2()
            import PyQt4
            os.environ[API_VAR] = 'pyqt'

from  core.QtCompat             import QtCore
from  core.QtCompat.QtCore      import Qt, Signal, Slot, Property
from  core.QtCompat.ui_loader   import qt_load_ui

logger.info("Using %s" % os.environ[API_VAR])

__all__ = ['QtCore', 'Qt', 'Signal', 'Slot', 'Property', 'qt_load_ui']
