import pandas as pd
import os
from os.path import *

work_dir = r'E:\work\s1_change'
tile = "n39w077"
gran_dir = join(work_dir,tile)
text_dir = join(gran_dir,'text')

csv_path = join(text_dir, f'{tile}_id.csv')#for now just grabbing one scene per month
df = pd.read_csv(csv_path)

#S1-A
#Relative Orbit Number = mod (Absolute Orbit Number orbit - 73, 175) + 1
#S1-B
#Relative Orbit Number = mod (Absolute Orbit Number orbit - 27, 175) + 1

df_relorb = df
df_relorb = df_relorb.drop_duplicates(subset=['relorb'],keep='first')

for orb_num in df_relorb['relorb']:
    print(orb_num)
    df2 = df.loc[df['relorb'] == orb_num]
    print(f'relorb number {orb_num}')
    print(df2['Name'])
    print()
    csv_out = join(text_dir, f'{tile}_relorb_{orb_num}.csv')

    df2.to_csv(csv_out, columns=['Id', 'Name','relorb'])
