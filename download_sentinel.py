import json
import requests
import pandas as pd
import os
from os.path import *

work_dir = r'E:\work\s1_change'
oneX1 = "n38w078"
gran_dir = join(work_dir,oneX1)
text_dir = join(gran_dir,'text')


csv_path = join(text_dir, f'{oneX1}_id.csv')#for now just grabbing one scene per month
df = pd.read_csv(csv_path)


#i don't have automated way, or a gui select options yet,
#so just going to manually search for ID's

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

#can only download 3 at a time... :(
for i in df.index:
    id = df['Id'][i]
    safe = df['Name'][i][:-5]
    print(safe)
    #product = join(gran_dir, f'S2A_MSIL2A_{id[0:9]}.zip')
    product = join(gran_dir, f'{safe}.zip')
    if exists(product):
        print(f"{product} already exists")

    if not exists(product):
        url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({id})/$value"
        headers = {"Authorization": f"Bearer {access_token}"}

        session = requests.Session()
        session.headers.update(headers)
        response = session.get(url, headers=headers, stream=True)


        with open(product, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
