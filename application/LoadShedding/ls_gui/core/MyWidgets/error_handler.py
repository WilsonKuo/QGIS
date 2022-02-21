# coding=utf-8
"""
Provides an exception hook for use in Qt GUI applications, to
prevent unhandled exceptions from going unseen.

:Copyright: © 2017 Advanced Control Systems, Inc. All Rights Reserved.
"""

import logging
import os
import traceback
import sys
from acs._compat import PY2
from acs.i18n_common import ugettext as _
from  core.QtCompat.QtWidgets import QApplication, QMessageBox

__author__ = 'Sam Hartsfield'

logger = logging.getLogger(__name__)


# On Python 2, the traceback module returns encoded bytes. Need to decode
# for non-English languages (try e.g. 'export LANG=es_ES.utf8').
# On Python 3, it's unicode.
if PY2:
    def text_list(l, encoding='utf-8'):
        return [s.decode(encoding) for s in l]
else:
    def text_list(l, encoding='utf-8'):
        return l


_error_active = False
_instance = None


def get_instance():
    global _instance
    if _instance is None:
        _instance = ErrorHandler()
    return _instance


def set_log_path(log_path):
    get_instance().log_path = log_path


# May not actually be needed now that we use QApplication.activeWindow()
def set_default_parent(parent_widget):
    get_instance().parent_widget = parent_widget


def install(error_handler=None):
    """
    Install the error handler as the global exception hook.

    :param error_handler: if set, override the default error handler
    """
    # Allow overriding the default handler with e.g. a subclass
    if error_handler is None:
        error_handler = get_instance()
    else:
        global _instance
        _instance = error_handler
    sys.excepthook = error_handler.exception_hook


class ErrorHandler(object):
    def __init__(self, log_filename=None):
        self.parent_widget = None
        self.log_path = log_filename

    def exception_hook(self, exctype, value, tb):
        """
        In case of unhandled exceptions (especially in PyQt event handlers),
        log them instead of just printing to stderr (so they will get recorded
        in any log file(s)).

        If a Qt GUI is active (i.e. there is a QApplication instance), then pop
        up a message box with the exception message. Afterwards, the
        application aborts.

        Originally copied from Centrix Builder project.
        """
        logger.error(
            u"Unhandled exception:\n%s",
            u''.join(text_list(traceback.format_exception(exctype, value, tb))))

        if not issubclass(exctype, Exception):
            # Don't display a dialog for e.g. KeyboardInterrupt
            sys.exit(1)

        # noinspection PyArgumentList
        q_app = QApplication.instance()
        if q_app:
            # Don't pop up multiple dialog boxes
            global _error_active
            if _error_active:
                return
            _error_active = True

            # Try to pop up over the currently-active window
            parent = q_app.activeWindow()
            if not parent:
                parent = self.parent_widget
            msg_box = QMessageBox(parent)
            msg_box.setWindowTitle(_("Unexpected Error"))
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText(
                u''.join(text_list(traceback.format_exception_only(
                    exctype, value))).strip())

            # Path to directory containing the file, so it opens an explorer
            # window (instead of opening the file itself in a text editor).
            # My reasoning is that the user doesn't want to look at the file,
            # they just need to transfer it to the developer; that may or
            # may not be a valid assumption.
            if self.log_path:
                log_url = 'file:///' + os.path.split(
                    self.log_path)[0].replace('\\', '/')
                # log_url = 'file:///' + self.log_filename.replace('\\', '/')

                msg_box.setInformativeText(
                    _("More information may be available in the log file"
                      " (<a href=\"%s\">%s</a>).")
                    % (log_url, self.log_path))

            msg_box.exec_()
            # QApplication.exit doesn't quite seem to do what we want
            # q_app.exit(1)
            sys.exit(1)
