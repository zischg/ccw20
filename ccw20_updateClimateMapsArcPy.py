import arcpy
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import os
arcpy.CheckOutExtension('Spatial')

importdir="L:/D/CCW20/input/Meteotest"
climatemapsdir="L:/D/CCW20/GIS/climatemaps"
tas_anomalies_folder=importdir+"/anomalies/tas"
tasmax_anomalies_folder=importdir+"/anomalies/tasmax"
tasmin_anomalies_folder=importdir+"/anomalies/tasmin"
pr_anomalies_folder=importdir+"/anomalies/pr"
etap_swb_anomalies_folder=importdir+"/anomalies/etap_swb"
scenarionameprefix="ch2018_dsd_"
outdir="L:/D/CCW20/GIS/climatemapsUpdateCH2018"
tempgdb="C:/temp/temp.gdb"
arcpy.env.workspace = tempgdb
arcpy.env.overwriteOutput = True

scenarioslist=["CLMCOM-CCLM5_HADGEM_EUR44_RCP85", "DMI-HIRHAM_ECEARTH_EUR11_RCP26", "SMHI-RCA_MPIESM_EUR44_RCP45"]
periodslist=["2070_2099-1981_2010"] #"2011_2044-1981_2010", "2045_2074-1981_2010",
tmapstoupdate_tas_list=["tyymean8110","toctmean8110","tjulmean8110","tjanmean8110","taprmean8110","tamjjasmean8110"]
tmapstoupdate_tasmin_list=["tabsmin","tyymin8110","toctmin8110","tjulmin8110","tjanmin8110","taprmin8110"]
tmapstoupdate_tasmax_list=["tabsmax","tyymax8110","toctmax8110","tjulmax8110","tjanmax8110","taprmax8110"]

#set einvironment
referenceraster=arcpy.Raster("L:/D/CCW20/GIS/dhm25.tif")
arcpy.env.cellSize = referenceraster
arcpy.env.extent = referenceraster
arcpy.env.snapRaster = referenceraster
arcpy.env.Mask = arcpy.Raster("L:/D/CCW20/GIS/chmask.tif")


#***********************************************************************
#functions

#***********************************************************************


#loop through temperature maps
scenario=0
while scenario < len(scenarioslist):
    print(scenarioslist[scenario])
    period=0
    while period < len(periodslist):
        print(periodslist[period])
        # convert NETCDF file to 25m tas anomaly raster
        arcpy.MakeNetCDFRasterLayer_md(in_netCDF_file=tas_anomalies_folder + "/" + scenarionameprefix + scenarioslist[
            scenario] + "_tas_anomalies_" + periodslist[period] + ".nc", variable="tas", x_dimension="chx",
                                       y_dimension="chy", out_raster_layer="taslayer", band_dimension="",
                                       dimension_values="", value_selection_method="BY_VALUE",
                                       cell_registration="CENTER")
        arcpy.CopyRaster_management(in_raster="taslayer",
                                    out_rasterdataset=outdir + "/" + scenarionameprefix + scenarioslist[
                                        scenario] + "_" + periodslist[period] + "/tas.tif", config_keyword="",
                                    background_value="", nodata_value="-9.990000e+02", onebit_to_eightbit="NONE",
                                    colormap_to_RGB="NONE", pixel_type="", scale_pixel_value="NONE",
                                    RGB_to_Colormap="NONE", format="TIFF", transform="NONE")
        arcpy.DefineProjection_management(
            in_dataset=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tas.tif",
            coor_system="PROJCS['CH1903+_LV95',GEOGCS['GCS_CH1903+',DATUM['D_CH1903+',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',2600000.0],PARAMETER['False_Northing',1200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]")
        arcpy.ProjectRaster_management(
            in_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tas.tif",
            out_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasLV03.tif",
            out_coor_system="PROJCS['CH1903_LV03',GEOGCS['GCS_CH1903',DATUM['D_CH1903',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',600000.0],PARAMETER['False_Northing',200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]",
            resampling_type="NEAREST", cell_size="250 250", geographic_transform="CH1903_To_CH1903+_1_NTv2",
            Registration_Point="",
            in_coor_system="PROJCS['CH1903+_LV95',GEOGCS['GCS_CH1903+',DATUM['D_CH1903+',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',2600000.0],PARAMETER['False_Northing',1200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]",
            vertical="NO_VERTICAL")
        arcpy.RasterToPoint_conversion(
            in_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasLV03.tif", out_point_features=tempgdb + "/raspoints", raster_field="Value")
        arcpy.gp.NaturalNeighbor_sa("raspoints", "grid_code", outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasLV03_25m.tif", referenceraster)

        # convert NETCDF file to 25m tasmax anomaly raster
        arcpy.MakeNetCDFRasterLayer_md(in_netCDF_file=tasmax_anomalies_folder + "/" + scenarionameprefix + scenarioslist[
            scenario] + "_tasmax_anomalies_" + periodslist[period] + ".nc", variable="tasmax", x_dimension="chx",
                                       y_dimension="chy", out_raster_layer="taslayer", band_dimension="",
                                       dimension_values="", value_selection_method="BY_VALUE",
                                       cell_registration="CENTER")
        arcpy.CopyRaster_management(in_raster="taslayer",
                                    out_rasterdataset=outdir + "/" + scenarionameprefix + scenarioslist[
                                        scenario] + "_" + periodslist[period] + "/tasmax.tif", config_keyword="",
                                    background_value="", nodata_value="-9.990000e+02", onebit_to_eightbit="NONE",
                                    colormap_to_RGB="NONE", pixel_type="", scale_pixel_value="NONE",
                                    RGB_to_Colormap="NONE", format="TIFF", transform="NONE")
        arcpy.DefineProjection_management(
            in_dataset=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasmax.tif",
            coor_system="PROJCS['CH1903+_LV95',GEOGCS['GCS_CH1903+',DATUM['D_CH1903+',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',2600000.0],PARAMETER['False_Northing',1200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]")
        arcpy.ProjectRaster_management(
            in_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasmax.tif",
            out_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasmaxLV03.tif",
            out_coor_system="PROJCS['CH1903_LV03',GEOGCS['GCS_CH1903',DATUM['D_CH1903',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',600000.0],PARAMETER['False_Northing',200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]",
            resampling_type="NEAREST", cell_size="250 250", geographic_transform="CH1903_To_CH1903+_1_NTv2",
            Registration_Point="",
            in_coor_system="PROJCS['CH1903+_LV95',GEOGCS['GCS_CH1903+',DATUM['D_CH1903+',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',2600000.0],PARAMETER['False_Northing',1200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]",
            vertical="NO_VERTICAL")
        arcpy.RasterToPoint_conversion(
            in_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasmaxLV03.tif", out_point_features=tempgdb + "/raspoints", raster_field="Value")
        arcpy.gp.NaturalNeighbor_sa("raspoints", "grid_code", outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasmaxLV03_25m.tif", referenceraster)

        # convert NETCDF file to 25min anomaly raster
        arcpy.MakeNetCDFRasterLayer_md(in_netCDF_file=tasmin_anomalies_folder + "/" + scenarionameprefix + scenarioslist[
            scenario] + "_tasmin_anomalies_" + periodslist[period] + ".nc", variable="tasmin", x_dimension="chx",
                                       y_dimension="chy", out_raster_layer="taslayer", band_dimension="",
                                       dimension_values="", value_selection_method="BY_VALUE",
                                       cell_registration="CENTER")
        arcpy.CopyRaster_management(in_raster="taslayer",
                                    out_rasterdataset=outdir + "/" + scenarionameprefix + scenarioslist[
                                        scenario] + "_" + periodslist[period] + "/tasmin.tif", config_keyword="",
                                    background_value="", nodata_value="-9.990000e+02", onebit_to_eightbit="NONE",
                                    colormap_to_RGB="NONE", pixel_type="", scale_pixel_value="NONE",
                                    RGB_to_Colormap="NONE", format="TIFF", transform="NONE")
        arcpy.DefineProjection_management(
            in_dataset=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasmin.tif",
            coor_system="PROJCS['CH1903+_LV95',GEOGCS['GCS_CH1903+',DATUM['D_CH1903+',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',2600000.0],PARAMETER['False_Northing',1200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]")
        arcpy.ProjectRaster_management(
            in_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasmin.tif",
            out_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasminLV03.tif",
            out_coor_system="PROJCS['CH1903_LV03',GEOGCS['GCS_CH1903',DATUM['D_CH1903',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',600000.0],PARAMETER['False_Northing',200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]",
            resampling_type="NEAREST", cell_size="250 250", geographic_transform="CH1903_To_CH1903+_1_NTv2",
            Registration_Point="",
            in_coor_system="PROJCS['CH1903+_LV95',GEOGCS['GCS_CH1903+',DATUM['D_CH1903+',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',2600000.0],PARAMETER['False_Northing',1200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]",
            vertical="NO_VERTICAL")
        arcpy.RasterToPoint_conversion(
            in_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasminLV03.tif", out_point_features=tempgdb + "/raspoints", raster_field="Value")
        arcpy.gp.NaturalNeighbor_sa("raspoints", "grid_code",
                                    outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                                        period] + "/tasminLV03_25m.tif", referenceraster)

        # convert NETCDF file to 25m tas AMJJA anomaly raster
        arcpy.MakeNetCDFRasterLayer_md(
            in_netCDF_file=tas_anomalies_folder + "/" + scenarionameprefix + scenarioslist[
                scenario] + "_tas_anomalies_" + periodslist[period] + "_AMJJA.nc", variable="tas", x_dimension="chx",
            y_dimension="chy", out_raster_layer="taslayer", band_dimension="",
            dimension_values="", value_selection_method="BY_VALUE",
            cell_registration="CENTER")
        arcpy.CopyRaster_management(in_raster="taslayer",
                                    out_rasterdataset=outdir + "/" + scenarionameprefix + scenarioslist[
                                        scenario] + "_" + periodslist[period] + "/tasAMJJA.tif", config_keyword="",
                                    background_value="", nodata_value="-9.990000e+02", onebit_to_eightbit="NONE",
                                    colormap_to_RGB="NONE", pixel_type="", scale_pixel_value="NONE",
                                    RGB_to_Colormap="NONE", format="TIFF", transform="NONE")
        arcpy.DefineProjection_management(
            in_dataset=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasAMJJA.tif",
            coor_system="PROJCS['CH1903+_LV95',GEOGCS['GCS_CH1903+',DATUM['D_CH1903+',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',2600000.0],PARAMETER['False_Northing',1200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]")
        arcpy.ProjectRaster_management(
            in_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasAMJJA.tif",
            out_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasAMJJALV03.tif",
            out_coor_system="PROJCS['CH1903_LV03',GEOGCS['GCS_CH1903',DATUM['D_CH1903',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',600000.0],PARAMETER['False_Northing',200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]",
            resampling_type="NEAREST", cell_size="250 250", geographic_transform="CH1903_To_CH1903+_1_NTv2",
            Registration_Point="",
            in_coor_system="PROJCS['CH1903+_LV95',GEOGCS['GCS_CH1903+',DATUM['D_CH1903+',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',2600000.0],PARAMETER['False_Northing',1200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]",
            vertical="NO_VERTICAL")
        arcpy.RasterToPoint_conversion(
            in_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasAMJJALV03.tif", out_point_features=tempgdb + "/raspoints", raster_field="Value")
        arcpy.gp.NaturalNeighbor_sa("raspoints", "grid_code",
                                    outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                                        period] + "/tasAMJJALV03_25m.tif", referenceraster)

        # convert NETCDF file to 25m tas NDJFM anomaly raster
        arcpy.MakeNetCDFRasterLayer_md(
            in_netCDF_file=tas_anomalies_folder + "/" + scenarionameprefix + scenarioslist[
                scenario] + "_tas_anomalies_" + periodslist[period] + "_NDJFM.nc", variable="tas", x_dimension="chx",
            y_dimension="chy", out_raster_layer="taslayer", band_dimension="",
            dimension_values="", value_selection_method="BY_VALUE",
            cell_registration="CENTER")
        arcpy.CopyRaster_management(in_raster="taslayer",
                                    out_rasterdataset=outdir + "/" + scenarionameprefix + scenarioslist[
                                        scenario] + "_" + periodslist[period] + "/tasNDJFM.tif", config_keyword="",
                                    background_value="", nodata_value="-9.990000e+02", onebit_to_eightbit="NONE",
                                    colormap_to_RGB="NONE", pixel_type="", scale_pixel_value="NONE",
                                    RGB_to_Colormap="NONE", format="TIFF", transform="NONE")
        arcpy.DefineProjection_management(
            in_dataset=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasNDJFM.tif",
            coor_system="PROJCS['CH1903+_LV95',GEOGCS['GCS_CH1903+',DATUM['D_CH1903+',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',2600000.0],PARAMETER['False_Northing',1200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]")
        arcpy.ProjectRaster_management(
            in_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasNDJFM.tif",
            out_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasNDJFMLV03.tif",
            out_coor_system="PROJCS['CH1903_LV03',GEOGCS['GCS_CH1903',DATUM['D_CH1903',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',600000.0],PARAMETER['False_Northing',200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]",
            resampling_type="NEAREST", cell_size="250 250", geographic_transform="CH1903_To_CH1903+_1_NTv2",
            Registration_Point="",
            in_coor_system="PROJCS['CH1903+_LV95',GEOGCS['GCS_CH1903+',DATUM['D_CH1903+',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',2600000.0],PARAMETER['False_Northing',1200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]",
            vertical="NO_VERTICAL")
        arcpy.RasterToPoint_conversion(
            in_raster=outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasNDJFMLV03.tif", out_point_features=tempgdb + "/raspoints", raster_field="Value")
        arcpy.gp.NaturalNeighbor_sa("raspoints", "grid_code",
                                    outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                                        period] + "/tasNDJFMLV03_25m.tif", referenceraster)
        #update climate maps
        for item in tmapstoupdate_tas_list:
            if "jan" in item or "oct" in item:
                arcpy.gp.Plus_sa(climatemapsdir+"/"+item+".tif", outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[period] + "/tasNDJFMLV03_25m.tif",outdir + "/" + item.replace("8110","")+scenarioslist[scenario] + "_" + periodslist[period][:9]+".tif")
            elif "apr" in item or "jul" in item or "tamjjasmean" in item:
                arcpy.gp.Plus_sa(climatemapsdir+"/"+item+".tif", outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                    period] + "/tasAMJJALV03_25m.tif",
                                 outdir + "/" + item.replace("8110","")+"_"+scenarioslist[scenario] + "_" + periodslist[
                    period][:9]+".tif")
            else:
                arcpy.gp.Plus_sa(climatemapsdir+"/"+item+".tif", outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                    period] + "/tasLV03_25m.tif",
                                 outdir + "/" + item.replace("8110","")+"_"+scenarioslist[scenario] + "_" + periodslist[
                    period][:9]+".tif")

        for item in tmapstoupdate_tasmax_list:
            arcpy.gp.Plus_sa(climatemapsdir+"/"+item+".tif", outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasmaxLV03_25m.tif",
                             outdir + "/" + item.replace("8110","")+"_"+scenarioslist[scenario] + "_" + periodslist[
                period][:9]+".tif")#tasmaxLV03_25m

        for item in tmapstoupdate_tasmin_list:
            arcpy.gp.Plus_sa(climatemapsdir+"/"+item+".tif", outdir + "/" + scenarionameprefix + scenarioslist[scenario] + "_" + periodslist[
                period] + "/tasminLV03_25m.tif",
                             outdir + "/" + item.replace("8110","")+"_"+scenarioslist[scenario] + "_" + periodslist[
                period][:9]+".tif") #tasminLV03_25m
        period+=1
    scenario+=1







