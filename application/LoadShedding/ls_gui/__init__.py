# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""

import os
from core.OracleInterface import OracleInterface
__author__ = 'Darren Liang'

TITLE = "LS APP"


def connent_dasdb():
    USER  = os.getenv('ORACLE_USER', 'acs_qa')
    PSWD  = os.getenv('ORACLE_PW'  , 'acs_qa')
    TNS   = os.getenv('ORACLE_DBSTRING', 'emsa')
    PRISMdb = OracleInterface(USER, PSWD, TNS)
    return PRISMdb