"""
Experimental: I'm trying to improve the "Qt Compatibility" module to allow
statements like::

    from QtCompat.QtCore import QAbstractTableModel

You can accomplish this by messing with sys.modules, but IDEs don't
normally understand that.
"""

import os

__author__ = 'Sam Hartsfield'

if os.environ['QT_API'] == 'pyqt5':
    from PyQt5.QtCore import *
    # Add references to PySide-compatible generic names.
    # PyCharm completion/type inference seems to work better with imports than
    # assignments (e.g. "Signal = pyqtSignal").
    from PyQt5.QtCore import pyqtSignal as Signal
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtCore import pyqtProperty as Property

if os.environ['QT_API'] == 'pyside2':
    from PySide2.QtCore import *

elif os.environ['QT_API'] == 'pyside':
    from PySide.QtCore import *

    # Moved to QtCore in Qt5
    from PySide.QtGui import (
        QAbstractProxyModel,
        QSortFilterProxyModel,
        QItemSelection,
        QStringListModel,
        QItemSelectionModel)

elif os.environ['QT_API'] == 'pyqt':
    from PyQt4.QtCore import *
    # Add references to PySide-compatible generic names.
    # PyCharm completion/type inference seems to work better with imports than
    # assignments (e.g. "Signal = pyqtSignal").
    from PyQt4.QtCore import pyqtSignal as Signal
    from PyQt4.QtCore import pyqtSlot as Slot
    from PyQt4.QtCore import pyqtProperty as Property

    # Moved to QtCore in Qt5
    from PyQt4.QtGui import (
        QAbstractProxyModel,
        QSortFilterProxyModel,
        QItemSelection,
        QStringListModel,
        QItemSelectionModel)


# Attempt to give better code completion
# TODO: would it work to set __all__ dynamically?
# TODO: change to use cog?
# NOTE: currently has some manual addition due to Qt5 compatibility
# >>> import QtCompat  # to set sip API versions
# >>> import PyQt4.QtCore
# >>> from pprint import pprint
# >>> pprint([x for x in dir(PyQt4.QtCore) if not x.startswith('_')])
__all__ = [
 'Signal', 'Slot', 'Property',  # Generic names not in PyQt4.QtCore module
 'PYQT_CONFIGURATION',
 'PYQT_VERSION',
 'PYQT_VERSION_STR',
 'QAbstractAnimation',
 'QAbstractEventDispatcher',
 'QAbstractFileEngine',
 'QAbstractFileEngineHandler',
 'QAbstractFileEngineIterator',
 'QAbstractItemModel',
 'QAbstractListModel',
 'QAbstractState',
 'QAbstractTableModel',
 'QAbstractTransition',
 'QAnimationGroup',
 'QBasicTimer',
 'QBitArray',
 'QBuffer',
 'QByteArray',
 'QByteArrayMatcher',
 'QChildEvent',
 'QCoreApplication',
 'QCryptographicHash',
 'QDataStream',
 'QDate',
 'QDateTime',
 'QDir',
 'QDirIterator',
 'QDynamicPropertyChangeEvent',
 'QEasingCurve',
 'QElapsedTimer',
 'QEvent',
 'QEventLoop',
 'QEventTransition',
 'QFSFileEngine',
 'QFile',
 'QFileInfo',
 'QFileSystemWatcher',
 'QFinalState',
 'QGenericArgument',
 'QGenericReturnArgument',
 'QHistoryState',
 'QIODevice',
 'QLibrary',
 'QLibraryInfo',
 'QLine',
 'QLineF',
 'QLocale',
 'QMargins',
 'QMetaClassInfo',
 'QMetaEnum',
 'QMetaMethod',
 'QMetaObject',
 'QMetaProperty',
 'QMetaType',
 'QMimeData',
 'QModelIndex',
 'QMutex',
 'QMutexLocker',
 'QObject',
 'QObjectCleanupHandler',
 'QParallelAnimationGroup',
 'QPauseAnimation',
 'QPersistentModelIndex',
 'QPluginLoader',
 'QPoint',
 'QPointF',
 'QProcess',
 'QProcessEnvironment',
 'QPropertyAnimation',
 'QPyNullVariant',
 'QReadLocker',
 'QReadWriteLock',
 'QRect',
 'QRectF',
 'QRegExp',
 'QResource',
 'QRunnable',
 'QSemaphore',
 'QSequentialAnimationGroup',
 'QSettings',
 'QSharedMemory',
 'QSignalMapper',
 'QSignalTransition',
 'QSize',
 'QSizeF',
 'QSocketNotifier',
 'QState',
 'QStateMachine',
 'QSysInfo',
 'QSystemLocale',
 'QSystemSemaphore',
 'QT_TRANSLATE_NOOP',
 'QT_TR_NOOP',
 'QT_TR_NOOP_UTF8',
 'QT_VERSION',
 'QT_VERSION_STR',
 'QTemporaryFile',
 'QTextBoundaryFinder',
 'QTextCodec',
 'QTextDecoder',
 'QTextEncoder',
 'QTextStream',
 'QTextStreamManipulator',
 'QThread',
 'QThreadPool',
 'QTime',
 'QTimeLine',
 'QTimer',
 'QTimerEvent',
 'QTranslator',
 'QUrl',
 'QUuid',
 'QVariant',
 'QVariantAnimation',
 'QWaitCondition',
 'QWriteLocker',
 'QXmlStreamAttribute',
 'QXmlStreamAttributes',
 'QXmlStreamEntityDeclaration',
 'QXmlStreamEntityResolver',
 'QXmlStreamNamespaceDeclaration',
 'QXmlStreamNotationDeclaration',
 'QXmlStreamReader',
 'QXmlStreamWriter',
 'Q_ARG',
 'Q_CLASSINFO',
 'Q_ENUMS',
 'Q_FLAGS',
 'Q_RETURN_ARG',
 'Qt',
 'QtCriticalMsg',
 'QtDebugMsg',
 'QtFatalMsg',
 'QtMsgType',
 'QtSystemMsg',
 'QtWarningMsg',
 'SIGNAL',
 'SLOT',
 'bin_',
 'bom',
 'center',
 'dec',
 'endl',
 'fixed',
 'flush',
 'forcepoint',
 'forcesign',
 'hex_',
 'left',
 'lowercasebase',
 'lowercasedigits',
 'noforcepoint',
 'noforcesign',
 'noshowbase',
 'oct_',
 'pyqtBoundSignal',
 'pyqtPickleProtocol',
 'pyqtProperty',
 'pyqtRemoveInputHook',
 'pyqtRestoreInputHook',
 'pyqtSetPickleProtocol',
 'pyqtSignal',
 'pyqtSignature',
 'pyqtSlot',
 'pyqtWrapperType',
 'qAbs',
 'qAddPostRoutine',
 'qChecksum',
 'qCompress',
 'qCritical',
 'qDebug',
 'qErrnoWarning',
 'qFatal',
 'qFuzzyCompare',
 'qInf',
 'qInstallMsgHandler',
 'qIsFinite',
 'qIsInf',
 'qIsNaN',
 'qIsNull',
 'qQNaN',
 'qRegisterResourceData',
 'qRemovePostRoutine',
 'qRound',
 'qRound64',
 'qSNaN',
 'qSetFieldWidth',
 'qSetPadChar',
 'qSetRealNumberPrecision',
 'qSharedBuild',
 'qSwap',
 'qUncompress',
 'qUnregisterResourceData',
 'qVersion',
 'qWarning',
 'qrand',
 'qsrand',
 'reset',
 'right',
 'scientific',
 'showbase',
 'uppercasebase',
 'uppercasedigits',
 'ws',

 # Qt5
 'QAbstractProxyModel',
 'QSortFilterProxyModel',
 'QItemSelection',
 'QStringListModel',
 'QItemSelectionModel',
]
