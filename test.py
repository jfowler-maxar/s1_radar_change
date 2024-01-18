import json
import requests
import pandas as pd
import os
from os.path import *

work_dir = r'E:\work\s1_change'
oneX1 = "n38w078"
gran_dir = join(work_dir,oneX1)
text_dir = join(gran_dir,'text')

csv_path = join(text_dir, f'{oneX1}_select.csv')
df = pd.read_csv(csv_path)

#for i in range(len(df['date'])):
#    date = df['date'][i].split('T')[0]
#    print(date)
#    df['date'][i] = date
def get_date(name):
    date = name.split('T')[0][:-2]
    return date

df['date'] = df['Name'].apply(get_date)
df = df.drop_duplicates(subset=['date'], keep='last')

print(df['date'])
