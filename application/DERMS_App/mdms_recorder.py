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
    mdmstabletimestamp = previous_date.strftime("%B%Y")
    mdmstablename      = f"MDMS_{mdmstabletimestamp}".upper()
    mdmspreviousday    = previous_date.day
    mdmsprevioustimestamp  = previous_date.strftime("%m/%d/%Y")

    # #######################
    # # os.system("/home/acs/bin/mdms")
    # #######################


    query = f"SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = '{mdmstablename}'"
    result = PRISMdb.ExecQuery(query)[0][0]
    print(result)

    if result == 0:
        print(f"CREATE <{mdmstablename}> TABLE")
        query = f"""
        CREATE TABLE {mdmstablename} 
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
                        INSERT INTO {mdmstablename} SELECT
                            LP.NAME, NVL(T.PA, 0) PA, NVL(T.PB, 0) PB, NVL(T.PC, 0) PC,
                                     NVL(T.QA, 0) QA, NVL(T.QB, 0) QB, NVL(T.QC, 0) QC,
                                     {mdmspreviousday}, {hour}, {minute} FROM {loadparamcondition} LP 
                    """

            query += """
                        LEFT JOIN  (
                            SELECT TTU_NAME, SUM(P_KWH) PA, SUM(P_KWH) PB, SUM(P_KWH) PC, 
                                   SUM(P_KQH_P) QA, SUM(P_KQH_P) QB, SUM(P_KQH_P) QC
                                   FROM INTF_MDMS_DATA IMD, TTU_METER TM
                            WHERE TM.METER_NAME = IMD.METER AND 
                                READINGTIME BETWEEN 
                                TO_DATE('{0} {hh:02d}:{m1:02d}:00', 'DD/MM/YYYY HH24:MI:SS') 
                                AND
                                TO_DATE('{0} {hh:02d}:{m2:02d}:59', 'DD/MM/YYYY HH24:MI:SS') 
                            GROUP BY TM.TTU_NAME
                        ) T
                        ON LP.NAME = T.TTU_NAME
                    """.format(mdmsprevioustimestamp, hh = hour, m1 = minute, m2 = minute + 14)

            print(query)
            PRISMdb.ExecNonQuery(query)
    
    #######################################################
    # 1 = C, 2 = B, 3 = BC, 4 = A, 5 = AC, 6 = AB, 7 = ABC#
    #######################################################

    ##C PHASE
    query = f"""
                UPDATE {mdmstablename} SET PA = 0, PB = 0, QA = 0, QB = 0 
                WHERE NAME IN (SELECT METER_NAME FROM TTU_METER WHERE TTU_NAME IN (SELECT NAME FROM LOADPARAM WHERE PHASE = 1))
                AND DAY = {mdmspreviousday}
            """
    print(query)
    PRISMdb.ExecNonQuery(query)
    ## B PHASE
    query = f"""
                UPDATE {mdmstablename} SET PA = 0, PC = 0, QA = 0, QC = 0 
                WHERE NAME IN (SELECT METER_NAME FROM TTU_METER WHERE TTU_NAME IN (SELECT NAME FROM LOADPARAM WHERE PHASE = 2))
                AND DAY = {mdmspreviousday}
            """
    print(query)
    PRISMdb.ExecNonQuery(query)
    ## BC PHASE
    query = f"""
                UPDATE {mdmstablename} SET PA = 0, PB = PB/2, PC = PC/2, QA = 0, QB = QB/2, QC = QC/2
                WHERE NAME IN (SELECT METER_NAME FROM TTU_METER WHERE TTU_NAME IN (SELECT NAME FROM LOADPARAM WHERE PHASE = 3))
                AND DAY = {mdmspreviousday}
            """
    print(query)
    PRISMdb.ExecNonQuery(query)
    ## A PHASE
    query = f"""
                UPDATE {mdmstablename} SET PB = 0, PC = 0, QB = 0, QC = 0
                WHERE NAME IN (SELECT METER_NAME FROM TTU_METER WHERE TTU_NAME IN (SELECT NAME FROM LOADPARAM WHERE PHASE = 4))
                AND DAY = {mdmspreviousday}
            """
    print(query)
    PRISMdb.ExecNonQuery(query)
    ## AC PHASE
    query = f"""
                UPDATE {mdmstablename} SET PA = PA/2, PB = 0, PC = PC/2, QA = QA/2, QB = 0, QC = QC/2
                WHERE NAME IN (SELECT METER_NAME FROM TTU_METER WHERE TTU_NAME IN (SELECT NAME FROM LOADPARAM WHERE PHASE = 5))
                AND DAY = {mdmspreviousday}
            """
    print(query)
    PRISMdb.ExecNonQuery(query)
    ## AB PHASE
    query = f"""
                UPDATE {mdmstablename} SET PA = PA/2, PB = PB/2, PC = 0, QA = QA/2, QB = QB/2, QC = 0
                WHERE NAME IN (SELECT METER_NAME FROM TTU_METER WHERE TTU_NAME IN (SELECT NAME FROM LOADPARAM WHERE PHASE = 6))
                AND DAY = {mdmspreviousday}
            """
    print(query)
    PRISMdb.ExecNonQuery(query)
    ## ABC PHASE
    query = f"""
                UPDATE {mdmstablename} SET PA = PA/3, PB = PB/3, PC = PC/3, QA = QA/3, QB = QB/3, QC = QC/3
                WHERE NAME IN (SELECT METER_NAME FROM TTU_METER WHERE TTU_NAME IN (SELECT NAME FROM LOADPARAM WHERE PHASE = 7))
                AND DAY = {mdmspreviousday}
            """
    print(query)
    PRISMdb.ExecNonQuery(query)


if __name__ == "__main__":
    main()
