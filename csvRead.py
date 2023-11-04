import pandas
#import numpy as np
#import matplotlib.pyplot as plt
import re



def lakeSize1(x):
    
    d = {}
    column_name = "Hylak_id"
    column_data = x[column_name]
    for i in range (x.shape[0]): 
        h = column_data[i]
        for j in range(x.shape[1]): 
            waterSize = x.iloc[i,j]
            june = "-06-"
            july = "-07-"
            august = "-08-"
            september = "-09-"
            date = x.columns[j]
            summer = re.search(june, str(date))
            summe = re.search(july, str(date))
            summ = re.search(august, str(date))
            su = re.search(september, str(date))
            
          
            if (summer or summe or summ or su) and waterSize != 0:
                d[column_data[i]] = waterSize
                break
        #breakpoint()
    return d

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
area = pandas.read_csv("1_openwater_area.csv")
take = lakeSize1(area)
breakpoint()