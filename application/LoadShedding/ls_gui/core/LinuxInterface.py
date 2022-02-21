#!/usr/bin/python3.6
# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
import os
import subprocess
from acsprism import *
__author__ = 'Darren Liang'


class LinuxInterface:
    def __init__(self):
        self.usr = os.getenv('ORACLE_USER')
        self.pwd = os.getenv('ORACLE_PW')
        self.tns = os.getenv('ORACLE_DBSTRING')

    def ExeCommand(self, command):
        return subprocess.check_output("%s" % command, shell=True).replace('\n','')

    def ExeNonCommand(self, command):
        subprocess.call(command, shell=True)

    def readrtdb(self, station, category, point, point_type, attr):
        
        rtdb_init()

        station    = int(station)
        category   = str(category)
        point      = int(point)
        point_type = str(point_type)
        attr       = str(attr)
        rtdb_pt = RtdbPoint(station, category, point,point_type)
        return str(rtdb_pt.read_attr(attr))
    def writertdb(self, station, category, point, point_type, attr, value):
        rtdb_init()
        RtdbPoint(station, category, point, point_type).write_attr(attr, value)