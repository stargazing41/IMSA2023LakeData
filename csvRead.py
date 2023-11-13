import pandas
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE


def lakeSize1(x):
   
    d = {}
    column_name = "Hylak_id"
    column_data = x[column_name]
    for i in range (50000):#x.shape[0]): 
        h = column_data[i]
        for j in range(x.shape[1]): 
            waterSize = x.iloc[i,j]
            june = "-06-"
            july = "-07-"
            august = "-08-"
            date = x.columns[j]
            summer = re.search(june, str(date))
            summe = re.search(july, str(date))
            summ = re.search(august, str(date))
            
          
            if (summer): #and waterSize != 0:
                d[h] = {"Size": waterSize, "Date": date}
                break
        #breakpoint()
    return d
def SecondSize(x):
    a = 50000
    u = []
    kept = []
    years = {}
    all_year_size = {}
    all_changes = {}
    change = []
    s = lakeSize1(x)
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
            if yy not in years and mm == "06" and s[column_data[i]]["Date"] != date:
                u.append(water)
                years[yy] = water
        #print(len(u))
        if len(u) != 33:
            print(years)
            print(s[column_data[i]])
            breakpoint()
        assert(len(u) == 33)




        change = [] 
        
        aj = []
        var = 0
        for j in range (len(u)):
            
            if int(s[column_data[i]]["Size"]) == 0:
                var += 1
                continue
            minus = float(u[j]) - float(s[column_data[i]]["Size"])
            minus = minus / float(s[column_data[i]]["Size"])
            minus = float(minus) * 100.0
            kept.append(column_data[i])
        
            
            change.append(float(minus))
            aj.append(float(j))
        if var == 0:

            all_changes[column_data[i]] = change
            assert(len(change) == 33)
    
    mat = [values for values in all_changes.values()]
    #breakpoint()
    mat = np.array(mat)
    tsne = TSNE(n_components=2, perplexity=10, learning_rate=200, random_state=42)
    X_tsne = tsne.fit_transform(mat)
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
    plt.title('t-SNE Visualization')
    plt.show()
        
    breakpoint()
    return all_year_size

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
take = lakeSize1(area)
other = SecondSize(area)
other
#breakpoint()