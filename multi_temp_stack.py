import os
from os.path import *
from osgeo import gdal
import numpy as np

work_dir = r"E:\work\s1_change"
tile = 'n39w077'
relorb = '4'
tile_dir = join(work_dir, tile)
prepro_dir = join(tile_dir, 'prepro')
relorb_dir = join(prepro_dir, f'relorb_{relorb}')
stack_dir = join(tile_dir,'multi_temp_stack')
if not exists(stack_dir):
    os.mkdir(stack_dir)

#get list of all mosaics
sig_lst = []
for orb in os.listdir(relorb_dir):
    if len(orb) == 6:
        abs_orb_dir = join(relorb_dir, orb)
        mosaic_dir = join(abs_orb_dir,f'mosaic_{orb}.data')
        sigma0 = join(mosaic_dir,'Sigma0_VH_db.img')
        if exists(sigma0):
            sig_lst.append(sigma0)

stack_vrt = f'{tile}_relorb{relorb}_stack.vrt'
stack = join(stack_dir,stack_vrt)

if not exists(stack):
    print(f'creating vrt {stack_vrt}')
    gdal.BuildVRT(stack, sig_lst, separate='separate', resolution='highest')

print('done')