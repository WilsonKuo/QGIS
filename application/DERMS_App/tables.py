#!/usr/bin/python3
# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
import os 

# Non-System
from acstw.OracleInterface import OracleInterface

USER = os.getenv("ORACLE_USER")
PSWD = os.getenv("ORACLE_PW")
TNS  = os.getenv("ORACLE_DBSTRING")
PRISMdb = OracleInterface(USER, PSWD, TNS)


class TTU_TABLE_SCHEMA:
    def __init__(self, columns, resultSet):
        self.columns   = columns
        self.resultSet = resultSet
    @classmethod
    def init_meter_data(cls):
        query = """TRUNCATE TABLE INTF_MDMS_METER_DATA"""
        PRISMdb.ExecNonQuery(query)
        query = """INSERT INTO INTF_MDMS_METER_DATA (METER_NAME) SELECT METER_NAME FROM TTU_METER;"""
        PRISMdb.ExecNonQuery(query)
    @classmethod
    def init_fci_ttu_data(cls):
        query = """TRUNCATE TABLE INTF_FCI_TTU_POOL"""
        PRISMdb.ExecNonQuery(query)
    @classmethod
    def get_meter_data(cls, ttu_name):
        columns  = ['METER_NAME', 'METERUNIQUEID', 'P_KWH', 'P_KQH_P', 'P_KQH_M']
        columns  += ['S_KWH', 'S_KQH_P', 'S_KQH_M', 'P_KW', 'P_KQ_P', 'P_KQ_M']
        columns  += ['S_KW', 'S_KQ_P', 'S_KQ_M', 'READINGTIME', 'RECEIVETIME']
        query = """SELECT {0} FROM INTF_MDMS_METER_DATA WHERE METER_NAME IN (SELECT METER_NAME FROM TTU_METER WHERE TTU_NAME = '{1}')""".format(",".join(columns), ttu_name)
        result  = PRISMdb.ExecQuery(query)
        resultSet = [ dict(zip(columns, row)) for row in result ]
        return cls(columns, resultSet)
    @classmethod
    def get_meter_sum(cls):
        columns  = ['TTU_NAME', 'P', 'AMP', 'LOCKFLAG2', 'METERCNT']
        query = """SELECT {0} FROM VIEW_METERSUM""".format(",".join(columns))
        result  = PRISMdb.ExecQuery(query)
        resultSet = [ dict(zip(columns, row)) for row in result ]
        return cls(columns, resultSet)
    @classmethod
    def get_ttu_info(cls, switch_name = None):
        columns  = ['TTU_NAME', 'DISPLAY_NUMBER', 'CAPACITY']
        columns += ['MDMS_P', 'MDMS_Q']
        columns += ['DPF_P' , 'DPF_Q' ]
        columns += ['STATION_PA', 'CATEGORY_PA', 'POINT_PA', 'RTDBTYPE_PA', 'ATTRIBUTE_PA']   
        columns += ['STATION_PB', 'CATEGORY_PB', 'POINT_PB', 'RTDBTYPE_PB', 'ATTRIBUTE_PB']   
        columns += ['STATION_PC', 'CATEGORY_PC', 'POINT_PC', 'RTDBTYPE_PC', 'ATTRIBUTE_PC']   
        columns += ['STATION_QA', 'CATEGORY_QA', 'POINT_QA', 'RTDBTYPE_QA', 'ATTRIBUTE_QA']
        columns += ['STATION_QB', 'CATEGORY_QB', 'POINT_QB', 'RTDBTYPE_QB', 'ATTRIBUTE_QB']   
        columns += ['STATION_QC', 'CATEGORY_QC', 'POINT_QC', 'RTDBTYPE_QC', 'ATTRIBUTE_QC']   
        columns += ['STATION_FLAG1', 'CATEGORY_FLAG1', 'POINT_FLAG1', 'RTDBTYPE_FLAG1', 'ATTRIBUTE_FLAG1']
        columns += ['STATION_FLAG2', 'CATEGORY_FLAG2', 'POINT_FLAG2', 'RTDBTYPE_FLAG2', 'ATTRIBUTE_FLAG2']
        columns += ['STATION_FLAG3', 'CATEGORY_FLAG3', 'POINT_FLAG3', 'RTDBTYPE_FLAG3', 'ATTRIBUTE_FLAG3']
        columns += ['STATION_FLAG4', 'CATEGORY_FLAG4', 'POINT_FLAG4', 'RTDBTYPE_FLAG4', 'ATTRIBUTE_FLAG4']
        if switch_name:
            query = """SELECT {0} FROM TTUINFO WHERE TTU_NAME IN (SELECT NAME FROM TB_TP WHERE (FEEDER1_NONLINEPARENT = '{1}' OR FEEDER2_NONLINEPARENT = '{1}'))""".format(",".join(columns), switch_name)
        else:
            query = """SELECT {0} FROM TTUINFO""".format(",".join(columns))
        result  = PRISMdb.ExecQuery(query)
        resultSet = [ dict(zip(columns, row)) for row in result ]
        return cls(columns, resultSet)
    @classmethod
    def get_fci_ttu_info(cls, obj_name):
        columns  = ['NAME']
        columns += ['STATION_PA', 'CATEGORY_PA', 'POINT_PA', 'RTDBTYPE_PA', 'ATTRIBUTE_PA']   
        columns += ['STATION_PB', 'CATEGORY_PB', 'POINT_PB', 'RTDBTYPE_PB', 'ATTRIBUTE_PB']   
        columns += ['STATION_PC', 'CATEGORY_PC', 'POINT_PC', 'RTDBTYPE_PC', 'ATTRIBUTE_PC']   
        columns += ['STATION_QA', 'CATEGORY_QA', 'POINT_QA', 'RTDBTYPE_QA', 'ATTRIBUTE_QA']
        columns += ['STATION_QB', 'CATEGORY_QB', 'POINT_QB', 'RTDBTYPE_QB', 'ATTRIBUTE_QB']   
        columns += ['STATION_QC', 'CATEGORY_QC', 'POINT_QC', 'RTDBTYPE_QC', 'ATTRIBUTE_QC']
        columns += ['STATION_AMPA', 'CATEGORY_AMPA', 'POINT_AMPA', 'RTDBTYPE_AMPA', 'ATTRIBUTE_AMPA']   
        columns += ['STATION_AMPB', 'CATEGORY_AMPB', 'POINT_AMPB', 'RTDBTYPE_AMPB', 'ATTRIBUTE_AMPB']   
        columns += ['STATION_AMPC', 'CATEGORY_AMPC', 'POINT_AMPC', 'RTDBTYPE_AMPC', 'ATTRIBUTE_AMPC']
        columns += ['STATION_VOLTMAGA', 'CATEGORY_VOLTMAGA', 'POINT_VOLTMAGA', 'RTDBTYPE_VOLTMAGA', 'ATTRIBUTE_VOLTMAGA']   
        columns += ['STATION_VOLTMAGB', 'CATEGORY_VOLTMAGB', 'POINT_VOLTMAGB', 'RTDBTYPE_VOLTMAGB', 'ATTRIBUTE_VOLTMAGB']   
        columns += ['STATION_VOLTMAGC', 'CATEGORY_VOLTMAGC', 'POINT_VOLTMAGC', 'RTDBTYPE_VOLTMAGC', 'ATTRIBUTE_VOLTMAGC']
        columns += ['STATION_FAULTFLAGA', 'CATEGORY_FAULTFLAGA', 'POINT_FAULTFLAGA', 'RTDBTYPE_FAULTFLAGA', 'ATTRIBUTE_FAULTFLAGA']   
        columns += ['STATION_FAULTFLAGB', 'CATEGORY_FAULTFLAGB', 'POINT_FAULTFLAGB', 'RTDBTYPE_FAULTFLAGB', 'ATTRIBUTE_FAULTFLAGB']   
        columns += ['STATION_FAULTFLAGC', 'CATEGORY_FAULTFLAGC', 'POINT_FAULTFLAGC', 'RTDBTYPE_FAULTFLAGC', 'ATTRIBUTE_FAULTFLAGC']
        if obj_name:
            query = "SELECT FEEDER1 FROM TB_TP WHERE NAME = '{0}' UNION SELECT FEEDER2 FROM TB_TP WHERE NAME = '{0}'".format(obj_name)
            result = "','".join([feeder[0] for feeder in PRISMdb.ExecQuery(query) if feeder[0]])
            query = """SELECT {0} FROM FCI_TTU_INFO WHERE (FEEDER1 IN ('{1}') OR FEEDER2 IN ('{1}')) AND FSC = 114""".format(",".join(columns), result)
        else:
            query = """SELECT {0} FROM FCI_TTU_INFO""".format(",".join(columns))
        result  = PRISMdb.ExecQuery(query)
        resultSet = [ dict(zip(columns, row)) for row in result ]
        return cls(columns, resultSet)

    @classmethod
    def get_fci_ttu_data(cls, seq):
        columns = ['EQUIP_NUM', 'COLNAME', 'VALUE_RT']
        query = """SELECT {0} FROM INTF_FCI_TTU_POOL WHERE SEQ <= {1}""".format(",".join(columns), seq)
        result  = PRISMdb.ExecQuery(query)
        resultSet = [ dict(zip(columns, row)) for row in result ]
        query = """DELETE INTF_FCI_TTU_POOL WHERE SEQ <= {0}""".format(seq)
        #PRISMdb.ExecNonQuery(query)
        return cls(columns, resultSet)

    @classmethod
    def get_fci_ttu_seq(cls):
        columns = ''
        query = """SELECT MAX(SEQ) FROM INTF_FCI_TTU_POOL"""
        result  = PRISMdb.ExecQuery(query)
        resultSet  = result[0][0]
        return cls(columns, resultSet)

    @classmethod
    def get_colorcode(cls):
        columns  = ['COLORCODE', 'NAME']
        query = """SELECT {0} FROM FEEDERPARAM""".format(",".join(columns))
        result  = PRISMdb.ExecQuery(query)
        resultSet = [ dict(zip(columns, row)) for row in result ]
        return cls(columns, resultSet)

    @classmethod
    def get_cmp_name(cls, obj_name):
        columns = ['NAME']
        query   = "SELECT FEEDER1 FROM TB_TP WHERE NAME = '{0}' UNION SELECT FEEDER2 FROM TB_TP WHERE NAME = '{0}'".format(obj_name)
        result  = "','".join([feeder[0] for feeder in PRISMdb.ExecQuery(query) if feeder[0]])
        query   = "SELECT {0} FROM TB_TP WHERE (FEEDER1 IN ('{1}') OR FEEDER2 IN ('{1}')) AND FSC = 115".format(",".join(columns), result)
        result  = PRISMdb.ExecQuery(query)
        resultSet = [ row[0] for row in result ]
        return cls(columns, resultSet)


    @classmethod
    def get_cmp_info(cls, tablename, obj_name, year, month, day, hour, minute):
        columns  = ['NAME', 'PA', 'PB', 'PC', 'QA', 'QB', 'QC']
        query = "SELECT FEEDER1 FROM TB_TP WHERE NAME = '{0}' UNION SELECT FEEDER2 FROM TB_TP WHERE NAME = '{0}'".format(obj_name)
        result = "','".join([feeder[0] for feeder in PRISMdb.ExecQuery(query) if feeder[0]])
        query = """SELECT {0} FROM {1}_{2}{3} WHERE NAME IN (SELECT NAME FROM TB_TP WHERE FEEDER1 IN ('{4}') OR FEEDER2 IN ('{4}'))
                   AND DAY = {5} AND HOUR = {6} AND MINUTE = {7}""".format(",".join(columns), tablename, month, year, result, day, hour, minute)
        result  = PRISMdb.ExecQuery(query)
        resultSet = [ dict(zip(columns, row)) for row in result ]
        return cls(columns, resultSet)




if __name__ == "__main__":
    c = TTU_TABLE_SCHEMA.get_ttu_meter().columns
    d = TTU_TABLE_SCHEMA.get_ttu_meter().resultSet
    print(c)
    print(d)
    
