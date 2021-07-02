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
    
def get_store_data():
    items  = scrape_store_data('https://python.zach.lol/api/v1/items','items')
    stores = scrape_store_data('https://python.zach.lol/api/v1/stores', 'stores')
    sales  = scrape_store_data('https://python.zach.lol/api/v1/sales', 'sales')
    item_sales = items.merge(sales, how='left', left_on= items.item_id, right_on=sales.item )
    complete = item_sales.merge(stores, how='left', left_on='store', right_on=stores.store_id)
    complete.to_csv('complete.csv', index=False)
    return complete

def feature_engineering():
    df = get_store_data()
    df.sale_date = pd.to_datetime(df.sale_date)
    df = df.set_index('sale_date')
    df['month'] = df.index.month
    df['week']  = df.index.isocalendar().week
    df['sale_total'] = df.sale_amount * df.item_price
    return df 


def get_germany():
    if os.path.isfile('opsd_germany.csv'):
        return pd.read_csv('opsd_germany.csv')
    df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    df.to_csv('opsd_germany.csv')
    return df
    
def prep_germany(df):
    df.Date = pd.to_datetime(df.Date)
    df = df.set_index('Date')
    df['month'] = df.index.month
    df['year'] = df.index.year
    df.Wind  = df.Wind.fillna(0)
    df.Solar = df.Solar.fillna(0)
    df['Wind+Solar'] = df['Wind+Solar'].fillna(0)
    return df