#!/bin/python3.6
"""
:Copyright: © 2022 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
import logging

# Non-System
from acstw.OracleInterface import OracleInterface
from mergemain import MergeMain
from mergesub  import MergeSub

####PARAMETER####
MAINDISTRICT = "TC"
MAINDISTRICT_CODE = "105"

#################
MAINUSER = f"ACS_MAP_{MAINDISTRICT}{MAINDISTRICT_CODE}"
MAINPSWD = "acs"
MAINTNS  = "DASMAP"
MAINMAPDB = OracleInterface(MAINUSER, MAINPSWD, MAINTNS)

logger = logging.getLogger(__name__)


def main():
    from logger import setup_logger
    setup_logger()

    target_dict = dict()
    get_exists_districts_query = """
    SELECT DISTINCT CSV.DISTRICT, CSV.DISTRICT_CODE FROM GIS_BREAKER BRK, REGION_SUBSTATION_XREF CSV 
    WHERE BRK.SWTYPE = 'BFD' AND SUBSTR(BRK.NAME,1,2) = CSV.CODE AND CSV.DISTRICT <> (SELECT SUBSTR(USER,9,2) FROM DUAL) 
                             AND 'ACS_MAP_' || CSV.DISTRICT || CSV.DISTRICT_CODE IN (SELECT USERNAME FROM ALL_USERS)
    """
    SUBDISTRICTSINFO = MAINMAPDB.ExecQuery(get_exists_districts_query)
    for SUBDISTRICT, SUBDISTRICT_CODE in SUBDISTRICTSINFO:
        get_feeders_query = f"""
        SELECT BRK.NAME FROM GIS_BREAKER BRK, REGION_SUBSTATION_XREF CSV 
        WHERE BRK.SWTYPE = 'BFD' AND SUBSTR(BRK.NAME,1,2) = CSV.CODE AND CSV.DISTRICT = '{SUBDISTRICT}' AND CSV.DISTRICT_CODE = {SUBDISTRICT_CODE}
        ORDER BY NAME
        """
        feeders = MAINMAPDB.ExecQuery(get_feeders_query)
        
        SUBMAPDB = f"ACS_MAP_{SUBDISTRICT}{SUBDISTRICT_CODE}"
        SUBPSWD = "acs"
        SUBTNS  = "DASMAP"

        logger.info(f"Using {SUBMAPDB} for merging to {MAINUSER}")

        SUBMAPDB = OracleInterface(SUBMAPDB, SUBPSWD, SUBTNS)

        mergesub = MergeSub(feeders, SUBMAPDB, MAINMAPDB)
        mergesub.get_trace_table()
        mergesub.start()
        mergesub.insert()

        target_dict = {**target_dict, **mergesub.get_name_to_equipment_dict()}
    
    logger.info(f"Start merging feeder to {MAINUSER}")
    mergemain = MergeMain(MAINMAPDB)
    mergemain.get_trace_table()
    mergemain.start()
    mergemain.rebuild_connectivity(target_dict)
    mergemain.delete()

if __name__ == '__main__':
    main()