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
    def get_ttu_meter(cls):
        columns  = ['TTU_NAME', 'METER_NAME']
        query = """SELECT {0} FROM TTU_METER""".format(",".join(columns))
        result  = PRISMdb.ExecQuery(query)
        resultSet = [ dict(zip(columns, row)) for row in result ]
        return cls(columns, resultSet)
    @classmethod
    def get_meter_data(cls, seq_id):
        columns  = ['METER_NAME', 'COLNAME','VALUE_RT']
        query = """SELECT {0} FROM MDMS_METER_PROCESSED WHERE SEQ_ID <= {1}""".format(",".join(columns), seq_id)
        result  = PRISMdb.ExecQuery(query)
        resultSet = [ dict(zip(columns, row)) for row in result ]
        return cls(columns, resultSet)
    # @classmethod
    # def get_meter_data(cls, ttu_name = None):
    #     columns  = ['METER_NAME', 'LOCKFLAG1','LOCKFLAG2', 'P', 'V', 'I', 'EFLAG']
    #     if ttu_name:
    #         query = """SELECT {0} FROM METERDATA WHERE METER_NAME IN (SELECT METER_NAME FROM TTU_METER WHERE TTU_NAME = '{1}')""".format(",".join(columns), ttu_name)
    #     else:
    #         query = """SELECT {0} FROM METERDATA""".format(",".join(columns))
    #     result  = PRISMdb.ExecQuery(query)
    #     resultSet = [ dict(zip(columns, row)) for row in result ]
    #     return cls(columns, resultSet)
    @classmethod
    def get_meter_info(cls, ttu_name = None):
        columns  = ['METER_NAME']
        columns += ['STATION_LOCKFLAG1', 'CATEGORY_LOCKFLAG1', 'POINT_LOCKFLAG1', 'RTDBTYPE_LOCKFLAG1', 'ATTRIBUTE_LOCKFLAG1']   
        columns += ['STATION_LOCKFLAG2', 'CATEGORY_LOCKFLAG2', 'POINT_LOCKFLAG2', 'RTDBTYPE_LOCKFLAG2', 'ATTRIBUTE_LOCKFLAG2']  
        columns += ['STATION_P', 'CATEGORY_P', 'POINT_P', 'RTDBTYPE_P', 'ATTRIBUTE_P']
        columns += ['STATION_V', 'CATEGORY_V', 'POINT_V', 'RTDBTYPE_V', 'ATTRIBUTE_V']  
        columns += ['STATION_I', 'CATEGORY_I', 'POINT_I', 'RTDBTYPE_I', 'ATTRIBUTE_I']
        columns += ['STATION_EFLAG', 'CATEGORY_EFLAG', 'POINT_EFLAG', 'RTDBTYPE_EFLAG', 'ATTRIBUTE_EFLAG']  
        if ttu_name:
            query = """SELECT {0} FROM METERINFO WHERE METER_NAME IN (SELECT METER_NAME FROM TTU_METER WHERE TTU_NAME = '{1}')""".format(",".join(columns), ttu_name)
        else:
            query = """SELECT {0} FROM METERINFO""".format(",".join(columns))

        result  = PRISMdb.ExecQuery(query)
        resultSet = [ dict(zip(columns, row)) for row in result ]
        return cls(columns, resultSet)
    @classmethod
    def get_ttu_info(cls, ttu_name = None):
        columns  = ['TTU_NAME', 'DISPLAY_NUMBER', 'CAPACITY']
        columns += ['STATION_P', 'CATEGORY_P', 'POINT_P', 'RTDBTYPE_P', 'ATTRIBUTE_P']   
        columns += ['STATION_Q', 'CATEGORY_Q', 'POINT_Q', 'RTDBTYPE_Q', 'ATTRIBUTE_Q']   
        columns += ['STATION_I', 'CATEGORY_I', 'POINT_I', 'RTDBTYPE_I', 'ATTRIBUTE_I']
        columns += ['STATION_V', 'CATEGORY_V', 'POINT_V', 'RTDBTYPE_V', 'ATTRIBUTE_V']
        columns += ['STATION_FLAG1', 'CATEGORY_FLAG1', 'POINT_FLAG1', 'RTDBTYPE_FLAG1', 'ATTRIBUTE_FLAG1']
        columns += ['STATION_FLAG2', 'CATEGORY_FLAG2', 'POINT_FLAG2', 'RTDBTYPE_FLAG2', 'ATTRIBUTE_FLAG2']
        columns += ['STATION_FLAG3', 'CATEGORY_FLAG3', 'POINT_FLAG3', 'RTDBTYPE_FLAG3', 'ATTRIBUTE_FLAG3']
        columns += ['STATION_FLAG4', 'CATEGORY_FLAG4', 'POINT_FLAG4', 'RTDBTYPE_FLAG4', 'ATTRIBUTE_FLAG4']
        if ttu_name:
            query = """SELECT {0} FROM TTUINFO WHERE TTU_NAME IN (SELECT TTU_NAME FROM SWITCH_TTU WHERE SWITCH_NAME = '{1}')""".format(",".join(columns), ttu_name)
        else:
            query = """SELECT {0} FROM TTUINFO """.format(",".join(columns))

        result  = PRISMdb.ExecQuery(query)
        resultSet = [ dict(zip(columns, row)) for row in result ]
        return cls(columns, resultSet)





if __name__ == "__main__":
    c = TTU_TABLE_SCHEMA.get_ttu_meter().columns
    d = TTU_TABLE_SCHEMA.get_ttu_meter().resultSet
    print(c)
    print(d)
    
