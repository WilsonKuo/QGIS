CREATE OR REPLACE VIEW TTUINFO AS SELECT TT.NAME TTU_NAME, DISPLAY_NUMBER,  CAPACITY,
TT.FEEDER1_NONLINEPARENT, TT.FEEDER2_NONLINEPARENT,
MDMS_P, MDMS_Q,
DPF_P, DPF_Q,
STATION_PA, CATEGORY_PA, POINT_PA, RTDBTYPE_PA, ATTRIBUTE_PA,
STATION_PB, CATEGORY_PB, POINT_PB, RTDBTYPE_PB, ATTRIBUTE_PB,
STATION_PC, CATEGORY_PC, POINT_PC, RTDBTYPE_PC, ATTRIBUTE_PC,
STATION_QA, CATEGORY_QA, POINT_QA, RTDBTYPE_QA, ATTRIBUTE_QA,
STATION_QB, CATEGORY_QB, POINT_QB, RTDBTYPE_QB, ATTRIBUTE_QB,
STATION_QC, CATEGORY_QC, POINT_QC, RTDBTYPE_QC, ATTRIBUTE_QC,
--STATION_I, CATEGORY_I, POINT_I, RTDBTYPE_I, ATTRIBUTE_I,
--STATION_V, CATEGORY_V, POINT_V, RTDBTYPE_V, ATTRIBUTE_V,
STATION_FLAG1, CATEGORY_FLAG1, POINT_FLAG1, RTDBTYPE_FLAG1, ATTRIBUTE_FLAG1,
STATION_FLAG2, CATEGORY_FLAG2, POINT_FLAG2, RTDBTYPE_FLAG2, ATTRIBUTE_FLAG2,
STATION_FLAG3, CATEGORY_FLAG3, POINT_FLAG3, RTDBTYPE_FLAG3, ATTRIBUTE_FLAG3,
STATION_FLAG4, CATEGORY_FLAG4, POINT_FLAG4, RTDBTYPE_FLAG4, ATTRIBUTE_FLAG4
FROM (SELECT * FROM TB_TP WHERE FSC = 115) TT
LEFT JOIN (SELECT PA+PB+PC DPF_P, QA+QB+QC DPF_Q, NAME FROM NODEOUTPUT NO, LOADPARAM LP WHERE NO.IDX = LP.NODEIDX) NLP
     ON TT.NAME = NLP.NAME
LEFT JOIN (SELECT TXTCONTENTS, CMD_STRING DISPLAY_NUMBER FROM COMMAND_LIST) CL 
    ON TT.NAME = CL.TXTCONTENTS
LEFT JOIN (SELECT NAME ,(NORMLOADA + NORMLOADB + NORMLOADC) CAPACITY FROM LOADPARAM) TP 
    ON TT.NAME = TP.NAME
LEFT JOIN (SELECT TTU_NAME, P_KWH MDMS_P, P_KQH_P MDMS_Q FROM VIEW_METERSUM) MDMS
    ON TT.NAME = MDMS.TTU_NAME
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_PA, CATEGORY CATEGORY_PA, POINT POINT_PA, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_PA, ATTRIBUTE ATTRIBUTE_PA FROM SMXREF 
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'PA') SMPA
    ON TT.NAME = SMPA.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_PB, CATEGORY CATEGORY_PB, POINT POINT_PB, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_PB, ATTRIBUTE ATTRIBUTE_PB FROM SMXREF 
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'PB') SMPB
    ON TT.NAME = SMPB.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_PC, CATEGORY CATEGORY_PC, POINT POINT_PC, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_PC, ATTRIBUTE ATTRIBUTE_PC FROM SMXREF 
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'PC') SMPC
    ON TT.NAME = SMPC.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_QA, CATEGORY CATEGORY_QA, POINT POINT_QA, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_QA, ATTRIBUTE ATTRIBUTE_QA FROM SMXREF 
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'QA') SMQA
    ON TT.NAME = SMQA.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_QB, CATEGORY CATEGORY_QB, POINT POINT_QB, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_QB, ATTRIBUTE ATTRIBUTE_QB FROM SMXREF 
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'QB') SMQB
    ON TT.NAME = SMQB.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_QC, CATEGORY CATEGORY_QC, POINT POINT_QC, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_QC, ATTRIBUTE ATTRIBUTE_QC FROM SMXREF 
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'QC') SMQC
    ON TT.NAME = SMQC.EQUIP_NUM
--LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_I, CATEGORY CATEGORY_I, POINT POINT_I, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_I, ATTRIBUTE ATTRIBUTE_I FROM SMXREF
--        WHERE TABLENAME = 'LOAD' AND COLNAME = 'AMPA') SMI 
--    ON TT.NAME = SMI.EQUIP_NUM
--LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_V, CATEGORY CATEGORY_V, POINT POINT_V, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_V, ATTRIBUTE ATTRIBUTE_V FROM SMXREF
--        WHERE TABLENAME = 'LOAD' AND COLNAME = 'VOLTMAGA') SMV
--    ON TT.NAME = SMV.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_FLAG1, CATEGORY CATEGORY_FLAG1, POINT POINT_FLAG1, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_FLAG1, ATTRIBUTE ATTRIBUTE_FLAG1 FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'FLAG1') SMFLAG1 
    ON TT.NAME = SMFLAG1.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_FLAG2, CATEGORY CATEGORY_FLAG2, POINT POINT_FLAG2, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_FLAG2, ATTRIBUTE ATTRIBUTE_FLAG2 FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'FLAG2') SMFLAG2 
    ON TT.NAME = SMFLAG2.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_FLAG3, CATEGORY CATEGORY_FLAG3, POINT POINT_FLAG3, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_FLAG3, ATTRIBUTE ATTRIBUTE_FLAG3 FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'FLAG3') SMFLAG3 
    ON TT.NAME = SMFLAG3.EQUIP_NUM
LEFT JOIN (SELECT EQUIP_NUM, STATION STATION_FLAG4, CATEGORY CATEGORY_FLAG4, POINT POINT_FLAG4, DECODE(RTDBTYPE, 1, 'S', 2, 'T', NULL) RTDBTYPE_FLAG4, ATTRIBUTE ATTRIBUTE_FLAG4 FROM SMXREF
        WHERE TABLENAME = 'LOAD' AND COLNAME = 'FLAG4') SMFLAG4 
    ON TT.NAME = SMFLAG4.EQUIP_NUM;

EXIT;

