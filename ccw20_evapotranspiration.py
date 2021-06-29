import os
import numpy as np
import pandas as pd
from osgeo import osr, gdal
import math
import matplotlib.pyplot as plt
drv = gdal.GetDriverByName('GTiff')
srs = osr.SpatialReference()
srs.ImportFromEPSG(21781) #LV03
gtiff_driver=gdal.GetDriverByName("GTiff")
#read sample data
myworkspace="D:/CCW20/GIS"
climatemapsdir=myworkspace+"/climatemaps"
referenceraster="D:/CCW20/GIS/dhm25.tif"
outdir=myworkspace+"/climatemapsUpdateCH2018"
#climatescenarioname="CLMCOM-CCLM5_HADGEM_EUR44_RCP85_2070_2099"
climatescenarioname="DMI-HIRHAM_ECEARTH_EUR11_RCP26_2070_2099"
#climatescenarioname="SMHI-RCA_MPIESM_EUR44_RCP45_2070_2099"
NODATA_value=-9999

#*************************************************************
#functions
def convert_tif_to_array(intifraster):
    inras = gdal.Open(intifraster)
    inband = inras.GetRasterBand(1)
    outarr = inband.ReadAsArray()
    return outarr
def convertarrtotif(arr, outfile, tifdatatype, referenceraster, nodatavalue):
    ds_in=gdal.Open(referenceraster)
    inband=ds_in.GetRasterBand(1)
    gtiff_driver=gdal.GetDriverByName("GTiff")
    ds_out = gtiff_driver.Create(outfile, inband.XSize, inband.YSize, 1, tifdatatype)
    ds_out.SetProjection(ds_in.GetProjection())
    ds_out.SetGeoTransform(ds_in.GetGeoTransform())
    outband=ds_out.GetRasterBand(1)
    outband.WriteArray(arr)
    outband.SetNoDataValue(nodatavalue)
    ds_out.FlushCache()
    del ds_in
    del ds_out
    del inband
    del outband
# end functions
# *************************************************************

#**************************************************************************************************************
#read the rasters
#reference tif raster
print("read reference raster")
referencetifraster=gdal.Open(referenceraster)
referencetifrasterband=referencetifraster.GetRasterBand(1)
referencerasterProjection=referencetifraster.GetProjection()
ncols=referencetifrasterband.XSize
nrows=referencetifrasterband.YSize
indatatype=referencetifrasterband.DataType
dhmarr=convert_tif_to_array("D:/CCW20/GIS/dhm25.tif")
if np.min(dhmarr)<NODATA_value:
    dhmarr=np.where(dhmarr==np.min(dhmarr),NODATA_value,dhmarr)


print(climatescenarioname)
print("read climate rasters")
globradjanarr=convert_tif_to_array(climatemapsdir+"/globradjanw.tif")
if np.min(globradjanarr)<NODATA_value:
    globradjanarr=np.where(globradjanarr==np.min(globradjanarr),NODATA_value,globradjanarr)
globradaprarr=convert_tif_to_array(climatemapsdir+"/globradaprw.tif")
if np.min(globradaprarr)<NODATA_value:
    globradaprarr=np.where(globradaprarr==np.min(globradaprarr),NODATA_value,globradaprarr)
globradjularr=convert_tif_to_array(climatemapsdir+"/globradjulw.tif")
if np.min(globradjularr)<NODATA_value:
    globradjularr=np.where(globradjularr==np.min(globradjularr),NODATA_value,globradjularr)
globradoctarr=convert_tif_to_array(climatemapsdir+"/globradoctw.tif")
if np.min(globradoctarr)<NODATA_value:
    globradoctarr=np.where(globradoctarr==np.min(globradoctarr),NODATA_value,globradoctarr)
globradyyarr=convert_tif_to_array(climatemapsdir+"/globradyyw.tif")
if np.min(globradyyarr)<NODATA_value:
    globradyyarr=np.where(globradyyarr==np.min(globradyyarr),NODATA_value,globradyyarr)

windjanarr=convert_tif_to_array(climatemapsdir+"/windjanmean.tif")
if np.min(windjanarr)<NODATA_value:
    windjanarr=np.where(windjanarr==np.min(windjanarr),NODATA_value,windjanarr)
windaprarr=convert_tif_to_array(climatemapsdir+"/windaprmean.tif")
if np.min(windaprarr)<NODATA_value:
    windaprarr=np.where(windaprarr==np.min(windaprarr),NODATA_value,windaprarr)
windjularr=convert_tif_to_array(climatemapsdir+"/windjulmean.tif")
if np.min(windjularr)<NODATA_value:
    windjularr=np.where(windjularr==np.min(windjularr),NODATA_value,windjularr)
windoctarr=convert_tif_to_array(climatemapsdir+"/windoctmean.tif")
if np.min(windoctarr)<NODATA_value:
    windoctarr=np.where(windoctarr==np.min(windoctarr),NODATA_value,windoctarr)
windyyarr=convert_tif_to_array(climatemapsdir+"/windyymean.tif")
if np.min(windyyarr)<NODATA_value:
    windyyarr=np.where(windyyarr==np.min(windyyarr),NODATA_value,windyyarr)

mlfjanarr=convert_tif_to_array(climatemapsdir+"/mlfjan.tif")
if np.min(mlfjanarr)<NODATA_value:
    mlfjanarr=np.where(mlfjanarr==np.min(mlfjanarr),NODATA_value,mlfjanarr)
mlfaprarr=convert_tif_to_array(climatemapsdir+"/mlfapr.tif")
if np.min(mlfaprarr)<NODATA_value:
    mlfaprarr=np.where(mlfaprarr==np.min(mlfaprarr),NODATA_value,mlfaprarr)
mlfjularr=convert_tif_to_array(climatemapsdir+"/mlfjul.tif")
if np.min(mlfjularr)<NODATA_value:
    mlfjularr=np.where(mlfjularr==np.min(mlfjularr),NODATA_value,mlfjularr)
mlfoctarr=convert_tif_to_array(climatemapsdir+"/mlfoct.tif")
if np.min(mlfoctarr)<NODATA_value:
    mlfoctarr=np.where(mlfoctarr==np.min(mlfoctarr),NODATA_value,mlfoctarr)
mlfyyarr=convert_tif_to_array(climatemapsdir+"/mlfyy.tif")
if np.min(mlfyyarr)<NODATA_value:
    mlfyyarr=np.where(mlfyyarr==np.min(mlfyyarr),NODATA_value,mlfyyarr)


tjanmeanarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/tjanmean_"+climatescenarioname+".tif")
if np.min(tjanmeanarr)<NODATA_value:
    tjanmeanarr=np.where(tjanmeanarr==np.min(tjanmeanarr),NODATA_value,tjanmeanarr)
taprmeanarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/taprmean_"+climatescenarioname+".tif")
if np.min(taprmeanarr)<NODATA_value:
    taprmeanarr=np.where(taprmeanarr==np.min(taprmeanarr),NODATA_value,taprmeanarr)
tjulmeanarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/tjulmean_"+climatescenarioname+".tif")
if np.min(tjulmeanarr)<NODATA_value:
    tjulmeanarr=np.where(tjulmeanarr==np.min(tjulmeanarr),NODATA_value,tjulmeanarr)
toctmeanarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/toctmean_"+climatescenarioname+".tif")
if np.min(toctmeanarr)<NODATA_value:
    toctmeanarr=np.where(toctmeanarr==np.min(toctmeanarr),NODATA_value,toctmeanarr)
tyymeanarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/tyymean_"+climatescenarioname+".tif")
if np.min(tyymeanarr)<NODATA_value:
    tyymeanarr=np.where(tyymeanarr==np.min(tyymeanarr),NODATA_value,tyymeanarr)

tjanmaxarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/tjanmax_"+climatescenarioname+".tif")
if np.min(tjanmaxarr)<NODATA_value:
    tjanmaxarr=np.where(tjanmaxarr==np.min(tjanmaxarr),NODATA_value,tjanmaxarr)
taprmaxarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/taprmax_"+climatescenarioname+".tif")
if np.min(taprmaxarr)<NODATA_value:
    taprmaxarr=np.where(taprmaxarr==np.min(taprmaxarr),NODATA_value,taprmaxarr)
tjulmaxarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/tjulmax_"+climatescenarioname+".tif")
if np.min(tjulmaxarr)<NODATA_value:
    tjulmaxarr=np.where(tjulmaxarr==np.min(tjulmaxarr),NODATA_value,tjulmaxarr)
toctmaxarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/toctmax_"+climatescenarioname+".tif")
if np.min(toctmaxarr)<NODATA_value:
    toctmaxarr=np.where(toctmaxarr==np.min(toctmaxarr),NODATA_value,toctmaxarr)
tyymaxarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/tyymax_"+climatescenarioname+".tif")
if np.min(tyymaxarr)<NODATA_value:
    tyymaxarr=np.where(tyymaxarr==np.min(tyymaxarr),NODATA_value,tyymaxarr)

tjanminarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/tjanmin_"+climatescenarioname+".tif")
if np.min(tjanminarr)<NODATA_value:
    tjanminarr=np.where(tjanminarr==np.min(tjanminarr),NODATA_value,tjanminarr)
taprminarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/taprmin_"+climatescenarioname+".tif")
if np.min(taprminarr)<NODATA_value:
    taprminarr=np.where(taprminarr==np.min(taprminarr),NODATA_value,taprminarr)
tjulminarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/tjulmin_"+climatescenarioname+".tif")
if np.min(tjulminarr)<NODATA_value:
    tjulminarr=np.where(tjulminarr==np.min(tjulminarr),NODATA_value,tjulminarr)
toctminarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/toctmin_"+climatescenarioname+".tif")
if np.min(toctminarr)<NODATA_value:
    toctminarr=np.where(toctminarr==np.min(toctminarr),NODATA_value,toctminarr)
tyyminarr=convert_tif_to_array(climatemapsdir+"UpdateCH2018/tyymin_"+climatescenarioname+".tif")
if np.min(tyyminarr)<NODATA_value:
    tyyminarr=np.where(tyyminarr==np.min(tyyminarr),NODATA_value,tyyminarr)

globradjan0arr=convert_tif_to_array(climatemapsdir+"/globradjan0w.tif")
if np.min(globradjan0arr)<NODATA_value:
    globradjan0arr=np.where(globradjan0arr==np.min(globradjan0arr),NODATA_value,globradjan0arr)
globradapr0arr=convert_tif_to_array(climatemapsdir+"/globradapr0w.tif")
if np.min(globradapr0arr)<NODATA_value:
    globradapr0arr=np.where(globradapr0arr==np.min(globradapr0arr),NODATA_value,globradapr0arr)
globradjul0arr=convert_tif_to_array(climatemapsdir+"/globradjul0w.tif")
if np.min(globradjul0arr)<NODATA_value:
    globradjul0arr=np.where(globradjul0arr==np.min(globradjul0arr),NODATA_value,globradjul0arr)
globradoct0arr=convert_tif_to_array(climatemapsdir+"/globradoct0w.tif")
if np.min(globradoct0arr)<NODATA_value:
    globradoct0arr=np.where(globradoct0arr==np.min(globradoct0arr),NODATA_value,globradoct0arr)
globradyy0arr=convert_tif_to_array(climatemapsdir+"/globradyy0w.tif")
if np.min(globradyy0arr)<NODATA_value:
    globradyy0arr=np.where(globradyy0arr==np.min(globradyy0arr),NODATA_value,globradyy0arr)

albedojanarr=convert_tif_to_array(climatemapsdir+"/albedojan.tif")
if np.min(albedojanarr)==-128:
    albedojanarr=np.where(albedojanarr==-128,NODATA_value,albedojanarr)
albedoaprarr=convert_tif_to_array(climatemapsdir+"/albedoapr.tif")
if np.min(albedoaprarr)==-128:
    albedoaprarr=np.where(albedoaprarr==-128,NODATA_value,albedoaprarr)
albedojularr=convert_tif_to_array(climatemapsdir+"/albedojul.tif")
if np.min(albedojularr)==-128:
    albedojularr=np.where(albedojularr==-128,NODATA_value,albedojularr)
albedooctarr=convert_tif_to_array(climatemapsdir+"/albedooct.tif")
if np.min(albedooctarr)==-128:
    albedooctarr=np.where(albedooctarr==-128,NODATA_value,albedooctarr)
albedoyyarr=convert_tif_to_array(climatemapsdir+"/albedoyy.tif")
if np.min(albedoyyarr)==-128:
    albedoyyarr=np.where(albedoyyarr==-128,NODATA_value,albedoyyarr)

#radiation
radsjan=0.0864*globradjanarr
radsapr=0.0864*globradaprarr
radsjul=0.0864*globradjularr
radsoct=0.0864*globradoctarr
radsyy=0.0864*globradyyarr
#delta slope
deltajan=4098.0*(0.6108*pow(math.e,(((17.27*tjanmeanarr)/(tjanmeanarr+237.3))))/pow((tjanmeanarr+273.15),2.0))
deltaapr=4098.0*(0.6108*pow(math.e,(((17.27*taprmeanarr)/(taprmeanarr+237.3))))/pow((taprmeanarr+273.15),2.0))
deltajul=4098.0*(0.6108*pow(math.e,(((17.27*tjulmeanarr)/(tjulmeanarr+237.3))))/pow((tjulmeanarr+273.15),2.0))
deltaoct=4098.0*(0.6108*pow(math.e,(((17.27*toctmeanarr)/(toctmeanarr+237.3))))/pow((toctmeanarr+273.15),2.0))
deltayy=4098.0*(0.6108*pow(math.e,(((17.27*tyymeanarr)/(tyymeanarr+237.3))))/pow((tyymeanarr+273.15),2.0))
#atmospheric pressure
p=101.3*pow(((293.0-0.0065*dhmarr)/293.0),5.26)
#psycometric constant
pc=0.000665*p
#delta term
dtjan=deltajan/(deltajan+pc*(1+0.34*windjanarr))
dtapr=deltaapr/(deltaapr+pc*(1+0.34*windaprarr))
dtjul=deltajul/(deltajul+pc*(1+0.34*windjularr))
dtoct=deltaoct/(deltaoct+pc*(1+0.34*windoctarr))
dtyy=deltayy/(deltayy+pc*(1+0.34*windyyarr))
#psi term
ptjan=pc/(deltajan+pc*(1+0.34*windjanarr))
ptapr=pc/(deltaapr+pc*(1+0.34*windaprarr))
ptjul=pc/(deltajul+pc*(1+0.34*windjularr))
ptoct=pc/(deltaoct+pc*(1+0.34*windoctarr))
ptyy=pc/(deltayy+pc*(1+0.34*windyyarr))
#temperature term
ttjan=(900.0/(tjanmeanarr+273.15)*windjanarr)
ttapr=(900.0/(taprmeanarr+273.15)*windaprarr)
ttjul=(900.0/(tjulmeanarr+273.15)*windjularr)
ttoct=(900.0/(toctmeanarr+273.15)*windoctarr)
ttyy=(900.0/(tyymeanarr+273.15)*windyyarr)
#sat vapor press
esjan=(0.6108*pow(math.e,(17.27*tjanmaxarr)/(tjanmaxarr+273.15))+0.6108*pow(math.e,(17.27*tjanminarr)/(tjanminarr+273.15)))/2.0
esapr=(0.6108*pow(math.e,(17.27*taprmaxarr)/(taprmaxarr+273.15))+0.6108*pow(math.e,(17.27*taprminarr)/(taprminarr+273.15)))/2.0
esjul=(0.6108*pow(math.e,(17.27*tjulmaxarr)/(tjulmaxarr+273.15))+0.6108*pow(math.e,(17.27*tjulminarr)/(tjulminarr+273.15)))/2.0
esoct=(0.6108*pow(math.e,(17.27*toctmaxarr)/(toctmaxarr+273.15))+0.6108*pow(math.e,(17.27*toctminarr)/(toctminarr+273.15)))/2.0
esyy=(0.6108*pow(math.e,(17.27*tyymaxarr)/(tyymaxarr+273.15))+0.6108*pow(math.e,(17.27*tyyminarr)/(tyyminarr+273.15)))/2.0
#ea
eajan=mlfjanarr/100.0*(0.6108*pow(math.e,(17.27*tjanmaxarr)/(tjanmaxarr+273.15))+0.6108*pow(math.e,(17.27*tjanminarr)/(tjanminarr+273.15)))/2.0
eaapr=mlfaprarr/100.0*(0.6108*pow(math.e,(17.27*taprmaxarr)/(taprmaxarr+273.15))+0.6108*pow(math.e,(17.27*taprminarr)/(taprminarr+273.15)))/2.0
eajul=mlfjularr/100.0*(0.6108*pow(math.e,(17.27*tjulmaxarr)/(tjulmaxarr+273.15))+0.6108*pow(math.e,(17.27*tjulminarr)/(tjulminarr+273.15)))/2.0
eaoct=mlfoctarr/100.0*(0.6108*pow(math.e,(17.27*toctmaxarr)/(toctmaxarr+273.15))+0.6108*pow(math.e,(17.27*toctminarr)/(toctminarr+273.15)))/2.0
eayy=mlfyyarr/100.0*(0.6108*pow(math.e,(17.27*tyymaxarr)/(tyymaxarr+273.15))+0.6108*pow(math.e,(17.27*tyyminarr)/(tyyminarr+273.15)))/2.0
eajan=np.where(eajan<0,0,eajan)
eaapr=np.where(eaapr<0,0,eaapr)
eajul=np.where(eajul<0,0,eajul)
eaoct=np.where(eaoct<0,0,eaoct)
eayy=np.where(eayy<0,0,eayy)



#net radiation
rsjan=globradjanarr*0.0864
rsapr=globradaprarr*0.0864
rsjul=globradjularr*0.0864
rsoct=globradoctarr*0.0864
rsyy=globradyyarr*0.0864
rnsjan=(1-albedojanarr/100.0)*globradjanarr*0.0864
rnsapr=(1-albedoaprarr/100.0)*globradaprarr*0.0864
rnsjul=(1-albedojularr/100.0)*globradjularr*0.0864
rnsoct=(1-albedooctarr/100.0)*globradoctarr*0.0864
rnsyy=(1-albedoyyarr/100.0)*globradyyarr*0.0864
rs0jan=globradjan0arr*0.0864
rs0apr=globradapr0arr*0.0864
rs0jul=globradjul0arr*0.0864
rs0oct=globradoct0arr*0.0864
rs0yy=globradyy0arr*0.0864
rnljan=0.000000004903*((pow((tjanmaxarr+273.15),4.0)+pow((tjanminarr+273.15),4))/2.0)*(0.34-0.14*np.sqrt(eajan)*(1.35*(rsjan/rs0jan)-0.35))
rnlapr=0.000000004903*((pow((taprmaxarr+273.15),4.0)+pow((taprminarr+273.15),4))/2.0)*(0.34-0.14*np.sqrt(eaapr)*(1.35*(rsapr/rs0apr)-0.35))
rnljul=0.000000004903*((pow((tjulmaxarr+273.15),4.0)+pow((tjulminarr+273.15),4))/2.0)*(0.34-0.14*np.sqrt(eajul)*(1.35*(rsjul/rs0jul)-0.35))
rnloct=0.000000004903*((pow((toctmaxarr+273.15),4.0)+pow((toctminarr+273.15),4))/2.0)*(0.34-0.14*np.sqrt(eaoct)*(1.35*(rsoct/rs0oct)-0.35))
rnlyy=0.000000004903*((pow((tyymaxarr+273.15),4.0)+pow((tyyminarr+273.15),4))/2.0)*(0.34-0.14*np.sqrt(eayy)*(1.35*(rsyy/rs0yy)-0.35))
rnjan=rnsjan-rnljan
rnapr=rnsapr-rnlapr
rnjul=rnsjul-rnljul
rnoct=rnsoct-rnloct
rnyy=rnsyy-rnlyy
rngjan=np.where(rnjan>0,rnjan*0.408*31,0.11)
rngapr=np.where(rnapr>0,rnapr*0.408*30,0.11)
rngjul=np.where(rnjul>0,rnjul*0.408*31,0.11)
rngoct=np.where(rnoct>0,rnoct*0.408*30,0.11)
rngyy=np.where(rnyy>0,rnyy*0.408*365,0.11)
#evapotranspiration
etradjan=dtjan*rngjan*0.408
etradapr=dtapr*rngapr*0.408
etradjul=dtjul*rngjul*0.408
etradoct=dtoct*rngoct*0.408
etradyy=dtyy*rngyy*0.408
etwjan=ptjan*ttjan*(esjan-eajan)*31.0
etwapr=ptapr*ttapr*(esapr-eaapr)*30.0
etwjul=ptjul*ttjul*(esjul-eajul)*31.0
etwoct=ptoct*ttoct*(esoct-eaoct)*30.0
etwyy=ptyy*ttyy*(esyy-eayy)*365.0
et0jan=np.where(etwjan>=0,etradjan+etwjan,etradjan)
et0apr=np.where(etwapr>=0,etradapr+etwapr,etradapr)
et0jul=np.where(etwjul>=0,etradjul+etwjul,etradjul)
et0oct=np.where(etwoct>=0,etradoct+etwoct,etradoct)
et0yy=np.where(etwyy>=0,etradyy+etwyy,etradyy)

#re-mask NODATA values
et0jan=np.where(dhmarr==NODATA_value,NODATA_value,et0jan)
et0jan=np.where(tjanmeanarr==NODATA_value,NODATA_value,et0jan)
et0apr=np.where(dhmarr==NODATA_value,NODATA_value,et0apr)
et0apr=np.where(taprmeanarr==NODATA_value,NODATA_value,et0apr)
et0jul=np.where(dhmarr==NODATA_value,NODATA_value,et0jul)
et0jul=np.where(tjulmeanarr==NODATA_value,NODATA_value,et0jul)
et0oct=np.where(dhmarr==NODATA_value,NODATA_value,et0oct)
et0oct=np.where(toctmeanarr==NODATA_value,NODATA_value,et0oct)
et0yy=np.where(dhmarr==NODATA_value,NODATA_value,et0yy)
et0yy=np.where(tyymeanarr==NODATA_value,NODATA_value,et0yy)
print("write the output")
convertarrtotif(et0jan, outdir+"/"+"et0jan_"+climatescenarioname+".tif", 6, referenceraster, NODATA_value)
convertarrtotif(et0apr, outdir+"/"+"et0apr_"+climatescenarioname+".tif", 6, referenceraster, NODATA_value)
convertarrtotif(et0jul, outdir+"/"+"et0jul_"+climatescenarioname+".tif", 6, referenceraster, NODATA_value)
convertarrtotif(et0oct, outdir+"/"+"et0oct_"+climatescenarioname+".tif", 6, referenceraster, NODATA_value)
convertarrtotif(et0yy, outdir+"/"+"et0yy_"+climatescenarioname+".tif", 6, referenceraster, NODATA_value)