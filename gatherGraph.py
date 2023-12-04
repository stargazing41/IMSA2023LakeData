import pandas
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
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
    northern_lakes = 0
    southern_lakes = 0
    determaine = {}
    hylak = location["Hylak_id"]
    
    for i in range(location.shape[0]):
        if geo[hylak[i]]["Latitude"] < 0:
            determaine[hylak[i]] = {"Hemishpere": "Southern"}
            southern_lakes += 1
        else:
            determaine[hylak[i]] = {"Hemishpere": "Northern"}
            northern_lakes += 1
    return determaine, southern_lakes, northern_lakes
def dead_lake_counter(x):
  
    dead_lakes = 0
   
    for i in range(x.shape[0]):

        if sum(x.iloc[i,1:]) == 0:
            dead_lakes += 1
    return dead_lakes

def makeGraph(southern, duds, northern):
    
    #lakes = {}
  
    #lakes["Northern"] = northern
    #lakes["Southern"] = southern
    #lakes["Disqualified"] = duds
    print("Northern:", northern, "Southern:", southern, "Disqualified:", duds)
    catagories = ["Northern_Lakes", "Southern_Lakes", "Disqualified_Lakes"]
    values = [northern, southern, duds]
    plt.bar(catagories, values)
    plt.xlabel('Lakes')
    plt.ylabel('Values')
    plt.title('All_Lakes')
    plt.savefig("Nov_27_100_north_or_south.png")
    plt.show()

area = pandas.read_csv("local-data/1_openwater_area.csv")
polygons_with_geolocation = pandas.read_csv("local-data/Hylakes_with_location.csv")


#print("Finished")

geolocate = get_geolocation(polygons_with_geolocation)
hemisphere_of_lake, south_lakes, north__lakes= hemisphere(geolocate, polygons_with_geolocation)
dead_lakes = dead_lake_counter(area)
print(makeGraph(south_lakes, dead_lakes, north__lakes))