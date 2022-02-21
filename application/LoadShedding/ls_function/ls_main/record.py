#!/bin/python3.6
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
from __future__ import absolute_import
import os
import logging
# Non-System
from acsprism import RtdbAddress,RtdbPoint

__author__ = 'Wilson Kuo'

logger = logging.getLogger(__name__)


# https://stackoverflow.com/questions/16017397/injecting-function-call-after-init-with-decorator
# define a new metaclass which overrides the "__call__" function
class NewInitCaller(type):
    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        obj.new_init()
        return obj

class LSRecord(object, metaclass = NewInitCaller):
    def __init__(self, dataSet):
        # print ("Init class")
        self.dataSet = dataSet
    def new_init(self):
        # print ("New init!!")
        # LSGROUPLOCKFLAG
        try:
            self.addr_lsgrouplockflag = RtdbAddress(self.station_lsgrouplockflag, self.category_lsgrouplockflag, self.point_lsgrouplockflag, self.rtdbtype_lsgrouplockflag)
            self.p_lsgrouplockflag = RtdbPoint(self.addr_lsgrouplockflag)
        except:
            self.p_lsgrouplockflag = None
        # ACT
        try:
            self.addr_lsact = RtdbAddress(self.station_lsact, self.category_lsact, self.point_lsact, self.rtdbtype_lsact)
            self.p_lsact = RtdbPoint(self.addr_lsact)
        except:
            self.p_lsact = None
        # UPLINECOLORCODE
        try:
            self.addr_uplinecolorcode = RtdbAddress(self.station_uplinecolorcode, self.category_uplinecolorcode, self.point_uplinecolorcode, self.rtdbtype_uplinecolorcode)
            self.p_uplinecolorcode = RtdbPoint(self.addr_uplinecolorcode)
        except:
            self.p_uplinecolorcode = None

        # FCB STATUS
        try:
            self.addr_stastatus = RtdbAddress(self.station_stastatus, self.category_stastatus, self.point_stastatus, self.rtdbtype_stastatus)
            self.p_stastatus = RtdbPoint(self.addr_stastatus)
        except:
            self.p_stastatus = None
        # FCB LSLOCKFLAG
        try:
            self.addr_lslockflag = RtdbAddress(self.station_lslockflag, self.category_lslockflag, self.point_lslockflag, self.rtdbtype_lslockflag)
            self.p_lslockflag = RtdbPoint(self.addr_lslockflag)
        except:
            self.p_lslockflag = None
        # REAL POWER TELEMETRY
        try:
            self.addr_pa = RtdbAddress(self.station_pa, self.category_pa, self.point_pa, self.rtdbtype_pa)
            self.p_pa = RtdbPoint(self.addr_pa)
        except:
            self.p_pa = None
        try:
            self.addr_pb = RtdbAddress(self.station_pb, self.category_pb, self.point_pb, self.rtdbtype_pb)
            self.p_pb = RtdbPoint(self.addr_pb)
        except:
            self.p_pb = None
        try:
            self.addr_pc = RtdbAddress(self.station_pc, self.category_pc, self.point_pc, self.rtdbtype_pc)
            self.p_pc = RtdbPoint(self.addr_pc)
        except:
            self.p_pc = None
            
    @property
    def groupname(self):
        return self.dataSet["GROUPNAME"]

###########LS GROUPLOCKFLAG###########
    @property
    def station_lsgrouplockflag(self):
        return self.dataSet["STATION_LSGROUPLOCKFLAG"]

    @property
    def category_lsgrouplockflag(self):
        return self.dataSet["CATEGORY_LSGROUPLOCKFLAG"]

    @property
    def point_lsgrouplockflag(self):
        return self.dataSet["POINT_LSGROUPLOCKFLAG"]

    @property
    def rtdbtype_lsgrouplockflag(self):
        return self.dataSet["RTDBTYPE_LSGROUPLOCKFLAG"]
    @property
    def attribute_lsgrouplockflag(self):
        return self.dataSet["ATTRIBUTE_LSGROUPLOCKFLAG"]

    @property
    def lsgrouplockflag(self):
        if self.p_lsgrouplockflag:
            return self.p_lsgrouplockflag.read_attr(self.attribute_lsgrouplockflag)
    @lsgrouplockflag.setter
    def lsgrouplockflag(self, value):
        self.p_lsgrouplockflag.write_attr(self.attribute_lsgrouplockflag, value)
###################################
    @property
    def substation(self):
        return self.dataSet["SUBSTATION"]

    @property
    def feeder(self):
        return self.dataSet["FEEDER"]

    @property
    def lsfeeder_priority(self):
        return self.dataSet["LSFEEDER_PRIORITY"]
    @property
    def lsfdidx(self):
        return self.dataSet["LSFDIDX"]
###########FCB uplinecolorcodeCOLORCODE###########
    @property
    def station_uplinecolorcode(self):
        return self.dataSet["STATION_UPLINECOLORCODE"]

    @property
    def category_uplinecolorcode(self):
        return self.dataSet["CATEGORY_UPLINECOLORCODE"]

    @property
    def point_uplinecolorcode(self):
        return self.dataSet["POINT_UPLINECOLORCODE"]

    @property
    def rtdbtype_uplinecolorcode(self):
        return self.dataSet["RTDBTYPE_UPLINECOLORCODE"]
    @property
    def attribute_uplinecolorcode(self):
        return self.dataSet["ATTRIBUTE_UPLINECOLORCODE"]

    @property
    def uplinecolorcode(self):
        if self.p_uplinecolorcode:
            return int(self.p_uplinecolorcode.read_attr(self.attribute_uplinecolorcode))
###########LS ACT###########
    @property
    def station_lsact(self):
        return self.dataSet["STATION_LSACT"]

    @property
    def category_lsact(self):
        return self.dataSet["CATEGORY_LSACT"]

    @property
    def point_lsact(self):
        return self.dataSet["POINT_LSACT"]

    @property
    def rtdbtype_lsact(self):
        return self.dataSet["RTDBTYPE_LSACT"]
    @property
    def attribute_lsact(self):
        return self.dataSet["ATTRIBUTE_LSACT"]

    @property
    def lsact(self):
        if self.p_lsact:
            return self.p_lsact.read_attr(self.attribute_lsact)
    @lsact.setter
    def lsact(self, value):
        self.p_lsact.write_attr(self.attribute_lsact, value)
###########FCB STASTATUS###########
    @property
    def station_stastatus(self):
        return self.dataSet["STATION_STASTATUS"]

    @property
    def category_stastatus(self):
        return self.dataSet["CATEGORY_STASTATUS"]

    @property
    def point_stastatus(self):
        return self.dataSet["POINT_STASTATUS"]

    @property
    def rtdbtype_stastatus(self):
        return self.dataSet["RTDBTYPE_STASTATUS"]
    @property
    def attribute_stastatus(self):
        return self.dataSet["ATTRIBUTE_STASTATUS"]

    @property
    def stastatus(self):
        if self.p_stastatus:
            return self.p_stastatus.read_attr(self.attribute_stastatus)
    @stastatus.setter
    def stastatus(self, value):
        if value == 0:
            print("Open Feeder {0}".format(self.feeder))
        else:
            print("Close Feeder {0}".format(self.feeder))
        self.p_stastatus.write_attr(self.attribute_stastatus, value)
###########FCB CONTROL###########
    @property
    def fep(self):
        return self.dataSet["FEP"]
    @property
    def ctrlstation(self):
        return self.dataSet["CTRLSTATION"]

    @property
    def ctrlrecord(self):
        return self.dataSet["CTRLRECORD"]

    @property
    def control(self):
        if self.ctrlstation and self.ctrlrecord:
            return True
        else:
            return False
    @control.setter
    def control(self, value):
        self.cons = 0
        self.clos = 250
        self.v1 = 0
        self.v2 = 0
        self.stim = 10
        if value == 0:
            logger.debug("Open Feeder {0}".format(self.feeder))
            logger.debug("dcntrl {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} > /dev/null 2>&1".format(self.fep, value, self.ctrlstation, self.ctrlrecord, self.cons, self.clos, self.v1, self.v2, self.station_stastatus, self.category_stastatus, self.point_stastatus, self.stim))
            os.system("dcntrl {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} > /dev/null 2>&1".format(self.fep, value, self.ctrlstation, self.ctrlrecord, self.cons, self.clos, self.v1, self.v2, self.station_stastatus, self.category_stastatus, self.point_stastatus, self.stim))

        else:
            logger.debug("Close Feeder {0}".format(self.feeder))
            logger.debug("dcntrl {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} > /dev/null 2>&1".format(self.fep, value, self.ctrlstation, self.ctrlrecord, self.cons, self.clos, self.v1, self.v2, self.station_stastatus, self.category_stastatus, self.point_stastatus, self.stim))
            os.system("dcntrl {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} > /dev/null 2>&1".format(self.fep, value, self.ctrlstation, self.ctrlrecord, self.cons, self.clos, self.v1, self.v2, self.station_stastatus, self.category_stastatus, self.point_stastatus, self.stim))

###########FCB LOCKFLAG STATUS###########
    @property
    def station_lslockflag(self):
        return self.dataSet["STATION_LSLOCKFLAG"]

    @property
    def category_lslockflag(self):
        return self.dataSet["CATEGORY_LSLOCKFLAG"]

    @property
    def point_lslockflag(self):
        return self.dataSet["POINT_LSLOCKFLAG"]

    @property
    def rtdbtype_lslockflag(self):
        return self.dataSet["RTDBTYPE_LSLOCKFLAG"]
    @property
    def attribute_lslockflag(self):
        return self.dataSet["ATTRIBUTE_LSLOCKFLAG"]

    @property
    def lslockflag(self):
        if self.p_lslockflag:
            return self.p_lslockflag.read_attr(self.attribute_lslockflag)
    @lslockflag.setter
    def lslockflag(self, value):
        if self.p_lslockflag:
            if value == 0:
                print("Enable Feeder {0}".format(self.feeder))
            else:
                print("Disable Feeder {0}".format(self.feeder))
            self.p_lslockflag.write_attr(self.attribute_lslockflag, value)
    #PA
    @property
    def station_pa(self):
        return self.dataSet["STATION_PA"]

    @property
    def category_pa(self):
        return self.dataSet["CATEGORY_PA"]

    @property
    def point_pa(self):
        return self.dataSet["POINT_PA"]
        
    @property
    def rtdbtype_pa(self):
        return self.dataSet["RTDBTYPE_PA"]

    @property
    def attribute_pa(self):
        return self.dataSet["ATTRIBUTE_PA"]
    @property
    def pa(self):
        if self.p_pa:
            return self.p_pa.read_attr(self.attribute_pa)
        else:
            return 0
    @pa.setter
    def pa(self, value):
        if self.p_pa:
            self.p_pa.write_attr(self.attribute_pa, value)
    #PB
    @property
    def station_pb(self):
        return self.dataSet["STATION_PB"]

    @property
    def category_pb(self):
        return self.dataSet["CATEGORY_PB"]

    @property
    def point_pb(self):
        return self.dataSet["POINT_PB"]
        
    @property
    def rtdbtype_pb(self):
        return self.dataSet["RTDBTYPE_PB"]

    @property
    def attribute_pb(self):
        return self.dataSet["ATTRIBUTE_PB"]

    @property
    def pb(self):
        if self.p_pb:
            return self.p_pb.read_attr(self.attribute_pb)
        else:
            return 0
    @pb.setter
    def pb(self, value):
        if self.p_pb:
            self.p_pb.write_attr(self.attribute_pb, value)
    #PC
    @property
    def station_pc(self):
        return self.dataSet["STATION_PC"]

    @property
    def category_pc(self):
        return self.dataSet["CATEGORY_PC"]

    @property
    def point_pc(self):
        return self.dataSet["POINT_PC"]
        
    @property
    def rtdbtype_pc(self):
        return self.dataSet["RTDBTYPE_PC"]

    @property
    def attribute_pc(self):
        return self.dataSet["ATTRIBUTE_PC"]

    @property
    def pc(self):
        if self.p_pc:
            return self.p_pc.read_attr(self.attribute_pc)
        else:
            return 0
    @pc.setter
    def pc(self, value):
        if self.p_pc:
            self.p_pc.write_attr(self.attribute_pc, value)
###################################################################
    @property
    def p(self):
        return self.pa + self.pb + self.pc
###################################################################

    # @property
    # def systemlockflag(self):
    #     return self.dataSet["SYSTEMLOCKFLAG"]
    # @systemlockflag.setter
    # def systemlockflag(self, value):
    #     self.dataSet["SYSTEMLOCKFLAG"] = value
    #     if value == 0:
    #         print("DISABLE {0} SYSTEMLOCKFLAG".format(self.feeder))
    #     else:
    #         print("ENABLE {0} SYSTEMLOCKFLAG".format(self.feeder))
    #     DASDB.ExecNonQuery("UPDATE LS_FD_XREF SET SYSTEMLOCKFLAG = {0} WHERE FEEDER = '{1}'".format(value, self.feeder))


class LSRecord_DTS(object):
    def __init__(self, ls):
        self.groupname_dts         = ls.groupname
        self.lsgrouplockflag_dts   = ls.lsgrouplockflag
        self.substation_dts        = ls.substation
        self.feeder_dts            = ls.feeder
        self.lsfeeder_priority_dts = ls.lsfeeder_priority
        self.lsfdidx_dts           = ls.lsfdidx
        self.lsact_dts             = ls.lsact
        self.uplinecolorcode_dts   = ls.uplinecolorcode
        self.stastatus_dts         = ls.stastatus
        self.lslockflag_dts        = ls.lslockflag
        self.pa_dts                = ls.pa
        self.pb_dts                = ls.pb
        self.pc_dts                = ls.pc
        self.pa_dts_solid          = ls.pa
        self.pb_dts_solid          = ls.pb
        self.pc_dts_solid          = ls.pc
        self.control_dts           = 1 if (ls.fep and ls.ctrlstation and ls.ctrlrecord and ls.station_stastatus and ls.category_stastatus and ls.point_stastatus) else 0

    @property
    def groupname(self):
        return self.groupname_dts

    @property
    def substation(self):
        return self.substation_dts

    @property
    def feeder(self):
        return self.feeder_dts

    @property
    def lsfeeder_priority(self):
        return self.lsfeeder_priority_dts

    @property
    def lsfdidx(self):
        return self.lsfdidx_dts

    @property
    def lsgrouplockflag(self):
        return self.lsgrouplockflag_dts
    @lsgrouplockflag.setter
    def lsgrouplockflag(self, value):
        self.lsgrouplockflag_dts = value

    @property
    def lsact(self):
        return self.lsact_dts
    @lsact.setter
    def lsact(self, value):
        self.lsact_dts = value

    @property
    def stastatus(self):
        return self.stastatus_dts
    @stastatus.setter
    def stastatus(self, value):
        self.stastatus_dts = value
    
    @property
    def control(self):
        return self.control_dts
    @control.setter
    def control(self, value):
        #self.control_dts = value
        self.stastatus_dts = value
        if value == 0:
            self.pa_dts = 0
            self.pb_dts = 0
            self.pc_dts = 0
        elif value == 1:
            self.pa_dts = self.pa_dts_solid
            self.pb_dts = self.pb_dts_solid
            self.pc_dts = self.pc_dts_solid

    @property
    def lslockflag(self):
        return self.lslockflag_dts
    @lslockflag.setter
    def lslockflag(self, value):
        self.lslockflag_dts = value

    @property
    def pa(self):
        return self.pa_dts
    @pa.setter
    def pa(self, value):
        self.pa_dts = value

    @property
    def pb(self):
        return self.pb_dts
    @pb.setter
    def pb(self, value):
        self.pb_dts = value

    @property
    def pc(self):
        return self.pc_dts
    @pc.setter
    def pc(self, value):
        self.pc_dts = value

    @property
    def p(self):
        return self.pa_dts + self.pb_dts + self.pc_dts




class UFRecord(object, metaclass = NewInitCaller):
    def __init__(self, dataSet):
        # print ("Init class")
        self.dataSet = dataSet
    def new_init(self):
        # print ("New init!!")
        # UF STATUS
        try:
            self.addr_stastatus = RtdbAddress(self.station_stastatus, self.category_stastatus, self.point_stastatus, self.rtdbtype_stastatus)
            self.p_stastatus = RtdbPoint(self.addr_stastatus)
        except:
            self.p_stastatus = None
        #  UF LOCKFLAG
        try:
            self.addr_lockflag = RtdbAddress(self.station_lockflag, self.category_lockflag, self.point_lockflag, self.rtdbtype_lockflag)
            self.p_lockflag = RtdbPoint(self.addr_lockflag)
        except:
            self.p_lockflag = None

    @property
    def name(self):
        return self.dataSet['NAME']
    @property
    def colorcode(self):
        return self.dataSet['COLORCODE']
    # UF STASTATUS #
    @property
    def rtdbtype_stastatus(self):
        return self.dataSet['RTDBTYPE_STASTATUS']

    @property
    def station_stastatus(self):
        return self.dataSet['STATION_STASTATUS']
    
    @property
    def category_stastatus(self):
        return self.dataSet['CATEGORY_STASTATUS']

    @property
    def point_stastatus(self):
        return self.dataSet['POINT_STASTATUS']
    
    @property
    def attribute_stastatus(self):
        return self.dataSet['ATTRIBUTE_STASTATUS']

    @property
    def stastatus(self):
        return self.p_stastatus.read_attr(self.attribute_stastatus)
    # UF LOCKFLAG #
    @property
    def rtdbtype_lockflag(self):
        return self.dataSet['RTDBTYPE_LOCKFLAG']

    @property
    def station_lockflag(self):
        return self.dataSet['STATION_LOCKFLAG']
    
    @property
    def category_lockflag(self):
        return self.dataSet['CATEGORY_LOCKFLAG']

    @property
    def point_lockflag(self):
        return self.dataSet['POINT_LOCKFLAG']
    
    @property
    def attribute_lockflag(self):
        return self.dataSet['ATTRIBUTE_LOCKFLAG']

    @property
    def lockflag(self):
        if self.p_lockflag:
            return self.p_lockflag.read_attr(self.attribute_lockflag)
        else:
            # has no lockflag, force to lock 
            return 1


def main():
    pass


if __name__ == "__main__":
    main()     
