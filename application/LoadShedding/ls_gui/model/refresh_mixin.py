# coding=utf-8
"""
:Copyright: © 2014 Advanced Control Systems, Inc. All Rights Reserved.
"""
from contextlib import contextmanager
from core.QtCompat   import QtCore

__author__ = 'Sam Hartsfield'


class RefreshMixin(object):
    def __init__(self, *args, **kwargs):
        # noinspection PyArgumentList
        super(RefreshMixin, self).__init__(*args, **kwargs)
        # Instead of the timer, we could actually listen for changes,
        # but I'm not sure if that would actually be more efficient
        # (presumably it would be quicker to update, so long as it didn't
        # get bogged down).
        self._refresh_timer = QtCore.QTimer(self)
        self._refresh_timer.timeout.connect(self._on_refresh)
        self._refresh_timer.setInterval(2000)

    def _on_refresh(self):
        # raise NotImplementedError()
        # print("raise NotImplementedError()")
        pass

    def enable_refresh(self, enable):
        if enable:
            self._refresh_timer.start()
        else:
            self._refresh_timer.stop()

    def is_refresh_enabled(self):
        return self._refresh_timer.isActive()

    @property
    def refresh_interval_ms(self):
        return self._refresh_timer.interval()

    @refresh_interval_ms.setter
    def refresh_interval_ms(self, interval_ms):
        self._refresh_timer.setInterval(interval_ms)

    @contextmanager
    def _pause_refresh(self):
        refresh_enabled = self.is_refresh_enabled()
        if refresh_enabled:
            self.enable_refresh(False)
        yield
        # Resume refresh, only if it was active before
        if refresh_enabled:
            self.enable_refresh(True)
