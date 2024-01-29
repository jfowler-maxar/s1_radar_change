import os
from os.path import *
#from osgeo import gdal, ogr,osr
import numpy as np
#from rasterstats import zonal_stats
import rasterio as rio
import geopandas as gpd
import pandas as pd
import time
import csv

work_dir = r'D:\s1_change'
tile = "n22e114"
relorb = '113'
tile_dir = join(work_dir, tile)
prepro_dir = join(tile_dir,'prepro')
relorb_dir = join(prepro_dir, f'relorb_{relorb}')
chang_dir = join(tile_dir, 'change')
vec_dir = join(tile_dir, 'vec')
stack_dir = join(tile_dir,'multi_temp_stack')

start_time = time.time()

in_name = f'{tile}_relorb{relorb}_ch_tmp.shp'
#in_name = r"E:\work\change_detect_solo\T37RBM\vec\test.shp" #testing smaller subset
in_shp = join(vec_dir, in_name)

out_test = f'{tile}_relorb{relorb}_ch_final.shp'
#out_test = r"E:\work\change_detect_solo\T37RBM\vec\test_out.shp"
out_shp = join(vec_dir, out_test)

ts_std_file = join(chang_dir,f'{tile}_relorb{relorb}_tempslope_std.tif')

#probably be smart to make this a seperate script and save dates as csv or something
csv_file = join(stack_dir,f'date_relorb_{relorb}.csv')
if not exists(csv_file):
    print('csv dne')
    exit(2)
with open(csv_file, newline='') as f:
    reader = csv.reader(f)
    date_lst = list(reader)
print(date_lst)
#for i in range(1,len(date_lst)+1):
#    print(f'{i} and {date_lst[i-1]}')

gdf = gpd.read_file(in_shp)
gdf['change_d'] = gdf['date']
for i in range(1,len(date_lst)+1):
    gdf['change_d'] = np.where(gdf['date'] == i, date_lst[i-1], gdf['change_d'])

gdf['date'] = gdf['change_d']
gdf = gpd.GeoDataFrame.drop(gdf,columns=['change_d'])
src = rio.open(ts_std_file)

gdf['centroid'] = gdf.centroid
coord_list = [(x, y) for x, y in zip(gdf["centroid"].x, gdf["centroid"].y)]
gdf = gpd.GeoDataFrame.drop(gdf,columns=['centroid'])

#create fields
print('working on adding slope std')
gdf['slope_std'] = [x for x in src.sample(coord_list)]
gdf['slope_std'] = gdf['slope_std'].astype('int32')

print("geopandas clipping done --- %s seconds ---" % (time.time() - start_time))
print(f'creating {out_shp}')
gdf.to_file(out_shp,driver='ESRI Shapefile')
