import json
import requests
import pandas as pd


def find_postal(lst, filename):
    '''With the block number and street name, get the full address of the hdb flat,
    including the postal code, geogaphical coordinates (lat/long)'''
    
    for index,add in enumerate(lst):
        # do not need to change the URL
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
    