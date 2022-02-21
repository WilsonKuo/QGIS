#!/bin/python3.6
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
import os 
import time
import datetime
import logging

# Non-System
from supply_customer_counter import Supply_Customer_Counter
from acstw.OracleInterface import OracleInterface

__author__ = 'Wilson Kuo'


USER = os.getenv("ORACLE_USER")
PSWD = os.getenv("ORACLE_PW")
TNS  = os.getenv("ORACLE_DBSTRING")
PRISMdb = OracleInterface(USER, PSWD, TNS)

logger = logging.getLogger(__name__)


class ModeBase:
    def __init__(self, Amode):
        self.supply_customer_counter = Supply_Customer_Counter()
        self.whoami  = type(self).__name__
        self.logname = self.whoami + '-' + time.strftime("%m%d%Y%H%M%S")
        self.ls_app_log = "LS_APP_LOG"
        self.set_lsSet()
        self.set_cfg_dict()
        #self.logseq  = TABLE.get_log_seq().dataSet

        self._running = False
        self.processed_feeder = dict()

        self.Amode = Amode
        if self.Amode == 0:
            self.Amode_prefix = "[REAL TIME MODE] "
        else:
            self.Amode_prefix = "[DTS MODE] "
            self.dts_env_setup()

    @property
    def mode(self):
        raise NotImplementedError
    def set_lsSet(self):
        from acsprism import vde
        vde_file = vde.BaseVdeFile(read_only = False)
        query = "SELECT DISTINCT CTRLSTATION FROM  VIEW_LS_CFG WHERE CTRLSTATION IS NOT NULL"
        result = PRISMdb.ExecQuery(query)
        stationfepdict = dict()
        for record in result:
            vde_file.open_control(record[0])
            stationfepdict[record[0]] = vde_file.read(0).status_pair_code
        from record import LSRecord 
        columns  = ["GROUPNAME", "SUBSTATION", "FEEDER", "LSFEEDER_PRIORITY", "LSFDIDX", "CTRLSTATION", "CTRLRECORD"                                       ]
        columns += ["STATION_STASTATUS", "CATEGORY_STASTATUS", "POINT_STASTATUS", "RTDBTYPE_STASTATUS", "ATTRIBUTE_STASTATUS"                              ]
        columns += ["STATION_LSGROUPLOCKFLAG", "CATEGORY_LSGROUPLOCKFLAG", "POINT_LSGROUPLOCKFLAG", "RTDBTYPE_LSGROUPLOCKFLAG", "ATTRIBUTE_LSGROUPLOCKFLAG"]
        columns += ["STATION_UPLINECOLORCODE", "CATEGORY_UPLINECOLORCODE", "POINT_UPLINECOLORCODE", "RTDBTYPE_UPLINECOLORCODE", "ATTRIBUTE_UPLINECOLORCODE"]
        columns += ["STATION_LSACT", "CATEGORY_LSACT", "POINT_LSACT", "RTDBTYPE_LSACT", "ATTRIBUTE_LSACT"                                                  ]
        columns += ["STATION_LSLOCKFLAG", "CATEGORY_LSLOCKFLAG", "POINT_LSLOCKFLAG", "RTDBTYPE_LSLOCKFLAG", "ATTRIBUTE_LSLOCKFLAG"                                   ]
        columns += ["STATION_PA", "CATEGORY_PA", "POINT_PA", "RTDBTYPE_PA", "ATTRIBUTE_PA"                                                                 ]
        columns += ["STATION_PB", "CATEGORY_PB", "POINT_PB", "RTDBTYPE_PB", "ATTRIBUTE_PB"                                                                 ]
        columns += ["STATION_PC", "CATEGORY_PC", "POINT_PC", "RTDBTYPE_PC", "ATTRIBUTE_PC"                                                                 ]
        query   = "SELECT {0} FROM  VIEW_LS_CFG WHERE FDTYPE = 0 ORDER BY LSFEEDER_PRIORITY".format(",".join(columns))
        result  = PRISMdb.ExecQuery(query)
        result  = [ dict(zip(columns, row)) for row in result ]
        self.lsSet = list()
        for record in result:
            if record['CTRLSTATION'] in stationfepdict.keys():
                record.update({'FEP': stationfepdict[record['CTRLSTATION']]})
            else:
                record.update({'FEP': None})
            self.lsSet.append(LSRecord(record))

    def set_ufDict(self):
        from record import UFRecord
        columns  = ["NAME", "COLORCODE"]  
        columns += ["STATION_STASTATUS", "CATEGORY_STASTATUS", "POINT_STASTATUS", "RTDBTYPE_STASTATUS", "ATTRIBUTE_STASTATUS"]
        columns += ["STATION_LOCKFLAG", "CATEGORY_LOCKFLAG", "POINT_LOCKFLAG", "RTDBTYPE_LOCKFLAG", "ATTRIBUTE_LOCKFLAG"     ]
        query    = "SELECT {0} FROM  VIEW_UF_CFG".format(",".join(columns))
        result   = PRISMdb.ExecQuery(query)
        result   = [ dict(zip(columns, row)) for row in result ]

        self.ufSet = list()
        for record in result:
            self.ufSet.append(UFRecord(record))
        


    def set_cfg_dict(self):
        columns = ["NAME", "VALUE" ]
        query   = "SELECT {0} FROM LS_CONFIGURATION".format(",".join(columns))
        result  = PRISMdb.ExecQuery(query)
        result  = { row[0]:row[1] for row in result }
        self.fd_open_delay     = result['FD_OPEN_DELAY']
        self.fd_close_delay    = result['FD_CLOSE_DELAY']
        # self.fd_open_delay     = 0.1
        # self.fd_close_delay    = 0.1
        self.check_p_interval  = result['CHECK_P_INTERVAL']
        self.use_reduce        = result['USE_REDUCE']
        self.uf_check_interval = result['UF_CHECK_INTERVAL']
        self.restore_last_area = result['RESTORE_LAST_AREA']
        self.uf_check_if_fcbopen_work_interval = result['UF_CHECK_IF_FCBOPEN_WORK_INTERVAL']
    
    def dts_env_setup(self):
        from record import LSRecord_DTS
        # CREATE SEQUENCE SEQ_LSSID INCREMENT BY 1 START WITH 1 NOMAXVALUE NOMINVALUE 
        # DROP TABLE LS_APP_LOG;
        # CREATE TABLE LS_APP_LOG
        # (
        #     SID         NUMBER,
        #     OBJ_TYPE    VARCHAR2(19),
        #     NAME        VARCHAR2(19),
        #     PARAMETER   VARCHAR2(19),
        #     VALUE       NUMBER,
        #     TIMESTAMP   TIMESTAMP,
        #     ARCHIVED    NUMBER(1)
        # );
        tmp_lsSet = list()

        query   = "SELECT SEQ_LSSID.NEXTVAL FROM DUAL"
        sid  = PRISMdb.ExecQuery(query)[0][0]
        template_array = list()
        for ls in self.lsSet:
            template_array.append([sid, "FEEDER", ls.feeder, "PA", ls.pa, datetime.datetime.now(), 0])
            template_array.append([sid, "FEEDER", ls.feeder, "PB", ls.pb, datetime.datetime.now(), 0])
            template_array.append([sid, "FEEDER", ls.feeder, "PC", ls.pc, datetime.datetime.now(), 0])
            template_array.append([sid, "FEEDER", ls.feeder, "LSACT", ls.lsact, datetime.datetime.now(), 0])
            template_array.append([sid, "FEEDER", ls.feeder, "LSGROUPLOCKFLAG", ls.lsgrouplockflag, datetime.datetime.now(), 0])
            template_array.append([sid, "FEEDER", ls.feeder, "LSLOCKFLAG", ls.lslockflag, datetime.datetime.now(), 0])
            tmp_lsSet.append(LSRecord_DTS(ls))
        self.lsSet = tmp_lsSet
        del tmp_lsSet


        print('template...')
        return
        #"UF"!!!!!!!!!!!!!!!
        colStr = 'SID,OBJ_TYPE,NAME,PARAMETER,VALUE,TIMESTAMP,ARCHIVED'
        valPlaceholder = ":0,:1,:2,:3,:4,:5,:6"
        insSql = "insert /* array */ into %s (%s) values (%s)" % (self.ls_app_log, colStr, valPlaceholder)
        PRISMdb.InsertArray(insSql, template_array)

    @property
    def wholepsum(self):
        psum = 0
        for ls in self.lsSet:
            psum += ls.p
        return psum

    def open_fcb(self, ls):
        feederinfo = self.Amode_prefix + "FEEDER:{0} ".format(ls.feeder)
        if ls.stastatus == 1:
            if ls.lsgrouplockflag == 0:
                if ls.lslockflag == 0:
                    if ls.lsact == 0:
                        if ls.p > 0:
                            if ls.control:
                                for i in (1, 2):
                                    logger.info("{0}--->> Try {1} time(s) <<<---".format(self.Amode_prefix, i))
                                    ls.control = 0
                                    logger.info(feederinfo + "Send Control Instruction, Waiting control feedback")
                                    time.sleep(self.fd_open_delay)
                                    logger.info(feederinfo + "Check feedback")
                                    if ls.stastatus == 0:
                                        logger.info(feederinfo + "Open Successfully")
                                        ls.lsact = self.mode
                                        self.processed_feeder[ls.feeder] = True
                                        return True
                                    else:
                                        logger.info(feederinfo + "Open Unsuccessfully")
                                        ls.lsact = -13
                            else:
                                logger.info(feederinfo + "No Control Point")
                                ls.lsact = -11
                        else:
                            logger.info(feederinfo + "P Is Zero, Ignore This")
                            ls.lsact = -9
                    else:
                        logger.info(feederinfo + "Control By Other Job, Ignore This")
                        ls.lsact = -7
                else:
                    logger.info(feederinfo + "Feeder Disable")
                    ls.lsact = -5
            else:
                logger.info(feederinfo + "Group Disable")
                ls.lsact = -3 
        else:
            logger.info(feederinfo + "Already In Open Status, Ignore This")
            ls.lsact = -1
            
    def close_fcb(self, ls):
        feederinfo = self.Amode_prefix + "FEEDER:{0} ".format(ls.feeder)
        if ls.stastatus == 0:
            if ls.lsgrouplockflag == 0:
                if ls.lslockflag == 0:
                    if ls.lsact == self.mode:
                        if ls.control:
                            for i in (1, 2):
                                logger.info("{0}--->> Try {1} time(s) <<<---".format(self.Amode_prefix, i))
                                ls.control = 1
                                logger.info(feederinfo + "Send Control, Waiting control feedback")
                                time.sleep(self.fd_close_delay)
                                logger.info(feederinfo + "Check feedback")
                                if ls.stastatus == 1:
                                    logger.info(feederinfo + "Close Successfully")
                                    ls.lsact = self.mode
                                    return True
                                else:
                                    logger.info(feederinfo + "Close Unsuccessfully")
                                    ls.lsact = -10
                        else:
                            logger.info(feederinfo + "No Control Point")
                    else:
                        logger.info(feederinfo + "Control By Other Job Or Some Problem, Ignore This")
                        ls.lsact = -8
                else:
                    logger.info(feederinfo + "Disable")
                    ls.lsact = -6
            else:
                logger.info(feederinfo + "Group Disable")
                ls.lsact = -4
        else:
            if ls.lsact < 0:
                logger.info(feederinfo + "Opened Unsuccessfully In Previous Operation, Ignore This")
            else:
                logger.info(feederinfo + "Already In Close Status, No Need To Restore This")
            ls.lsact = -2
    
    def job(self):
        raise NotImplementedError
    def start(self):
        cntchange = 0
        logger.info(self.Amode_prefix + "Start Reading RTDB For Memorizing Transformer # Dictionary and Meter # Dictionary Before Running Load Shedding")
        b4_ls_fd_ttu_cnt_dict, b4_ls_fd_meter_cnt_dict = self.supply_customer_counter.cnt_supply_customer()
        logger.info(self.Amode_prefix + "Finish Reading RTDB For Memorizing Transformer # Dictionary and Meter # Dictionary Before Running Load Shedding")
        self._running = True
        self.job()
        if self.Amode == 0:
            logger.info(self.Amode_prefix + "Start Reading RTDB For Comparing Transformer # Dictionary and Meter # Dictionary After Running Load Shedding")
            af_ls_fd_ttu_cnt_dict, af_ls_fd_meter_cnt_dict = self.supply_customer_counter.cnt_supply_customer()
            logger.info(self.Amode_prefix + "Finish Reading RTDB For Comparing Transformer # Dictionary and Meter # Dictionary After Running Load Shedding")
            for feeder in b4_ls_fd_ttu_cnt_dict.keys():
                if b4_ls_fd_ttu_cnt_dict[feeder] != af_ls_fd_ttu_cnt_dict[feeder] and feeder in self.processed_feeder.keys():
                    cntchange += 1
                    logger.info(self.Amode_prefix + "FEEDER:{0} Downstream Load from {1} -> {2}".format(feeder, b4_ls_fd_ttu_cnt_dict[feeder], af_ls_fd_ttu_cnt_dict[feeder]))
                if b4_ls_fd_meter_cnt_dict[feeder] != af_ls_fd_meter_cnt_dict[feeder] and feeder in self.processed_feeder.keys():
                    logger.info(self.Amode_prefix + "FEEDER:{0} Downstream Customer from {1} -> {2}".format(feeder, b4_ls_fd_meter_cnt_dict[feeder], af_ls_fd_meter_cnt_dict[feeder]))
        else:
            for feeder in self.processed_feeder.keys():
                if b4_ls_fd_ttu_cnt_dict != 0:
                    cntchange += 1
                    logger.info(self.Amode_prefix + "FEEDER:{0} Downstream Load from {1} -> 0".format(feeder, b4_ls_fd_ttu_cnt_dict[feeder]))
                if b4_ls_fd_meter_cnt_dict != 0:
                    logger.info(self.Amode_prefix + "FEEDER:{0} Downstream Customer from {1} -> 0".format(feeder, b4_ls_fd_meter_cnt_dict[feeder], 0))
        if cntchange == 0:
            logger.info(self.Amode_prefix + "No Customer got affected")

    def stop(self):
        self._running = False

def main():
    from logger import setup_logger
    from acsprism import rtdb_init
    rtdb_init()

    class Inheritance(ModeBase):
        def __init__(self):
            super(Inheritance, self).__init__()

    i = Inheritance()
    setup_logger(i.logname)


if __name__ == "__main__":
    main()     
