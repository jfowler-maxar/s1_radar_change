import os
from os.path import *
import subprocess

work_dir = r"E:\work\s1_change"
tile = 'n39w077'
relorb = '4'
tile_dir = join(work_dir, tile)
stack_dir = join(tile_dir,'multi_temp_stack')
temp_slope_dir = join(tile_dir,'temp_slope')
chang_dir = join(tile_dir, 'change')

sieve = r'C:\Program Files\QGIS 3.28.1\apps\Python39\Scripts\gdal_sieve.py'

in_name = f'{tile}_relorb{relorb}_ch_tmp.tif'
in_path = join(chang_dir, in_name)
if not exists(in_path):
    print('oh no')
    exit()
out_name = f'{tile}_relorb{relorb}_ch.tif'
output_path = join(chang_dir, out_name)
#cmd = ['python',sieve,'-st','2','-8','-mask',in_path,'-of', 'GTiff',in_path,output_path]
cmd = ['python',sieve,'-st','2','-8','-of', 'GTiff',in_path,output_path]
print(cmd)
subprocess.call(cmd,shell=True)
#os.remove(output_path)