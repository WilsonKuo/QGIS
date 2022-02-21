#!/bin/python3.6
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
import time
import logging
# Non-System
from modebase import ModeBase

__author__ = 'Wilson Kuo'

logger = logging.getLogger(__name__)

class Bydemand(ModeBase):
    def __init__(self, amode, group, demand):
        super(Bydemand,self).__init__(amode)
        self.group  = group.split(",")
        self.demand = demand
    
    @property
    def mode(self):    
        return 1
        
    @property
    def wholepsum(self):
        wholepsum = 0
        for ls in self.lsSet:
            if ls.groupname in self.group:
                wholepsum += ls.p
        return wholepsum
    def validate_capability(self):
        #call self.wholepsum is expensive!
        wholepsum = self.wholepsum
        if self.use_reduce:
            self.threshold = wholepsum - self.demand
        else:
            self.threshold = self.demand

        cutvalue = wholepsum - self.threshold

        controllable_psum = 0
        for ls in self.lsSet:
            if ls.lsgrouplockflag == 0:
                if ls.groupname in self.group:
                    if ls.lslockflag == 0:
                        if ls.stastatus == 1:
                            if ls.lsact == 0:
                                controllable_psum += ls.p
        if controllable_psum > cutvalue:
            logger.debug(self.Amode_prefix + "Controllable_psum: {0}, Cutvalue: {1}".format(controllable_psum, cutvalue))
            return True
        else:
            logger.debug(self.Amode_prefix + "Controllable_psum: {0}, Cutvalue: {1}".format(controllable_psum, cutvalue))
            return False

    def job(self):
        if self.validate_capability():
            logger.info(self.Amode_prefix + "Before doing load shedding, whole psum:{0}".format(self.wholepsum))
            for ls in self.lsSet:
                if self.wholepsum > self.threshold:
                    if ls.groupname in self.group:
                        if self._running:
                            logger.debug(self.Amode_prefix + "Not Meet Demand: WHOLEPSUM:{0} > THRESHOLD:{1}".format(self.wholepsum, self.threshold))
                            self.open_fcb(ls)
                        else:
                            break
                    # else:
                    #     logger.info(self.Amode_prefix + "FEEDER:{0} NOT IN GROUP:{1}, Ignore".format(ls.feeder, ','.join(self.group)))
                else:
                    logger.debug(self.Amode_prefix + "Meet Demand: WHOLEPSUM:{0} < THRESHOLD:{1}".format(self.wholepsum, self.threshold))
                    logger.info(self.Amode_prefix + "After doing load shedding, whole psum:{0}".format(self.wholepsum))
                    return
        


def main():
    from acsprism import rtdb_init
    from logger import setup_logger
    rtdb_init()
    bydemand = Bydemand(1, "A", 1500)
    setup_logger(bydemand.logname)
    bydemand.start()

if __name__ == "__main__":
    main()     
