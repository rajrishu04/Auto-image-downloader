import requests
import urllib.request
import json
import os
import csv
import requests
from datetime import datetime
from urllib.request import Request, urlopen

# api-endpoint
URL = "https://api.pexels.com/v1/search"

query = 'exercise'

orientation = 'portrait'  

authorization = "563492ad6f917000010000015bd5c524b40c42e5a7ad3e20de8da05c"

page = 1

current_dir = os.path.dirname(os.path.abspath(__file__))

curr_dir = os.path.join(current_dir,'pexels')
if(os.path.isdir(curr_dir) == False):
    os.mkdir(curr_dir)

save_dir = "pexels_" + query

save_path = os.path.join(curr_dir,save_dir)

if(os.path.isdir(save_path) == False):
    os.mkdir(save_path)

rows = 5000
arr = [['-']*7]*rows

csv_filename = "pexels_data_records_" + query + ".csv"   
os.chdir(curr_dir) 
with open(csv_filename,'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['photo_no' , 'photographer_id' , 'photographer' , 'photographer_url' , 'Image_url' , 'Date' , 'Time' ])
    csvfile.close()
k = 0

os.chdir(save_path)

for j in range(0,60):
    PARAMS = { 'Authorization' : authorization , 'query': query , 'page' : page , 'orientation':orientation }
    # sending get request and saving the response as response object
    
    r = requests.get(url = URL, params=  PARAMS , headers={'Authorization': authorization})

    if(r.status_code == 200):    
        data = r.json()
    else:
        print("nhi chla code")

    print(r.status_code)
    for i in range(0,data['per_page']):

        # req = requests(data['photos'][i]["src"]['medium'], headers={'User-Agent': 'Mozilla/5.0'})

        localFile_name = query + "_"+  str(k)
        localFile = open(query + "_"+ str(k)+".jpg", "wb")

        if(data['photos'][i]['width'] >=512 and data['photos'][i]['height'] >=512  ):

            req = Request(data['photos'][i]['src']['original'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as f:
                localFile.write(f.read())
            localFile.close()

            arr[k][0] = localFile_name
            arr[k][1] = data['photos'][i]['photographer_id']
            arr[k][2] = data['photos'][i]['photographer']
            arr[k][3] = data['photos'][i]['photographer_url']
            arr[k][4] = data['photos'][i]['url']
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
    page += 1        
    