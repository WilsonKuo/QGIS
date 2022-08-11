#!/bin/python3.6

# System
import os
import sys
import time


# Non-system
from tables    import TTU_TABLE_SCHEMA as TABLE
from fci_ttu_info   import FCI_TTU_Info
from acsprism  import rtdb_init
from acstw.OracleInterface import OracleInterface

##############################User Define#################################################
#Update Rate Setting
update_rate = 5 # seconds
# 0.1 = ±10%

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
    print('Start Creating Dictionary (FCITTUINFO)')
    fci_ttuinfoSet   = TABLE.get_fci_ttu_info().resultSet
    fci_ttuinfoDict  = dict()
    for fci_ttuinfo in fci_ttuinfoSet:
        fci_ttuinfoDict[fci_ttuinfo['EQUIP_NUM']] = FCI_TTU_Info(fci_ttuinfo)
        fci_ttuinfoDict[fci_ttuinfo['EQUIP_NUM']].init_val()
    print('Finish Creating Dictionary (FCITTUINFO)')
    
    
    print('Start Initializing INTF_FCI_TTU_POOL Table')
    #TABLE.init_fci_ttu_data()
    print('Finish Initializing INTF_FCI_TTU_POOL Table')


    tmp_update_rate = update_rate
    print('Start Synchronizing TTU, FCI Data to RTDB')
    while True:

        if tmp_update_rate == 0:
            sys.stdout.write('\rUpdate TTU, FCI to RTDB in {0} second(s)'.format(tmp_update_rate))
            sys.stdout.flush()
            max_seq = TABLE.get_fci_ttu_seq().resultSet
            print('\n')
            for rec in TABLE.get_fci_ttu_data(max_seq).resultSet:
                print(rec['EQUIP_NUM'], rec['COLNAME'].lower(), rec['VALUE_RT'])
                try:
                    updatedpoint = fci_ttuinfoDict[rec['EQUIP_NUM']]
                    setattr(updatedpoint, rec['COLNAME'].lower(), rec['VALUE_RT'])  
                    print('Updated Point Successfully')
                except:
                    print('Updated Point Unsuccessfully')



            print('\nUpdated TTU, FCI Successfully')
            tmp_update_rate = update_rate

        else:
            sys.stdout.write('\rUpdate TTU, FCI to RTDB in {0} second(s)'.format(tmp_update_rate))
            sys.stdout.flush()
        time.sleep(1)
        tmp_update_rate -= 1

if __name__ == "__main__":
    main()
