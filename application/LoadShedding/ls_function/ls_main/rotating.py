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

class Rotating(ModeBase):
    def __init__(self, Amode, areas):
        super(Rotating,self).__init__(Amode)
        self.areas = areas.split(",")

        self.groupidx = dict()
        for index, area in enumerate(self.areas):
            for group in area.split("-"):
                self.groupidx[group] = index


        self.areaslsSet = list()
        for idx in range(len(self.areas)):
            self.areaslsSet.append(list())
        #Always handle index = 0
        for idx in range(len(self.lsSet)):
            self.areaslsSet[self.groupidx[self.lsSet[idx].groupname]].append(self.lsSet[idx])

        # To memorize processing elements, we need openlist list and restorelist list
        self.processing_ls = {'openlist':list(), 'restorelist':list()}
        del self.lsSet
    
    @property
    def mode(self):    
        return 2
    
    # def validate_capability(self):
    #     #call self.wholepsum is expensive!
    #     wholepsum = self.wholepsum
    #     if self.use_reduce:
    #         threshold = wholepsum - self.demand
    #     else:
    #         threshold = self.demand

    #     cutvalue = wholepsum - threshold

    #     controllable_psum = 0
    #     for ls in self.lsSet:
    #         if ls.lslockflag == 0:
    #             if ls.stastatus == 1:
    #                 if ls.lsact == 0:
    #                     controllable_psum += ls.p
    #     if controllable_psum > cutvalue:
    #         logger.info("Controllable_psum: {0}, Cutvalue: {1}".format(controllable_psum, cutvalue))
    #         return True
    #     else:
    #         logger.info("Controllable_psum: {0}, Cutvalue: {1}".format(controllable_psum, cutvalue))
    #         return False
    
    def job(self):

        first = True
        for areaidx, arealsSet in enumerate(self.areaslsSet):
            if first:
                first = False
                lenarealsSet = len(arealsSet)
                #Always handle index = 0
                for idx in range(lenarealsSet):
                    if self._running:
                        self.open_fcb(self.areaslsSet[areaidx][idx])
                        self.processing_ls['openlist'].append(self.areaslsSet[areaidx][idx])
                    else:
                        return
            else:
                # copy function to prevent shallow copy
                # move openlist to restorelist, the feeders which are opened in last iteration, they need to be restored in this iteration
                self.processing_ls['restorelist'] = self.processing_ls['openlist'].copy()
                # we need empty openlist for this iteration
                self.processing_ls['openlist'] *= 0
                # take # ls in restorelst as key because having to restore all ls which is open in last iteration
                processing_ls_restorelist_cnt = len(self.processing_ls['restorelist'])
                
                
                lenarealsSet = len(arealsSet)
                idx = 0
                #Always handle index = 0
                while idx < lenarealsSet:
                    #open
                    if self._running:
                        self.open_fcb(self.areaslsSet[areaidx][idx])
                        self.processing_ls['openlist'].append(self.areaslsSet[areaidx][idx])
                    else:
                        return
                    #close
                    if self._running:
                        if idx < processing_ls_restorelist_cnt:
                            self.close_fcb(self.processing_ls['restorelist'][idx])
                    else:
                        return
                    idx += 1
                
                #Restore the rest of feeder which are in restorelist
                while idx < processing_ls_restorelist_cnt:
                    if self._running:
                        self.close_fcb(self.processing_ls['restorelist'][idx])
                    else:
                        return
                    idx += 1

        if self.restore_last_area:
            for ls in self.processing_ls['openlist']:
                if self._running:
                    self.close_fcb(ls)
                else:
                    return

        



def main():
    from acsprism import rtdb_init
    from logger import setup_logger
    rtdb_init()
    rotating = Rotating(0, "B,A")
    setup_logger(rotating.logname)
    rotating.start()

if __name__ == "__main__":
    main()     
