#!/bin/python3.6
from math import sqrt
from acsprism import RtdbAddress, RtdbPoint

class NewInitCaller(type):
    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        obj.new_init()
        return obj

class TTUInfo(object, metaclass = NewInitCaller):
    def __init__(self, dataSet):
        self.dataSet = dataSet
    
    def new_init(self):

        try:
            self.addr_pa = RtdbAddress(self.station_pa, self.category_pa, self.point_pa, self.rtdbtype_pa)
            self.p_pa = RtdbPoint(self.addr_pa)
        except:
            self.p_pa = None
        try:
            self.addr_pb = RtdbAddress(self.station_pb, self.category_pb, self.point_pb, self.rtdbtype_pb)
            self.p_pb = RtdbPoint(self.addr_pb)
        except:
            self.p_pb = None
        try:
            self.addr_pc = RtdbAddress(self.station_pc, self.category_pc, self.point_pc, self.rtdbtype_pc)
            self.p_pc = RtdbPoint(self.addr_pc)
        except:
            self.p_pc = None
        try:
            self.addr_qa = RtdbAddress(self.station_qa, self.category_qa, self.point_qa, self.rtdbtype_qa)
            self.p_qa = RtdbPoint(self.addr_qa)
        except:
            self.p_qa = None
        try:
            self.addr_qb = RtdbAddress(self.station_qb, self.category_qb, self.point_qb, self.rtdbtype_qb)
            self.p_qb = RtdbPoint(self.addr_qb)
        except:
            self.p_qb = None
        try:
            self.addr_qc = RtdbAddress(self.station_qc, self.category_qc, self.point_qc, self.rtdbtype_qc)
            self.p_qc = RtdbPoint(self.addr_qc)
        except:
            self.p_qc = None
            
        try:
            self.addr_flag1 = RtdbAddress(self.station_flag1, self.category_flag1, self.point_flag1, self.rtdbtype_flag1)
            self.p_flag1 = RtdbPoint(self.addr_flag1)
        except:
            self.p_flag1 = None
        try:
            self.addr_flag2 = RtdbAddress(self.station_flag2, self.category_flag2, self.point_flag2, self.rtdbtype_flag2)
            self.p_flag2 = RtdbPoint(self.addr_flag2)
        except:
            self.p_flag2 = None
        try:
            self.addr_flag3 = RtdbAddress(self.station_flag3, self.category_flag3, self.point_flag3, self.rtdbtype_flag3)
            self.p_flag3 = RtdbPoint(self.addr_flag3)
        except:
            self.p_flag3 = None
        try:
            self.addr_flag4 = RtdbAddress(self.station_flag4, self.category_flag4, self.point_flag4, self.rtdbtype_flag4)
            self.p_flag4 = RtdbPoint(self.addr_flag4)
        except:
            self.p_flag4 = None

    def init_val(self):
        if self.p_flag3:
            self.p_flag3.write_attr(self.attribute_flag3, 0)
        if self.p_flag4:
            self.p_flag4.write_attr(self.attribute_flag4, 0)

    @property
    def name(self):
        return self.dataSet['TTU_NAME']
        
    @property
    def display_number(self):
        if self.dataSet['DISPLAY_NUMBER']:
            return self.dataSet['DISPLAY_NUMBER']
        else:
            return 84001
    @property
    def capacity(self):
        return self.dataSet['CAPACITY']

    @property
    def station_pa(self):
        return self.dataSet['STATION_PA']
    @property
    def category_pa(self):
        return self.dataSet['CATEGORY_PA']
    @property
    def point_pa(self):
        return self.dataSet['POINT_PA']
    @property
    def rtdbtype_pa(self):
        return self.dataSet['RTDBTYPE_PA']
    @property
    def attribute_pa(self):
        return self.dataSet['ATTRIBUTE_PA']
    @property
    def addrstring_pa(self):
        try:
            return ",".join([str(value) for value in self.addr_pa.as_tuple()])
        except:
            return ''
    @property
    def pa(self):
        if self.p_pa:
            return round(self.p_pa.read_attr(self.attribute_pa), 6)
        else:
            return 0

    @property
    def station_pb(self):
        return self.dataSet['STATION_PB']
    @property
    def category_pb(self):
        return self.dataSet['CATEGORY_PB']
    @property
    def point_pb(self):
        return self.dataSet['POINT_PB']
    @property
    def rtdbtype_pb(self):
        return self.dataSet['RTDBTYPE_PB']
    @property
    def attribute_pb(self):
        return self.dataSet['ATTRIBUTE_PB']
    @property
    def addrstring_pb(self):
        try:
            return ",".join([str(value) for value in self.addr_pb.as_tuple()])
        except:
            return ''
    @property
    def pb(self):
        if self.p_pb:
            return round(self.p_pb.read_attr(self.attribute_pb), 6)
        else:
            return 0

    @property
    def station_pc(self):
        return self.dataSet['STATION_PC']
    @property
    def category_pc(self):
        return self.dataSet['CATEGORY_PC']
    @property
    def point_pc(self):
        return self.dataSet['POINT_PC']
    @property
    def rtdbtype_pc(self):
        return self.dataSet['RTDBTYPE_PC']
    @property
    def attribute_pc(self):
        return self.dataSet['ATTRIBUTE_PC']
    @property
    def addrstring_pc(self):
        try:
            return ",".join([str(value) for value in self.addr_pc.as_tuple()])
        except:
            return ''
    @property
    def pc(self):
        if self.p_pc:
            return round(self.p_pc.read_attr(self.attribute_pc), 6)
        else:
            return 0

    @property
    def station_qa(self):
        return self.dataSet['STATION_QA']
    @property
    def category_qa(self):
        return self.dataSet['CATEGORY_QA']
    @property
    def point_qa(self):
        return self.dataSet['POINT_QA']
    @property
    def rtdbtype_qa(self):
        return self.dataSet['RTDBTYPE_QA']
    @property
    def attribute_qa(self):
        return self.dataSet['ATTRIBUTE_QA']
    @property
    def addrstring_qa(self):
        try:
            return ",".join([str(value) for value in self.addr_pa.as_tuple()])
        except:
            return ''
    @property
    def qa(self):
        if self.p_qa:
            return round(self.p_qa.read_attr(self.attribute_qa), 6)
        else:
            return 0

    @property
    def station_qb(self):
        return self.dataSet['STATION_QB']
    @property
    def category_qb(self):
        return self.dataSet['CATEGORY_QB']
    @property
    def point_qb(self):
        return self.dataSet['POINT_QB']
    @property
    def rtdbtype_qb(self):
        return self.dataSet['RTDBTYPE_QB']
    @property
    def attribute_qb(self):
        return self.dataSet['ATTRIBUTE_QB']
    @property
    def addrstring_qb(self):
        try:
            return ",".join([str(value) for value in self.addr_qb.as_tuple()])
        except:
            return ''
    @property
    def qb(self):
        if self.p_qb:
            return round(self.p_qb.read_attr(self.attribute_qb), 6)
        else:
            return 0                                    

    @property
    def station_qc(self):
        return self.dataSet['STATION_QC']
    @property
    def category_qc(self):
        return self.dataSet['CATEGORY_QC']
    @property
    def point_qc(self):
        return self.dataSet['POINT_QC']
    @property
    def rtdbtype_qc(self):
        return self.dataSet['RTDBTYPE_QC']
    @property
    def attribute_qc(self):
        return self.dataSet['ATTRIBUTE_QC']
    @property
    def addrstring_qc(self):
        try:
            return ",".join([str(value) for value in self.addr_qc.as_tuple()])
        except:
            return ''
    @property
    def qc(self):
        if self.p_qc:
            return round(self.p_qc.read_attr(self.attribute_qc), 6)
        else:
            return 0 

    @property
    def ttu_p(self):
        return self.pa + self.pb + self.pc
    @property
    def addrstring_ttu_p(self):
        return self.addrstring_pa + self.addrstring_pb + self.addrstring_pc

    @property
    def ttu_q(self):
        return self.qa + self.qb + self.qc
    @property
    def addrstring_ttu_q(self):
        return self.addrstring_qa + self.addrstring_qb + self.addrstring_qc

    @property
    def mdms_p(self):
        if self.dataSet['MDMS_P']:
            return self.dataSet['MDMS_P']
        else:
            return 0
    @property
    def mdms_q(self):
        if self.dataSet['MDMS_Q']:
            return self.dataSet['MDMS_Q']
        else:
            return 0
    
    @property
    def dpf_p(self):
        if self.dataSet['DPF_P']:
            return self.dataSet['DPF_P']
        else:
            return 0

    @property
    def dpf_q(self):
        if self.dataSet['DPF_Q']:
            return self.dataSet['DPF_Q']
        return 0

    @property
    def usage_rate(self):
        if self.capacity == 0:
            return 'X'
        else:
            if isinstance(self.ttu_p, float) and isinstance(self.ttu_q, float):
                str(round((sqrt(pow(self.ttu_p, 2) + pow(self.ttu_q, 2)) / self.capacity) / 100, 6))
                return str(round((sqrt(pow(self.ttu_p, 2) + pow(self.ttu_q, 2)) / self.capacity) / 100, 3)) + '%'
            else:
                return 'X'
    @property
    def station_flag1(self):
        return self.dataSet['STATION_FLAG1']
    @property
    def category_flag1(self):
        return self.dataSet['CATEGORY_FLAG1']
    @property
    def point_flag1(self):
        return self.dataSet['POINT_FLAG1']
    @property
    def rtdbtype_flag1(self):
        return self.dataSet['RTDBTYPE_FLAG1']
    @property
    def attribute_flag1(self):
        return self.dataSet['ATTRIBUTE_FLAG1']
    @property
    def addrstring_flag1(self):
        try:
            return ",".join([str(value) for value in self.addr_flag1.as_tuple()])
        except:
            return None
    @property
    def flag1(self):
        if self.p_flag1:
            return self.p_flag1.read_attr(self.attribute_flag1)
        else:
            return None
    @flag1.setter
    def flag1(self, value):
        if self.p_flag1:
            self.p_flag1.write_attr(self.attribute_flag1, value)

    @property
    def station_flag2(self):
        return self.dataSet['STATION_FLAG2']
    @property
    def category_flag2(self):
        return self.dataSet['CATEGORY_FLAG2']
    @property
    def point_flag2(self):
        return self.dataSet['POINT_FLAG2']
    @property
    def rtdbtype_flag2(self):
        return self.dataSet['RTDBTYPE_FLAG2']
    @property
    def attribute_flag2(self):
        return self.dataSet['ATTRIBUTE_FLAG2']
    @property
    def addrstring_flag2(self):
        try:
            return ",".join([str(value) for value in self.addr_flag2.as_tuple()])
        except:
            return None
    @property
    def flag2(self):
        if self.p_flag2:
            return self.p_flag2.read_attr(self.attribute_flag2)
        else:
            return None
    @flag2.setter
    def flag2(self, value):
        if self.p_flag2:
            self.p_flag2.write_attr(self.attribute_flag2, value)

    @property
    def station_flag3(self):
        return self.dataSet['STATION_FLAG3']
    @property
    def category_flag3(self):
        return self.dataSet['CATEGORY_FLAG3']
    @property
    def point_flag3(self):
        return self.dataSet['POINT_FLAG3']
    @property
    def rtdbtype_flag3(self):
        return self.dataSet['RTDBTYPE_FLAG3']
    @property
    def attribute_flag3(self):
        return self.dataSet['ATTRIBUTE_FLAG3']
    @property
    def addrstring_flag3(self):
        try:
            return ",".join([str(value) for value in self.addr_flag3.as_tuple()])
        except:
            return None
    @property
    def flag3(self):
        if self.p_flag3:
            return self.p_flag3.read_attr(self.attribute_flag3)
        else:
            return None
    @flag3.setter
    def flag3(self, value):
        if self.p_flag3:
            self.p_flag3.write_attr(self.attribute_flag3, value)

    @property
    def station_flag4(self):
        return self.dataSet['STATION_FLAG4']
    @property
    def category_flag4(self):
        return self.dataSet['CATEGORY_FLAG4']
    @property
    def point_flag4(self):
        return self.dataSet['POINT_FLAG4']
    @property
    def rtdbtype_flag4(self):
        return self.dataSet['RTDBTYPE_FLAG4']
    @property
    def attribute_flag4(self):
        return self.dataSet['ATTRIBUTE_FLAG4']
    @property
    def addrstring_flag4(self):
        try:
            return ",".join([str(value) for value in self.addr_flag4.as_tuple()])
        except:
            return None
    @property
    def flag4(self):
        if self.p_flag4:
            return self.p_flag4.read_attr(self.attribute_flag4)
        else:
            return None
    @flag4.setter
    def flag4(self, value):
        if self.p_flag4:
            self.p_flag4.write_attr(self.attribute_flag4, value)


