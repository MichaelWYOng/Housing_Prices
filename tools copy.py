import os
import numpy as np
import json
import requests
import pandas as pd
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
import cufflinks
cufflinks.go_offline(connected=False)
init_notebook_mode(connected=False)

def main():
    pass

def find_postal(lst, filename):
    
    for index,add in enumerate(lst):
        url= "https://developers.onemap.sg/commonapi/search?returnGeom=Y&getAddrDetails=Y&pageNum=1&searchVal="+add
        print(index,url)
        response = requests.get(url)
        data = json.loads(response.text) 
    
        temp_df = pd.DataFrame.from_dict(data["results"])
        temp_df["address"] = add
    
        if index == 0:
            file = temp_df
        else:
            file = file.append(temp_df)
    file.to_csv(filename + '.csv')
    

def clean_address(string, dictionary):
    for item in string.split(" "):
        if item in dictionary.keys():
             string = string.replace(item,dictionary[item])
        else:
            string
    return string

def find_nearest(house, amenity):
    """
    this function finds the nearest locations from the 2nd table from the 1st address
    add_lat_lon_start, add_lat_lon_end --> both is a data frame with a specific format:
        1st column: any string column ie addresses, mrt stations
        2nd column: latitude (float)
        3rd column: longitude (float)
    Column name doesn't matter.
    """
    results = {}
    # first column must be address
    for index,flat in enumerate(house.iloc[:,0]):
        
        # 2nd column must be latitude, 3rd column must be longitude
        flat_loc = (house.iloc[index,1],house.iloc[index,2])
        flat_amenity = ['','',100]
        for ind, eachloc in enumerate(amenity.iloc[:,0]):
            amenity_loc = (amenity.iloc[ind,1],amenity.iloc[ind,2])
            distance = geodesic(flat_loc,amenity_loc)

            if distance < flat_amenity[2]:
                flat_amenity[0] = flat
                flat_amenity[1] = eachloc
                flat_amenity[2] = distance

        results[flat] = flat_amenity
    return results

def save_file(data, filename):
    data1 = pd.DataFrame(data)
    data2 = data1.transpose()
    data2.to_csv(filename + '.csv', index=False)

if __name__ == '__main__':
    main()