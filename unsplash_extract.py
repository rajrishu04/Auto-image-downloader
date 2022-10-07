import requests
import urllib.request
import json
import os
import csv
from datetime import datetime

# api-endpoint
URL = "https://api.unsplash.com/search/photos"

query = 'stunts'

content_filter = 'high'

page = 1

access_key = "Vgnw8CGA0FSwwyEDtMVeHoFKV9f_JgwT901tyHbZj9k"


current_dir = os.path.dirname(os.path.abspath(__file__))

curr_dir = os.path.join(current_dir,'unsplash')
if(os.path.isdir(curr_dir) == False):
    os.mkdir(curr_dir)

save_dir = "unsplash_" + query

save_path = os.path.join(curr_dir,save_dir)

if(os.path.isdir(save_path) == False):
    os.mkdir(save_path)

rows = 5000
arr = [['-']*7]*rows

print(save_path)

os.chdir(curr_dir)
csv_filename = "unsplash_data_records_" + query + ".csv"   
with open(csv_filename,'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Image' , 'user_id' , 'username' , 'name' , 'Image_url' , 'Date' , 'Time'])
    csvfile.close()

os.chdir(save_path)    
k = 0

for j in range(0,50):
    PARAMS = {  'client_id' : access_key , 'query': query , 'page' : page , 'content_filter': content_filter  }
  
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)

    if(r.status_code == 200):    
        data = r.json()
    else:
        print("nhi chla code")

    for i in range(0,len(data['results'])):

        localFile_name = query + "_" + str(k)
        localFile = open(query + "_" + str(k)+".jpg", "wb")

        if(data['results'][i]['width'] >=512 and data['results'][i]['height'] >=512  ):

            with urllib.request.urlopen(data['results'][i]['links']['download']) as f:
                localFile.write(f.read())
            localFile.close()  

            arr[k][0] = localFile_name
            arr[k][1] = data['results'][i]['user']['id']
            arr[k][2] = data['results'][i]['user']['username']
            arr[k][3] = data['results'][i]['user']['name']
            arr[k][4] = data['results'][i]['urls']['raw']
            now = datetime.now()
            arr[k][5] = now.strftime("%d/%b/%Y")
            arr[k][6] = now.strftime("%H:%M:%S")
            k += 1

            os.chdir(curr_dir)    
        with open(csv_filename,'a', encoding="utf-8") as csvfile_obj:
            csvwrite = csv.writer(csvfile_obj)
            csvwrite.writerow(arr[k])  
            csvfile_obj.close()      
            os.chdir(save_path)
    print(page)        
    page = page + 1          
    



 

     
  
