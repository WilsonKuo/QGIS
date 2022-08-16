#!/bin/python3.6
"""
:Copyright: © 2022 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
import logging

# Non-System
from mergebase import *


logger = logging.getLogger(__name__)

class MergeSub(MergeBase):
    def __init__(self, feeders, submapdb, mainmapdb):
        super(MergeSub, self).__init__()
        self.submapdb  = submapdb
        self.mainmapdb = mainmapdb
        self.subuser   = self.submapdb.Username
        self.mainuser  = self.mainmapdb.Username
        self.subdistrict_code  = self.subuser[-3:]
        self.maindistrict_code = self.mainuser[-3:]

        self.feeders   = [feeder[0] for feeder in feeders]

    def get_trace_table(self):
        columns  = ["UFID", "FRNODEID", "TONODEID", "FSC", "NAME", "STASTATUS"]

        get_change_substation_query = f"""
        SELECT FSC, UFID FROM {self.subuser}.GIS_SUBSTATION WHERE NAME IN (SELECT DISTINCT CSV.CODE FROM GIS_BREAKER BRK, REGION_SUBSTATION_XREF CSV 
        WHERE BRK.SWTYPE = 'BFD' AND SUBSTR(BRK.NAME,1,2) = CSV.CODE AND CSV.DISTRICT_CODE = {self.subdistrict_code} AND BRK.TEXTHEIGHT = {self.maindistrict_code})
        """
        substations = self.mainmapdb.ExecQuery(get_change_substation_query)
        self.substations = [(substation[0], substation[1]) for substation in substations]
        for substation in self.substations:
            substationfsc = substation[0]
            substationufid = substation[1]
            self.processdevice[substationfsc].append(substationufid)

        get_feederlist_query = """
        SELECT {0} FROM GIS_BREAKER WHERE NAME IN ('{1}')
        """.format(",".join(columns), "','".join(self.feeders))

        get_devicelist_query = """
        SELECT {0} FROM  VIEW_ELECTRIC_CONN  WHERE NAME NOT IN (SELECT BRKNAME FROM FEEDER WHERE FDTYPE = 0)
        """.format(",".join(columns), "','".join(self.feeders))
        
        feeders  = self.submapdb.ExecQuery(get_feederlist_query)
        feeders  = [ dict(zip(self.columns, row)) for row in feeders ]
        devices  = self.submapdb.ExecQuery(get_devicelist_query)
        devices  = [ dict(zip(self.columns, row)) for row in devices ]

        self.initialize_dict(feeders, devices)

    def insert(self):
        
        logger.info(f"Delete equipments which belongs to {self.subdistrict_code}")

        for fsc in self.important_fsc:
            logger.info("INSERT {0} which equipments which belongs to {1}".format(self.fsctotable[fsc], self.subdistrict_code))
            query = f"DELETE {self.fsctotable[fsc]} WHERE TEXTHEIGHT = {self.subdistrict_code}"
            self.mainmapdb.ExecNonQuery(query)

        logger.info(f"Insert equipments which belongs to {self.subdistrict_code}")
        for fsc in self.important_fsc:
            logger.info("INSERT {0} which equipments which belongs to {1}".format(self.fsctotable[fsc], self.subdistrict_code))
            repeat = 1
            tempList = []
            for i in range(0, len(self.processdevice[fsc]), 1000):
                for j in range(i, 1000*repeat):
                    if j+1 <= len(self.processdevice[fsc]):
                        tempList.append(str(self.processdevice[fsc][j]))
                query = "INSERT INTO {0} SELECT * FROM {1}.{0} WHERE UFID IN ({2})".format(self.fsctotable[fsc], self.subuser, ",".join(tempList))
                self.mainmapdb.ExecNonQuery(query)
                tempList = []
                repeat += 1

        logger.info(f"Successfully insert equipments which belongs to {self.subdistrict_code}")

    def get_name_to_equipment_dict(self):
        tmp_dict = dict()
        for fsc in self.processdevice:
            for ufid in self.processdevice[fsc]:
                if ufid in self.devicedict.keys():
                    tmp_dict[self.devicedict[ufid].normalized_name] = self.devicedict[ufid]
                else:
                    tmp_dict[self.feederdict[ufid].normalized_name] = self.feederdict[ufid]
        return tmp_dict