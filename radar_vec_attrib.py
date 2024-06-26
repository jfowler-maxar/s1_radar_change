import os
from os.path import *
#from osgeo import gdal, ogr,osr
import numpy as np
from rasterstats import zonal_stats
import rasterio as rio
import geopandas as gpd
import pandas as pd
import time

work_dir = r'E:\work\change_detect_solo'
gran = "T18SUJ"
gran_dir = join(work_dir, gran)
change_dir = join(gran_dir,'change')
time_stats_dir = join(gran_dir,'time_stats')
vec_dir = join(gran_dir,'vec')

bnum = '1'
in_name = f'{gran}_b{bnum}_ch_tmp.shp'
#in_name = r"E:\work\change_detect_solo\T37RBM\vec\test.shp" #testing smaller subset
in_shp = join(vec_dir, in_name)

out_test = f'{gran}_b{bnum}_ch_final.shp'
#out_test = r"E:\work\change_detect_solo\T37RBM\vec\test_out3.shp"
out_shp = join(vec_dir, out_test)

#attributes to start out with: change date, tempslope_std, veg, water
#tempslope_std
ts_std_file = join(change_dir,f'{gran}_b{bnum}_stacktempslope_std.tif')
veg_std_file = join(time_stats_dir,f'{gran}_ndvi_std.tif')#veg_std to find osciallating veg(ag/decidious)
veg_mean_file = join(time_stats_dir,f'{gran}_ndvi_mean.tif')#veg_mean for now to get if vegated change
water_median_file = join(time_stats_dir,f'{gran}_ndwi_median.tif')#water_std to find osciallating water
#std_tempslope uses ndwi_mean to mask out water

#get change dates
month_lst = []
for month in os.listdir(gran_dir):
    if len(month) == 6 and month.startswith('2'):
        month_lst.append(month)
print(month_lst)

gdf = gpd.read_file(in_shp)
gdf['month'] = gdf['date']
#gdf['changedate'] = pd.cut(x=gdf.date,bins = date_lst,labels = month_lst)
for i in range(1,len(month_lst)+1):
    print(f'replacing {i} with {month_lst[i-1]}')
    print(type(i))
    gdf['month'] = np.where(gdf['date'] == i,month_lst[i-1],gdf['month'])

gdf = gpd.GeoDataFrame.drop(gdf,columns=['date'])#remove change number


#gdf['slope_std'] = 0 delete if below works
start_time = time.time()
src = rio.open(ts_std_file)

print('adding area attrib, and filtering')
gdf['area'] = gdf.area
gdf = gdf[gdf['area']<100000]

gdf['centroid'] = gdf.centroid
coord_list = [(x, y) for x, y in zip(gdf["centroid"].x, gdf["centroid"].y)]
gdf = gpd.GeoDataFrame.drop(gdf,columns=['centroid'])

print('working on adding slope std')
gdf['slope_std'] = [x for x in src.sample(coord_list)]
gdf['slope_std'] = gdf['slope_std'].astype('int32')

print('working on adding veg')
src = rio.open(veg_mean_file)
gdf['veg_mean'] = [x for x in src.sample(coord_list)]
gdf['veg_mean'] = gdf['veg_mean'].astype('int32')
gdf['veg_mean'] = np.where(gdf['veg_mean'] >= 20,'veg','non-veg')

src = rio.open(veg_std_file)
gdf['veg_std'] = [x for x in src.sample(coord_list)]
gdf['veg_std'] = gdf['veg_std'].astype('int32')
gdf['veg_std'] = np.where(gdf['veg_std'] >= 15,'oscillating','non-oscillating')

print('working on adding water')
src = rio.open(water_median_file)
gdf['water_med'] = [x for x in src.sample(coord_list)]
gdf['water_med'] = gdf['water_med'].astype('int32')
gdf['water_med'] = np.where(gdf['water_med'] >= 8,'water','non-water')

print("geopandas clipping done --- %s seconds ---" % (time.time() - start_time))
print(f'creating {out_shp}')
gdf.to_file(out_shp,driver='ESRI Shapefile')
