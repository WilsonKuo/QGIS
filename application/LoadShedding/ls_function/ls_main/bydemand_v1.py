# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
import time
import logging
import datetime

# Non-System
from loadshedding.record import LSRecord
from loadshedding.tables import LS_TABLE_SCHEMA as TABLE
from loadshedding.common import Const
from loadshedding.exporttable import exportcsv as CSVWRITER

__author__ = 'Wilson Kuo'

logger = logging.getLogger(__name__)


class Bydemand:
    def __init__(self, group, demand):
        self.fname = "bydemand" + '-' + time.strftime("%m%d%Y%H%M%S")
        self.cfgDict = TABLE.get_config_data().dataSet
        self.dataSet = TABLE.get_view_data().dataSet
        self.log_seq = TABLE.get_log_seq().dataSet
        self.const = Const()

        self.fd_open_delay    = self.cfgDict['FD_OPEN_DELAY']
        self.check_p_interval = self.cfgDict['CHECK_P_INTERVAL']
        self.reducemode = True if self.cfgDict['USE_REDUCE'] == 1 else False
        self.validate_load_capability = True if self.cfgDict['VALIDATE_LOAD_CAPABILITY'] == 1 else False
        
        self.mname = "Bydemand"
        self.mode = 1
        self.group = group.split(",")
        self.demand = demand

        self.lsSet = list()
        for record in self.dataSet:
            self.lsSet.append(LSRecord(record))
        
        self._running = False
        self.valid_ls = list()
        self.invalid_ls = list()
        self.wholepsumlist = list()

        self.get_wholepsum_ls()
        self.check_valid_ls_bygroup()

    def check_valid_ls_bygroup(self):
        for ls in self.lsSet:
            if ls.systemlockflag == 0  and ls.groupname in self.group:
                #To exclude objects which don't have remote point or p point
                if ls.p > 0:
                    self.valid_ls.append(ls)
                else:
                    self.invalid_ls.append(ls)    
                    ls.act = - 2
            else:
                self.invalid_ls.append(ls)
    def get_wholepsum_ls(self):
        for ls in self.lsSet:
            if ls.groupname in self.group:
                if ls.p > 0:
                    self.wholepsumlist.append(ls)

    def mutex(self, enable):
        for ls in self.lsSet:
            if ls.groupname in self.group:
                if enable:
                    ls.systemlockflag = 1
                else:
                    ls.systemlockflag = 0

    @property
    def wholepsum(self):
        wholepsum = 0
        for ls in self.wholepsumlist:
            wholepsum += ls.p
        return wholepsum

    def validate_group_capability(self):
        wholepsum = self.wholepsum
        #!!!Don't change threshold value!!!, we need to keep it.
        if self.reducemode:
            self.const.threshold = wholepsum - self.demand
        else:
            self.const.threshold = self.demand

        reduce = wholepsum - self.const.threshold
        #To prevent group is not able to hanlde demand
        psum = 0

        for vls in self.valid_ls:
            if vls.status_f == 1:
                psum += vls.p      

        if psum < reduce:
            if self.validate_load_capability:
                logger.info("Couldn't meet:{0} because psum is {1}, exit".format(reduce, psum))
                self.mutex(False)
                return False
            else:
                logger.info("Couldn't meet:{0} because psum is {1}, do anyway".format(reduce, psum))
                return True
        return True

    def open_fcb(self, ls):
        if ls.status_f == 1:
            if ls.lslockflag == 0:
                ls.status_f = 0
                ls.act = self.mode
                ls.act_open_time = datetime.datetime.now()
                ls.pa = 0
                ls.pb = 0
                ls.pc = 0
                TABLE.insert_event(self.log_seq, ls.feeder, "open feeder successfully", datetime.datetime.now())
                time.sleep(self.fd_open_delay)
                return True
            else:
                ls.act = -3
                TABLE.insert_event(self.log_seq, ls.feeder, "feeder is disable! ignore this feeder ", datetime.datetime.now())
                time.sleep(self.fd_open_delay)
                return False
        else:
            ls.act = -1
            logger.info("feeder:{0} is open, ignore this, set act = -1".format(ls.feeder))
            TABLE.insert_event(self.log_seq, ls.feeder, "feeder is open status! ignore this feeder ", datetime.datetime.now())
            time.sleep(self.fd_open_delay)
            return False

    def start(self):
        self.mutex(True)

        logger.info("=====================Start to process group {0}=====================".format(",".join(self.group)))
        
        if not self.validate_group_capability():
            return False
        self._running = True
        index_processing = 0
        valid_ls_cnt = len(self.valid_ls)

        while self.wholepsum > self.const.threshold:
            if self._running:
                self.open_fcb(self.valid_ls[index_processing])

                index_processing += 1                    
        logger.info('Meet Demand, Detecting wholepsum periodically!')



        tmp_check_p_interval = self.check_p_interval

        while self._running:
            tmp_check_p_interval -= 1
            if tmp_check_p_interval == 0:
                tmp_check_p_interval = self.check_p_interval
                if self.wholepsum > self.const.threshold:
                    if  index_processing > valid_ls_cnt - 1:
                        logger.info("run out of candidate, do nothing")
                    else:
                        logger.info("wholepsum:{0} is over threshold:{1}, need to use candidate".format(self.wholepsum, self.const.threshold))
                        self.open_fcb(self.valid_ls[index_processing])
                        index_processing += 1
                else:
                    logger.info("wholepsum:{0} is not over threshold:{1}, no need to use candidate".format(self.wholepsum, self.const.threshold))
            time.sleep(1)
                


        CSVWRITER(self.fname, self.log_seq)
        self.mutex(False)
        del self
    def stop(self):
        self._running = False
        self.mutex(False)
            
        

        
def main():
    from acsprism import rtdb_init

    rtdb_init()
    
    group = "A,B"
    demand = 800

    bydemand = Bydemand(group, demand)
    bydemand.start()


if __name__ == "__main__":
    main()     
