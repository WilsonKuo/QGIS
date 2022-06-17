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
            self.addr_line = RtdbAddress(self.station_line, self.category_line, self.point_line, self.rtdbtype_line)
            self.p_line = RtdbPoint(self.addr_line)
        except:
            self.p_line = None
        try:
            self.addr_p = RtdbAddress(self.station_p, self.category_p, self.point_p, self.rtdbtype_p)
            self.p_p = RtdbPoint(self.addr_p)
        except:
            self.p_p = None
        try:
            self.addr_q = RtdbAddress(self.station_q, self.category_q, self.point_q, self.rtdbtype_q)
            self.p_q = RtdbPoint(self.addr_q)
        except:
            self.p_q = None
        try:
            self.addr_i = RtdbAddress(self.station_i, self.category_i, self.point_i, self.rtdbtype_i)
            self.p_i = RtdbPoint(self.addr_i)
        except:
            self.p_i = None
        try:
            self.addr_v = RtdbAddress(self.station_v, self.category_v, self.point_v, self.rtdbtype_v)
            self.p_v = RtdbPoint(self.addr_v)
        except:
            self.p_v = None

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
    def station_line(self):
        return self.dataSet['STATION_LINE']
    @property
    def category_line(self):
        return self.dataSet['CATEGORY_LINE']
    @property
    def point_line(self):
        return self.dataSet['POINT_LINE']
    @property
    def rtdbtype_line(self):
        return self.dataSet['RTDBTYPE_LINE']
    @property
    def attribute_line(self):
        return self.dataSet['ATTRIBUTE_LINE']
    @property
    def addrstring_line(self):
        try:
            return ",".join([str(value) for value in self.addr_line.as_tuple()])
        except:
            return None
    @property
    def feeder(self):
        if self.p_line:
            return self.p_line.read_attr(self.attribute_line)
        else:
            return None

    @property
    def station_p(self):
        return self.dataSet['STATION_P']
    @property
    def category_p(self):
        return self.dataSet['CATEGORY_P']
    @property
    def point_p(self):
        return self.dataSet['POINT_P']
    @property
    def rtdbtype_p(self):
        return self.dataSet['RTDBTYPE_P']
    @property
    def attribute_p(self):
        return self.dataSet['ATTRIBUTE_P']
    @property
    def addrstring_p(self):
        try:
            return ",".join([str(value) for value in self.addr_p.as_tuple()])
        except:
            return None
    @property
    def p(self):
        if self.p_p:
            return round(self.p_p.read_attr(self.attribute_p), 6)
        else:
            return 0

    @property
    def station_q(self):
        return self.dataSet['STATION_Q']
    @property
    def category_q(self):
        return self.dataSet['CATEGORY_Q']
    @property
    def point_q(self):
        return self.dataSet['POINT_Q']
    @property
    def rtdbtype_q(self):
        return self.dataSet['RTDBTYPE_Q']
    @property
    def attribute_q(self):
        return self.dataSet['ATTRIBUTE_Q']
    @property
    def addrstring_q(self):
        try:
            return ",".join([str(value) for value in self.addr_q.as_tuple()])
        except:
            return None
    @property
    def q(self):
        if self.p_q:
            return self.p_q.read_attr(self.attribute_q)
        else:
            return 0

    @property
    def station_i(self):
        return self.dataSet['STATION_I']
    @property
    def category_i(self):
        return self.dataSet['CATEGORY_I']
    @property
    def point_i(self):
        return self.dataSet['POINT_I']
    @property
    def rtdbtype_i(self):
        return self.dataSet['RTDBTYPE_I']
    @property
    def attribute_i(self):
        return self.dataSet['ATTRIBUTE_I']
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
            print('?')
            self.p_i.write_attr(self.attribute_i, value)

    @property
    def station_v(self):
        return self.dataSet['STATION_V']
    @property
    def category_v(self):
        return self.dataSet['CATEGORY_V']
    @property
    def point_v(self):
        return self.dataSet['POINT_V']
    @property
    def rtdbtype_v(self):
        return self.dataSet['RTDBTYPE_V']
    @property
    def attribute_v(self):
        return self.dataSet['ATTRIBUTE_V']
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
            
    @property
    def usage_rate(self):
        if self.capacity == 0:
            return 'X'
        else:
            if isinstance(self.p, float) and isinstance(self.q, float):
                str(round((sqrt(pow(self.p, 2) + pow(self.q, 2)) / self.capacity) / 100, 6))
                return str(round((sqrt(pow(self.p, 2) + pow(self.q, 2)) / self.capacity) / 100, 3)) + '%'
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


