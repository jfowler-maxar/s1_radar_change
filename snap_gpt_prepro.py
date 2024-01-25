import os
import subprocess
import xml.etree.ElementTree as ET
from os.path import *

snap_bin = r"D:\Program Files\snap\bin"
snap_cli = join(snap_bin,"snap-cli.bat")
gpt_exe = join(snap_bin,"gpt.exe") ###

work_dir = r"E:\work\s1_change"
tile = 'n39w077'
relorb = '4'
source_dir = join(work_dir,tile)
graphs_dir = join(work_dir,"graphs")
prepro_graph = join(graphs_dir,"s1_prepro.xml")

prepro_dir = join(source_dir,'prepro')
if not exists(prepro_dir):
    os.mkdir(prepro_dir)
target_dir = join(prepro_dir,f'relorb_{relorb}')
if not exists(target_dir):
    os.mkdir(target_dir)

#setup subset as 1x1 tile
lat2 = int(tile[1:3])
long1 = int(tile[-3:])
if 'w' in tile:
    long1 = long1*-1
if 's' in tile:
    lat2 = lat2*-1
lat1 = lat2 + 1
long2 = long1 + 1
#POLYGON ((long1 lat1, long2 lat1, long2 lat2, long1 lat2, long1 lat1))
subset = f'POLYGON (({long1} {lat1}, {long2} {lat1}, {long2} {lat2}, {long1} {lat2}, {long1} {lat1}))'

for safe in os.listdir(source_dir):
    if safe.endswith('.zip'):
        print(f'safe: {safe}')
        read_file = join(source_dir,safe)
        safe_lst = safe.split('_')
        #keep mission id(S1A), start_date, absolute orb num, and product unique ID
        outname = f'{safe_lst[0]}_{safe_lst[4].split("T")[0]}_{safe_lst[6]}_{safe_lst[8].split(".")[0]}.dim'
        abs_orb = safe_lst[6]
        abs_orb_dir = join(target_dir,abs_orb)

        write_file = join(abs_orb_dir,outname)
        #prevous, without absolute orb dirs
        #write_file = join(target_dir,outname)

        if not exists(write_file):

            #idk why this isn't working, just gonna do some python to edit actual graph
            '''
            cmd = f'set subset_polygon="{subset}"'
            print(cmd)
            os.system(cmd)
            cmd = f'set read_file="{read_file}"'
            os.system(cmd)
            cmd = f'set write_file="{write_file}"'
            os.system(cmd)
            '''
            tree = ET.parse(prepro_graph)
            root = tree.getroot()
            for node in root.iter('file'):
                #print(node.text)
                if node.text == '${read_file}':
                    node.text = read_file
                if node.text == '${write_file}':
                    node.text = write_file
            for node in root.iter('geoRegion'):
                #print(node.text)
                if node.text == '${subset_polygon}':
                    node.text= subset

            tmp_graph = join(graphs_dir, "s1_prepro_tmp.xml")
            tree.write(tmp_graph)
            procCmd = f'"{gpt_exe}" "{tmp_graph}" -e' #-t "{write_file}" "{read_file}"'
            print(procCmd)
            subprocess.run(procCmd)
            #os.system(procCmd)

            os.remove(tmp_graph)