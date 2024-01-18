import json
import requests
import pandas as pd
import os
from os.path import *

work_dir = r'E:\work\s1_change'
oneX1 = "n38w078"
gran_dir = join(work_dir,oneX1)

if not exists(work_dir):
    os.mkdir(work_dir)
if not exists(gran_dir):
    os.mkdir(gran_dir)
text_dir = join(gran_dir,'text')
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

access_token = get_access_token("fowlerjustin29@yahoo.com", "PanCakes2023@)@#")
#print(access_token)

data_collection = "SENTINEL-1"
productType = "IW_GRDH"
polarisation = "VV"
pass_ = "ASCENDING"
#pass_ = "DESCENDING"
bbox = f"-77.0001389 39.0001389," \
       f"-76.0001389 39.0001389," \
       f"-76.0001389 38.0001389," \
       f"-77.0001389 38.0001389," \
       f"-77.0001389 39.0001389"

for i in range(1,13):
    if i<9:
        start_date = f"2023-0{i}-01"
        end_date = f"2023-0{i + 1}-01"
    elif i>=10 and i <12:
        start_date = f"2023-{i}-01"
        end_date = f"2023-{i+1}-01"
    elif i == 12:
        start_date = f"2023-{i}-01"
        end_date = f"2023-{i}-31"
    print(start_date)
    json = requests.get("https://catalogue.dataspace.copernicus.eu/odata/v1/Products?"
                        f"$filter=contains(Name, '{productType}') and "
                        f"contains(Name, 'COG') and "
                        f"Collection/Name eq '{data_collection}' and "
                        f"OData.CSC.Intersects(area=geography'SRID=4326;"
                        f"POLYGON(({bbox}))') and "
                        f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'orbitDirection' and "
                        f"att/OData.CSC.StringAttribute/Value eq '{pass_}') and " 
                        f"ContentDate/Start gt {start_date}T00:00:00.000Z and "
                        f"ContentDate/Start lt {end_date}T00:11:00.000Z").json()

    df = pd.DataFrame.from_dict(json['value'])

    def get_date(name):
        date = name.split('T')[0][:-2]#just get 1 date per month
        return date

    df['date'] = df['Name'].apply(get_date)
    df = df.drop_duplicates(subset=['date'], keep='last')

    csv_out = join(text_dir,f'{oneX1}_2023_{str(i)}_list.csv')

    df.to_csv(csv_out)

csv_lst = []
for csv in os.listdir(text_dir):
    print(csv)
    csv_path = join(text_dir,csv)
    data = pd.read_csv(csv_path)
    csv_lst.append(data)

frame = pd.concat(csv_lst,axis=0,ignore_index=True)
#print(frame[['Id','Name']])

csv_out = join(text_dir, f'{oneX1}_id.csv')

frame.to_csv(csv_out, columns=['Id','Name'])
