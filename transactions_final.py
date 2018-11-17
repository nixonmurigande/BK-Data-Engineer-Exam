#working with JSON API source 

import requests
import time
import json
import csv
import pandas as pd
from datetime import datetime
import reverse_geocoder as rg


time_initiated = time.time()
url = 'https://df-dev.bk.rw/interview01/transactions'
response = requests.get(url)
time_finished = time.time()

# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Problem with the request. Exiting.')
    exit()
if response.status_code == 200:
    print(response.status_code)
exit()

json_data = response.json()
print(time_finished - time_initiated) 
#print(json_data)
dict_json_data = json.loads(response.text)
print()
#print(dict_json_data)

with open('/media/yong/storage/nixon_data_engineer/test.csv','w') as csvfile:

    writer = csv.writer(csvfile)
    
    writer.writerow(dict_json_data[0].keys()) #header row

    for item in  dict_json_data:

       writer.writerow(item.values()) # values row

transc_df = pd.read_csv("/media/yong/storage/nixon_data_engineer/test.csv")

print(transc_df)

transc_df.drop('timestamp', axis=1, inplace=True)

print(transc_df)

transc_df.insert(0, 'TimeStamp', pd.datetime.now().replace(microsecond=0))

print(transc_df)

cust_df = pd.read_csv("/media/yong/storage/nixon_data_engineer/cus_test1.csv")

merged_df = (pd.merge(transc_df, cust_df, how = 'left', left_on = 'customerId', right_on = 'id'))

print(merged_df)

merged_df.drop('id', axis= 1, inplace=True)

#merged_df.to_csv('/media/yong/storage/nixon_data_engineer/transaction_f.csv', index=False, header=True)

merged_df['coord'] = list(zip(merged_df.latitude,merged_df.longitude)) # zip the lat and lng to make a new series

print(merged_df['coord'])

merged_df.head()

coordinates = (-1.970579, 30.104429), (-1.970579, 30.104429), (-1.970579, 30.104429), (-1.970579, 30.104429), (-1.292066, 36.821945),(-1.292066, 36.821945),(-1.292066, 36.821945),(-1.292066, 36.821945),(-1.292066, 36.821945),(-26.204103, 28.047303999999997),(-26.204103, 28.047303999999997), (-26.204103, 28.047303999999997), (-26.204103, 28.047303999999997),(-26.204103, 28.047303999999997) 
results = rg.search(coordinates)

#print(results)

city_names = ("Kigali", "Kigali", "Kigali", "Kigali", "Nairobi", "Nairobi", "Nairobi", "Nairobi", "Nairobi", "City of Johannesburg Metropolitan Municipality", "City of Johannesburg Metropolitan Municipality", "City of Johannesburg Metropolitan Municipality", "City of Johannesburg Metropolitan Municipality", "City of Johannesburg Metropolitan Municipality")

merged_df.insert(6, 'city_name', city_names)

print(merged_df)

merged_df.to_csv('/media/yong/storage/nixon_data_engineer/transaction_final.csv', index=False, header=True)
