#!/bin/python3.6
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
import os
import sys
import time
import logging
import threading
from datetime import datetime

# Non-System
from acsprism import RtdbAddress,RtdbPoint
from acsprism import rtdb_init
from acstw.OracleInterface import OracleInterface

USER = os.getenv("ORACLE_USER")
PSWD = os.getenv("ORACLE_PW")
TNS  = os.getenv("ORACLE_DBSTRING")
PRISMdb = OracleInterface(USER, PSWD, TNS)

logger = logging.getLogger(__name__)

query = "select station, category, point, decode(rtdbtype, 1, 'S', 2, 'T'), attribute from inputxref where keyidx in (select idx from switchparam ) and tablename='SWITCHINPUT' and colname='STASTATUS'"
result = PRISMdb.ExecQuery(query)

rtdb_init()

for station, category, point, rtdbtype, attribute in result:
    addr_stastatus = RtdbAddress(station, category, point, rtdbtype)
    addr_stastatus.analysis_mode = 0
    p_stastatus = RtdbPoint(addr_stastatus)
    value = p_stastatus.read_attr(attribute)
    addr_stastatus.analysis_mode = 1
    p_stastatus = RtdbPoint(addr_stastatus)
    old_value = p_stastatus.read_attr(attribute)
    if value != old_value:
        p_stastatus.write_attr(attribute, value)


