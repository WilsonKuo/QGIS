#!/bin/python3.6
"""
:Copyright: © 2022 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
import logging


# Non-System
from device import Device

# sys.setrecursionlimit(2000)


logger = logging.getLogger(__name__)

class MergeBase:
    def __init__(self):
        self.nodeiddict       = dict()
        self.feederdict       = dict()
        self.devicedict       = dict()
        self.visiteddict      = dict()
        self.conndict         = dict()
        self.processdevice    = dict()


        self.columns  = ["UFID", "FRNODEID", "TONODEID", "FSC", "NAME", "STASTATUS"]

        self.fsctotable = dict()
        self.fsctotable[102]  = "GIS_CAPACITOR"
        self.fsctotable[106]  = "GIS_CONDUCTOR"
        self.fsctotable[108]  = "GIS_BREAKER"
        self.fsctotable[114]  = "GIS_SWITCH"
        self.fsctotable[115]  = "GIS_LOADTRANSFORMER"
        self.fsctotable[131]  = "GIS_SUBSTATION"
        self.fsctotable[4321] = "GIS_GENERATOR"
        self.important_fsc = [102, 106, 108, 114, 115, 4321, 131]
        
        for fsc in self.important_fsc:
            self.processdevice[fsc] = list()
    
    def get_trace_table(self):
        raise NotImplementedError

    def initialize_dict(self, feeders, devices):

        for feeder in feeders:
            frnodeid    = feeder['FRNODEID']
            tonodeid    = feeder['TONODEID']
            feederufid  = feeder['UFID']
            self.feederdict[feederufid] = (Device(feeder))


        for device in devices:
            frnodeid    = device['FRNODEID']
            tonodeid    = device['TONODEID']
            deviceufid  = device['UFID']
            if frnodeid not in self.nodeiddict.keys():
                self.nodeiddict[frnodeid] = list()
            if tonodeid not in self.nodeiddict.keys():
                self.nodeiddict[tonodeid] = list()
            # 0 = frnode, 1 = tonodeid
            self.nodeiddict[frnodeid].append((deviceufid, 0))
            self.nodeiddict[tonodeid].append((deviceufid, 1))
            self.devicedict[deviceufid] = Device(device)

    def trace(self, inDEVICEUFID, inNODEID):
        if inNODEID in self.nodeiddict.keys():
            for deviceufid, fromto in self.nodeiddict[inNODEID]:
                device = self.devicedict[deviceufid]
                if deviceufid != inDEVICEUFID:
                    if deviceufid not in self.visiteddict.keys():
                        self.processdevice[device.fsc].append(device.ufid)
                        self.visiteddict[deviceufid] = dict()
                        # logger.debug(device.name + ' ' + str(device.ufid) + "\n")
                        self.visiteddict[deviceufid] = True
                        if fromto == 0:
                            device.flowdir = 0
                            if device.stastatus != 0:
                                if device.frnodeid == 0 or device.tonodeid == 0:
                                    # meet load or capacitor
                                    pass
                                else:
                                    self.trace(deviceufid, device.tonodeid)
                        else:
                            device.flowdir = 1
                            if device.stastatus != 0:
                                if device.frnodeid == 0 or device.tonodeid == 0:
                                    # meet load or capacitor
                                    pass
                                else:
                                    self.trace(deviceufid, device.frnodeid)

                    else:
                        ###################prevent back trace at source
                        pass

            # else:
            #     logger.info("back trace")

    def start(self):
        for feederufid in self.feederdict:
            logger.info(f"START AT {self.feederdict[feederufid].name}")
            self.processdevice[self.feederdict[feederufid].fsc].append(self.feederdict[feederufid].ufid)
            self.trace(self.feederdict[feederufid].ufid, self.feederdict[feederufid].tonodeid)
        logger.info(f"Trace is done")

