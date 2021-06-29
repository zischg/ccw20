import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
myworkspace="D:/CCW20/input/anomalies"
nf=myworkspace+"/pr/ch2018_dsd_CLMCOM-CCLM5_HADGEM_EUR44_RCP85_pr_anomalies_2070_2099-1981_2010.nc"
def convert_netcdf_gridascii(in_netcdf_file):
    ds = nc.Dataset(nf)
    ds
    deltapr = ds['pr'][:]
    type(deltapr)
    deltaprflip = np.flip(deltapr, axis=1)
    np.shape(deltaprflip[0])
    upperleftxy = [min(ds['chx'][:]), max(ds['chy'][:])]
    lowerleftxy = [min(ds['chx'][:]), min(ds['chy'][:])]
    gridsizex = ds['chx'][1] - ds['chx'][0]
    gridsizey = ds['chy'][1] - ds['chy'][0]
    #plt.imshow(deltaprflip[0])
    # convert to GRIDASCII
    headerstr = "ncols\t" + str(np.shape(deltapr)[2]) + "\n"
    headerstr = headerstr + "nrows\t" + str(np.shape(deltapr)[1]) + "\n"
    headerstr = headerstr + "xllcorner\t" + str(lowerleftxy[0]) + "\n"
    headerstr = headerstr + "yllcorner\t" + str(lowerleftxy[1]) + "\n"
    headerstr = headerstr + "cellsize\t" + str(gridsizex) + "\n"
    headerstr = headerstr + "NODATA_value\t" + str(9.969209968386869e+36)
    np.savetxt(in_netcdf_file.replace(".nc",".asc"),deltaprflip[0], fmt='%.2f', delimiter=' ', newline='\n', header=headerstr, comments='')

convert_netcdf_gridascii(myworkspace+"/tas/ch2018_dsd_CLMCOM-CCLM5_HADGEM_EUR44_RCP85_tas_anomalies_2070_2099-1981_2010.nc")
