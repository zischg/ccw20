#prepares the sample data for the development of the models

import arcpy
import numpy

myworkspace="D:/CCW20/GIS"
cmapsdir=myworkspace+"/climatemaps"
dhmraster=arcpy.Raster("D:/CCW20/GIS/dhm25.tif")
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension('Spatial')
#read the positive sample dataset
samples_n_fc=myworkspace+"/samples.gdb/samples_n_6190"
samples_s_fc=myworkspace+"/samples.gdb/samples_s_6190"
arcpy.env.workspace=cmapsdir
inrasterlist=[["dhm25.tif","dhm25"],["litho7g.tif","litho7g"],["tyymin6190.tif","tyymin6190"],["tyymean6190.tif","tyymean6190"],["tyymax6190.tif","tyymax6190"],["toctmin6190.tif","toctmin6190"],["toctmean6190.tif","toctmean6190"],["toctmax6190.tif","toctmax6190"],["tjulmin6190.tif","tjulmin6190"],["tjulmean6190.tif","tjulmean6190"],["tjulmax6190.tif","tjulmax6190"],["tjanmin6190.tif","tjanmin6190"],["tjanmean6190.tif","tjanmean6190"],["tjanmax6190.tif","tjanmax6190"],["taprmin6190.tif","taprmin6190"],["taprmean6190.tif","taprmean6190"],["taprmax6190.tif","taprmax6190"],["tabsmin.tif","tabsmin"],["tabsmax.tif","tabsmax"],["rnormyy6190.tif","rnormyy6190"],["rnormsep6190.tif","rnormsep6190"],["rnormoct6190.tif","rnormoct6190"],["rnormnov6190.tif","rnormnov6190"],["rnormmay6190.tif","rnormmay6190"],["rnormmar6190.tif","rnormmar6190"],["rnormjun6190.tif","rnormjun6190"],["rnormjul6190.tif","rnormjul6190"],["rnormjan6190.tif","rnormjan6190"],["rnormfeb6190.tif","rnormfeb6190"],["rnormdec6190.tif","rnormdec6190"],["rnormaug6190.tif","rnormaug6190"],["rnormapr6190.tif","rnormapr6190"],["rnormjja6190.tif","rnormjja6190"],["rnormamjjas6190.tif","rnormamjjas6190"],["rnormamjja6190.tif","rnormamjja6190"],["mlfyy.tif","mlfyy"],["mlfoct.tif","mlfoct"],["mlfjul.tif","mlfjul"],["mlfjan.tif","mlfjan"],["mlfapr.tif","mlfapr"],["lfoct.tif","lfoct"],["lfjul.tif","lfjul"],["lfjan.tif","lfjan"],["lfyy.tif","lfyy"],["kontyy1800.tif","kontyy1800"],["kontyy1400.tif","kontyy1400"],["kontyy1000.tif","kontyy1000"],["kontyy.tif","kontyy"],["kontoct2000.tif","kontoct2000"],["kontoct1800.tif","kontoct1800"],["kontoct1400.tif","kontoct1400"],["kontoct1000.tif","kontoct1000"],["kontoct.tif","kontoct"],["kontjul2000.tif","kontjul2000"],["kontjul1800.tif","kontjul1800"],["kontjul1400.tif","kontjul1400"],["kontjul1000.tif","kontjul1000"],["kontjul.tif","kontjul"],["kontjan2000.tif","kontjan2000"],["kontjan1800.tif","kontjan1800"],["kontjan1400.tif","kontjan1400"],["kontjan1000.tif","kontjan1000"],["kontjan.tif","kontjan"],["kontjahr2000.tif","kontjahr2000"],["kontapr2000.tif","kontapr2000"],["kontapr1800.tif","kontapr1800"],["kontapr1400.tif","kontapr1400"],["kontapr1000.tif","kontapr1000"],["kontapr.tif","kontapr"],["kontabs2000.tif","kontabs2000"],["kontabs1000.tif","kontabs1000"],["kontabs.tif","kontabs"],["globradyyw.tif","globradyyw"],["globradoctw.tif","globradoctw"],["globradjulw.tif","globradjulw"],["globradjanw.tif","globradjanw"],["globradaprw.tif","globradaprw"],["foehnhyy.tif","foehnhyy"],["foehnhoct.tif","foehnhoct"],["foehnhjul.tif","foehnhjul"],["foehnhjan.tif","foehnhjan"],["foehnhapr.tif","foehnhapr"],["etaetp","etaetp"]]
#inrasterlist=[["dhm25.tif","dhm25"],["litho7g.tif","litho7g"],["tyymin8110.tif","tyymin8110"],["tyymean8110.tif","tyymean8110"],["tyymax8110.tif","tyymax8110"],["toctmin8110.tif","toctmin8110"],["toctmean8110.tif","toctmean8110"],["toctmax8110.tif","toctmax8110"],["tjulmin8110.tif","tjulmin8110"],["tjulmean8110.tif","tjulmean8110"],["tjulmax8110.tif","tjulmax8110"],["tjanmin8110.tif","tjanmin8110"],["tjanmean8110.tif","tjanmean8110"],["tjanmax8110.tif","tjanmax8110"],["taprmin8110.tif","taprmin8110"],["taprmean8110.tif","taprmean8110"],["taprmax8110.tif","taprmax8110"],["tabsmin.tif","tabsmin"],["tabsmax.tif","tabsmax"],["nsyy.tif","nsyy"],["nssep.tif","nssep"],["nsoct.tif","nsoct"],["nsnov.tif","nsnov"],["nsmay.tif","nsmay"],["nsmar.tif","nsmar"],["nsjun.tif","nsjun"],["nsjul.tif","nsjul"],["nsjan.tif","nsjan"],["nsfeb.tif","nsfeb"],["nsdec.tif","nsdec"],["nsaug.tif","nsaug"],["nsapr.tif","nsapr"],["ns_jja.tif","ns_jja"],["ns_amjjas.tif","ns_amjjas"],["ns_amjja.tif","ns_amjja"],["mlfyy.tif","mlfyy"],["mlfoct.tif","mlfoct"],["mlfjul.tif","mlfjul"],["mlfjan.tif","mlfjan"],["mlfapr.tif","mlfapr"],["lfoct.tif","lfoct"],["lfjul.tif","lfjul"],["lfjan.tif","lfjan"],["lfyy.tif","lfyy"],["kontyy1800.tif","kontyy1800"],["kontyy1400.tif","kontyy1400"],["kontyy1000.tif","kontyy1000"],["kontyy.tif","kontyy"],["kontoct2000.tif","kontoct2000"],["kontoct1800.tif","kontoct1800"],["kontoct1400.tif","kontoct1400"],["kontoct1000.tif","kontoct1000"],["kontoct.tif","kontoct"],["kontjul2000.tif","kontjul2000"],["kontjul1800.tif","kontjul1800"],["kontjul1400.tif","kontjul1400"],["kontjul1000.tif","kontjul1000"],["kontjul.tif","kontjul"],["kontjan2000.tif","kontjan2000"],["kontjan1800.tif","kontjan1800"],["kontjan1400.tif","kontjan1400"],["kontjan1000.tif","kontjan1000"],["kontjan.tif","kontjan"],["kontjahr2000.tif","kontjahr2000"],["kontapr2000.tif","kontapr2000"],["kontapr1800.tif","kontapr1800"],["kontapr1400.tif","kontapr1400"],["kontapr1000.tif","kontapr1000"],["kontapr.tif","kontapr"],["kontabs2000.tif","kontabs2000"],["kontabs1000.tif","kontabs1000"],["kontabs.tif","kontabs"],["globradyyw.tif","globradyyw"],["globradoctw.tif","globradoctw"],["globradjulw.tif","globradjulw"],["globradjanw.tif","globradjanw"],["globradaprw.tif","globradaprw"],["foehnhyy.tif","foehnhyy"],["foehnhoct.tif","foehnhoct"],["foehnhjul.tif","foehnhjul"],["foehnhjan.tif","foehnhjan"],["foehnhapr.tif","foehnhapr"],["etaetp","etaetp"]]
arcpy.gp.ExtractMultiValuesToPoints_sa(samples_n_fc,inrasterlist, "NONE")
arcpy.gp.ExtractMultiValuesToPoints_sa(samples_s_fc,inrasterlist, "NONE")

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "samples_n_6190"
arcpy.gp.ExtractMultiValuesToPoints_sa("samples_n_6190", "rnormjan6190.tif rnormjan6190;rnormfeb6190.tif rnormfeb6190;rnormmar6190.tif rnormmar6190;rnormapr6190.tif rnormapr6190;rnormmay6190.tif rnormmay6190;rnormjun6190.tif rnormjun6190;rnormjul6190.tif rnormjul6190;rnormaug6190.tif rnormaug6190;rnormsep6190.tif rnormsep6190;rnormoct6190.tif rnormoct6190;rnormnov6190.tif rnormnov6190;rnormdec6190.tif rnormdec6190;rnormyy6190.tif rnormyy6190;rnormamjja6190.tif rnormamjja6190;rnormamjjas6190.tif rnormamjjas6190", "NONE")
arcpy.gp.ExtractMultiValuesToPoints_sa("D:/CCW20/GIS/samples.gdb/samples_n_6190", "tjanmax6190.tif tjanmax6190;tjanmean6190.tif tjanmean6190;tjanmin6190.tif tjanmin6190;taprmax6190.tif taprmax6190;taprmean6190.tif taprmean6190;taprmin6190.tif taprmin6190;tjulmax6190.tif tjulmax6190;tjulmean6190.tif tjulmean6190;tjulmin6190.tif tjulmin6190;toctmax6190.tif toctmax6190;toctmean6190.tif toctmean6190;toctmin6190.tif toctmin6190;tyymax6190.tif tyymax6190;tyymean6190.tif tyymean6190;tyymin6190.tif tyymin6190;vegper6191.tif vegper6191;tamjjasmean6190.tif tamjjasmean6190", "NONE")







#Create a negative sample dataset of points above the upper limit of altitudinal vegetation belts
lowerLeft = arcpy.Point(dhmraster.extent.XMin,dhmraster.extent.YMin)
cellSize = dhmraster.meanCellWidth
upperlimit_n_points=myworkspace+"/samples.gdb/"+"hssample_n"
upperlimit_n = arcpy.Raster(myworkspace+"/samples/"+"hssample_n.tif")
# Convert Raster to numpy array
dhm_arr = arcpy.RasterToNumPyArray(dhmraster)
upperlimit_n_arr = arcpy.RasterToNumPyArray(upperlimit_n)
rows=numpy.shape(upperlimit_n_arr)[0]
cols=numpy.shape(upperlimit_n_arr)[1]
#create a new array and iterate through original sampe array and dhm and select the raster cell exactly above the original array
negative_upperlimit_n_arr=numpy.zeros((rows, cols), dtype=int)
negative_upperlimit_n_arr[:]=-2147483648
i=1
while i < rows-1:
    j=1
    while j<cols-1:
        hs_pos=upperlimit_n_arr[i,j]
        if hs_pos>0:
            z0=dhm_arr[i,j]
            #look around for the 8 neighbors and chose the cell with the highest z-value (higher than center cell)
            zlist=[]
            for d in [-1,0,1]:
                for e in [-1,0,1]:
                    zlist.append(dhm_arr[i+d,j+e])
                    maxz=max(zlist)
            for d in [-1,0,1]:
                for e in [-1,0,1]:
                    if dhm_arr[i+d,j+e]==maxz and maxz>z0:
                        negative_upperlimit_n_arr[i + d, j + e]=hs_pos
        j+=1
    i+=1

#Convert Array to raster (keep the origin and cellsize the same as the input)
newRaster = arcpy.NumPyArrayToRaster(negative_upperlimit_n_arr,lowerLeft,cellSize)
newRaster.save(myworkspace+"/samples/"+"hssample_n_negative.tif")
#convert the raster to sample points
samples_n_negative_fc=myworkspace+"/samples.gdb/samples_n_negative"
arcpy.RasterToPoint_conversion(in_raster="hssample_n_negative.tif", out_point_features=samples_n_negative_fc, raster_field="Value")
arcpy.AddField_management(in_table=samples_n_negative_fc, field_name="HSmax", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=samples_n_negative_fc, field="HSmax", expression="!grid_code!", expression_type="PYTHON", code_block="")
arcpy.DeleteField_management(in_table=samples_n_negative_fc, drop_field="grid_code")
arcpy.DeleteField_management(in_table=samples_n_negative_fc, drop_field="pointid")
#extract raster values
arcpy.env.workspace=myworkspace
inrasterlist=[["dhm25.tif","dhm25"]]
arcpy.gp.ExtractMultiValuesToPoints_sa(samples_n_negative_fc,inrasterlist, "NONE")
arcpy.env.workspace=cmapsdir
inrasterlist=[["litho7g.tif","litho7g"],["tyymin8110.tif","tyymin8110"],["tyymean8110.tif","tyymean8110"],["tyymax8110.tif","tyymax8110"],["toctmin8110.tif","toctmin8110"],["toctmean8110.tif","toctmean8110"],["toctmax8110.tif","toctmax8110"],["tjulmin8110.tif","tjulmin8110"],["tjulmean8110.tif","tjulmean8110"],["tjulmax8110.tif","tjulmax8110"],["tjanmin8110.tif","tjanmin8110"],["tjanmean8110.tif","tjanmean8110"],["tjanmax8110.tif","tjanmax8110"],["taprmin8110.tif","taprmin8110"],["taprmean8110.tif","taprmean8110"],["taprmax8110.tif","taprmax8110"],["tabsmin.tif","tabsmin"],["tabsmax.tif","tabsmax"],["nsyy.tif","nsyy"],["nssep.tif","nssep"],["nsoct.tif","nsoct"],["nsnov.tif","nsnov"],["nsmay.tif","nsmay"],["nsmar.tif","nsmar"],["nsjun.tif","nsjun"],["nsjul.tif","nsjul"],["nsjan.tif","nsjan"],["nsfeb.tif","nsfeb"],["nsdec.tif","nsdec"],["nsaug.tif","nsaug"],["nsapr.tif","nsapr"],["ns_jja.tif","ns_jja"],["ns_amjjas.tif","ns_amjjas"],["ns_amjja.tif","ns_amjja"],["mlfyy.tif","mlfyy"],["mlfoct.tif","mlfoct"],["mlfjul.tif","mlfjul"],["mlfjan.tif","mlfjan"],["mlfapr.tif","mlfapr"],["lfoct.tif","lfoct"],["lfjul.tif","lfjul"],["lfjan.tif","lfjan"],["lfyy.tif","lfyy"],["kontyy1800.tif","kontyy1800"],["kontyy1400.tif","kontyy1400"],["kontyy1000.tif","kontyy1000"],["kontyy.tif","kontyy"],["kontoct2000.tif","kontoct2000"],["kontoct1800.tif","kontoct1800"],["kontoct1400.tif","kontoct1400"],["kontoct1000.tif","kontoct1000"],["kontoct.tif","kontoct"],["kontjul2000.tif","kontjul2000"],["kontjul1800.tif","kontjul1800"],["kontjul1400.tif","kontjul1400"],["kontjul1000.tif","kontjul1000"],["kontjul.tif","kontjul"],["kontjan2000.tif","kontjan2000"],["kontjan1800.tif","kontjan1800"],["kontjan1400.tif","kontjan1400"],["kontjan1000.tif","kontjan1000"],["kontjan.tif","kontjan"],["kontjahr2000.tif","kontjahr2000"],["kontapr2000.tif","kontapr2000"],["kontapr1800.tif","kontapr1800"],["kontapr1400.tif","kontapr1400"],["kontapr1000.tif","kontapr1000"],["kontapr.tif","kontapr"],["kontabs2000.tif","kontabs2000"],["kontabs1000.tif","kontabs1000"],["kontabs.tif","kontabs"],["globradyyw.tif","globradyyw"],["globradoctw.tif","globradoctw"],["globradjulw.tif","globradjulw"],["globradjanw.tif","globradjanw"],["globradaprw.tif","globradaprw"],["foehnhyy.tif","foehnhyy"],["foehnhoct.tif","foehnhoct"],["foehnhjul.tif","foehnhjul"],["foehnhjan.tif","foehnhjan"],["foehnhapr.tif","foehnhapr"],["etaetp","etaetp"]]
arcpy.gp.ExtractMultiValuesToPoints_sa(samples_n_negative_fc,inrasterlist, "NONE")

#arcpy.AddField_management(in_table=myworkspace+"/samples.gdb/samples_n_negative", field_name="class", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
#arcpy.CalculateField_management(in_table=myworkspace+"/samples.gdb/samples_n_negative", field="class", expression="1", expression_type="PYTHON", code_block="")


