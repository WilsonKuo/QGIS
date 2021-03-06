CREATE OR REPLACE VIEW TTUINFO AS SELECT TTU_NAME, DISPLAY_NUMBER,  CAPACITY,
STATION_LINE, CATEGORY_LINE, POINT_LINE, RTDBTYPE_LINE, ATTRIBUTE_LINE,
STATION_P, CATEGORY_P, POINT_P, RTDBTYPE_P, ATTRIBUTE_P,
STATION_Q, CATEGORY_Q, POINT_Q, RTDBTYPE_Q, ATTRIBUTE_Q,
STATION_I, CATEGORY_I, POINT_I, RTDBTYPE_I, ATTRIBUTE_I,
STATION_V, CATEGORY_V, POINT_V, RTDBTYPE_V, ATTRIBUTE_V,
STATION_FLAG1, CATEGORY_FLAG1, POINT_FLAG1, RTDBTYPE_FLAG1, ATTRIBUTE_FLAG1,
STATION_FLAG2, CATEGORY_FLAG2, POINT_FLAG2, RTDBTYPE_FLAG2, ATTRIBUTE_FLAG2,
STATION_FLAG3, CATEGORY_FLAG3, POINT_FLAG3, RTDBTYPE_FLAG3, ATTRIBUTE_FLAG3,
STATION_FLAG4, CATEGORY_FLAG4, POINT_FLAG4, RTDBTYPE_FLAG4, ATTRIBUTE_FLAG4
FROM SWITCH_TTU ST
LEFT JOIN (SELECT TXTCONTENTS, CMD_STRING DISPLAY_NUMBER FROM COMMAND_LIST) CL 
    ON ST.TTU_NAME = CL.TXTCONTENTS
LEFT JOIN (SELECT NAME ,(NORMLOADA + NORMLOADB + NORMLOADC) CAPACITY FROM LOADPARAM) TP 
    ON ST.TTU_NAME = TP.NAME
LEFT JOIN (SELECT * FROM LINEXREF WHERE TABLENAME = 'LOADINPUT') LX 
    ON ST.TTU_NAME = LX.NAME
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_P, CATEGORY CATEGORY_P, POINT POINT_P, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_P, ATTRIBUTE ATTRIBUTE_P FROM SMXREF 
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'PA' AND STATION < 200
        UNION 
        SELECT EQUIP_NUM, STATION STATION_P, CATEGORY CATEGORY_P, POINT POINT_P, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_P, ATTRIBUTE ATTRIBUTE_P FROM SMXREF 
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'PB' AND STATION < 200
        UNION
        SELECT EQUIP_NUM, STATION STATION_P, CATEGORY CATEGORY_P, POINT POINT_P, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_P, ATTRIBUTE ATTRIBUTE_P FROM SMXREF 
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'PC' AND STATION < 200
        ) SMP 
    ON ST.TTU_NAME = SMP.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_Q, CATEGORY CATEGORY_Q, POINT POINT_Q, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_Q, ATTRIBUTE ATTRIBUTE_Q FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'QA' AND STATION < 200
        UNION
        SELECT EQUIP_NUM, STATION STATION_Q, CATEGORY CATEGORY_Q, POINT POINT_Q, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_Q, ATTRIBUTE ATTRIBUTE_Q FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'QB' AND STATION < 200
        UNION
        SELECT EQUIP_NUM, STATION STATION_Q, CATEGORY CATEGORY_Q, POINT POINT_Q, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_Q, ATTRIBUTE ATTRIBUTE_Q FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'QC' AND STATION < 200
        ) SMQ 
    ON ST.TTU_NAME = SMQ.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_I, CATEGORY CATEGORY_I, POINT POINT_I, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_I, ATTRIBUTE ATTRIBUTE_I FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'AMPA') SMI 
    ON ST.TTU_NAME = SMI.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_V, CATEGORY CATEGORY_V, POINT POINT_V, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_V, ATTRIBUTE ATTRIBUTE_V FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'VOLTMAGA') SMV 
    ON ST.TTU_NAME = SMV.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_FLAG1, CATEGORY CATEGORY_FLAG1, POINT POINT_FLAG1, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_FLAG1, ATTRIBUTE ATTRIBUTE_FLAG1 FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'FLAG1') SMFLAG1 
    ON ST.TTU_NAME = SMFLAG1.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_FLAG2, CATEGORY CATEGORY_FLAG2, POINT POINT_FLAG2, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_FLAG2, ATTRIBUTE ATTRIBUTE_FLAG2 FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'FLAG2') SMFLAG2 
    ON ST.TTU_NAME = SMFLAG2.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_FLAG3, CATEGORY CATEGORY_FLAG3, POINT POINT_FLAG3, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_FLAG3, ATTRIBUTE ATTRIBUTE_FLAG3 FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'FLAG3') SMFLAG3 
    ON ST.TTU_NAME = SMFLAG3.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_FLAG4, CATEGORY CATEGORY_FLAG4, POINT POINT_FLAG4, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_FLAG4, ATTRIBUTE ATTRIBUTE_FLAG4 FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'FLAG4') SMFLAG4 
    ON ST.TTU_NAME = SMFLAG4.EQUIP_NUM;
EXIT;