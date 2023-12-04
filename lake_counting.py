import pandas
import numpy as np
import matplotlib.pyplot as plt
import json
import re
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import datetime
import time
#from MulticoreTSNE import MulticoreTSNE




def get_geolocation(location):
    geolocation = {}
    hylak = location["Hylak_id"]
    name = location["Lake_name"]
    country = location["Country"]
    latitude = location["Pour_lat"]
    for row in range (location.shape[0]):
      
        geolocation[hylak[row]] = {"Name": name[row], "Country": country[row], "Latitude": latitude[row]}
    return geolocation

def hemisphere(geo, location):
    determaine = {}
    hylak = location["Hylak_id"]
    name = location["Lake_name"]
    country = location["Country"]
    for i in range(location.shape[0]):
        if geo[hylak[i]]["Latitude"] < 0:
            determaine[hylak[i]] = {"Hemishpere": "Southern", "Name": name[i], "Country": country[i]}
        else:
            determaine[hylak[i]] = {"Hemishpere": "Northern", "Name": name[i], "Country": country[i]}
    return determaine

def min_max(openwater, geolocation, country):
    hylak = openwater["Hylak_id"]
    size = 0
    greater = 0
    less = 4377704000
    month = "-07-"
    if country == "Brazil":
        month = "-01-"
    for id in range(openwater.shape[0]):
       if geolocation[hylak[id]]["Country"] != country:
           continue 
       for y in range(openwater.shape[1]):
            size = openwater.iloc[id, y]
            if re.search(month, openwater.columns[y]) is not None and size != 0:
                    
                    if size > greater:
                        greater = size
                    if size < less:
                        less = size
    return greater, less

def count_lakes(greater, less, num_segs, geolocation, openwater, year, coutnry): 
    counter = {}  
    hylak = openwater["Hylak_id"]
    month = "-07-"    
    if country == "Brazil":
        month = "-01-"
    seg_len = (greater - less) / num_segs
    for r in range(openwater.shape[0]):
       if geolocation[hylak[r]]["Country"] != coutnry:
           continue
       for c in range(openwater.shape[1]):
            surface_area = openwater.iloc[r, c]
            if re.search(month, openwater.columns[c]) is not None \
                and re.search(year, openwater.columns[c]) is not None:
                if surface_area == 0:
                    #-1 means dead lakes
                    if "-1" not in counter:
                        counter["-1"] = 0
                    counter["-1"] +=1
                for k in range(num_segs):                      
                    if less + k * seg_len < surface_area and surface_area < less + (k+1) * seg_len:
                        if k not in counter:
                            counter[k] = 0
                        counter[k] += 1
                        break               
    return dict(sorted(counter.items(), key=lambda x: int(x[0])))

stopwatch = time.time()
area = pandas.read_csv("local-data/1_openwater_area.csv")
polygons_with_geolocation = pandas.read_csv("local-data/Hylakes_with_location.csv")

print("Finished reading csv files",time.time() - stopwatch)
geolocate = get_geolocation(polygons_with_geolocation)
hem = hemisphere(geolocate, polygons_with_geolocation)

print("Finished gathering GEOLOCATION",time.time() - stopwatch)

for number_catagories in range(100, 2100, 100):
    number_lakes = {}

    country_choice = ["Indonesia", "China", "Brazil", "India", "Russia", "Algeria"]

    year = [years for years in range(1985, 2018, 5)]
    year.append(2018)

    for country in country_choice:
        max, min = min_max(area, hem, country)
        number_lakes[country] = {"Min": min, "Max": max}
        for i in year:
            
            number_lakes[country][i] = count_lakes(max, min, number_catagories, hem, area, str(i), country)
    
    d = datetime.datetime.now()
    datet = d.strftime("%Y-%m-%d-%H-%M-%S")
    with open(f"Counted_lakes_{number_catagories}_{datet}.json","w") as outf:
        json.dump(number_lakes, outf)
    print("Wrote json file for number of catagories",number_catagories, time.time() - stopwatch)