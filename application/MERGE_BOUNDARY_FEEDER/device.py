#!/bin/python3.6
"""
:Copyright: © 2022 Advanced Control Systems, Inc. All Rights Reserved.
"""

class Device(object):
    def __init__(self, data):
        self.data = data
        self.flowdir = -1
    @property
    def ufid(self):
        return self.data['UFID']
    @property
    def fsc(self):
        return self.data['FSC']
    @property
    def name(self):
        return self.data['NAME']
    @property
    def frnodeid(self):
        return self.data['FRNODEID']
    @property
    def tonodeid(self):
        return self.data['TONODEID']
    @property
    def stastatus(self):
        return self.data['STASTATUS']
    @property
    def normalized_name(self):
        if self.fsc in (108, 114):
            if "J0" in self.name:
                return self.name[:str.find(self.name, "J0")] + self.name[str.find(self.name, "J0"):].replace("0","")
            elif "S0" in self.name:
                return self.name[:str.find(self.name, "S0")] + self.name[str.find(self.name, "S0"):].replace("0","")
            else:
                return self.name
        