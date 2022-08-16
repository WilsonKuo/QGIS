#!/bin/python3.6
"""
:Copyright: © 2022 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
import logging

# Non-System
from mergebase import *


logger = logging.getLogger(__name__)


class MergeMain(MergeBase):
    def __init__(self, mainmapdb):
        super(MergeMain, self).__init__()
        self.mainmapdb = mainmapdb
        self.mainuser  = self.mainmapdb.Username
        self.maindistrict_code = self.mainuser[-3:]

    def get_trace_table(self):
        columns  = ["UFID", "FRNODEID", "TONODEID", "FSC", "NAME", "STASTATUS"]

        get_change_substation_query = f"""
        SELECT FSC, UFID FROM GIS_SUBSTATION WHERE NAME IN (SELECT DISTINCT CSV.CODE FROM GIS_BREAKER BRK, REGION_SUBSTATION_XREF CSV 
        WHERE BRK.SWTYPE = 'BFD' AND SUBSTR(BRK.NAME,1,2) = CSV.CODE AND CSV.DISTRICT_CODE != {self.maindistrict_code}) AND TEXTHEIGHT = {self.maindistrict_code}
        """
        substations = self.mainmapdb.ExecQuery(get_change_substation_query)
        self.substations = [(substation[0], substation[1]) for substation in substations]
        for substation in self.substations:
            substationfsc = substation[0]
            substationufid = substation[1]
            self.processdevice[substationfsc].append(substationufid)

        get_change_feeders_query = f"""
        SELECT BRK.NAME FROM GIS_BREAKER BRK, REGION_SUBSTATION_XREF CSV 
        WHERE BRK.SWTYPE = 'BFD' AND SUBSTR(BRK.NAME,1,2) = CSV.CODE AND CSV.DISTRICT_CODE != {self.maindistrict_code}
        ORDER BY NAME
        """
        feeders = self.mainmapdb.ExecQuery(get_change_feeders_query)
        self.feeders = [feeder[0] for feeder in feeders]

        ## Only dealed with date with insert sucessfully
        get_feederlist_query = """
        SELECT {0} FROM GIS_BREAKER WHERE NAME IN ('{1}') AND TEXTHEIGHT = {2} AND NAME IN (SELECT NAME FROM GIS_BREAKER GROUP BY NAME HAVING COUNT(*)>1)
        """.format(",".join(self.columns), "','".join(self.feeders), self.maindistrict_code)
        get_devicelist_query = """
        SELECT {0} FROM  VIEW_ELECTRIC_CONN  WHERE NAME NOT IN (SELECT BRKNAME FROM FEEDER WHERE FDTYPE = 0)
        """.format(",".join(self.columns), "','".join(self.feeders))
        feeders  = self.mainmapdb.ExecQuery(get_feederlist_query)
        feeders  = [ dict(zip(self.columns, row)) for row in feeders ]
        devices  = self.mainmapdb.ExecQuery(get_devicelist_query)
        devices  = [ dict(zip(self.columns, row)) for row in devices ]

        self.initialize_dict(feeders, devices)

    def delete(self):
        for fsc in self.important_fsc:
            logger.info("DELETE {0} which equipments which belongs to {1}".format(self.fsctotable[fsc], self.maindistrict_code))
            repeat = 1
            tempList = []
            for i in range(0, len(self.processdevice[fsc]), 1000):
                for j in range(i, 1000*repeat):
                    if j+1 <= len(self.processdevice[fsc]):
                        tempList.append(str(self.processdevice[fsc][j]))
                query = "DELETE {0} WHERE UFID IN ({1})".format(self.fsctotable[fsc], ",".join(tempList))
                self.mainmapdb.ExecNonQuery(query)
                tempList = []
                repeat += 1
    
    def rebuild_connectivity(self, target_dict):
        source_dict = dict()
        for fsc in self.processdevice:
            for ufid in self.processdevice[fsc]:
                if ufid in self.devicedict.keys():
                    source_dict[self.devicedict[ufid].normalized_name] = self.devicedict[ufid]


        for devicename in target_dict:
            if devicename in source_dict.keys():
                source = source_dict[devicename]
                target = target_dict[devicename]
                if target.fsc == source.fsc and target.fsc in (108, 114):
                    logger.info(f"Rebuild {devicename}'s connectivity")
                    if source.flowdir == 0:
                        if target.flowdir == 0:
                            logger.info("update source tonodeid to target tonodeid")
                            self.mainmapdb.ExecNonQuery("UPDATE {0} SET TONODEID = {1} WHERE UFID = {2}".format(self.fsctotable[target.fsc], source.tonodeid, target.ufid))
                        elif  target.flowdir == 1:
                            logger.info("update source tonodeid to target frnodeid")
                            self.mainmapdb.ExecNonQuery("UPDATE {0} SET FRNODEID = {1} WHERE UFID = {2}".format(self.fsctotable[target.fsc], source.tonodeid, target.ufid))
                        else:
                            logger.info("problematic equipment 1")
                    elif source.flowdir == 1:
                        if target.flowdir == 0:
                            logger.info("update source frnodeid to target tonodeid")
                            self.mainmapdb.ExecNonQuery("UPDATE {0} SET TONODEID = {1} WHERE UFID = {2}".format(self.fsctotable[target.fsc], source.frnodeid, target.ufid))
                        elif  target.flowdir == 1:
                            logger.info("update source frnodeid to target frnodeid")
                            self.mainmapdb.ExecNonQuery("UPDATE {0} SET FRNODEID = {1} WHERE UFID = {2}".format(self.fsctotable[target.fsc], source.frnodeid, target.ufid))
                        else:
                            logger.info("problematic equipment 2")
                    else:
                        logger.info("problematic equipment 3")
