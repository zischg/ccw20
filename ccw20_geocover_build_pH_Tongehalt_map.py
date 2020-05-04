import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import arcpy
#environment settings, reference raster
#myworkspace = "/home/exchange/andreas/CCW18"
myworkspace="D:/CCW20"
codespace="D:/CCW20/code/ccw20"
tempgdb="C:/temp/temp.gdb"
geocovergeodatabase=myworkspace+"/GIS/geocover.gdb"
arcpy.env.workspace = tempgdb
arcpy.env.overwriteOutput = True

#input pH classifications
phGR=myworkspace+"/GIS/Geocover_pH/"+"GeocoverGR_Legendeneinheiten_pH_LFI_Meyer_ strato06022018_forExport_mf.xls"
phDEPOSIT=myworkspace+"/GIS/Geocover_pH/"+"stat_geocoverV2_uncodesposit_mf_pH.xls"
phBEDROCK=myworkspace+"/GIS/Geocover_pH/"+"stat_geocoverV2_bedrock_mf_pH_mf.xls"
phLI=myworkspace+"/GIS/Geocover_pH/"+"stat_geologie_Liechtenstein_pH_mf.xls"

#input vector geonmetry
shpGR=geocovergeodatabase+"/"+"GEOCOVER_MAIN_F"
shpDEPOSIT=geocovergeodatabase+"/GC_ROCK_BODIES/"+"GC_UNCO_DESPOSIT"
shpBEDROCK=geocovergeodatabase+"/GC_ROCK_BODIES/"+"GC_BEDROCK"
shpLI=geocovergeodatabase+"/"+"Geologie_Liechtenstein"

#input reference raster
demras=arcpy.Raster("D:/CHGIS/RASTER/DHM25/dhm25")
arcpy.env.cellSize = demras
arcpy.env.extent = demras
arcpy.env.snapRaster = demras

#read excel tables of input pH classifications
#phGRdf=pd.read_csv(phGR, delimiter=";")
phGRdf=pd.read_excel(phGR, sheetname="GeocoverGR_forExport")
phDEPOSITdf=pd.read_excel(phDEPOSIT, sheetname="Sheet1")
phBEDROCKdf=pd.read_excel(phBEDROCK, sheetname="Sheet1")
phLIdf=pd.read_excel(phLI, sheetname="stat_geologie_Liechtenstein_pH")

#import excel files into geodatabase
arcpy.ExcelToTable_conversion(Input_Excel_File=phGR, Output_Table=geocovergeodatabase+"/xlsgr", Sheet="GeocoverGR_forExport")
arcpy.ExcelToTable_conversion(Input_Excel_File=phBEDROCK, Output_Table=geocovergeodatabase+"/xlsbedrock", Sheet="Sheet1")
arcpy.ExcelToTable_conversion(Input_Excel_File=phDEPOSIT, Output_Table=geocovergeodatabase+"/xlsdeposit", Sheet="Sheet1")
arcpy.ExcelToTable_conversion(Input_Excel_FilephLI, Output_Table=geocovergeodatabase+"/xlsli", Sheet="stat_geologie_Liechtenstein_pH")


#add fields to shapefiles
arcpy.AddField_management(in_table=shpGR, field_name="ccw20ph", field_type="LONG")
arcpy.AddField_management(in_table=shpGR, field_name="ccw20tg", field_type="LONG")
arcpy.AddField_management(in_table=shpGR, field_name="pauschalgef", field_type="LONG")
arcpy.AddField_management(in_table=shpGR, field_name="joinstr", field_type="TEXT", field_length="800")
arcpy.AddField_management(in_table=shpDEPOSIT, field_name="ccw20ph", field_type="LONG")
arcpy.AddField_management(in_table=shpDEPOSIT, field_name="ccw20tg", field_type="LONG")
arcpy.AddField_management(in_table=shpDEPOSIT, field_name="pauschalgef", field_type="LONG")
arcpy.AddField_management(in_table=shpBEDROCK, field_name="ccw20ph", field_type="LONG")
arcpy.AddField_management(in_table=shpBEDROCK, field_name="ccw20tg", field_type="LONG")
arcpy.AddField_management(in_table=shpBEDROCK, field_name="pauschalgef", field_type="LONG")
arcpy.AddField_management(in_table=shpBEDROCK, field_name="joinstr", field_type="TEXT", field_length="800")

arcpy.AddField_management(in_table=shpLI, field_name="ccw20ph", field_type="LONG")
arcpy.AddField_management(in_table=shpLI, field_name="ccw20tg", field_type="LONG")
arcpy.AddField_management(in_table=shpLI, field_name="pauschalgef", field_type="LONG")

#join pH and Tongehalt values to shapefiles
#LI
cursor = arcpy.da.UpdateCursor(shpLI, ["STRATI", "TEKTONIKGR", "EINHEIT", "PERIODE", "EPOCHE", "GESTEINSGR", "GESTEIN", "ccw20ph", "ccw20tg", "pauschalgef"])
for row in cursor:
    strati=row[0]
    tektonikgr=row[1]
    einheit=row[2]
    periode=row[3]
    epoche=row[4]
    gesteinsgr=row[5]
    gestein=row[6]
    for index, dfrow in phLIdf.iterrows():
        if dfrow.STRATI==strati and dfrow.TEKTONIKGR==tektonikgr and dfrow.EINHEIT==einheit and dfrow.PERIODE==periode and dfrow.EPOCHE==epoche and dfrow.GESTEINSGR==gesteinsgr and dfrow.GESTEIN==gestein:
            row[7] = dfrow.BodenpH
            row[8] = dfrow.Tongehalt
            if dfrow.Pauschalgefaelle==1:
                row[9]=dfrow.Pauschalgefaelle
    cursor.updateRow(row)
del row
del cursor
#gr
#done manually via LEG_T only and filling in the voids with values of map for CCWGR
#cursor = arcpy.da.UpdateCursor(shpGR, ["LEG_T", "Grob1","ccw20ph", "ccw20tg", "pauschalgef"])
#for row in cursor:
#    leg_t=row[0]
#    grob1=row[1]
#    for index, dfrow in phGRdf.iterrows():
#        if dfrow.LEG_T==strati and dfrow.Grob1==grob1:
#            row[2] = dfrow.BodenpH
#            row[3] = dfrow.Tongehalt
#            if dfrow.Pauschalgefaelle==1:
#                row[4]=dfrow.Pauschalgefaelle
#    cursor.updateRow(row)
#del row
#del cursor
##DEPOSIT
#cursor = arcpy.da.UpdateCursor(shpDEPOSIT, ["KIND", "RUNC_LITHO", "RUNC_LITSTRAT", "RUNC_STRUCTUR", "RUNC_MORPHOLO", "RUNC_GLAC_TYP", "RUNC_ORIG_DESCR", "ccw20ph", "ccw20tg", "pauschalgef"])
#for row in cursor:
#    kind=row[0]
#    runc_litho=row[1]
#    runc_litstrat=row[2]
#    runc_structur=row[3]
#    runc_morpholo=row[4]
#    runc_glac_typ=row[5]
#    runc_orig_descr=row[6]
#    for index, dfrow in phDEPOSITdf.iterrows():
#        if dfrow.KIND==kind and dfrow.RUNC_LITHO==runc_litho and dfrow.RUNC_LITSTRAT==runc_litstrat and dfrow.RUNC_STRUCTUR==runc_structur and dfrow.RUNC_MORPHOLO==runc_morpholo and dfrow.RUNC_GLAC_TYP==runc_glac_typ and dfrow.RUNC_ORIG_DESCR==runc_orig_descr:
#            row[7] = dfrow.BodenpH
#            row[8] = dfrow.Tongehalt
#            if dfrow.Pauschalgefaelle==1:
#                row[9]=dfrow.Pauschalgefaelle
#    cursor.updateRow(row)
#del row
#del cursor
#manueller join fuer DEPOSIT
arcpy.AddField_management(in_table="xlsdeposit", field_name="joinstr", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table="xlsdeposit", field="joinstr", expression='[KIND]&"_"& [RUNC_LITHO]&"_"& [RUNC_LITSTRAT]&"_"& [RUNC_STRUCTUR]&"_"& [RUNC_MORPHOLO]&"_"& [RUNC_GLAC_TYP]&"_"& [RUNC_ORIG_DESCR]', expression_type="VB", code_block="")
arcpy.AddField_management(in_table="GC_UNCO_DESPOSIT", field_name="joinstr", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.DomainToTable_management(in_workspace="D:/CCW20/GIS/geocover.gdb", domain_name="GC_LITHO_UNCO_CD", out_table="D:/CCW20/GIS/geocover.gdb/domain_GC_LITHO_UNCO_CD", code_field="code", description_field="GC_LITHO_UNCO_CD", configuration_keyword="")
arcpy.DomainToTable_management(in_workspace="D:/CCW20/GIS/geocover.gdb", domain_name="GC_LITSTRAT_UNCO_CD", out_table="D:/CCW20/GIS/geocover.gdb/domain_GC_LITSTRAT_UNCO_CD", code_field="code", description_field="GC_LITSTRAT_UNCO_CD", configuration_keyword="")
arcpy.DomainToTable_management(in_workspace="D:/CCW20/GIS/geocover.gdb", domain_name="GC_UN_DEP_RUNC_STRUCTUR_CD", out_table="D:/CCW20/GIS/geocover.gdb/domain_GC_UN_DEP_RUNC_STRUCTUR_CD", code_field="code", description_field="GC_UN_DEP_RUNC_STRUCTUR_CD", configuration_keyword="")
arcpy.DomainToTable_management(in_workspace="D:/CCW20/GIS/geocover.gdb", domain_name="GC_UN_DEP_RUNC_MORPHOLO_CD", out_table="D:/CCW20/GIS/geocover.gdb/domain_GC_UN_DEP_RUNC_MORPHOLO_CD", code_field="code", description_field="GC_UN_DEP_RUNC_MORPHOLO_CD", configuration_keyword="")
arcpy.DomainToTable_management(in_workspace="D:/CCW20/GIS/geocover.gdb", domain_name="GC_UN_DEP_RUNC_GLAC_TYP_CD", out_table="D:/CCW20/GIS/geocover.gdb/domain_GC_UN_DEP_RUNC_GLAC_TYP_CD", code_field="code", description_field="GC_UN_DEP_RUNC_GLAC_TYP_CD", configuration_keyword="")
#join manually
arcpy.CalculateField_management(in_table="GC_UNCO_DESPOSIT", field="GC_UNCO_DESPOSIT.joinstr", expression='[GC_UNCO_DESPOSIT.KIND]&"_"& [domain_GC_LITHO_UNCO_CD.GC_LITHO_UNCO_CD]&"_"& [domain_GC_LITSTRAT_UNCO_CD.GC_LITSTRAT_UNCO_CD]&"_"& [domain_GC_UN_DEP_RUNC_STRUCTUR_CD.GC_UN_DEP_RUNC_STRUCTUR_CD]&"_"& [domain_GC_UN_DEP_RUNC_MORPHOLO_CD.GC_UN_DEP_RUNC_MORPHOLO_CD]&"_"& [domain_GC_UN_DEP_RUNC_GLAC_TYP_CD.GC_UN_DEP_RUNC_GLAC_TYP_CD]&"_"& [GC_UNCO_DESPOSIT.RUNC_ORIG_DESCR]', expression_type="VB", code_block="")



##BEDROCK
#cursor = arcpy.da.UpdateCursor(shpBEDROCK, ["KIND", "RBED_TECTO", "RBED_FM_HOMOG", "RBED_ORIG_DESCR", "ccw20ph", "ccw20tg", "pauschalgef"])
#for row in cursor:
#    kind=row[0]
#    rbed_tecto=row[1]
#    rbed_fm_homog=row[2]
#    rbed_orig_descr=row[3]
#    for index, dfrow in phBEDROCKdf.iterrows():
#        if dfrow.KIND==kind and dfrow.RBED_TECTO==rbed_tecto and dfrow.RBED_FM_HOMOG==rbed_fm_homog and dfrow.RBED_ORIG_DESCR==rbed_orig_descr:
#            row[4] = dfrow.BodenpH
#            row[5] = dfrow.Tongehalt
#            if dfrow.Pauschalgefaelle==1:
#                row[6]=dfrow.Pauschalgefaelle
#    cursor.updateRow(row)
#del row
#del cursor
#manueller join fuer BEDROCK
arcpy.CalculateField_management(in_table="GC_BEDROCK", field="GC_BEDROCK.joinstr", expression='[GC_BEDROCK.KIND] &"_"&[domain_GC_TECTO_CD.GC_TECTO_CD]&"_"& [domain_GC_BEDR_RBED_FM_HOMOG_CD.RBED_FM_HOMOG]&"_"& [GC_BEDROCK.RBED_ORIG_DESCR]&"_"& [GC_BEDROCK.RBED_LITSTRAT_LINK]', expression_type="VB", code_block="")
arcpy.CalculateField_management(in_table="GC_BEDROCK", field="GC_BEDROCK.ccw20ph", expression="[xlsbedrock.SicherheitBodenpH]", expression_type="VB", code_block="")
arcpy.CalculateField_management(in_table="GC_BEDROCK", field="GC_BEDROCK.ccw20tg", expression="[xlsbedrock.SicherheitTongehalt]", expression_type="VB", code_block="")
arcpy.CalculateField_management(in_table="GC_BEDROCK", field="pauschalgef", expression="0", expression_type="VB", code_block="")
arcpy.CalculateField_management(in_table="GC_BEDROCK", field="GC_BEDROCK.ccw20ph", expression="[xlsbedrock.BodenpH]", expression_type="VB", code_block="")
arcpy.CalculateField_management(in_table="GC_BEDROCK", field="GC_BEDROCK.ccw20tg", expression="[xlsbedrock.Tongehalt]", expression_type="VB", code_block="")
arcpy.CalculateField_management(in_table="GC_BEDROCK", field="pauschalgef", expression="1", expression_type="VB", code_block="")
arcpy.CalculateField_management(in_table="GC_BEDROCK", field="GC_BEDROCK.joinstr", expression='[GC_BEDROCK.KIND] &"_"&[domain_GC_TECTO_CD.GC_TECTO_CD]&"_"& [domain_GC_BEDR_RBED_FM_HOMOG_CD.RBED_FM_HOMOG]&"_"& [GC_BEDROCK.RBED_ORIG_DESCR]&"_"& [GC_BEDROCK.RBED_LITSTRAT_LINK]', expression_type="VB", code_block="")



#join GR files


#convert shapefiles to raster
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/GC_ROCK_BODIES/GC_BEDROCK", value_field="ccw20ph", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/ph_bedrock", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/GC_ROCK_BODIES/GC_BEDROCK", value_field="ccw20tg", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/tg_bedrock", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/GC_ROCK_BODIES/GC_BEDROCK", value_field="pauschalgef", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/pg_bedrock", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/GC_ROCK_BODIES/GC_UNCO_DESPOSIT", value_field="ccw20ph", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/ph_deposit", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/GC_ROCK_BODIES/GC_UNCO_DESPOSIT", value_field="ccw20tg", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/tg_deposit", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/GC_ROCK_BODIES/GC_UNCO_DESPOSIT", value_field="pauschalgef", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/pg_deposit", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/GEOCOVER_MAIN_F", value_field="ccw20ph", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/ph_gr", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/GEOCOVER_MAIN_F", value_field="ccw20tg", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/tg_gr", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/GEOCOVER_MAIN_F", value_field="pauschalgef", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/pg_gr", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/Geologie_Liechtenstein", value_field="pauschalgef", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/pg_li", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/Geologie_Liechtenstein", value_field="ccw20ph", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/ph_li", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")
arcpy.PolygonToRaster_conversion(in_features="D:/CCW20/GIS/geocover.gdb/Geologie_Liechtenstein", value_field="ccw20tg", out_rasterdataset="D:/CCW20/GIS/geocover_tmp.gdb/tg_li", cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="D:\CHGIS\RASTER\DHM25\dhm25")









#Kuppenlagen bereinigen


#GR Moraenen HUF


#Pauschalgefaelle


