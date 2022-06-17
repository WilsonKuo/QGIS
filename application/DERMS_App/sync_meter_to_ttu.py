#!/bin/python3.6

# System
import os
import sys
import time
import threading
from functools import reduce  # Required in Python 3
from multiprocessing.managers import SyncManager
import socket
import json


# Non-system
from tables    import TTU_TABLE_SCHEMA as TABLE
from ttuinfo   import TTUInfo
from acsprism  import rtdb_init
from acstw.OracleInterface import OracleInterface

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

##############################User Define#################################################
#Update Rate Setting
update_rate = 5 # seconds
# 0.1 = ±10%
reasonable_rate_of_i = 0.1
#Column Setting
col_lockflag1 = 'LOCKFLAG1'
col_lockflag2 = 'LOCKFLAG2'
col_p = 'PA'
col_v = 'VOLTMAGA'
col_i = 'AMPA'
col_eflag = 'EFLAG'
#Connection Setting
USER = os.getenv("ORACLE_USER")
PSWD = os.getenv("ORACLE_PW")
TNS  = os.getenv("ORACLE_DBSTRING")
PRISMdb = OracleInterface(USER, PSWD, TNS)
##########################################################################################

def main():
    #Rtdb Init
    print('Start Initializing Rtdb')
    rtdb_init()
    print('Finish Initializing Rtdb')

    ##Create ttuinfo Dictionary
    print('Start Creating Dictionary (TTUINFO)')
    ttuinfoSet   = TABLE.get_ttu_info().resultSet
    ttuinfoDict  = dict()
    for ttuinfo in ttuinfoSet:
        ttuinfoDict[ttuinfo['TTU_NAME']] = TTUInfo(ttuinfo)
    print('Finish Creating Dictionary (TTUINFO)')

    print('Start Initializing MDMS_METER_INFO Table')
    TABLE.init_meter_data()
    print('Finish Initializing MDMS_METER_INFO Table')


    tmp_update_rate = update_rate
    print('Start Synchronizing Meter Data to TTU')
    while True:

        if tmp_update_rate == 0:
            sys.stdout.write('\rUpdate Meter Data to TTU in {0} second(s)'.format(tmp_update_rate))
            sys.stdout.flush()
            for data in TABLE.get_meter_sum().resultSet:
                if ttuinfoDict[data['TTU_NAME']].p != data['P']:
                    ttuinfoDict[data['TTU_NAME']].p = data['P']
                if ttuinfoDict[data['TTU_NAME']].i != data['AMP']:
                    ttuinfoDict[data['TTU_NAME']].i = data['AMP']
                if data['LOCKFLAG2'] == data['METERCNT']:
                    if ttuinfoDict[data['TTU_NAME']].flag3 != 2:
                        ttuinfoDict[data['TTU_NAME']].flag3 = 2
                elif data['LOCKFLAG2'] < data['METERCNT'] and data['LOCKFLAG2'] > 0:
                    if ttuinfoDict[data['TTU_NAME']].flag3 != 1:
                        ttuinfoDict[data['TTU_NAME']].flag3 = 1
                else:
                    if ttuinfoDict[data['TTU_NAME']].flag3 != 0:
                        ttuinfoDict[data['TTU_NAME']].flag3 = 0

            print('\nUpdated TTU Successfully')
            tmp_update_rate = update_rate

        else:
            sys.stdout.write('\rUpdate Meter Data to TTU in {0} second(s)'.format(tmp_update_rate))
            sys.stdout.flush()
        time.sleep(1)
        tmp_update_rate -= 1

if __name__ == "__main__":
    main()
