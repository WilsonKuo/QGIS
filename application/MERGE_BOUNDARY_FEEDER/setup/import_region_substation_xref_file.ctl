options(skip=1)
load data
infile '/home/acs/tmp/Wilson/QGIS/MERGE_BOUNDARY_FEEDER/setup/region_substation_xref.csv'
insert into table REGION_SUBSTATION_XREF 
fields terminated by ","
(Region,district_code,district,code) 