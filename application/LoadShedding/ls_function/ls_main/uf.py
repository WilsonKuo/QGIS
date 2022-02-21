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

class UF(ModeBase):
    def __init__(self, Amode):
        super(UF,self).__init__(Amode)
        self.set_ufDict()
        #print(self.ufSet)
        if self.Amode != 0:
            print("UF Right Now Only Support Real Time Mode")
    
    @property
    def mode(self):    
        return 3

    def job(self):
        # import traceback
        # traceback.print_exc()
        check_times = 0
        while self._running:
            check_times += 1
            logger.info(self.Amode_prefix + "--------------Check Times:{0}-------------------".format(check_times))
            colorcodedict = dict()
            for ls in self.lsSet:
                if ls.uplinecolorcode not in colorcodedict.keys():
                    colorcodedict[ls.uplinecolorcode] = list()
                colorcodedict[ls.uplinecolorcode].append(ls)
            for uf in self.ufSet:
                if uf.lockflag == 0:
                    if uf.stastatus == 1:
                        logger.info(self.Amode_prefix + "UF:{0} is abnormal, start doing loadshedding".format(uf.name))
                        if uf.colorcode in colorcodedict.keys():
                            for ls in colorcodedict[uf.colorcode]:
                                if uf.stastatus == 1:
                                    if self.open_fcb(ls):
                                        time.sleep(self.uf_check_if_fcbopen_work_interval)
                                    # else : no need to wait
                                else:
                                    logger.info(self.Amode_prefix + "UF:{0} is back to normal".format(uf.name))
                                    break
                        else:
                            logger.info(self.Amode_prefix + "UF:{0} has no downstream".format(uf.name))
                    else:
                        logger.info(self.Amode_prefix + "UF:{0} is normal".format(uf.name))
                        
            time.sleep(self.uf_check_interval)



def main():
    from acsprism import rtdb_init
    from logger import setup_logger
    rtdb_init()
    uf = UF(0)
    setup_logger(uf.logname)
    uf.start()

if __name__ == "__main__":
    main()     
