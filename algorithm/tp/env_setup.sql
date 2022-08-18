--## LOAD ENGZFLAG?????????????????????????????????????????????????
CREATE OR REPLACE VIEW VIEW_TB_TP_XREF AS SELECT 
BRK.IDX + 1000000 UFID, 108 FSC, BRK.NAME, BRK.FRNODEIDX FRNODEID, BRK.TONODEIDX TONODEID, IX.STATION, IX.CATEGORY, IX.POINT, DECODE(IX.RTDBTYPE,1,'S',2,'T') RTDBTYPE, IX.ATTRIBUTE, FP.COLORCODE
FROM (SELECT * FROM SWITCHPARAM WHERE DEVTYPE > 2) BRK
LEFT JOIN INPUTXREF IX ON IX.KEYIDX = BRK.IDX
LEFT JOIN FEEDERPARAM FP ON BRK.NAME = FP.NAME
WHERE TABLENAME = 'SWITCHINPUT' AND COLNAME = 'STASTATUS'
UNION
SELECT 
SWT.IDX + 2000000 UFID, 114 FSC, SWT.NAME, SWT.FRNODEIDX FRNODEID, SWT.TONODEIDX TONODEID, IX.STATION, IX.CATEGORY, IX.POINT, DECODE(IX.RTDBTYPE,1,'S',2,'T') RTDBTYPE, IX.ATTRIBUTE, NULL COLORCODE
FROM (SELECT * FROM SWITCHPARAM WHERE DEVTYPE <= 2) SWT
LEFT JOIN INPUTXREF IX ON IX.KEYIDX = SWT.IDX
WHERE TABLENAME = 'SWITCHINPUT' AND COLNAME = 'STASTATUS'
UNION
SELECT 
LOAD.IDX + 3000000 UFID, 115 FSC, LOAD.NAME, LOAD.NODEIDX FRNODEID, 0 TONODEID, NULL STATION, NULL CATEGORY, NULL POINT, NULL RTDBTYPE, NULL ATTRIBUTE, NULL COLORCODE
FROM (SELECT * FROM LOADPARAM) LOAD
UNION
SELECT 
LINE.IDX + 4000000 UFID, 106 FSC, LINE.NAME, LINE.FRNODEIDX FRNODEID, LINE.TONODEIDX TONODEID, OX.STATION, OX.CATEGORY, OX.POINT, DECODE(OX.RTDBTYPE,1,'S',2,'T') RTDBTYPE, OX.ATTRIBUTE, NULL COLORCODE
FROM (SELECT * FROM LINEPARAM) LINE
LEFT JOIN OUTPUTXREF OX ON OX.KEYIDX = LINE.IDX
WHERE TABLENAME = 'LINEOUTPUT' AND COLNAME = 'COLORCODE'

--  drop table testtable;
--  drop table feeder;
--  create table feeder as select * from feeder@dasmap;
--  create table testtable as select c.ufid,c.fsc,c.name,c.frnodeid,c.tonodeid,c.station,c.category,c.point, c.rtdbtype,c.attribute, d.colorcode
--      from (select ufid,fsc,name,frnodeid,tonodeid,station,category,point,decode(rtdbtype,1,'S',2,'T') rtdbtype,attribute 
--  from das_rtdb@dasmap a, view_electric_conn@dasmap b where a.equip_num=b.name and a.colname in ('STASTATUS','ENGZFLAG','COLORCODE')) c
--  left join feeder d on c.name = d.name;



--  update testtable a set station = (select station from inputxref b, switchparam c where b.keyidx = c.idx and b.tablename='SWITCHINPUT' and b.colname='STASTATUS' and a.name=c.name),
--                         point = (select point from inputxref b, switchparam c where b.keyidx = c.idx and b.tablename='SWITCHINPUT' and b.colname='STASTATUS' and a.name=c.name)
--  where a.fsc in (108,114) and name in (select name from switchparam);

--  update testtable a set station = (select station from outputxref b, lineparam c where b.keyidx = c.idx and b.tablename='LINEOUTPUT' and b.colname='COLORCODE' and a.name=c.name),
--                         point =   (select point from outputxref b, lineparam c where b.keyidx = c.idx and b.tablename='LINEOUTPUT' and b.colname='COLORCODE' and a.name=c.name)
--  where a.fsc in (106) and name in (select name from lineparam);

DROP TABLE TB_TP;
CREATE TABLE TB_TP
(
    UFID NUMBER(11),
    FSC NUMBER(5),
    NAME VARCHAR2(19),
    STATUS NUMBER(3),
    FEEDER1 VARCHAR2(19),
    FEEDER1_NONLINEPARENT VARCHAR2(19),
    FEEDER1_PARENT VARCHAR2(19),
    FEEDER2 VARCHAR2(19),
    FEEDER2_NONLINEPARENT VARCHAR2(19),
    FEEDER2_PARENT VARCHAR2(19),
    FLAG NUMBER(1)
);
CREATE INDEX TB_TP_UFID_IDX ON TB_TP (UFID);
CREATE INDEX IDX_TB_TP_FD1_NONLINEPARENT ON TB_TP(FEEDER1_NONLINEPARENT);
CREATE INDEX IDX_TB_TP_FD2_NONLINEPARENT ON TB_TP(FEEDER2_NONLINEPARENT);

EXIT;

