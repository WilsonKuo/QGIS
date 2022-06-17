#!/bin/python3.6

# System
import os
import sys
import time
import random
import datetime

# Non-system
from acstw.OracleInterface import OracleInterface

USER = os.getenv("ORACLE_USER")
PSWD = os.getenv("ORACLE_PW")
TNS  = os.getenv("ORACLE_DBSTRING")
PRISMdb = OracleInterface(USER, PSWD, TNS)
result = PRISMdb.ExecQuery("SELECT TTU_NAME, METER_NAME FROM TTU_METER")
arr = list()
seq_id = 1
for ttu_name, meter_name in result:
    arr.append([ttu_name, 'PA',meter_name, seq_id, random.uniform(10,20), datetime.datetime.now()])
    seq_id += 1
    arr.append([ttu_name, 'AMPA',meter_name, seq_id, random.uniform(5,9), datetime.datetime.now()])
    seq_id += 1

colStr = 'EQUIP_NUM, COLNAME, NAMEID, SEQ_ID, VALUE_RT, DATATIME'
valPlaceholder = ":0,:1,:2,:3,:4,:5"
insSql = "insert /* array */ into %s (%s) values (%s)" % ('MDMS_METER', colStr, valPlaceholder)
PRISMdb.InsertArray(insSql,arr)
print('\nInsert data successfully!')