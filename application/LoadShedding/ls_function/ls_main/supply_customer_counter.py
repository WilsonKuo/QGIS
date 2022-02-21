#!/bin/python3.6
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""

#System
import sys
import time
import os
import datetime
import logging
#Non-System
from acsprism import rtdb_init, RtdbAddress,RtdbPoint
from acstw.OracleInterface import OracleInterface

__author__ = 'Wilson Kuo'

logger = logging.getLogger(__name__)

USER = os.getenv("ORACLE_USER")
PSWD = os.getenv("ORACLE_PW")
TNS  = os.getenv("ORACLE_DBSTRING")
PRISMdb = OracleInterface(USER, PSWD, TNS)

class Supply_Customer_Counter:
    def __init__(self):
        self.progressbar = False
        self.ttu_downstream_meter_cnt_dict = dict()
        self.colorcode_name_dict = dict()
        self.feeder_downstream_ttu_cnt_dict = dict()
        self.feeder_downstream_meter_cnt_dict = dict()
        if self.progressbar:
            self.bar_length = 30
        self.setup_ttu_meter_dict()
        self.setup_feeder_dict()
    def setup_ttu_meter_dict(self):
        query = """
        SELECT TTU_NAME, COUNT(*) FROM TTU_METER GROUP BY TTU_NAME
        """
        logger.info("Start Creating Dictionary (TTU_DOWNSTREAM_METER_CNT_DICT), timestamp:{0}".format(datetime.datetime.now()))
        result = PRISMdb.ExecQuery(query)
        if self.progressbar:
            total = len(result) - 1
        for i, (ttu_name, cnt) in enumerate(result):
            if self.progressbar:
                percent = 100.0 * i / total
                sys.stdout.write('\r')
                sys.stdout.write("Completed: [{:{}}] {:>3}%".format('=' * int(percent / (100.0 / self.bar_length)), self.bar_length, int(percent)))
                sys.stdout.flush()
            self.ttu_downstream_meter_cnt_dict[ttu_name] = cnt
        outputmessage = "Finish Creating Dictionary (TTU_DOWNSTREAM_METER_CNT_DICT), timestamp:{0}".format(datetime.datetime.now())
        if self.progressbar:
            outputmessage = '\n' + outputmessage
        logger.info(outputmessage)
    def setup_feeder_dict(self):
        query = """
        SELECT COLORCODE, NAME FROM FEEDERPARAM ORDER BY COLORCODE
        """
        logger.info("Start Creating Dictionary (COLORCODE_NAME_DICT) (FEEDER_DOWNSTREAM_TTU_CNT_DICT) (FEEDER_DOWNSTREAM_METER_CNT_DICT), timestamp:{0}".format(datetime.datetime.now()))
        result = PRISMdb.ExecQuery(query)
        if self.progressbar:
            total = len(result) - 1
        for i, (colorcode, name) in enumerate(result):
            if self.progressbar:
                percent = 100.0 * i / total
                sys.stdout.write('\r')
                sys.stdout.write("Completed: [{:{}}] {:>3}%".format('=' * int(percent / (100.0 / self.bar_length)), self.bar_length, int(percent)))
                sys.stdout.flush()
            self.colorcode_name_dict[colorcode] = name
            self.feeder_downstream_ttu_cnt_dict[colorcode] = 0
            self.feeder_downstream_meter_cnt_dict[colorcode] = 0
        outputmessage = "Finish Creating Dictionary (COLORCODE_NAME_DICT) (FEEDER_DOWNSTREAM_TTU_CNT_DICT) (FEEDER_DOWNSTREAM_METER_CNT_DICT), timestamp:{0}".format(datetime.datetime.now())
        if self.progressbar:
            outputmessage = '\n' + outputmessage
        logger.info(outputmessage)
    def cnt_supply_customer(self):
        #Initializing value
        self.feeder_downstream_ttu_cnt_dict   = dict.fromkeys(self.feeder_downstream_ttu_cnt_dict, 0)
        self.feeder_downstream_meter_cnt_dict = dict.fromkeys(self.feeder_downstream_meter_cnt_dict, 0)
        
        query = """
        SELECT NAME, RTDBTYPE_LINE, STATION_LINE, CATEGORY_LINE, POINT_LINE, ATTRIBUTE_LINE FROM LINEXREF WHERE TABLENAME='LOADINPUT'
        """
        #logger.info("Start Reading RTDB, timestamp:{0}")
        result = PRISMdb.ExecQuery(query)
        if self.progressbar:
            total = len(result) - 1
        for i, (loadname, rtdbtype_line, station_line, category_line, point_line, attribute_line) in enumerate(result):
            if self.progressbar:
                percent = 100.0 * i / total
                sys.stdout.write('\r')
                sys.stdout.write("Completed: [{:{}}] {:>3}%".format('=' * int(percent / (100.0 / self.bar_length)), self.bar_length, int(percent)))
                sys.stdout.flush()
            try:
                addr_line = RtdbAddress(station_line, category_line, point_line, rtdbtype_line)
            except:
                #logger.info("Upstream of LOAD: {0} is not line, ignore this".format(loadname.ljust(19)))
                continue
            p_line = RtdbPoint(addr_line)
            colorcode = int(p_line.read_attr(attribute_line))
            if colorcode > 0:
                #No need to handle exception here because we started from TTU
                self.feeder_downstream_ttu_cnt_dict[colorcode] += 1
                try:
                    self.feeder_downstream_meter_cnt_dict[colorcode] += self.ttu_downstream_meter_cnt_dict[loadname]
                except:
                    #logger.info("#Meter in LOAD: {0} downstream is unknown, ignore this")
                    continue
        outputmessage = "Finish Reading RTDB"
        if self.progressbar:
            outputmessage = '\n' + outputmessage
        #logger.info(outputmessage)
        
        feeder_downstream_ttu_cnt_dict_decode   = dict()
        feeder_downstream_meter_cnt_dict_decode = dict()
        for colorcode in self.feeder_downstream_ttu_cnt_dict.keys():
            feeder_downstream_ttu_cnt_dict_decode[self.colorcode_name_dict[colorcode]] = self.feeder_downstream_ttu_cnt_dict[colorcode]
        for colorcode in self.feeder_downstream_meter_cnt_dict.keys():
            feeder_downstream_meter_cnt_dict_decode[self.colorcode_name_dict[colorcode]] = self.feeder_downstream_meter_cnt_dict[colorcode]
        return feeder_downstream_ttu_cnt_dict_decode, feeder_downstream_meter_cnt_dict_decode


def main():
    from logger import setup_logger
    setup_logger("supply_customer_counter")
    logger.info("Start Initializing RTDB, timestamp:{0}".format(datetime.datetime.now()))
    rtdb_init()
    logger.info("Finish Initializing RTDB, timestamp:{0}".format(datetime.datetime.now()))
    supply_customer_counter = Supply_Customer_Counter()
    b4_ls_fd_ttu_cnt_dict, b4_ls_fd_meter_cnt_dict = supply_customer_counter.cnt_supply_customer()
    time.sleep(3)
    af_ls_fd_ttu_cnt_dict, af_ls_fd_meter_cnt_dict = supply_customer_counter.cnt_supply_customer()
    for feeder in b4_ls_fd_ttu_cnt_dict.keys():
        if b4_ls_fd_ttu_cnt_dict[feeder] != af_ls_fd_ttu_cnt_dict[feeder]:
            logger.info("FEEDER:{0} Downstream Load from {1} -> {2}".format(feeder, b4_ls_fd_ttu_cnt_dict[feeder], af_ls_fd_ttu_cnt_dict[feeder]))
        if b4_ls_fd_meter_cnt_dict[feeder] != af_ls_fd_meter_cnt_dict[feeder]:
            logger.info("FEEDER:{0} Downstream Customer from {1} -> {2}".format(feeder, b4_ls_fd_meter_cnt_dict[feeder], af_ls_fd_meter_cnt_dict[feeder]))

if __name__ == "__main__":
    main()     