drop table REGION_SUBSTATION_XREF;
create table REGION_SUBSTATION_XREF(Region varchar2(19),district_code number(3), district varchar2(3), code varchar2(3));

host sqlldr userid = acs_map_tc105/acs@dasmap control = '/home/acs/tmp/Wilson/QGIS/MERGE_BOUNDARY_FEEDER/setup/import_region_substation_xref_file.ctl';
exit;

