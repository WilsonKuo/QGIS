 drop table testtable;
 drop table feeder;
 create table feeder as select * from feeder@dasmap;
 create table testtable as select c.ufid,c.fsc,c.name,c.frnodeid,c.tonodeid,c.station,c.category,c.point, c.rtdbtype,c.attribute, d.colorcode
     from (select ufid,fsc,name,frnodeid,tonodeid,station,category,point,decode(rtdbtype,1,'S',2,'T') rtdbtype,attribute 
 from das_rtdb@dasmap a, view_electric_conn@dasmap b where a.equip_num=b.name and a.colname in ('STASTATUS','ENGZFLAG','COLORCODE')) c
 left join feeder d on c.name = d.name;



 update testtable a set station = (select station from inputxref b, switchparam c where b.keyidx = c.idx and b.tablename='SWITCHINPUT' and b.colname='STASTATUS' and a.name=c.name),
                        point = (select point from inputxref b, switchparam c where b.keyidx = c.idx and b.tablename='SWITCHINPUT' and b.colname='STASTATUS' and a.name=c.name)
 where a.fsc in (108,114) and name in (select name from switchparam);

 update testtable a set station = (select station from outputxref b, lineparam c where b.keyidx = c.idx and b.tablename='LINEOUTPUT' and b.colname='COLORCODE' and a.name=c.name),
                        point =   (select point from outputxref b, lineparam c where b.keyidx = c.idx and b.tablename='LINEOUTPUT' and b.colname='COLORCODE' and a.name=c.name)
 where a.fsc in (106) and name in (select name from lineparam);

drop table tb_tp;
create table tb_tp
(
    ufid number(11),
    fsc number(5),
    name varchar2(19),
    status number(3),
    feeder1 varchar2(19),
    feeder1_nonlineparent varchar2(19),
    feeder1_parent varchar2(19),
    feeder2 varchar2(19),
    feeder2_nonlineparent varchar2(19),
    feeder2_parent varchar2(19)
);
create index tb_tp_ufid_idx on tb_tp (ufid);