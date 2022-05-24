#!/bin/python3.6
# System
import os
import sys
import time
import datetime
# Non-system
from tables       import TTU_TABLE_SCHEMA as TABLE
from ttuinfo      import TTUInfo
from feederinfo   import FEEDERInfo
from acsprism     import rtdb_init
from acstw.OracleInterface import OracleInterface


USER = os.getenv("ORACLE_USER")
PSWD = os.getenv("ORACLE_PW")
TNS  = os.getenv("ORACLE_DBSTRING")
PRISMdb = OracleInterface(USER, PSWD, TNS)

def main():
    update_rate = 20
    tmp_update_rate = update_rate

    rtdb_init()
    print("Start Creating Dictionary (COLORCODE_NAME_DICT) (FEEDER_DOWNSTREAM_TTU_CNT_DICT) (FEEDER_DOWNSTREAM_METER_CNT_DICT), timestamp:{0}".format(datetime.datetime.now()))
    feederinfoDict = dict()
    feederinfoSet = TABLE.get_colorcode().resultSet
    for feederinfo in feederinfoSet:
        feederinfoDict[feederinfo['COLORCODE']] = FEEDERInfo(feederinfo)
    print("Finish Creating Dictionary (COLORCODE_NAME_DICT) (FEEDER_DOWNSTREAM_TTU_CNT_DICT) (FEEDER_DOWNSTREAM_METER_CNT_DICT), timestamp:{0}".format(datetime.datetime.now()))

    print('Start Creating LIST (TTUINFO)')
    ttuinfoSet   = TABLE.get_ttu_info().resultSet
    ttuinfoList  = list()
    for ttuinfo in ttuinfoSet:
        ttuinfoList.append(TTUInfo(ttuinfo))
    print('Finish Creating LIST (TTUINFO)')


    while True:
        if tmp_update_rate == 0:
            sys.stdout.write('\rUpdate meterdataSet in {0} second(s)'.format(tmp_update_rate))
            sys.stdout.flush()
            for key in feederinfoDict:
                feederinfoDict[key].reset_val()
            for ttu in ttuinfoList:
                if ttu.p:
                    feederinfoDict[ttu.feeder].p_sum += ttu.p
            

            arr = list()
            for key in feederinfoDict:
                arr.append([key, feederinfoDict[key].p_sum, feederinfoDict[key].q_sum, datetime.datetime.now().hour])
 
            colStr = 'COLORCODE,P,Q,TIME'
            valPlaceholder = ":0,:1,:2,:3"
            insSql = "insert /* array */ into %s (%s) values (%s)" % ('LOADHDA', colStr, valPlaceholder)
            PRISMdb.InsertArray(insSql,arr)
            print('\nInsert data successfully!')
            tmp_update_rate = update_rate
        else:
            sys.stdout.write('\rUpdate feederPQsum in {0} second(s)'.format(tmp_update_rate))
            sys.stdout.flush()
        


        time.sleep(1)
        tmp_update_rate -= 1

if __name__ == "__main__":
    main()
