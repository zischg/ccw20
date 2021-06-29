import numpy as np
import time
import netCDF4
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy import stats


myworkspace="D:/CCW20/input/Schwellenwerte"
cddata=myworkspace+"/"+"tas_SMHI-RCA-IPSL-EUR11-RCP85_QM_1981-2099_monthly_mean.nc"
#time units = "days since 1900-1-1 00:00:00", timestep 0 is January 1981
f = netCDF4.MFDataset(cddata)
tas = f.variables['tas']
ntimes, ny, nx = tas.shape #ny=rows=latitudes, ny=columns=longitudes

# compute the cdf for each pixel (months of January in the period 1981-2010) and extract exceedence probability of 0.5°C
monthslist=np.arange(0,30*12, 12)

outarr = np.zeros((ny, nx), dtype=float)

i=0
while i<ny:
    j=0
    while j<0:
        taslist=[]
        for month in monthslist:
            taslist.append(tas[i,j,month])
            mydf=stats.norm()
            y=mydf.cdf(taslist)

        j+=1
    i+=1




rootgrp = Dataset(cddata, "r", format="NETCDF4")
print(rootgrp.data_model)
print(rootgrp.dimensions)
for dimobj in rootgrp.dimensions.values():
    print(dimobj)
