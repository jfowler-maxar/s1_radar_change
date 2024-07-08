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
stack_dir = join(tile_dir,'multi_temp_stack')
if not exists(stack_dir):
    os.mkdir(stack_dir)

date_lst = []
for orb in os.listdir(relorb_dir):
    if len(orb) == 6:
        abs_orb_dir = join(relorb_dir,orb)
        for data in os.listdir(abs_orb_dir):
            if data.startswith('S1A') and data.endswith('.dim'):
                date_lst.append(data.split('_')[1])

date_lst = list(set(date_lst))
date_lst.sort()
print(date_lst)
out_csv = join(stack_dir,f'date_relorb_{relorb}.csv')
np.savetxt(out_csv,
        date_lst,
        delimiter =", ",
        fmt ='% s')

#get list of all mosaics
sig_lst = []
for orb in os.listdir(relorb_dir):
    if len(orb) == 6:
        abs_orb_dir = join(relorb_dir, orb)
        mosaic_dir = join(abs_orb_dir,f'mosaic_{orb}.data')
        if exists(mosaic_dir):
            sigma0 = join(mosaic_dir,'Sigma0_VH_db.img')
            if exists(sigma0):
                sig_lst.append(sigma0)
        else:
            for data_take in os.listdir(abs_orb_dir):
                if data_take.endswith('.data'):
                    data_take_dir = join(abs_orb_dir,data_take)
                    sigma0 = join(data_take_dir, 'Sigma0_VH_db.img')
                    if exists(sigma0):
                        sig_lst.append(sigma0)

print(sig_lst)
stack_vrt = f'{tile}_relorb{relorb}_stack.vrt'
stack = join(stack_dir,stack_vrt)

if not exists(stack):
    print(f'creating vrt {stack_vrt}')
    gdal.BuildVRT(stack, sig_lst, separate='separate', resolution='highest')

print('done')
