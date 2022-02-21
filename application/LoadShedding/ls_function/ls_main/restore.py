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

class Restore(ModeBase):
    def __init__(self, group):
        super(Restore,self).__init__()
        self.group  = group.split(",")
    
    @property
    def mode(self):    
        return 0
    
    def job(self):
        for ls in self.lsSet:
            if ls.groupname in self.group:
                if self._running:
                    if ls.lsact > 0:
                        if ls.stastatus == 0:
                            self.close_fcb(ls)
                    ls.lsact = 0
                else:
                    return
            # else:
            #     logger.info("FEEDER:{0} NOT IN GROUP:{1}, Ignore".format(ls.feeder, ','.join(self.group)))
        


def main():
    from acsprism import rtdb_init
    from logger import setup_logger
    rtdb_init()
    restore = Restore("A,B")
    setup_logger(restore.logname)
    restore.start()

if __name__ == "__main__":
    main()     
