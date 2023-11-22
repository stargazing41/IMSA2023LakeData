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
        for column in range(location.shape[1]):
            geolocation[hylak[row]] = {"Name": name[row], "Country": country[row], "Latitude": latitude[row]}
    return geolocation
def hemisphere(geo, location):
    determaine = {}
    hylak = location["Hylak_id"]
    name = location["Lake_name"]
    country = location["Country"]
    for i in range(location.shape[0]):
        for y in range(location.shape[1]):
            if geo[hylak[i]]["Latitude"] < 0:
                determaine[hylak[i]] = {"Hemishpere": "Southern", "Name": name[i], "Country": country[i]}
            else:
                determaine[hylak[i]] = {"Hemishpere": "Northern", "Name": name[i], "Country": country[i]}
    return determaine

def lakeSize1(x, geo):
   
    d = {}
    column_name = "Hylak_id"
    column_data = x[column_name]
    for i in range (x.shape[0]): 
        winter = False
        summer = False 
        h = column_data[i]
        for j in range(x.shape[1]):
            
            waterSize = x.iloc[i,j]
            june = "-06-"
            july = "-07-"
            december = "-12-"
            date = x.columns[j]
           
            #print(column_data[i])
            if geo[column_data[i]]["Hemishpere"] == "Northern":
                summer = re.search(july, str(date))
            else:
            
                winter = re.search(december, str(date))
            
            #if waterSize == 0 and i == 20:
                #breakpoint()
          
            if summer and waterSize != 0:
                d[h] = {"Size": waterSize, "Date": date}
                break
            elif winter and waterSize != 0:
                d[h] = {"Size": waterSize, "Date": date}
                break
    return d
def SecondSize(x, req):
    a = x.shape[0]
    u = []
    kept = []
    years = {}
    all_year_size = {}
    all_changes = {}
    change = []
    s = lakeSize1(x, req)
    column_data = x["Hylak_id"]
    mat = np.ones((a, x.shape[1]))
    for i in range(a):
        years = {}
        u = []
        for y in range(1, x.shape[1]):
            date = x.columns[y]
            #print(date)
            water = x.iloc[i,y]
            yy,mm,dd = date.split("-")
            if yy not in years:
                if req[column_data[i]]["Hemishpere"] == "Northern" and mm == "06":
                    if s[column_data[i]]["Date"] != date:
                        u.append(water)
                        years[yy] = water
                elif req[column_data[i]]["Hemishpere"] == "Southern" and mm == "12":
                    if s[column_data[i]]["Date"] != date:
                        u.append(water)
                        years[yy] = water
        assert(len(u) == 33)




        change = [] 
        
        aj = []
        for j in range (len(u)):
            
           
            minus = float(u[j]) - float(s[column_data[i]]["Size"])
            print(s[column_data[i]], column_data[i])
            minus = minus / float(s[column_data[i]]["Size"])
            minus = float(minus) * 100.0
            kept.append(column_data[i])
        
            
            change.append(float(minus))
            aj.append(float(j))
  

        all_changes[column_data[i]] = change
        assert(len(change) == 33)
    
    mat = [values for values in all_changes.values()]
    #breakpoint()
    mat = np.array(mat)
    
    breakpoint()
    return mat

def kmeans(mat, k):
    scaler = StandardScaler()
    mat_scaled = scaler.fit_transform(mat)
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(mat_scaled)
    cluster_centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    tSNE(mat_scaled, labels)
    breakpoint()

def tSNE(mat_scaled, cluster_labels):
    tsne = TSNE(n_components=2, perplexity=10, learning_rate=20, random_state=42)
    mat_tsne = tsne.fit(mat_scaled)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.scatter(mat_tsne[:, 0], mat_tsne[:, 1], c=cluster_labels, cmap='viridis', alpha=0.7)
    plt.title('k-means_visulization')
    plt.savefig("k_means_400_lakes_Nov_18_2023.png")
    plt.show()
#saltLake = surfaceArea[surfaceArea["Hylak_id"]==67]
#Lake = surfaceArea[surfaceArea["Hylak_id"]==60]
#sevierLake = surfaceArea[surfaceArea["Hylak_id"]==793]
#walkerLake = surfaceArea[surfaceArea["Hylak_id"]==795]
#bigTroutLake = surfaceArea[surfaceArea["Hylak_id"]==587]
#greatBearLake = surfaceArea[surfaceArea["Hylak_id"]==2]

#print(bigTroutLake)
#sa = bigTroutLake.to_numpy()[4:]
#plt.plot(range(len(sa)), sa)
#plt.savefig('Figure1.png')

#(data to save to csv FE: Lake).to_csv
area = pandas.read_csv("local-data/1_openwater_area.csv")
polygons_with_geolocation = pandas.read_csv("local-data/Hylakes_with_location.csv")


#print("Finished")
#
geolocate = get_geolocation(polygons_with_geolocation)
hem = hemisphere(geolocate, polygons_with_geolocation)
take = lakeSize1(area, hem)
surface_area_fraction = SecondSize(area, hem)
kmeans(surface_area_fraction, 10)

