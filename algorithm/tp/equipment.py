#!/bin/python3.6
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
# Non-System
from acsprism import RtdbAddress,RtdbPoint

# https://stackoverflow.com/questions/16017397/injecting-function-call-after-init-with-decorator
# define a new metaclass which overrides the "__call__" function
class NewInitCaller(type):
    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        obj.new_init()
        return obj

class Equipment(object, metaclass = NewInitCaller):
    def __init__(self, data, analysis_mode):
        self.data = data
        self.analysis_mode = analysis_mode
        
        self.sourceufiddict = dict()
        self.parentufiddict = dict()
        self.nonlineparentufiddict = dict()
    def new_init(self):
        try:
            self.addr_stastatus = RtdbAddress(self.station, self.category, self.point, self.rtdbtype)
            self.addr_stastatus.analysis_mode = self.analysis_mode
            self.p_stastatus = RtdbPoint(self.addr_stastatus)
        except Exception as e:
            print(e)
            self.p_stastatus = None
        # for not line tmp
        self.__colorcode = None
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
    def station(self):
        return self.data['STATION']
    @property
    def category(self):
        return self.data['CATEGORY']
    @property
    def point(self):
        return self.data['POINT']
    @property
    def rtdbtype(self):
        return self.data['RTDBTYPE']
    @property
    def attribute(self):
        return self.data['ATTRIBUTE']
    @property
    def stastatus(self):
        if self.p_stastatus:
            if self.rtdbtype == 'T':
                return 1
            else:
                return self.p_stastatus.read_attr(self.attribute)
        else:
            return 0
    #ONLY SOURCE, WILL CREATE SOURCE OBJECT AND LINE OBJECT LATER...
    @property
    def colorcodebook(self):
         return self.data['COLORCODE']

    @property
    def colorcode(self):
        if self.p_stastatus:
            if self.rtdbtype == 'T':
                return self.p_stastatus.read_attr(self.attribute)
            else:
                return self.__colorcode
    @colorcode.setter
    def colorcode(self, value):
        if self.p_stastatus:
            if self.rtdbtype == 'T':
                self.p_stastatus.write_attr(self.attribute, value)
            else:
                self.__colorcode = value

