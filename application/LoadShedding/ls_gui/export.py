# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
__author__ = 'Darren Liang'


import csv
from core.QtCompat import QtWidgets, QtGui, QtCore, Qt

class ExportTable(QtCore.QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.qmutex   = QtCore.QMutex()
        self._headers = None
        self._path    = None
        self._datas   = None

    @property
    def path(self):
        """
        :path: path of file location
        """
        return self._path

    @path.setter
    def path(self, path):
        self._path = path
    
    @property
    def headers(self):
        """
        :headers: header of table
        """
        return self._headers

    @headers.setter
    def headers(self, header):    
        self._headers = header
    
    @property
    def datas(self):
        """
        :datas: data of table
        """
        return self._datas

    @datas.setter
    def datas(self, data):
        if (data is not None) or (len(data) != 0):
            self._datas = data
            # self._datas = self.preprocessing(data)

    def preprocessing(self, dataSet):
        temp = list()
        for data in dataSet:
            convert = tuple(map(_, map(str, data)))
            temp.append(convert)
        return temp
    
    def manufactory(self):
        # open new csv file
        with open(self.path, 'w', encoding='utf-8') as csvfile:
            # set csv writer
            writer = csv.writer(csvfile)
            # write header to csv
            writer.writerow([s for s in self.headers])
            # insert into dataSet
            for row in self.datas:
                writer.writerow([str(s) for s in row])

    def run(self):
        self.qmutex.lock()
        self.manufactory()
        self.qmutex.unlock() 
