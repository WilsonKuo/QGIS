#!/bin/python3.6
print(2.1 +/- 0.05) 
exit()
# System
import os
import sys
import time
# Non-system
from tables    import TTU_TABLE_SCHEMA as TABLE
from meterinfo import MeterInfo
from ttuinfo   import TTUInfo
from acsprism  import rtdb_init
from acstw.OracleInterface import OracleInterface

##############################User Define#################################################
#Update Rate Setting
update_rate = 5 # seconds
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



import math
# for ttu_name in ttu_meter.keys():
#     for meter_name in ttu_meter[ttu_name]:
#         # sum(getattr(meterinfoDict[meter_name],'lockflag2'))
#         meterinfoDict[meter_name].lockflag2 for meter in meterinfoDict

##pass by reference, no need to worry memory usage?
ttu_meterinfoDict = dict()
for ttu_name in ttu_meter.keys():
    ttu_meterinfoDict[ttu_name] = list()
    for meter_name in ttu_meter[ttu_name]:
        ttu_meterinfoDict[ttu_name].append(meterinfoDict[meter_name])

print(sum(meter.lockflag2 for meter in ttu_meterinfoDict['B5934HE05T01'])