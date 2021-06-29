import numpy as np
import netCDF4 as nc
import xarray
import os
import datetime as dt
import matplotlib.pyplot as plt
import rioxarray



import gdal

import osr
import rasterio


from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid

#coordinate systems EPSG 2056 = LV95, EPSG 21781 = LV03


importdir="L:/D/CCW20/input/Meteotest"
tas_anomalies_folder=importdir+"/anomalies/tas"
tasmax_anomalies_folder=importdir+"/anomalies/tasmax"
tasmin_anomalies_folder=importdir+"/anomalies/tasmin"
pr_anomalies_folder=importdir+"/anomalies/pr"
etap_swb_anomalies_folder=importdir+"/anomalies/etap_swb"
scenarionameprefix="ch2018_dsd_"
outdir="L:/D/CCW20/GIS/climatemapsUpdateCH2018"


scenarioslist=["CLMCOM-CCLM5_HADGEM_EUR44_RCP85", "DMI-HIRHAM_ECEARTH_EUR11_RCP26", "SMHI-RCA_MPIESM_EUR44_RCP45"]
periodslist=["2011_2044-1981_2010", "2045_2074-1981_2010", "2070_2099-1981_2010"]
#gdal.gdal_translate -of GTiff file.nc test.tiff
#gdal_translate -of GTiff -b 10 file.nc test.tiff  # to get 10th band

#***********************************************************************
#functions


#***********************************************************************










ncfnin=tas_anomalies_folder+"/"+scenarionameprefix+scenarioslist[0]+"_tas_anomalies_"+periodslist[0]+".nc"
ds=nc.Dataset(ncfnin)
print(ds)
for dim in ds.dimensions.values():
    print(dim)
for var in ds.variables.values():
    print(var)
ds.dimensions
ds.variables
print(ds['tas'])
tasarr=ds['tas'][0]
np.shape(tasarr)
tasarr=np.flip(tasarr,axis=0)
plt.imshow(tasarr)
plt.contourf(ds[1,"tas",:,:])


xds = xarray.open_dataset(ncfnin)
#xds.rio.set_crs("epsg:2056")
xds["tas"].rio.to_raster('D:\Weather data\test.tif')

