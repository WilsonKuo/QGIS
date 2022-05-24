#!/bin/python3.6
from acsprism import RtdbAddress, RtdbPoint
class NewInitCaller(type):
    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        obj.new_init()
        return obj

class MeterInfo(object, metaclass = NewInitCaller):
    def __init__(self, resultSet):
        self.resultSet = resultSet
    
    def new_init(self):
        try:
            self.addr_lockflag1 = RtdbAddress(self.station_lockflag1, self.category_lockflag1, self.point_lockflag1, self.rtdbtype_lockflag1)
            self.p_lockflag1 = RtdbPoint(self.addr_lockflag1)
        except:
            self.p_lockflag1 = None
        try:
            self.addr_lockflag2 = RtdbAddress(self.station_lockflag2, self.category_lockflag2, self.point_lockflag2, self.rtdbtype_lockflag2)
            self.p_lockflag2 = RtdbPoint(self.addr_lockflag2)
        except:
            self.p_lockflag2 = None
        try:
            self.addr_p = RtdbAddress(self.station_p, self.category_p, self.point_p, self.rtdbtype_p)
            self.p_p = RtdbPoint(self.addr_p)
        except:
            self.p_p = None
        try:
            self.addr_v = RtdbAddress(self.station_v, self.category_v, self.point_v, self.rtdbtype_v)
            self.p_v = RtdbPoint(self.addr_v)
        except:
            self.p_v = None
        try:
            self.addr_i = RtdbAddress(self.station_i, self.category_i, self.point_i, self.rtdbtype_i)
            self.p_i = RtdbPoint(self.addr_i)
        except:
            self.p_i = None

        try:
            self.addr_eflag = RtdbAddress(self.station_eflag, self.category_eflag, self.point_eflag, self.rtdbtype_eflag)
            self.p_eflag = RtdbPoint(self.addr_eflag)
        except:
            self.p_eflag = None
    
    def init_val(self):
        if self.p_lockflag1:
            self.p_lockflag1.write_attr(self.attribute_lockflag1, 0)
        if self.p_lockflag2:
            self.p_lockflag2.write_attr(self.attribute_lockflag2, 0)
        if self.p_p:
            self.p_p.write_attr(self.attribute_p, 0)
        if self.p_v:
            self.p_v.write_attr(self.attribute_v, 0)
        if self.p_i:
            self.p_i.write_attr(self.attribute_i, 0)
        if self.p_eflag:
            self.p_eflag.write_attr(self.attribute_eflag, 0)

    @property
    def name(self):
        return self.resultSet['METER_NAME']

    @property
    def station_lockflag1(self):
        return self.resultSet['STATION_LOCKFLAG1']
    @property
    def category_lockflag1(self):
        return self.resultSet['CATEGORY_LOCKFLAG1']
    @property
    def point_lockflag1(self):
        return self.resultSet['POINT_LOCKFLAG1']
    @property
    def rtdbtype_lockflag1(self):
        return self.resultSet['RTDBTYPE_LOCKFLAG1']
    @property
    def attribute_lockflag1(self):
        return self.resultSet['ATTRIBUTE_LOCKFLAG1']
    @property
    def addrstring_lockflag1(self):
        try:
            return ",".join([str(value) for value in self.addr_lockflag1.as_tuple()])
        except:
            return None
    @property
    def lockflag1(self):
        if self.p_lockflag1:
            return self.p_lockflag1.read_attr(self.attribute_lockflag1)
        else:
            return 0
    @lockflag1.setter
    def lockflag1(self, value):
        if self.p_lockflag1:
            self.p_lockflag1.write_attr(self.attribute_lockflag1, value)

    @property
    def station_lockflag2(self):
        return self.resultSet['STATION_LOCKFLAG2']
    @property
    def category_lockflag2(self):
        return self.resultSet['CATEGORY_LOCKFLAG2']
    @property
    def point_lockflag2(self):
        return self.resultSet['POINT_LOCKFLAG2']
    @property
    def rtdbtype_lockflag2(self):
        return self.resultSet['RTDBTYPE_LOCKFLAG2']
    @property
    def attribute_lockflag2(self):
        return self.resultSet['ATTRIBUTE_LOCKFLAG2']
    @property
    def addrstring_lockflag2(self):
        try:
            return ",".join([str(value) for value in self.addr_lockflag2.as_tuple()])
        except:
            return None
    @property
    def lockflag2(self):
        if self.p_lockflag2:
            return self.p_lockflag2.read_attr(self.attribute_lockflag2)
        else:
            return 0
    @lockflag2.setter
    def lockflag2(self, value):
        if self.p_lockflag2:
            self.p_lockflag2.write_attr(self.attribute_lockflag2, value)

    @property
    def station_p(self):
        return self.resultSet['STATION_P']
    @property
    def category_p(self):
        return self.resultSet['CATEGORY_P']
    @property
    def point_p(self):
        return self.resultSet['POINT_P']
    @property
    def rtdbtype_p(self):
        return self.resultSet['RTDBTYPE_P']
    @property
    def attribute_p(self):
        return self.resultSet['ATTRIBUTE_P']
    @property
    def addrstring_p(self):
        try:
            return ",".join([str(value) for value in self.addr_p.as_tuple()])
        except:
            return None
    @property
    def p(self):
        if self.p_p:
            return self.p_p.read_attr(self.attribute_p)
        else:
            return None
    @p.setter
    def p(self, value):
        if self.p_p:
            self.p_p.write_attr(self.attribute_p, value)

    @property
    def station_v(self):
        return self.resultSet['STATION_V']
    @property
    def category_v(self):
        return self.resultSet['CATEGORY_V']
    @property
    def point_v(self):
        return self.resultSet['POINT_V']
    @property
    def rtdbtype_v(self):
        return self.resultSet['RTDBTYPE_V']
    @property
    def attribute_v(self):
        return self.resultSet['ATTRIBUTE_V']
    @property
    def addrstring_v(self):
        try:
            return ",".join([str(value) for value in self.addr_v.as_tuple()])
        except:
            return None
    @property
    def v(self):
        if self.p_v:
            return self.p_v.read_attr(self.attribute_v)
        else:
            return 0
    @v.setter
    def v(self, value):
        if self.p_v:
            self.p_v.write_attr(self.attribute_v, value)

    @property
    def station_i(self):
        return self.resultSet['STATION_I']
    @property
    def category_i(self):
        return self.resultSet['CATEGORY_I']
    @property
    def point_i(self):
        return self.resultSet['POINT_I']
    @property
    def rtdbtype_i(self):
        return self.resultSet['RTDBTYPE_I']
    @property
    def attribute_i(self):
        return self.resultSet['ATTRIBUTE_I']
    @property
    def addrstring_i(self):
        try:
            return ",".join([str(value) for value in self.addr_i.as_tuple()])
        except:
            return None
    @property
    def i(self):
        if self.p_i:
            return self.p_i.read_attr(self.attribute_i)
        else:
            return 0
    @i.setter
    def i(self, value):
        if self.p_i:
            self.p_i.write_attr(self.attribute_i, value)

    @property
    def station_eflag(self):
        return self.resultSet['STATION_EFLAG']
    @property
    def category_eflag(self):
        return self.resultSet['CATEGORY_EFLAG']
    @property
    def point_eflag(self):
        return self.resultSet['POINT_EFLAG']
    @property
    def rtdbtype_eflag(self):
        return self.resultSet['RTDBTYPE_EFLAG']
    @property
    def attribute_eflag(self):
        return self.resultSet['ATTRIBUTE_EFLAG']
    @property
    def addrstring_eflag(self):
        try:
            return ",".join([str(value) for value in self.addr_eflag.as_tuple()])
        except:
            return None
    @property
    def eflag(self):
        if self.p_eflag:
            return self.p_eflag.read_attr(self.attribute_eflag)
        else:
            return None
    @eflag.setter
    def eflag(self, value):
        if self.p_eflag:
            self.p_eflag.write_attr(self.attribute_eflag, value)

