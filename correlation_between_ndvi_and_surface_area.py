import json
import pandas as pd

file_ndvi = "/home/derick/workspace/IMSACODE/IMSA2023LakeData/ndvi_and_time_of_lakes_min5_max15_2023-12-03-21-40-19.json"
file_openwater_area = "local-data/1_openwater_area.csv"
with open(file_ndvi, "r") as inf:
    ndvi = json.load(inf)
openwater = pd.read_csv(file_openwater_area)
breakpoint()