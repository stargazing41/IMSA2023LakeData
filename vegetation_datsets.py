import dask
import xarray as xr
import numpy as np
import pandas as pd
import datetime
import json
#I randomly choose lakes within a certain size.


def look_up_ndvi_for_lat_lon(ds, target_latitude, target_longitude):
    # ds.shape = (12, 2160, 4320)
    #10000000/(2160 * 4320) = 54.65534979423868 km^2 this is the grid surface area estimation

    lat_idx = (np.abs(ds['lat'] - target_latitude)).argmin()
    lon_idx = (np.abs(ds['lon'] - target_longitude)).argmin()
    time_data = ds['time']
    readable_time = pd.to_datetime(time_data.values).strftime('%Y-%m-%d').tolist()

    ndvi = ds['ndvi'][:,lat_idx, lon_idx].values.astype(float).tolist()
    
    return ndvi, readable_time
def get_lakes_within_surface_area_ranges(hylak_dataf, mins, maxs):
    geolocation = hylak_dataf[(hylak_dataf["Lake_area"]>mins) & (hylak_dataf["Lake_area"]< maxs)]
    geolocation = geolocation.reset_index(drop=True)
    return geolocation

veg_files = ["/home/derick/Downloads/ndvi3g_geo_v1_1_1985_0712.nc4","/home/derick/Downloads/ndvi3g_geo_v1_1_2001_0106.nc4", "/home/derick/Downloads/ndvi3g_geo_v1_1_2001_0712.nc4", "/home/derick/Downloads/ndvi3g_geo_v1_2_2018_0712.nc4"]
geolocation = pd.read_csv("local-data/Hylakes_with_location.csv")





ds = xr.open_mfdataset(veg_files, combine='by_coords')

#Nan lake Wuhan China
#target_latitude = 30.486329
#target_longitude = 114.356751
#9.4 - 7.4

#Dong lake Wuhan China
#target_latitude = 30.551691
#target_longitude = 114.389195

#Huangjia lake Wuhan China 175989
#target_latitude = 30.430395
#target_longitude = 114.278473
#surface area 8.2 - 9.4

#Tangxun lake Wuhan China
#target_latitude = 30.428767
#target_longitude = 114.351429
#46 - 54

#Lu lake Wuhan China
#target_latitude = 30.226219
#target_longitude = 114.190583
#48.3 - 55.7

#Zhangdu lake Wuhan China Id = 15282
#target_latitude = 30.642451
#target_longitude = 114.701610

minimum = 5
maximum = 15
my_ranges = [[5, 15], [15, 25], [25, 35], [35, 45], [45, 55], [55, 65]]
for item in my_ranges:
    minimum = item[0]
    maximum = item[1]
    glwsar = get_lakes_within_surface_area_ranges(geolocation, minimum, maximum)
    ndvi_and_time_of_lakes = {}
    for gl in range(glwsar.shape[0]):
        ndvi, ndvi_time = look_up_ndvi_for_lat_lon(ds, glwsar["Pour_lat"][gl], glwsar["Pour_long"][gl])
        ndvi_and_time_of_lakes[str(glwsar["Hylak_id"][gl])] = {"Ndvi": ndvi, "Ndvi_time": ndvi_time}
    d = datetime.datetime.now()
    datet = d.strftime("%Y-%m-%d-%H-%M-%S")
    with open(f"ndvi_and_time_of_lakes_min{minimum}_max{maximum}_{datet}.json","w") as outf:
        json.dump(ndvi_and_time_of_lakes, outf)
    glwsar.to_csv(f"glwsar_min{minimum}_max{maximum}_{datet}.csv")