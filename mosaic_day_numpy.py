import os
from os.path import *
from osgeo import gdal
import numpy as np

work_dir = r'D:\s1_change'
tile = "n22e114"
relorb = '113'
tile_dir = join(work_dir, tile)
prepro_dir = join(tile_dir, 'prepro')
relorb_dir = join(prepro_dir, f'relorb_{relorb}')



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

print(f'{long1}, {lat2}, {long2}, {lat1}')


#gdal warp all Sigma's to .tifs
for orb in os.listdir(relorb_dir):
    if len(orb) == 6:
        abs_orb_dir = join(relorb_dir, orb)
        #data_lst = []
        for data in os.listdir(abs_orb_dir):
            if data.endswith('.data'):
                data_path = join(abs_orb_dir,data)
                img_name = 'Sigma0_VH_db.img' #will always be this
                img_path = join(data_path,img_name)

                out_path = f'{abs_orb_dir}\{img_name[:-4]}_{data.split("_")[3][:-5]}_warp.tif'
                #print(out_path)
                if not exists(out_path):
                    #geo_transform = (x top left, x cell size, x rotation, y top left, y rotation, negative y cell size)
                    kwargs = {'format': 'GTiff', 'outputBounds': [long1, lat2, long2, lat1], 'dstNodata': '0'}
                    print(f'Creating {out_path}')
                    gdal.Warp(out_path,img_path,**kwargs)

#mosaic all tifs
for orb in os.listdir(relorb_dir):
    if len(orb) == 6:
        abs_orb_dir = join(relorb_dir, orb)
        tif_lst = []
        for tif in os.listdir(abs_orb_dir):
            if tif.endswith('warp.tif'):
                tif_path = join(abs_orb_dir,tif)
                tif_lst.append(tif_path)

        out_name = f'mosaic_{orb}.tif'
        out_path = join(abs_orb_dir, out_name)
        if not exists(out_path):
            kwargs = {'format': 'GTiff', 'dstNodata': '0'}
            print(f'Creating {out_path}')
            gdal.Warp(out_path, tif_lst, **kwargs)





