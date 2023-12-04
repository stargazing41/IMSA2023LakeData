import matplotlib.pyplot as plt
import numpy as np
import json

fpath = "Counted_lakes_1500_2023-12-03-19-40-17.json"

with open(fpath, "r") as inf:
    data_f = json.load(inf)
for country in data_f.keys():
    del data_f[country]["Min"]
    del data_f[country]["Max"]
    fig, ax = plt.subplots()
    
    for i, key in enumerate(data_f[country].keys()): 
        in_key = 14
        if str(in_key) not in data_f[country][key].keys():
            data_f[country][key][str(in_key)] = 0
        #plt.figure(figsize=(100, 2000))
        listed_keys = list(data_f[country][key].keys())
        
        for get in (listed_keys):
            
            if int(get) > in_key:
                data_f[country][key][str(in_key)] += data_f[country][key][get]
                del data_f[country][key][get]
        values1 =  list(data_f[country][key].values())
        categories = list(data_f[country][key].keys())
        x = np.arange(len(categories))
        width = 0.85 / len(data_f[country].keys())

        #for j, (year, counts) in enumerate(data_f[country].items()):
        grey_shades = np.linspace(0, 1, 15)
        ax.bar(x+i*width, values1, width, label = int(key), color = str(grey_shades[i]))

    ax.set_xlabel("Lake Surface Area Catergories")
    ax.set_ylabel("Counts")
    ax.set_title(f"Histogram Counts From 1985 to 2018 for {country}")
    ax.set_xticks(x+width * len(data_f[country].keys())/ 2 - 0.5)
    ax.set_xticklabels(categories)
    ax.legend()
    plt.savefig(f"Histogram_of_1500_{country}.png")
    #plt.show()