#!/bin/python3.6
import datetime
import os
# Non-System
from acstw.OracleInterface import OracleInterface

USER = os.getenv("ORACLE_USER")
PSWD = os.getenv("ORACLE_PW")
TNS  = os.getenv("ORACLE_DBSTRING")
PRISMdb = OracleInterface(USER, PSWD, TNS)


######################################
# RUN EVERY 15 MINUTES AND INSERT DATA
######################################


def main():
    dpftabletimestamp = datetime.datetime.now().strftime("%B%Y")
    dpftablename      = f"DPF_{dpftabletimestamp}".upper()
    print(dpftablename)
    minute = datetime.datetime.now().minute
    if minute >= 0 and minute < 15:
        minute = 0
    elif minute >= 15 and minute < 30:
        minute = 15
    elif minute >= 30 and minute < 45:
        minute = 30
    else:
        minute = 45
    dpfdatatimestamp  = {'month': datetime.datetime.now().month, 'hour': datetime.datetime.now().hour, 'minute': minute }
    print(dpfdatatimestamp)


    #######################
    os.system("/home/acs/bin/dpf > /home/acs/tmp/dpf.out")
    #######################


    query = f"SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = '{dpftablename}'"
    result = PRISMdb.ExecQuery(query)[0][0]
    print(result)

    if result == 0:
        print(f"CREATE <{dpftablename}> TABLE")
        query = f"""
        CREATE TABLE {dpftablename} 
        (
            NAME   VARCHAR2(63),
            PA     NUMBER(8,2),
            PB     NUMBER(8,2),
            PC     NUMBER(8,2),
            QA     NUMBER(8,2),
            QB     NUMBER(8,2),
            QC     NUMBER(8,2),
            DAY    NUMBER(2),
            HOUR   NUMBER(2),
            MINUTE NUMBER(2)
        )
        """
        PRISMdb.ExecNonQuery(query)

    if True:
        loadparamcondition = "(SELECT * FROM LOADPARAM WHERE NAME IN (SELECT NAME FROM TB_TP WHERE FEEDER1 IN ('K27D', '4D64', '4D52') UNION SELECT NAME FROM TB_TP WHERE FEEDER2 IN ('K27D', '4D64', '4D52')))"
    else:
        loadparamcondition = "LOADPARAM"


    query = f"""
                INSERT INTO {dpftablename}
                SELECT NAME, PA, PB, PC, QA, QB, QC, 
                '{dpfdatatimestamp['month']}', '{dpfdatatimestamp['hour']}', '{dpfdatatimestamp['minute']}'
                FROM {loadparamcondition} LP
                LEFT JOIN NODEOUTPUT NO
                ON LP.IDX = NO.IDX
            """
    PRISMdb.ExecNonQuery(query)


if __name__ == "__main__":
    main()
