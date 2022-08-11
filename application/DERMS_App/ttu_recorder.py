#!/bin/python3.6
import datetime
import os
# Non-System
from acstw.OracleInterface import OracleInterface

USER = os.getenv("ORACLE_USER")
PSWD = os.getenv("ORACLE_PW")
TNS  = os.getenv("ORACLE_DBSTRING")
PRISMdb = OracleInterface(USER, PSWD, TNS)

############################################
# RUN EVERY DAY AND INSERT PREVIOUS DAY DATA
############################################


def main():
    previous_date = datetime.datetime.now() - datetime.timedelta(days=1)
    ttutabletimestamp = previous_date.strftime("%B%Y")
    ttutablename      = f"TTU_{ttutabletimestamp}".upper()
    ttupreviousday    = previous_date.day
    ttuprevioustimestamp  = previous_date.strftime("%m/%d/%Y")

    # #######################
    # # os.system("/home/acs/bin/ttu")
    # #######################


    query = f"SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = '{ttutablename}'"
    result = PRISMdb.ExecQuery(query)[0][0]
    print(result)

    if result == 0:
        print(f"CREATE <{ttutablename}> TABLE")
        query = f"""
        CREATE TABLE {ttutablename} 
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

    for hour in range(0,24):
        for minute in [0, 15, 30, 45]:
            query = f"""
                        INSERT INTO {ttutablename} SELECT
                            LP.NAME, NVL(PA.CURVALUE, 0) PA, NVL(PB.CURVALUE, 0) PB, NVL(PC.CURVALUE, 0) PC,
                                     NVL(QA.CURVALUE, 0) QA, NVL(QB.CURVALUE, 0) QB, NVL(QC.CURVALUE, 0) QC,
                                     {ttupreviousday}, {hour}, {minute} FROM {loadparamcondition} LP 
                        """
            for column in ['PA', 'PB', 'PC', 'QA', 'QB', 'QC']:
                query += """
                            LEFT JOIN  (
                                SELECT TPCID||LOOPID NAME, CURVALUE FROM INTF_FCI_TTU_DATA 
                                WHERE COLNAME = '{0}' AND 
                                READINGTIME BETWEEN 
                                    TO_DATE('{1} {hh:02d}:{m1:02d}:00', 'DD/MM/YYYY HH24:MI:SS') 
                                    AND
                                    TO_DATE('{1} {hh:02d}:{m2:02d}:59', 'DD/MM/YYYY HH24:MI:SS') 
                            ) {0} 
                            ON LP.NAME = {0}.NAME
                        """.format(column, ttuprevioustimestamp, hh = hour, m1 = minute, m2 = minute + 14)
            print(query)
            PRISMdb.ExecNonQuery(query)



if __name__ == "__main__":
    main()
