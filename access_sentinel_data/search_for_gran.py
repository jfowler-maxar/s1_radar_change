import json
import requests
import pandas as pd
import os
from os.path import *

work_dir = r'E:\work\s1_change'
tile = "n39w077"
tile_dir = join(work_dir,tile)

if not exists(work_dir):
    os.mkdir(work_dir)
if not exists(tile_dir):
    os.mkdir(tile_dir)
text_dir = join(tile_dir,'text')
if not exists(text_dir):
    os.mkdir(text_dir)

def get_access_token(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    try:
        r = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data=data,
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Access token creation failed. Reponse from the server was: {r.json()}"
        )
    return r.json()["access_token"]

access_token = get_access_token("username", "password")
#print(access_token)

data_collection = "SENTINEL-1"
productType = "IW_GRDH"
polarisation = "VV"
pass_ = "ASCENDING"
#pass_ = "DESCENDING"
lat2 = int(tile[1:3])
long1 = int(tile[-3:])
if 'w' in tile:
    long1 = long1*-1
    #print(long1)
if 's' in tile:
    lat2 = lat2*-1
#subtract or add to get other coords
lat1 = lat2 + 1
long2 = long1 + 1


#polygon coords go: long1 lat1, long2 lat1, long2 lat2, long1 lat2, long1 lat1
bbox = f'{long1} {lat1}, ' \
       f'{long2} {lat1}, ' \
       f'{long2} {lat2}, ' \
       f'{long1} {lat2}, ' \
       f'{long1} {lat1}'

#S1-A
#Relative Orbit Number = mod (Absolute Orbit Number orbit - 73, 175) + 1
def get_relorb(name):
    abs_orb = name.split('_')[6]
    abs_orb = int(abs_orb)
    relorb = ((abs_orb-73) % 175) + 1
    return relorb

for i in range(1,13):
    if i<9:
        start_date = f"2023-0{i}-01"
        end_date = f"2023-0{i + 1}-01"
    elif i == 9:
        start_date = f"2023-0{i}-01"
        end_date = f"2023-{i + 1}-01"
    elif i>=10 and i <12:
        start_date = f"2023-{i}-01"
        end_date = f"2023-{i+1}-01"
    elif i == 12:
        start_date = f"2023-{i}-01"
        end_date = f"2023-{i}-31"
    print(start_date)
    json = requests.get(
        f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?"
        f"$filter=contains(Name, '{productType}') and "
        f"Collection/Name eq '{data_collection}' and "
        f"OData.CSC.Intersects(area=geography'SRID=4326;"
        f"POLYGON(({bbox}))') and "
        f"ContentDate/Start gt {start_date}T00:00:00.000Z and "
        f"ContentDate/Start lt {end_date}T00:11:00.000Z").json()

    df = pd.DataFrame.from_dict(json['value'])
    df = df[df['Name'].str.contains('COG.') == False]

    df['relorb'] = df['Name'].apply(get_relorb)
    csv_out = join(text_dir, f'{tile}_2023_{str(i)}_list.csv')

    df.to_csv(csv_out,columns=['Id','Name','relorb'])

csv_lst = []
for csv in os.listdir(text_dir):
    print(csv)
    csv_path = join(text_dir,csv)
    data = pd.read_csv(csv_path)
    csv_lst.append(data)

frame = pd.concat(csv_lst,axis=0,ignore_index=True)
#print(frame[['Id','Name']])

csv_out = join(text_dir, f'{tile}_id.csv')
frame.to_csv(csv_out,columns=['Id','Name','relorb'])#, columns=['Id','Name'])
