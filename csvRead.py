import pandas
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.manifold import TSNE



def lakeSize1(x):
    
    d = {}
    column_name = "Hylak_id"
    column_data = x[column_name]
    for i in range (100):#x.shape[0]): 
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
            
          
            if (summer or summe or summ) and waterSize != 0:
                d[h] = {"Size": waterSize, "Date": date}
                break
        #breakpoint()
    return d
def SecondSize(x):
    u = []
    years = {}
    all_year_size = {}
    all_changes = {}
    change = []
    s = lakeSize1(x)
    column_name = "Hylak_id"
    column_data = x[column_name]
    for i in range(100):
        for y in range(x.shape[1]):
            june = "-06-"
            july = "-07-"
            august = "-08-"
            date = x.columns[y]
            summer = re.search(june, str(date))
            summe = re.search(july, str(date))
            summ = re.search(august, str(date))
            water = x.iloc[i,y]
          
            if (summer or summe or summ) and water != 0:
                if s[column_data[i]]["Size"] != water:
                    u.append(water)
            all_year_size[column_data[i]] = {"Size": u, "Date": date}
            years[column_data[i]] = water
            
        
    #breakpoint()
        aj = []
        for j in range (len(u)):
            
            minus = float(u[j]) - float(s[column_data[i]]["Size"])
            minus = minus / float(s[column_data[i]]["Size"])
            minus = float(minus) * 100.0
            
            if minus <= 0:
                #hi = int(s[column_data[i]]) - int(u[column_data[i]])
                #hi = hi / int(s[column_data[i]])
                #print("Negative change")
                change.append(float(minus))
                aj.append(float(j))
            else:
                #print("Positive change")
                change.append(float(minus))
                aj.append(float(j))
        breakpoint()
    #all_changes[] = change
    #converted = pandas.DataFrame(all_year_size)
    #conv = np
    plt.plot(aj, change)
    plt.xlabel('Random')
    plt.ylabel('Size')
    #plt.title(column_data[i])
    #plt.show()
    #df = pandas.DataFrame.from_dict(change, orient='index')
    #breakpoint()
    matrix = np.array(change).reshape((100, 49))
    breakpoint()
    tsne = TSNE(n_components=2, perplexity=10, learning_rate=200, random_state=42)
    X_tsne = tsne.fit_transform(matrix)
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
    plt.title('t-SNE Visualization')
    plt.show()
    change = [] 
    u = []
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