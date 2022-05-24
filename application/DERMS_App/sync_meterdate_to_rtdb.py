#!/bin/python3.6

# System
import os
import sys
import time
import threading
from functools import reduce  # Required in Python 3
# Non-system
from tables    import TTU_TABLE_SCHEMA as TABLE
from meterinfo import MeterInfo
from ttuinfo   import TTUInfo
from acsprism  import rtdb_init
from acstw.OracleInterface import OracleInterface

##############################User Define#################################################
#Update Rate Setting
update_rate = 5 # seconds
#If million point have been updated, 2 seconds might not be enough
waiting_rtdb_update_time = 2 # seconds
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
    #Create meter ttu Dictionary    
    print('Start Creating Dictionary (METER->TTU)')
    meter_ttu = dict()
    for mt in TABLE.get_ttu_meter().resultSet:
        meter_ttu[mt['METER_NAME']] = mt['TTU_NAME']
    print('Finish Creating Dictionary (METER->TTU)')
    #Create ttu meter Dictionary    
    print('Start Creating Dictionary (TTU->METER)')
    ttu_meter = dict()
    for tm in TABLE.get_ttu_meter().resultSet:
        if tm['TTU_NAME'] not in ttu_meter.keys():
            ttu_meter[tm['TTU_NAME']] = list()
        ttu_meter[tm['TTU_NAME']].append(tm['METER_NAME'])
    print('Finish Creating Dictionary (TTU->METER)')
    ##Create meterinfo Dictionary
    print('Start Creating Dictionary (METERINFO)')
    meterinfoSet  = TABLE.get_meter_info().resultSet
    meterinfoDict = dict()
    for meterinfo in meterinfoSet:
        meterinfoDict[meterinfo['METER_NAME']] = MeterInfo(meterinfo)
    print('Finish Creating Dictionary (METERINFO)')
    ##Create ttuinfo Dictionary
    print('Start Creating Dictionary (TTUINFO)')
    ttuinfoSet   = TABLE.get_ttu_info().resultSet
    ttuinfoDict  = dict()
    for ttuinfo in ttuinfoSet:
        ttuinfoDict[ttuinfo['TTU_NAME']] = TTUInfo(ttuinfo)
    print('Finish Creating Dictionary (TTUINFO)')

    #Create ttu_meterinfoDict Dictionary
    ##pass by reference, no need to worry memory usage?
    print('Start Creating Dictionary (TTU_METERINFODICT)')
    ttu_meterinfoDict = dict()
    for ttu_name in ttu_meter.keys():
        ttu_meterinfoDict[ttu_name] = list()
        for meter_name in ttu_meter[ttu_name]:
            ttu_meterinfoDict[ttu_name].append(meterinfoDict[meter_name])
    print('Finish Creating Dictionary (TTU_METERINFODICT)')

    #Create ttu_metercnt Dictionary
    print('Start Creating Dictionary (TTU_METERINFODICT)')
    ttu_metercnt = dict()
    for ttu_name in ttu_meterinfoDict.keys():
        ttu_metercnt[ttu_name] = len(ttu_meterinfoDict[ttu_name])

    print('Finish Creating Dictionary (TTU_METERCNT)')

    #Initializing rtdb before starting program
    print('Start Initializing Meter Value')
    for val in meterinfoDict.values():
        val.init_val()
    print('Finish Initializing Meter Value')
    print('Start Initializing TTU Flag3, Flag4')
    for val in ttuinfoDict.values():
        val.init_val()
    print('Finish Initializing TTU Flag3, Flag4')

    #Truncate table before starting program
    print('Start Truncating <MDMS_METER_PROCESSED> Table')
    PRISMdb.ExecNonQuery("TRUNCATE TABLE MDMS_METER_PROCESSED")
    print('Finish Truncating <MDMS_METER_PROCESSED> Table')


    notready_flag1 = dict()
    notready_flag2 = dict()
    notready_i = dict()
    #unionCheck if METER LOCKFLAG1 # change, then check if writertdb to TTU FLAG3 is required
    #unionCheck if METER LOCKFLAG2 # change, then check if writertdb to TTU FLAG4 is required
    #unionCheck if METER AMPA  # change, if value is weird, writertdb to TTU FLAG1
    unionCheck_lockflag1 = dict()
    unionCheck_lockflag2 = dict()
    unionCheck_i = dict()

    tmp_update_rate = update_rate
    print('Start Synchronizing Meter Data To Rtdb')
    while True:
        if tmp_update_rate == 0:
            sys.stdout.write('\rUpdate meterdataSet in {0} second(s)'.format(tmp_update_rate))
            sys.stdout.flush()
            max_seq_id = PRISMdb.ExecQuery("SELECT MAX(SEQ_ID) FROM MDMS_METER_PROCESSED")[0][0]
            #Prevent none condition
            if max_seq_id:
                print('\nUpdate meterdataSet!')
                #Prevent new data coming when select max(sqe_id)
                meterdataSet = TABLE.get_meter_data(max_seq_id).resultSet
                #Flush data
                PRISMdb.ExecNonQuery("DELETE MDMS_METER_PROCESSED WHERE SEQ_ID <= {0}".format(max_seq_id))
                for data in meterdataSet:
                    #print(data)
                    #print('New Meter Data : {0}'.format(data['METER_NAME']))
                    ###################################
                    if data['COLNAME'] == col_lockflag1:
                        int_VALUE_RT = int(data['VALUE_RT'])
                        if int_VALUE_RT != meterinfoDict[data['METER_NAME']].lockflag1:
                            print('{0} from {1} -> {2}'.format(col_lockflag1, meterinfoDict[data['METER_NAME']].lockflag1, int_VALUE_RT))
                            meterinfoDict[data['METER_NAME']].lockflag1 = int_VALUE_RT
                        if meter_ttu[data['METER_NAME']] not in unionCheck_lockflag1.keys():
                            unionCheck_lockflag1[meter_ttu[data['METER_NAME']]] = True
                    ###################################
                    elif data['COLNAME'] == col_lockflag2:
                        int_VALUE_RT = int(data['VALUE_RT'])
                        if int_VALUE_RT != meterinfoDict[data['METER_NAME']].lockflag2:
                            print('{0} from {1} -> {2}'.format(col_lockflag2, meterinfoDict[data['METER_NAME']].lockflag2, int_VALUE_RT))
                            meterinfoDict[data['METER_NAME']].lockflag2 = int_VALUE_RT
                        if meter_ttu[data['METER_NAME']] not in unionCheck_lockflag2.keys():
                            unionCheck_lockflag2[meter_ttu[data['METER_NAME']]] = True
                    ###################################
                    elif data['COLNAME'] == col_p:
                        if data['VALUE_RT'] != meterinfoDict[data['METER_NAME']].p:
                            print('{0} from {1} -> {2}'.format(col_p, meterinfoDict[data['METER_NAME']].p, data['VALUE_RT']))
                            meterinfoDict[data['METER_NAME']].p = data['VALUE_RT']
                    ###################################
                    elif data['COLNAME'] == col_v:
                        if data['VALUE_RT'] != meterinfoDict[data['METER_NAME']].v:
                            print('{0} from {1} -> {2}'.format(col_v, meterinfoDict[data['METER_NAME']].v, data['VALUE_RT']))
                            meterinfoDict[data['METER_NAME']].v = data['VALUE_RT']
                    ###################################
                    elif data['COLNAME'] == col_i:
                        if data['VALUE_RT'] != meterinfoDict[data['METER_NAME']].i:
                            print('{0} from {1} -> {2}'.format(col_i, meterinfoDict[data['METER_NAME']].i, data['VALUE_RT']))
                            meterinfoDict[data['METER_NAME']].i = data['VALUE_RT']
                        if meter_ttu[data['METER_NAME']] not in unionCheck_i.keys():
                            unionCheck_i[meter_ttu[data['METER_NAME']]] = True
                    ###################################
                    elif data['COLNAME'] == col_eflag:
                        if data['VALUE_RT'] != meterinfoDict[data['METER_NAME']].eflag:
                            print('{0} from {1} -> {2}'.format(col_eflag, meterinfoDict[data['METER_NAME']].eflag, data['VALUE_RT']))
                            meterinfoDict[data['METER_NAME']].eflag = data['VALUE_RT']
                    else:
                        raise NotImplementedError("Colname {0} not implemented".format(data['COLNAME']))

                tmp_waiting_rtdb_update_time = waiting_rtdb_update_time
                if bool(unionCheck_lockflag1) or bool(unionCheck_lockflag2) or bool(unionCheck_i):
                    print('Meter LOCKFLAG1 or LOCKFLAG2 or AMPA changed')
                    while True:
                        if tmp_waiting_rtdb_update_time == 0:
                            sys.stdout.write('\rUpdate TTU LOCKFLAG3 or LOCKFLAG4 or AMPA in {0} second(s)'.format(tmp_waiting_rtdb_update_time))
                            sys.stdout.flush()
                            print('\nUpdate TTU LOCKFLAG3 or LOCKFLAG4 or AMPA!')
                            # Check calculated point later, otherwise
                            # If writing meter lockflag1 and lockflag2, and then read rtdb immediately,
                            # might not read the changing value, ttu flag3 and flag4 will not be correct
                            for key in unionCheck_lockflag1.keys():
                                cnt = (reduce(lambda x, y: x + y, (meter.lockflag1 for meter in ttu_meterinfoDict[key]))) / 2
                                if cnt == ttu_metercnt[ttu_name]:
                                    print('All Meter Got communication problem at TTU:{} downstream'.format(key))
                                    ttuinfoDict[key].flag3 = 2
                                elif cnt < ttu_metercnt[ttu_name] and cnt > 0:
                                    print('Some Meter Got communication problem at TTU:{} downstream'.format(key))
                                    ttuinfoDict[key].flag3 = 1
                                else:
                                    ttuinfoDict[key].flag3 = 0
                            for key in unionCheck_lockflag2.keys():
                                cnt = (reduce(lambda x, y: x + y, (meter.lockflag2 for meter in ttu_meterinfoDict[key]))) / 2
                                if cnt == ttu_metercnt[ttu_name]:
                                    print('All Meter In Stock at TTU:{} downstream'.format(key))
                                    ttuinfoDict[key].flag4 = 2
                                elif cnt < ttu_metercnt[ttu_name] and cnt > 0:
                                    print('Some Meter In Stock at TTU:{} downstream'.format(key))
                                    ttuinfoDict[key].flag4 = 1
                                else:
                                    ttuinfoDict[key].flag4 = 0
                            for key in unionCheck_i.keys():
                                total_meter_i = reduce(lambda x, y: x+y, (meter.i for meter in ttu_meterinfoDict[key]))
                                ttu_i = ttuinfoDict[key].i
                                if total_meter_i  * (1 + reasonable_rate_of_i) < ttu_i:
                                    ttuinfoDict[key].flag2 = 1
                                    print('Total Meter AMPA = {0} , over the resonable value TTU:{1} AMPA {2}, some consumer might steal electricity'.format(total_meter_i, key, ttu_i))
                                else:
                                    ttuinfoDict[key].flag2 = 0
                            unionCheck_lockflag1.clear()
                            unionCheck_lockflag2.clear()
                            unionCheck_i.clear()
                            break

                        else:
                            sys.stdout.write('\rUpdate TTU LOCKFLAG3 or LOCKFLAG4 or AMPA in {0} second(s)'.format(tmp_waiting_rtdb_update_time))
                            sys.stdout.flush()
                        time.sleep(1)
                        tmp_waiting_rtdb_update_time -= 1

            else:
                print('\nNo New Data, Ignore!')
            tmp_update_rate = update_rate

        else:
            sys.stdout.write('\rUpdate meterdataSet in {0} second(s)'.format(tmp_update_rate))
            sys.stdout.flush()
        time.sleep(1)
        tmp_update_rate -= 1

if __name__ == "__main__":
    main()
