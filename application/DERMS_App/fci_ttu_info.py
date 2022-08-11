#!/bin/python3.6
from acsprism import RtdbAddress, RtdbPoint

class NewInitCaller(type):
    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        obj.new_init()
        return obj

class FCI_TTU_Info(object, metaclass = NewInitCaller):
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
            self.addr_ampa = RtdbAddress(self.station_ampa, self.category_ampa, self.point_ampa, self.rtdbtype_ampa)
            self.p_ampa = RtdbPoint(self.addr_ampa)
        except:
            self.p_ampa = None
        try:
            self.addr_ampb = RtdbAddress(self.station_ampb, self.category_ampb, self.point_ampb, self.rtdbtype_ampb)
            self.p_ampb = RtdbPoint(self.addr_ampb)
        except:
            self.p_ampb = None
        try:
            self.addr_ampc = RtdbAddress(self.station_ampc, self.category_ampc, self.point_ampc, self.rtdbtype_ampc)
            self.p_ampc = RtdbPoint(self.addr_ampc)
        except:
            self.p_ampc = None
        try:
            self.addr_voltmaga = RtdbAddress(self.station_voltmaga, self.category_voltmaga, self.point_voltmaga, self.rtdbtype_voltmaga)
            self.p_voltmaga = RtdbPoint(self.addr_voltmaga)
        except:
            self.p_voltmaga = None
        try:
            self.addr_voltmagb = RtdbAddress(self.station_voltmagb, self.category_voltmagb, self.point_voltmagb, self.rtdbtype_voltmagb)
            self.p_voltmagb = RtdbPoint(self.addr_voltmagb)
        except:
            self.p_voltmagb = None
        try:
            self.addr_voltmagc = RtdbAddress(self.station_voltmagc, self.category_voltmagc, self.point_voltmagc, self.rtdbtype_voltmagc)
            self.p_voltmagc = RtdbPoint(self.addr_voltmagc)
        except:
            self.p_voltmagc = None
        try:
            self.addr_faultflaga = RtdbAddress(self.station_faultflaga, self.category_faultflaga, self.point_faultflaga, self.rtdbtype_faultflaga)
            self.p_faultflaga = RtdbPoint(self.addr_faultflaga)
        except:
            self.p_faultflaga = None
        try:
            self.addr_faultflagb = RtdbAddress(self.station_faultflagb, self.category_faultflagb, self.point_faultflagb, self.rtdbtype_faultflagb)
            self.p_faultflagb = RtdbPoint(self.addr_faultflagb)
        except:
            self.p_faultflagb = None
        try:
            self.addr_faultflagc = RtdbAddress(self.station_faultflagc, self.category_faultflagc, self.point_faultflagc, self.rtdbtype_faultflagc)
            self.p_faultflagc = RtdbPoint(self.addr_faultflagc)
        except:
            self.p_faultflagc = None
            


    def init_val(self):
        if self.p_pa:
            self.p_pa.write_attr(self.attribute_pa, 0)
        if self.p_pb:
            self.p_pb.write_attr(self.attribute_pb, 0)
        if self.p_pc:
            self.p_pc.write_attr(self.attribute_pc, 0)
        if self.p_qa:
            self.p_qa.write_attr(self.attribute_qa, 0)
        if self.p_qb:
            self.p_qb.write_attr(self.attribute_qb, 0)
        if self.p_qc:
            self.p_qc.write_attr(self.attribute_qc, 0)
        if self.p_ampa:
            self.p_ampa.write_attr(self.attribute_ampa, 0)
        if self.p_ampb:
            self.p_ampb.write_attr(self.attribute_ampb, 0)
        if self.p_ampc:
            self.p_ampc.write_attr(self.attribute_ampc, 0)
        if self.p_voltmaga:
            self.p_voltmaga.write_attr(self.attribute_voltmaga, 0)
        if self.p_voltmagb:
            self.p_voltmagb.write_attr(self.attribute_voltmagb, 0)
        if self.p_voltmagc:
            self.p_voltmagc.write_attr(self.attribute_voltmagc, 0)
        if self.p_faultflaga:
            self.p_faultflaga.write_attr(self.attribute_faultflaga, 0)
        if self.p_faultflagb:
            self.p_faultflagb.write_attr(self.attribute_faultflagb, 0)
        if self.p_faultflagc:
            self.p_faultflagc.write_attr(self.attribute_faultflagc, 0)

    @property
    def name(self):
        return self.dataSet['NAME']

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
    @pa.setter
    def pa(self, value):
        if self.p_pa:
            self.p_pa.write_attr(self.attribute_pa, value)

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
    @pb.setter
    def pb(self, value):
        if self.p_pb:
            self.p_pb.write_attr(self.attribute_pb, value)

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
    @pc.setter
    def pc(self, value):
        if self.p_pc:
            self.p_pc.write_attr(self.attribute_pc, value)

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
    @qa.setter
    def qa(self, value):
        if self.p_qa:
            self.p_qa.write_attr(self.attribute_qa, value)

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
    @qb.setter
    def qb(self, value):
        if self.p_qb:
            self.p_qb.write_attr(self.attribute_qb, value)                            

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
    @qc.setter
    def qc(self, value):
        if self.p_qc:
            self.p_qc.write_attr(self.attribute_qc, value)

    @property
    def station_ampa(self):
        return self.dataSet['STATION_AMPA']
    @property
    def category_ampa(self):
        return self.dataSet['CATEGORY_AMPA']
    @property
    def point_ampa(self):
        return self.dataSet['POINT_AMPA']
    @property
    def rtdbtype_ampa(self):
        return self.dataSet['RTDBTYPE_AMPA']
    @property
    def attribute_ampa(self):
        return self.dataSet['ATTRIBUTE_AMPA']
    @property
    def addrstring_ampa(self):
        try:
            return ",".join([str(value) for value in self.addr_ampa.as_tuple()])
        except:
            return ''
    @property
    def ampa(self):
        if self.p_ampa:
            return round(self.p_ampa.read_attr(self.attribute_ampa), 6)
        else:
            return 0
    @ampa.setter
    def ampa(self, value):
        if self.p_ampa:
            self.p_ampa.write_attr(self.attribute_ampa, value)
    @property
    def station_ampb(self):
        return self.dataSet['STATION_AMPB']
    @property
    def category_ampb(self):
        return self.dataSet['CATEGORY_AMPB']
    @property
    def point_ampb(self):
        return self.dataSet['POINT_AMPB']
    @property
    def rtdbtype_ampb(self):
        return self.dataSet['RTDBTYPE_AMPB']
    @property
    def attribute_ampb(self):
        return self.dataSet['ATTRIBUTE_AMPB']
    @property
    def addrstring_ampb(self):
        try:
            return ",".join([str(value) for value in self.addr_ampb.as_tuple()])
        except:
            return ''
    @property
    def ampb(self):
        if self.p_ampb:
            return round(self.p_ampb.read_attr(self.attribute_ampb), 6)
        else:
            return 0
    @ampb.setter
    def ampb(self, value):
        if self.p_ampb:
            self.p_ampb.write_attr(self.attribute_ampb, value)

    @property
    def station_ampc(self):
        return self.dataSet['STATION_AMPC']
    @property
    def category_ampc(self):
        return self.dataSet['CATEGORY_AMPC']
    @property
    def point_ampc(self):
        return self.dataSet['POINT_AMPC']
    @property
    def rtdbtype_ampc(self):
        return self.dataSet['RTDBTYPE_AMPC']
    @property
    def attribute_ampc(self):
        return self.dataSet['ATTRIBUTE_AMPC']
    @property
    def addrstring_ampc(self):
        try:
            return ",".join([str(value) for value in self.addr_ampc.as_tuple()])
        except:
            return ''
    @property
    def ampc(self):
        if self.p_ampc:
            return round(self.p_ampc.read_attr(self.attribute_ampc), 6)
        else:
            return 0
    @ampc.setter
    def ampc(self, value):
        if self.p_ampc:
            self.p_ampc.write_attr(self.attribute_ampc, value)

    @property
    def station_voltmaga(self):
        return self.dataSet['STATION_VOLTMAGA']
    @property
    def category_voltmaga(self):
        return self.dataSet['CATEGORY_VOLTMAGA']
    @property
    def point_voltmaga(self):
        return self.dataSet['POINT_VOLTMAGA']
    @property
    def rtdbtype_voltmaga(self):
        return self.dataSet['RTDBTYPE_VOLTMAGA']
    @property
    def attribute_voltmaga(self):
        return self.dataSet['ATTRIBUTE_VOLTMAGA']
    @property
    def addrstring_voltmaga(self):
        try:
            return ",".join([str(value) for value in self.addr_voltmaga.as_tuple()])
        except:
            return ''
    @property
    def voltmaga(self):
        if self.p_voltmaga:
            return round(self.p_voltmaga.read_attr(self.attribute_voltmaga), 6)
        else:
            return 0
    @voltmaga.setter
    def voltmaga(self, value):
        if self.p_voltmaga:
            self.p_voltmaga.write_attr(self.attribute_voltmaga, value)

    @property
    def station_voltmagb(self):
        return self.dataSet['STATION_voltmagb']
    @property
    def category_voltmagb(self):
        return self.dataSet['CATEGORY_voltmagb']
    @property
    def point_voltmagb(self):
        return self.dataSet['POINT_voltmagb']
    @property
    def rtdbtype_voltmagb(self):
        return self.dataSet['RTDBTYPE_voltmagb']
    @property
    def attribute_voltmagb(self):
        return self.dataSet['ATTRIBUTE_voltmagb']
    @property
    def addrstring_voltmagb(self):
        try:
            return ",".join([str(value) for value in self.addr_voltmagb.as_tuple()])
        except:
            return ''
    @property
    def voltmagb(self):
        if self.p_voltmagb:
            return round(self.p_voltmagb.read_attr(self.attribute_voltmagb), 6)
        else:
            return 0
    @voltmagb.setter
    def voltmagb(self, value):
        if self.p_voltmagb:
            self.p_voltmagb.write_attr(self.attribute_voltmagb, value)


    @property
    def station_voltmagc(self):
        return self.dataSet['STATION_VOLTMAGC']
    @property
    def category_voltmagc(self):
        return self.dataSet['CATEGORY_VOLTMAGC']
    @property
    def point_voltmagc(self):
        return self.dataSet['POINT_VOLTMAGC']
    @property
    def rtdbtype_voltmagc(self):
        return self.dataSet['RTDBTYPE_VOLTMAGC']
    @property
    def attribute_voltmagc(self):
        return self.dataSet['ATTRIBUTE_VOLTMAGC']
    @property
    def addrstring_voltmagc(self):
        try:
            return ",".join([str(value) for value in self.addr_voltmagc.as_tuple()])
        except:
            return ''
    @property
    def voltmagc(self):
        if self.p_voltmagc:
            return round(self.p_voltmagc.read_attr(self.attribute_voltmagc), 6)
        else:
            return 0
    @voltmagc.setter
    def voltmagc(self, value):
        if self.p_voltmagc:
            self.p_voltmagc.write_attr(self.attribute_voltmagc, value)

    @property
    def station_faultflaga(self):
        return self.dataSet['STATION_FAULTFLAGA']
    @property
    def category_faultflaga(self):
        return self.dataSet['CATEGORY_FAULTFLAGA']
    @property
    def point_faultflaga(self):
        return self.dataSet['POINT_FAULTFLAGA']
    @property
    def rtdbtype_faultflaga(self):
        return self.dataSet['RTDBTYPE_FAULTFLAGA']
    @property
    def attribute_faultflaga(self):
        return self.dataSet['ATTRIBUTE_FAULTFLAGA']
    @property
    def addrstring_faultflaga(self):
        try:
            return ",".join([str(value) for value in self.addr_faultflaga.as_tuple()])
        except:
            return ''
    @property
    def faultflaga(self):
        if self.p_faultflaga:
            return round(self.p_faultflaga.read_attr(self.attribute_faultflaga), 6)
        else:
            return 0
    @faultflaga.setter
    def faultflaga(self, value):
        if self.p_faultflaga:
            self.p_faultflaga.write_attr(self.attribute_faultflaga, value)

    @property
    def station_faultflagb(self):
        return self.dataSet['STATION_FAULTFLAGB']
    @property
    def category_faultflagb(self):
        return self.dataSet['CATEGORY_FAULTFLAGB']
    @property
    def point_faultflagb(self):
        return self.dataSet['POINT_FAULTFLAGB']
    @property
    def rtdbtype_faultflagb(self):
        return self.dataSet['RTDBTYPE_FAULTFLAGB']
    @property
    def attribute_faultflagb(self):
        return self.dataSet['ATTRIBUTE_FAULTFLAGB']
    @property
    def addrstring_faultflagb(self):
        try:
            return ",".join([str(value) for value in self.addr_faultflagb.as_tuple()])
        except:
            return ''
    @property
    def faultflagb(self):
        if self.p_faultflagb:
            return round(self.p_faultflagb.read_attr(self.attribute_faultflagb), 6)
        else:
            return 0
    @faultflagb.setter
    def faultflagb(self, value):
        if self.p_faultflagb:
            self.p_faultflagb.write_attr(self.attribute_faultflagb, value)

    @property
    def station_faultflagc(self):
        return self.dataSet['STATION_FAULTFLAGC']
    @property
    def category_faultflagc(self):
        return self.dataSet['CATEGORY_FAULTFLAGC']
    @property
    def point_faultflagc(self):
        return self.dataSet['POINT_FAULTFLAGC']
    @property
    def rtdbtype_faultflagc(self):
        return self.dataSet['RTDBTYPE_FAULTFLAGC']
    @property
    def attribute_faultflagc(self):
        return self.dataSet['ATTRIBUTE_FAULTFLAGC']
    @property
    def addrstring_faultflagc(self):
        try:
            return ",".join([str(value) for value in self.addr_faultflagc.as_tuple()])
        except:
            return ''
    @property
    def faultflagc(self):
        if self.p_faultflagc:
            return round(self.p_faultflagc.read_attr(self.attribute_faultflagc), 6)
        else:
            return 0
    @faultflagc.setter
    def faultflagc(self, value):
        if self.p_faultflagc:
            self.p_faultflagc.write_attr(self.attribute_faultflagc, value)


