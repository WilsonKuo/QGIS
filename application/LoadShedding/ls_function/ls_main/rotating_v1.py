# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""

# System
import time
import datetime
import logging

# Non-System
from loadshedding.record import LSRecord
from loadshedding.tables import LS_TABLE_SCHEMA as TABLE
from loadshedding.common import Const
from loadshedding.exporttable import exportcsv as CSVWRITER

__author__ = 'Wilson Kuo'


logger = logging.getLogger(__name__)


class Rotating:
    def __init__(self, group, demand):
        self.fname = "rotating" + '-' + time.strftime("%m%d%Y%H%M%S")
        self.cfgDict = TABLE.get_config_data().dataSet
        self.dataSet = TABLE.get_view_data().dataSet
        self.const = Const()
        self.log_seq = TABLE.get_log_seq().dataSet


        self.reducemode = True if self.cfgDict['USE_REDUCE'] == 1 else False
        self.fd_open_delay = self.cfgDict['FD_OPEN_DELAY']
        self.fd_close_delay = self.cfgDict['FD_CLOSE_DELAY']
        self.check_p_interval = self.cfgDict['CHECK_P_INTERVAL']
        self.check_area_interval = self.cfgDict['CHECK_AREA_INTERVAL']
        self.validate_load_capability = True if self.cfgDict['VALIDATE_LOAD_CAPABILITY'] == 1 else False
        self.rotating_mode = self.cfgDict['ROTATING_MODE']


        
        self.mode = 2
        self.group = group.replace("-",",").split(",")
        self.areas = group.split("-")
        self.demand = demand

        self.lsSet = list()
        for record in self.dataSet:
            self.lsSet.append(LSRecord(record))

        self._running = False
        self.start_time = datetime.datetime.now()
        self.time_call_times = 0
        self.valid_ls = list()
        self.invalid_ls = list()
        self.area_valid_ls = list()
        self.wholepsumlist = list()
        #precord memorize p value before open feeder breaker
        self.precord = dict()
        self.finish_time_list = list()
        self.completed_time = datetime.datetime.now() + datetime.timedelta(minutes = 5)
        # To memorize processing elements, we need openlist list and restorelist list
        self.processing_valid_ls = {'openlist':list(), 'restorelist':list()}


        self.check_valid_ls_bygroup()
        self.set_area()
        self.get_wholepsum_ls()

    def check_valid_ls_bygroup(self):
        for ls in self.lsSet:
            if ls.systemlockflag == 0  and ls.groupname in self.group:
                #To exclude objects which don't have remote point or p point
                if ls.p is not None:
                    self.valid_ls.append(ls)
                else:
                    self.invalid_ls.append(ls)    
                    ls.act = - 2
            else:
                self.invalid_ls.append(ls)    
    def get_wholepsum_ls(self):
        for ls in self.lsSet:
            if ls.groupname in self.group:
                if ls.p is not None:
                    self.wholepsumlist.append(ls)
    def mutex(self, enable):
        for ls in self.lsSet:
            if ls.groupname in self.group:
                if enable:
                    ls.systemlockflag = 1
                else:
                    ls.systemlockflag = 0
    def set_area(self):
        #print(self.valid_ls)
        for row, area in enumerate(self.areas):
            self.area_valid_ls.append(list())
            for group in area.split(","):
                for ls in self.valid_ls:
                    if ls.groupname == group:
                        self.area_valid_ls[row].append(ls)
    @property
    def wholepsum(self):
        wholepsum = 0
        for ls in self.wholepsumlist:
            wholepsum += ls.p
        return wholepsum
    @property
    def finish_time(self):
        self.time_call_times += 1
        return self.start_time + datetime.timedelta(seconds = self.check_area_interval * self.time_call_times)
    def open_fcb(self, ls):
        if ls.lslockflag == 0:
            if ls.status_f == 1:
                ls.status_f = 0
                ls.act = self.mode
                #ls.act_open_time = datetime.datetime.now()
                self.precord[ls.feeder] = (ls.pa, ls.pb, ls.pc)
                ls.pa = 0
                ls.pb = 0
                ls.pc = 0
                TABLE.insert_event(self.log_seq, ls.feeder, "open feeder successfully ", datetime.datetime.now())
                time.sleep(self.fd_open_delay)
                return True
            else:
                ls.act = -1
                print('=============================={0}'.format(ls.status_f))
                logger.info("feeder:{0} is open, ignore this, set act = -1".format(ls.feeder))
                TABLE.insert_event(self.log_seq, ls.feeder, "feeder is open status! ignore this feeder", datetime.datetime.now())
                time.sleep(self.fd_open_delay)
                return False
        else:
            ls.act = -3
            logger.info("feeder:{0} is disable, ignore this, set act = -3".format(ls.feeder))
            TABLE.insert_event(self.log_seq, ls.feeder, "feeder is disable! ignore this feeder", datetime.datetime.now())
            time.sleep(self.fd_open_delay)
            return False
    def close_fcb(self, ls):
        if ls.act == 2 and ls.lslockflag == 0:
            ls.pa, ls.pb, ls.pc = self.precord[ls.feeder]
            time.sleep(self.fd_close_delay)
            #ls.act_close_time = datetime.datetime.now()
            TABLE.insert_event(self.log_seq, ls.feeder, "close feeder successfully", datetime.datetime.now())

            #restore feeder to close state
            ls.status_f = 1
    def validate_area_capability(self):
        wholepsum = self.wholepsum
        #!!!Don't change threshold value!!!, we need to keep it.
        if self.reducemode:
            self.const.threshold = wholepsum - self.demand
        else:
            self.const.threshold = self.demand

        reduce = wholepsum - self.const.threshold
        #To prevent area is not able to hanlde demand
        psumlist = list()

        for als in self.area_valid_ls:
            psum = 0
            for vls in als:
                #We can only control status is close feeder breaker
                if vls.status_f == 1:
                    psum += vls.p
                    
            psumlist.append(psum)

        for psum in psumlist:
            if psum < reduce:
                if self.validate_load_capability == 1:
                    logger.info("Couldn't meet:{0} because psum is {1}, exit".format(reduce, psum))
                    self.mutex(False)
                    return False
                else:
                    logger.info("Couldn't meet:{0} because psum is {1}, do anyway".format(reduce, psum))
                    return True
        return True
    def check_p_periodically(self, candidate_ls, finish_time):
        logger.info("=====================check if p is over demand every 5 seconds=====================")        

        candidate_cnt = len(candidate_ls)
        index_candidate = 0

        tmp_check_p_interval = self.check_p_interval
        
        check = True

        while check:
            if self._running:
                tmp_check_p_interval -= 1
                if tmp_check_p_interval == 0:
                    tmp_check_p_interval = self.check_p_interval
                    if self.wholepsum > self.const.threshold:
                        if index_candidate > candidate_cnt - 1:
                            logger.info("run out of candidate, do nothing")
                        else:
                            if self.open_fcb(candidate_ls[index_candidate]):
                                self.processing_valid_ls['openlist'].append(candidate_ls[index_candidate])
                                index_candidate += 1
                                logger.info("wholepsum:{0} is over threshold:{1} now, use candidate".format(self.wholepsum, self.const.threshold))
                                logger.info("open {0} to reach threshold, get new p :{1}".format(candidate_ls[index_candidate].feeder, candidate_ls[index_candidate].p))
        
                    else:
                        logger.info("wholepsum:{0} is not over threshold:{1}, no need to use candidate".format(self.wholepsum, self.const.threshold))
                time.sleep(1)
                logger.debug("now:{0} finish time:{1}".format(datetime.datetime.now(), finish_time))
                if datetime.datetime.now() >= finish_time:
                    check = False
                    logger.info("Ready to next area")
            else:
                CSVWRITER(self.fname, self.log_seq)
                self.mutex(False)
                return 
    def mode0(self):
        # Most of the times it is easier (and cheaper) to make the first iteration the special case instead of the last one:
        first = True
        # to show info meet demand once
        first2 = True
        # For handling p value is not enough suddenly
        candidate_ls = list()

        self._running = True

        while self._running:
            for row, als in enumerate(self.area_valid_ls):
                psum = 0
                for vls in als:
                    psum += vls.p
                logger.info("=====================this area {0} psum:{1}=====================".format(self.areas[row], psum))
                #first element
                if first:
                    first = False
                    for ls in als:
                        #keep getting p until wholepsum is less than threshold
                        if self._running:
                            if self.wholepsum > self.const.threshold:
                                if self.open_fcb(ls):
                                    self.processing_valid_ls['openlist'].append(ls)
                                    logger.info("openlist {0}".format(ls.feeder))
                                    time.sleep(self.fd_open_delay)
                                    logger.info("right now wholepsum:{0}, target threshold:{1}".format(self.wholepsum, self.const.threshold))

                            else:
                                if first2:
                                    first2 = False
                                    logger.info("=====================Meet demand, first area load shedding ok=====================")
                                candidate_ls.append(ls)
                        else:
                            CSVWRITER(self.fname, self.log_seq)
                            self.mutex(False)
                            return 

                    self.check_p_periodically(candidate_ls, self.finish_time)
                    
                else:
                    index_restore = 0
                    index_open = 0
                    # copy function to prevent shallow copy
                    # move openlist to restorelist, the feeders which are opened in last iteration, they need to be restored in this iteration
                    self.processing_valid_ls['restorelist'] = self.processing_valid_ls['openlist'].copy()
                    # we need empty openlist for this iteration
                    self.processing_valid_ls['openlist'] *= 0
                    # take # ls in restorelst as key because having to restore all ls which is opend in last iteration
                    self.processing_valid_ls_restorelist_cnt = len(self.processing_valid_ls['restorelist'])
                    # empty candidate_ls for this iteration
                    candidate_ls *= 0

                    area_valid_ls_cnt = len(self.area_valid_ls[row])
                    # A1 close B1 openlist B2 openlist A2 close...
                    while index_restore < self.processing_valid_ls_restorelist_cnt:
                        #Let wholepsum value less than threshold
                        while self.wholepsum + sum(self.precord[self.processing_valid_ls['restorelist'][index_restore].feeder]) > self.const.threshold :
                            if self._running:
                                if index_open > area_valid_ls_cnt - 1:
                                    logger.info("stuck here, please stop the program manually!!!")
                                    time.sleep(self.check_p_interval)
                                else:
                                    if self.open_fcb(self.area_valid_ls[row][index_open]):
                                        self.processing_valid_ls['openlist'].append(self.area_valid_ls[row][index_open])
                                        logger.info("right now wholepsum:{0}, target threshold:{1}".format(self.wholepsum, self.const.threshold))

                                    index_open += 1
                            else:
                                CSVWRITER(self.fname, self.log_seq)
                                self.mutex(False)
                                return 
                        if self._running:
                            self.close_fcb(self.processing_valid_ls['restorelist'][index_restore])
                            #Release p
                            logger.info("right now wholepsum = {0}".format(self.wholepsum))

                            index_restore += 1
                        else:
                            CSVWRITER(self.fname, self.log_seq)
                            self.mutex(False)
                            return         

                    # append the rest of element to candidate_ls
                    for idx, ls in enumerate(als):
                        if idx > index_open:
                            candidate_ls.append(ls)

                    self.check_p_periodically(candidate_ls, self.finish_time)

        CSVWRITER(self.fname, self.log_seq)
        self.mutex(False)
        # logger.info("=====================last area=====================")

        # #Get p until last area ok
        # for dls in self.processing_valid_ls['openlist']:
        #     self.close_fcb(dls)
        #     logger.info("right now wholepsum = {0}".format(self.wholepsum))

    
        # self.mutex(False)
    # Open Next Group First 
    # Run periodically
    def mode1(self):
        
        first = True
        self._running = True
        while self._running:   
            for row, als in enumerate(self.area_valid_ls):
                if first:
                    first = False
                    for ls in als:
                        if self._running:
                            self.processing_valid_ls['openlist'].append(ls)
                            self.open_fcb(ls)
                else:
                    # copy function to prevent shallow copy
                    # move openlist to restorelist, the feeders which are opened in last iteration, they need to be restored in this iteration
                    self.processing_valid_ls['restorelist'] = self.processing_valid_ls['openlist'].copy()
                    # we need empty openlist for this iteration
                    self.processing_valid_ls['openlist'] *= 0
                    
                    print('Waiting for next area')
                    tmp_check_area_interval = self.check_area_interval
                    while True:
                        tmp_check_area_interval -= 1
                        print('Wait {} '.format(tmp_check_area_interval))
                        if self._running:
                            if tmp_check_area_interval == 0:
                                break
                        else:
                            CSVWRITER(self.fname, self.log_seq)
                            self.mutex(False)
                            return
                        time.sleep(1)
                        
                    for ls in als:
                        if self._running:
                            self.processing_valid_ls['openlist'].append(ls)
                            self.open_fcb(ls)
                    # print('Waiting for next area')
                    # tmp_check_area_interval = self.check_area_interval
                    # while True:
                    #     tmp_check_area_interval -= 1
                    #     print('Wait {} '.format(tmp_check_area_interval))
                    #     if self._running:
                    #         if tmp_check_area_interval == 0:
                    #             break
                    #     else:
                    #         CSVWRITER(self.fname, self.log_seq)
                    #         self.mutex(False)
                    #         return
                    #     time.sleep(1)

                    for rls in self.processing_valid_ls['restorelist']:
                        if self._running:
                            self.close_fcb(rls)
        CSVWRITER(self.fname, self.log_seq)
        self.mutex(False)

    # Open Next Group First 
    # Not running periodically
    def mode2(self):
        first = True
        self._running = True

        for row, als in enumerate(self.area_valid_ls):
            if first:
                first = False
                for ls in als:
                    if self._running:
                        self.processing_valid_ls['openlist'].append(ls)
                        self.open_fcb(ls)
            else:
                # copy function to prevent shallow copy
                # move openlist to restorelist, the feeders which are opened in last iteration, they need to be restored in this iteration
                self.processing_valid_ls['restorelist'] = self.processing_valid_ls['openlist'].copy()
                # we need empty openlist for this iteration
                self.processing_valid_ls['openlist'] *= 0
                
                print('Waiting for next area')
                tmp_check_area_interval = self.check_area_interval
                while True:
                    tmp_check_area_interval -= 1
                    print('Wait {} '.format(tmp_check_area_interval))
                    if self._running:
                        if tmp_check_area_interval == 0:
                            break
                    else:
                        CSVWRITER(self.fname, self.log_seq)
                        self.mutex(False)
                        return
                    time.sleep(1)

                for ls in als:
                    if self._running:
                        self.processing_valid_ls['openlist'].append(ls)
                        self.open_fcb(ls)
                        
                for rls in self.processing_valid_ls['restorelist']:
                    if self._running:
                        self.close_fcb(rls)

                    
        print('Waiting for last area restore')
        tmp_check_area_interval = self.check_area_interval
        while True:
            tmp_check_area_interval -= 1
            print('Wait {} '.format(tmp_check_area_interval))
            if self._running:
                if tmp_check_area_interval == 0:
                    break
            else:
                CSVWRITER(self.fname, self.log_seq)
                self.mutex(False)
                return
            time.sleep(1)
        #Last Area
        for rls in self.processing_valid_ls['openlist']:
            if self._running:
                self.close_fcb(rls)

        CSVWRITER(self.fname, self.log_seq)
        self.mutex(False)                    

                
                
    def start(self):
        self.mutex(True)
        logger.info("=====================Start to process area {0}=====================".format(self.areas))

        if not self.validate_area_capability():
            return False


        if self.rotating_mode == 0:
            self.mode0()
        elif self.rotating_mode == 1:
            self.mode1()
        elif self.rotating_mode == 2:
            self.mode2()
        else:
            raise NotImplementedError("rotating_mode {0} not implemented".format(self.rotating_mode))
    def stop(self):
        print('log')
        CSVWRITER(self.fname, self.log_seq)
        self._running = False
        self.mutex(False)

def main():
    from acsprism import rtdb_init
    rtdb_init()

    group = "A-B"
    demand = 4000
    rotating = Rotating(group, demand)
    rotating.start()
    


if __name__ == "__main__":
    main()  
