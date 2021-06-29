import pandas as pd 
import requests 
import os

def scrape_store_data(original, name):
    if os.path.isfile(name +'.csv'):
        return pd.read_csv(name + '.csv')
    else:
        
        tlist = []
        df = pd.DataFrame()
        response = requests.get(original)
        data = response.json()
        n = data['payload']['max_page']

        for i in range(1,n+1):
            url = original +'?page='+str(i)
            response = requests.get(url)
            data = response.json()
            page_items = data['payload'][name]
            tlist += page_items
            url = original
        df = pd.DataFrame(tlist)
        df.to_csv(name + '.csv',index=False)
        return df