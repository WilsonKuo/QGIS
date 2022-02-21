# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
__author__ = 'Darren Liang'

from loadshedding    import loadshedding
from core.QtCompat  import QtWidgets, QtGui, QtCore, Slot, Qt

class ThreadPool(object):
    def __init__(self):
        self._pool  = {}
        self._idnex = 0 

        self._pool.setdefault(f"restore" , {})
        self._pool.setdefault(f"bydemand", {})
        self._pool.setdefault(f"rotating", {})
        self._pool.setdefault(f"uf"      , {})

    @property
    def pool(self):
        return self._pool
    
    def add(self, name, index, worker):
        if not self._pool[name].__contains__(index):
            self._pool[name][index] = worker

    def delete(self, name, index):
        if self._pool[name].__contains__(index):
            self._pool[name].pop(index, None)

    def get(self, name, index):
        if self._pool[name].__contains__(index):
            return self._pool[name][index]
        else:
            return None

    def get_task_count(self, name):
        return len(list(self.pool[name].keys()))

    def get_task_tips(self, name):
        tasks = self.pool[name]
        return "" if tasks == None else "\n".join([ f"{i+1}. {t}"for i, t in enumerate(tasks)])


class Worker(QtCore.QThread):
    def __init__(self, args, parent):
        super().__init__(parent)
        self.qmutex  = QtCore.QMutex()
        self.args    = args
        self.process = loadshedding.main(self.args)

    def stop(self):
        self.process._running = False

    def run(self):
        self.qmutex.lock()
        self.process.start()
        self.qmutex.unlock() 



