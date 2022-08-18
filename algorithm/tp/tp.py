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
# from multiprocessing.managers import SyncManager

# Non-System
from acsprism import RtdbAddress,RtdbPoint
from acsprism.getchanges import GetChanges
from acstw.OracleInterface import OracleInterface
from equipment import Equipment

USER = os.getenv("ORACLE_USER")
PSWD = os.getenv("ORACLE_PW")
TNS  = os.getenv("ORACLE_DBSTRING")
PRISMdb = OracleInterface(USER, PSWD, TNS)

logger = logging.getLogger(__name__)

# USER = os.getenv("ORACLE_USER_BASEDB")
# PSWD = os.getenv("ORACLE_PW_BASEDB")
# TNS  = os.getenv("ORACLE_DBSTRING_BASEDB")
# MAPdb = OracleInterface(USER, PSWD, TNS)

# logger.info(sys.getrecursionlimit())
sys.setrecursionlimit(5000)

__author__ = 'Wilson Kuo'


# class MyManager(SyncManager):
#     pass
# MyManager.register("syncdict")

class Topology:
    def __init__(self, analysis_mode):

        self.analysis_mode = analysis_mode
        logger.info("analysis_mode = {0}".format(self.analysis_mode))
        self.retrace_rate   = 1 # s
        logger.info("retrace_rate  = {0}".format(self.retrace_rate))
        logger.info("START INITIALIZING DASDB")
        # sources = [{'UFID': 1,  'FRNODEID': 0  , 'TONODEID': 100, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 1, 'RTDBTYPE': 1},
        #         {'UFID': 2,  'FRNODEID': 0  , 'TONODEID': 200, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 2, 'RTDBTYPE': 1}
        #         ]
        # equipments = [{'UFID': 3,  'FRNODEID': 100, 'TONODEID': 101, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 2},
        #         {'UFID': 4,  'FRNODEID': 101, 'TONODEID': 102, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 1},
        #         {'UFID': 5,  'FRNODEID': 110, 'TONODEID': 111, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 1},
        #         {'UFID': 6,  'FRNODEID': 100, 'TONODEID': 110, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 2},
        #         {'UFID': 7,  'FRNODEID': 102, 'TONODEID': 103, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 2},
        #         {'UFID': 8,  'FRNODEID': 103, 'TONODEID': 104, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 1},
        #         {'UFID': 9,  'FRNODEID': 112, 'TONODEID': 999, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 1},
        #         {'UFID': 10, 'FRNODEID': 111, 'TONODEID': 999, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 2},
        #         {'UFID': 11, 'FRNODEID': 102, 'TONODEID': 112, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 2},
        #         {'UFID': 12, 'FRNODEID': 131, 'TONODEID': 132, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 1},
        #         {'UFID': 13, 'FRNODEID': 999, 'TONODEID': 132, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 2},
        #         {'UFID': 14, 'FRNODEID': 201, 'TONODEID': 202, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 1},
        #         {'UFID': 15, 'FRNODEID': 202, 'TONODEID': 131, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 2},
        #         {'UFID': 16, 'FRNODEID': 200, 'TONODEID': 201, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 2},
        #         {'UFID': 17, 'FRNODEID': 200, 'TONODEID': 210, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 2},
        #         {'UFID': 18, 'FRNODEID': 210, 'TONODEID': 211, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 1},
        #         {'UFID': 19, 'FRNODEID': 212, 'TONODEID': 213, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 1},
        #         {'UFID': 20, 'FRNODEID': 211, 'TONODEID': 212, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 2},
        #         {'UFID': 21, 'FRNODEID': 111, 'TONODEID': 132, 'STATION': 100, 'CATEGORY': 'R', 'POINT': 3, 'RTDBTYPE': 2}
        #         ]

        columns  = ["UFID", "FRNODEID", "TONODEID", "FSC", "NAME", "COLORCODE"]
        columns += ["STATION", "CATEGORY", "POINT", "RTDBTYPE", "ATTRIBUTE" ]
        query   = "SELECT {0} FROM  VIEW_TB_TP_XREF WHERE NAME IN (SELECT NAME FROM SWITCHPARAM WHERE DEVTYPE = 4) AND FSC = 108 ORDER BY NAME".format(",".join(columns))
        sources = PRISMdb.ExecQuery(query)
        sources = [ dict(zip(columns, row)) for row in sources ]
        
        columns  = ["UFID", "FRNODEID", "TONODEID", "FSC", "NAME"]
        columns += ["STATION", "CATEGORY", "POINT", "RTDBTYPE", "ATTRIBUTE" ]
        query   = "SELECT {0} FROM  VIEW_TB_TP_XREF  WHERE NAME NOT IN (SELECT NAME FROM SWITCHPARAM WHERE DEVTYPE >= 4)".format(",".join(columns))
        equipments = PRISMdb.ExecQuery(query)
        equipments = [ dict(zip(columns, row)) for row in equipments ]

        #static
        self.sourcelist          = list()
        self.sourcedict          = dict()
        self.nodeiddict          = dict()
        self.ufid_to_namedict    = dict()
        self.address_to_ufid     = dict()
        
        
        #dynamic
        self.equipmentdict       = dict()
        self.visiteddict         = dict()
        self.sourcedownstream    = dict()
        self.openswitchdict      = dict()
        self.sourcetree          = dict()
        self.loopidx             = 0
        self.sourceinlooparea    = dict()
        self.equipmentinlooparea = dict()
        self.betweenlooparea     = list()
        self.equipmentbetweenlooparea = dict()
        self.changeequipmentlist = list()



        for source in sources:
            sourceufid = source['UFID']
            station    = source['STATION' ]
            category   = source['CATEGORY']
            point      = source['POINT'] 
            rtdbtype   = source['RTDBTYPE']
            self.ufid_to_namedict[source['UFID']] = source['NAME']
            self.sourcelist.append(Equipment(source, self.analysis_mode))
            self.sourcedict[sourceufid] = Equipment(source, self.analysis_mode)
            self.sourceinlooparea[sourceufid] = dict()
            self.sourcedownstream[sourceufid] = set()
            self.sourcedict[sourceufid].sourceufiddict[sourceufid] = True
            self.address_to_ufid[(station, category, point, rtdbtype)] = sourceufid
        for equipment in equipments:
            frnodeid = equipment['FRNODEID']
            tonodeid = equipment['TONODEID']
            station  = equipment['STATION' ]
            category = equipment['CATEGORY']
            point    = equipment['POINT'] 
            rtdbtype = equipment['RTDBTYPE']
            equipmentufid  = equipment['UFID']
            equipmentfsc  = equipment['FSC']
            self.ufid_to_namedict[equipment['UFID']] = equipment['NAME']
            if frnodeid not in self.nodeiddict.keys():
                self.nodeiddict[frnodeid] = list()
            if tonodeid not in self.nodeiddict.keys():
                self.nodeiddict[tonodeid] = list()
            # 0 = frnode, 1 = tonodeid
            self.nodeiddict[frnodeid].append((equipmentufid, 0))
            self.nodeiddict[tonodeid].append((equipmentufid, 1))
            self.equipmentdict[equipmentufid] = Equipment(equipment, self.analysis_mode)
            self.address_to_ufid[(station, category, point, rtdbtype)] = equipmentufid
            equipment = self.equipmentdict[equipmentufid]
            #if equipment.colorcode != 0:
            #    equipment.colorcode = 0

        logger.info("INITIALIZING DASDB AND LINE COLORCODE IS DONE")
        # self.threads = list()
    
    # Recursive
    def inloop(self, inEQUIPMENT, inSOURCEUFID, inVISITEDUFID):
        self.sourceinlooparea[inSOURCEUFID][inEQUIPMENT.ufid] = True
        if inEQUIPMENT.ufid not in self.equipmentinlooparea.keys():
            self.equipmentinlooparea[inEQUIPMENT.ufid] = dict()
        if inSOURCEUFID not in self.equipmentinlooparea[inEQUIPMENT.ufid].keys():
            self.equipmentinlooparea[inEQUIPMENT.ufid][inSOURCEUFID] = True

        if inEQUIPMENT.ufid != inVISITEDUFID:
            if inSOURCEUFID != inEQUIPMENT.parentufiddict[inSOURCEUFID]:
                self.inloop(self.equipmentdict[inEQUIPMENT.parentufiddict[inSOURCEUFID]], inSOURCEUFID, inVISITEDUFID)


    # Recursive
    def trace(self, inEQUIPMENTUFID, inNODEID, inSOURCEUFID, inNONLINEUFID):
        if inNODEID in self.nodeiddict.keys():
            for equipmentufid, fromto in self.nodeiddict[inNODEID]:
                equipment = self.equipmentdict[equipmentufid]
                source = self.sourcedict[inSOURCEUFID]
                if equipmentufid != inEQUIPMENTUFID:
                    if equipmentufid not in self.visiteddict.keys():
                        self.visiteddict[equipmentufid] = dict()
                    if source.ufid not in self.visiteddict[equipmentufid].keys():
                        logger.debug(equipment.name + ' ' + str(equipment.ufid) + "\n")
                        self.visiteddict[equipmentufid][source.ufid] = True
                        if source.ufid not in self.sourcedownstream.keys():
                            self.sourcedownstream[source.ufid] = set()
                        self.sourcedownstream[source.ufid].add(equipmentufid)
                        equipment.parentufiddict[source.ufid] = inEQUIPMENTUFID
                        equipment.nonlineparentufiddict[source.ufid] = inNONLINEUFID
                        equipment.sourceufiddict[source.ufid] = True
                        if equipment.stastatus == 1:
                            if equipment.frnodeid == 0 or equipment.tonodeid == 0:
                                # meet load or capacitor
                                pass
                            else:
                                if fromto == 0:
                                    if equipment.fsc in (108, 114):
                                        self.trace(equipmentufid, equipment.tonodeid, source.ufid, equipment.ufid)
                                    else:
                                        self.trace(equipmentufid, equipment.tonodeid, source.ufid, inNONLINEUFID)
                                    
                                else:
                                    if equipment.fsc in (108, 114):
                                        self.trace(equipmentufid, equipment.frnodeid, source.ufid, equipment.ufid)
                                    else:
                                        self.trace(equipmentufid, equipment.frnodeid, source.ufid, inNONLINEUFID)
                    else:
                        ###################prevent back trace at source
                        if inEQUIPMENTUFID != source.ufid:
                            self.inloop(self.equipmentdict[inEQUIPMENTUFID], source.ufid, equipmentufid)

            # else:
            #     logger.info("back trace")

    def retrace(self, inSOURCEUFID, inNEWCOLOREQUIPMENTDICT):
        # init
        pre_sourcedownstream = self.sourcedownstream[inSOURCEUFID]
        source = self.sourcedict[inSOURCEUFID]
        for downstreamequipmentufid in self.sourcedownstream[source.ufid] :
            equipment = self.equipmentdict[downstreamequipmentufid]
            del self.visiteddict[downstreamequipmentufid][source.ufid]
            del equipment.parentufiddict[source.ufid]
            del equipment.nonlineparentufiddict[source.ufid]
            del equipment.sourceufiddict[source.ufid]
            if inSOURCEUFID in self.sourceinlooparea[source.ufid].keys():
                if downstreamequipmentufid in self.sourceinlooparea[source.ufid].keys():
                    del self.sourceinlooparea[source.ufid][downstreamequipmentufid]
            if downstreamequipmentufid in self.equipmentinlooparea.keys():
                if source.ufid in self.equipmentinlooparea[downstreamequipmentufid].keys():
                    del self.equipmentinlooparea[downstreamequipmentufid][inSOURCEUFID]
                    if len(self.equipmentinlooparea[downstreamequipmentufid]) == 0:
                        del self.equipmentinlooparea[downstreamequipmentufid]
                        # print(f"remove {downstreamequipmentufid} from equipmentinlooparea")


        self.sourcedownstream[source.ufid] = set()
        if source.stastatus == 1:
            self.trace(source.ufid, source.tonodeid, source.ufid, source.ufid)
        else:
            logger.info(f"{source.name} source open, ignore!")

        for nonoutageequipmentufid in self.sourcedownstream[source.ufid]:
            equipment = self.equipmentdict[nonoutageequipmentufid]
            inNEWCOLOREQUIPMENTDICT[nonoutageequipmentufid] = source.colorcodebook
        
        for outageequipmentufid in (pre_sourcedownstream - self.sourcedownstream[source.ufid]):
            if outageequipmentufid not in inNEWCOLOREQUIPMENTDICT.keys():
                inNEWCOLOREQUIPMENTDICT[outageequipmentufid] = 0


        logger.info("{0} retrace is done".format(source.name))

    def import_tp_result_to_db(self, import_mode, readytoupdatelist):
        
        tmp_arr = list()
        
        if import_mode == "INC":
            ###ORA-01795: maximum number of expressions in a list is 1000
            repeat = 1
            tempList = []
            for i in range(0, len(readytoupdatelist), 1000):
                for j in range(i, 1000*repeat):
                    if j+1 <= len(readytoupdatelist):
                        tempList.append(str(readytoupdatelist[j]))
                query = "DELETE TB_TP WHERE UFID IN ({0})".format(",".join(tempList))
                PRISMdb.ExecNonQuery(query)
                tempList = []
                repeat += 1

        else:
            query = "TRUNCATE TABLE TB_TP"
            PRISMdb.ExecNonQuery(query)
            
        for equipmentufid in readytoupdatelist:
            equipment = self.equipmentdict[equipmentufid]
            arr = [(self.ufid_to_namedict[sourceufid], self.ufid_to_namedict[equipment.nonlineparentufiddict[sourceufid]], self.ufid_to_namedict[equipment.parentufiddict[sourceufid]]) for sourceufid in equipment.sourceufiddict]
            arr_size = len(arr)
            #####################################################################
            # flag = -1:outage, 0:normal, 1:normal open, 2:inloop, 3:betweenloop#
            #####################################################################
            if arr_size > 1:
                if equipment.ufid in self.equipmentbetweenlooparea.keys():
                    flag = 3
                else:
                    flag = 1
                tmp_arr.append([equipment.ufid, equipment.fsc, equipment.name, equipment.stastatus, arr[0][0], arr[0][1], arr[0][2], arr[1][0], arr[1][1], arr[1][2], flag])
            elif arr_size == 1:
                if equipment.ufid in self.equipmentinlooparea.keys():
                    flag = 2
                else:
                    flag = 0
                tmp_arr.append([equipment.ufid, equipment.fsc, equipment.name, equipment.stastatus, arr[0][0], arr[0][1], arr[0][2], None, None, None, flag])
            else:
                flag = -1
                tmp_arr.append([equipment.ufid, equipment.fsc, equipment.name, equipment.stastatus, None, None, None, None, None, None, flag])
        colStr = 'UFID,FSC,NAME,STATUS,FEEDER1,FEEDER1_NONLINEPARENT,FEEDER1_PARENT,FEEDER2,FEEDER2_NONLINEPARENT,FEEDER2_PARENT,FLAG'
        valPlaceholder = ":0,:1,:2,:3,:4,:5,:6,:7,:8,:9,:10"
        insSql = "insert /* array */ into %s (%s) values (%s)" % ('TB_TP', colStr, valPlaceholder)
        PRISMdb.InsertArray(insSql,tmp_arr)
        logger.info(f'{import_mode} Insert data successfully!')
    


    def job1(self):
        starttime = datetime.now()
        len_sourcelist = len(self.sourcelist)
        for idx, source in enumerate(self.sourcelist):
            logger.info('START AT {0} {1}/{2}'.format(source.name, idx + 1, len_sourcelist))
            if source.stastatus == 1:
                self.trace(source.ufid, source.tonodeid, source.ufid, source.ufid)
            else:
                logger.info(f"{source.name} source open, ignore!")
        endtime = datetime.now()
        logger.info(endtime - starttime)
        logger.info("first trace is done")
        
        loopset = set()
        for equipmentufid in self.visiteddict.keys():
            if len(self.visiteddict[equipmentufid]) > 1:
                if self.equipmentdict[equipmentufid].stastatus != 1:
                    self.openswitchdict[equipmentufid] = True
                else:
                    loopset.add('-'.join([self.sourcedict[sourceufid].name for sourceufid in self.visiteddict[equipmentufid].keys()]))
                    self.betweenlooparea.append((equipmentufid, self.visiteddict[equipmentufid]))
                    self.equipmentbetweenlooparea[equipmentufid] = self.visiteddict[equipmentufid]
        for loop in loopset:
            logger.info("between loop :{0}".format(loop))

        # for sourceufid, downstreamequipmentufid in self.sourcedownstream.items():
        #     for equipmentufid in downstreamequipmentufid:
        #         equipment = self.equipmentdict[equipmentufid]
        #         source    = self.sourcedict[sourceufid]
        #         if equipment.colorcode == 0:
        #             """ write rtdb will slow down trace process, so I batch write the colorcode"""
        #             """ colorize correctly??,  need to check """
        #             equipment.colorcode = source.colorcodebook

        self.import_tp_result_to_db("BULK", list(self.equipmentdict.keys()))

        endtime2 = datetime.now()
        logger.info(endtime2 - endtime)
        # logger.info("colorize is done")
    
    def job2(self):
        logger.info("Start Detecting RTDB change...")
        detect_change = GetChanges()
        update_rate = 5000 # ms
        tmp_update_rate = update_rate
        while True:
            tmp_update_rate -= 1
            if tmp_update_rate == 0:
                tmp_update_rate = update_rate
            message = detect_change.get_next_point_change(True)
            if message:
                if message.attr_code == 128:
                    if message.address_tuple in self.address_to_ufid.keys():
                        if self.address_to_ufid[message.address_tuple] in self.equipmentdict.keys():
                            self.changeequipmentlist.append(self.equipmentdict[self.address_to_ufid[message.address_tuple]])
                        else:
                            self.changeequipmentlist.append(self.sourcedict[self.address_to_ufid[message.address_tuple]])
                    else:
                        logger.info(message.address_tuple)
                        logger.info("change point not in dasdb")

            time.sleep(0.001)
    

    def start(self):
        """                                                                                """
        """ Sourcedownstream list index is not equal to level because dfs!!!!!!!!!!!!!!!!! """
        """                                                                                """
        
        logger.info("Start Detecting RTDB change and  First trace")
        firsttrace = threading.Thread(target = self.job1)
        firsttrace.start()
        getchanges  = threading.Thread(target = self.job2)
        getchanges.start()
        firsttrace.join()
        


        while True:
            logger.info("--->>>TpFunc Print: Count: 0 <<<---")
            pre_changeequipmentsourcecntdict = dict()
            len_changeequipmentlist          = len(self.changeequipmentlist)
            if len_changeequipmentlist:
                logger.info("--->>>TpFunc Print: Count: {0} <<<---".format(len_changeequipmentlist))
                # 1
                newcolorequipmentdict = dict()
                retracesourceufidlist = set()
                for changeequipment in self.changeequipmentlist[0 : len_changeequipmentlist]:
                    pre_changeequipmentsourcecntdict[changeequipment.ufid] = 0
                    for sourceufid in changeequipment.sourceufiddict.keys():
                        retracesourceufidlist.add(sourceufid)
                        pre_changeequipmentsourcecntdict[changeequipment.ufid] += 1
                for retracesourceufid in retracesourceufidlist:
                    self.retrace(retracesourceufid, newcolorequipmentdict)

                # for equipmentufid, colorcodebook in newcolorequipmentdict.items():
                #     equipment = self.equipmentdict[equipmentufid]
                #     equipment.colorcode = colorcodebook


                # 2
                self.openswitchdict  = dict()
                self.betweenlooparea = list()
                self.equipmentbetweenlooparea = dict()
                for equipmentufid in self.visiteddict.keys():
                    if len(self.visiteddict[equipmentufid]) > 1:
                        if self.equipmentdict[equipmentufid].stastatus != 1:
                            self.openswitchdict[equipmentufid] = True
                        else:
                            self.betweenlooparea.append((equipmentufid, self.visiteddict[equipmentufid]))
                            self.equipmentbetweenlooparea[equipmentufid] = self.visiteddict[equipmentufid]

                for changeequipment in self.changeequipmentlist[0 : len_changeequipmentlist]:
                    new_changeequipmentsourcecnt = len(changeequipment.sourceufiddict)
                    changeequipmentstastatus    = changeequipment.stastatus
                    if pre_changeequipmentsourcecntdict[changeequipment.ufid] > 1 and new_changeequipmentsourcecnt <= 2 and changeequipmentstastatus != 1:
                        logger.info("{0} break the loop".format(changeequipment.ufid))
                    elif pre_changeequipmentsourcecntdict[changeequipment.ufid] >= 1 and new_changeequipmentsourcecnt > 1 and changeequipmentstastatus == 1:
                        logger.info("{0} cause the loop".format(changeequipment.ufid))


                self.changeequipmentlist = self.changeequipmentlist[len_changeequipmentlist : None]

                if len_changeequipmentlist < 10:
                    self.import_tp_result_to_db("INC", list(newcolorequipmentdict.keys()))
                else:
                    self.import_tp_result_to_db("BULK", list(self.equipmentdict.keys()))


            time.sleep(self.retrace_rate)
    
    def stop(self):
        logger.info("WITHIN LOOP")
        # logger.info(self.sourceinlooparea)
        # logger.info(self.equipmentinlooparea)
        # logger.info("BETWEEN LOOP")
        # logger.info(self.betweenlooparea)
        # logger.info("OPEN SWITCH")
        # logger.info(len(self.openswitchdict))
        # logger.info(len(self.visiteddict))

        

def main():
    from acsprism import rtdb_init
    from logger import setup_logger
    setup_logger()
    rtdb_init()
    tp = Topology(analysis_mode = 0)
    tp.start()
    tp.stop()

if __name__ == '__main__':
    main()
