import dask
import xarray as xr
import numpy as np
import pandas as pd



def look_up_ndvi_for_lat_lon(ds, target_latitude, target_longitude):
    # ds.shape = (12, 2160, 4320)
    #10000000/(2160 * 4320) = 54.65534979423868 km^2 this is the grid surface area estimation

    lat_idx = (np.abs(ds['lat'] - target_latitude)).argmin()
    lon_idx = (np.abs(ds['lon'] - target_longitude)).argmin()
    time_data = ds['time']
    readable_time = pd.to_datetime(time_data.values).strftime('%Y-%m-%d').tolist()

    ndvi = ds['ndvi'][:,lat_idx, lon_idx].values
    
    return ndvi, readable_time

veg_files = ["/home/derick/Downloads/ndvi3g_geo_v1_1_1985_0712.nc4","/home/derick/Downloads/ndvi3g_geo_v1_1_2001_0106.nc4", "/home/derick/Downloads/ndvi3g_geo_v1_1_2001_0712.nc4", "/home/derick/Downloads/ndvi3g_geo_v1_2_2018_0712.nc4"]

ds = xr.open_mfdataset(veg_files, combine='by_coords')

#Nan lake Wuhan China
#target_latitude = 30.486329
#target_longitude = 114.356751

#Dong lake Wuhan China
#target_latitude = 30.551691
#target_longitude = 114.389195

#Huangjia lake Wuhan China
#target_latitude = 30.430395
#target_longitude = 114.278473

#Tangxun lake Wuhan China
#target_latitude = 30.428767
#target_longitude = 114.351429

#Lu lake Wuhan China
#target_latitude = 30.226219
#target_longitude = 114.190583

#Zhangdu lake Wuhan China
target_latitude = 30.642451
target_longitude = 114.701610

# Specify your target latitude and longitude

nvdi, nvdi_time = look_up_ndvi_for_lat_lon(ds, target_latitude, target_longitude)
print(nvdi, nvdi_time)