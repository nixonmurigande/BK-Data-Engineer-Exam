#working with XML API source

import requests
import xml.etree.ElementTree as ET 
import csv
import time

time_initiated = time.time()
url = 'https://df-dev.bk.rw/interview01/customers'
resp = requests.get(url)
time_finished = time.time()

# Check for HTTP codes other than 200
if resp.status_code != 200:
    print('Status:', resp.status_code, 'Problem with the request. Exiting.')
    exit()
if resp.status_code == 200:
    print(resp.status_code)
exit()

root = ET.fromstring(resp.text)

tree = ET.ElementTree(root)
tree.write("/media/yong/storage/nixon_data_engineer/customer.xml")

treechild = ET.parse("/media/yong/storage/nixon_data_engineer/customer.xml")
root_nodes = treechild.getroot()

xml_to_csv = open('/media/yong/storage/nixon_data_engineer/cus_test1.csv', 'w')

list_head = []

csv_writer = csv.writer(xml_to_csv)

count = 0

for element in root_nodes.findall('customer'):
    list_nodes = []
    
    if count == 0:
        id = element.find('id').tag
        list_head.append(id)
        
        name = element.find('name').tag
        list_head.append(name)
        
        csv_writer.writerow(list_head)
        count = +1 
   
    id = element.find('id').text
    list_nodes.append(id)
    
    name = element.find('name').text
    list_nodes.append(name)
    
    csv_writer.writerow(list_nodes)

xml_to_csv.close()