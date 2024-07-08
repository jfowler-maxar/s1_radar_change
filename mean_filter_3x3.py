import os
from os.path import *
#from osgeo import gdal, ogr,osr
import numpy as np
import scipy
import rasterio as rio

work_dir = r'D:\work\s1_change'
tile = "n28e035"
relorb = '87'
tile_dir = join(work_dir, tile)
temp_slope_dir = join(tile,'temp_slope')
chang_dir = join(tile_dir,'change')
time_stats_dir = join(tile_dir,'time_stats')
vec_dir = join(tile_dir,'vec')

date_num = join(chang_dir, f'{tile}_relorb{relorb}_date_num.tif')
ts_std = join(chang_dir,f'{tile}_relorb{relorb}_tempslope_std.tif')

out_name = f'{tile}_relorb{relorb}_tempslope_std_focal_filter.tif'
out_path = join(chang_dir,out_name)

src = rio.open(ts_std)
arr_ch = src.read()
ch_pro = src.profile
#output_raster = np.full_like(arr_ch, -32767)

#thank you Geoprocessing with Python
arr_avg_std = scipy.ndimage.uniform_filter(arr_ch,size=3,mode='nearest')

print(f'Writing {out_name}')
with rio.open(out_path, "w", **ch_pro) as dst:
    dst.write(arr_avg_std)


out_name = f'{tile}_relorb{relorb}_date_num_focal_filter.tif'
out_path = join(chang_dir, out_name)

src = rio.open(date_num)
arr_ch = src.read()
ch_pro = src.profile
# output_raster = np.full_like(arr_ch, -32767)

# thank you Geoprocessing with Python
arr_avg_std = scipy.ndimage.uniform_filter(arr_ch, size=3, mode='nearest')

print(f'Writing {out_name}')
with rio.open(out_path, "w", **ch_pro) as dst:
    dst.write(arr_avg_std)

