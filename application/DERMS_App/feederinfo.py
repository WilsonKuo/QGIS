#!/bin/python3.6

class FEEDERInfo(object):
    def __init__(self, dataSet):
        self.dataSet = dataSet
        self.p_sum = 0
        self.q_sum = 0

    @property
    def name(self):
        return self.dataSet['NAME']
        
    @property
    def colorcode(self):
        return self.dataSet['COLORCODE']
    

    def reset_val(self):
        self.p_sum = 0
        self.q_sum = 0