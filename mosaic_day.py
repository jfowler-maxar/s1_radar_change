import os
from os.path import *
import subprocess
import xml.etree.ElementTree as ET

snap_bin = r"D:\Program Files\snap\bin"
gpt_exe = join(snap_bin,"gpt.exe")

work_dir = r"E:\work\s1_change"
tile = 'n39w077'
relorb = '4'
tile_dir = join(work_dir, tile)
prepro_dir = join(tile_dir, 'prepro')
relorb_dir = join(prepro_dir, f'relorb_{relorb}')
graphs_dir = join(work_dir,"graphs")

# get all same absolute orb images
for orb in os.listdir(relorb_dir):
    if len(orb) == 6:
        abs_orb_dir = join(relorb_dir, orb)
        data_lst = []
        for dim in os.listdir(abs_orb_dir):
            if dim.endswith('.dim'):
                dim_path = join(abs_orb_dir,dim)
                data_lst.append(dim_path)
        # where is where calcs needs to start
        print(data_lst)

        out_name = f'mosaic_{orb}.dim'
        out_path = join(abs_orb_dir, out_name)
        if not exists(out_path) and len(data_lst) == 2:
            #for now just doing for a scene with 2 data takes
            prepro_graph = join(graphs_dir, "mosaic_02_datatakes.xml")
            tree = ET.parse(prepro_graph)
            root = tree.getroot()

            for node in root.iter('file'):
                # print(node.text)
                if node.text == '${read_file1}':
                    node.text = data_lst[0]
                if node.text == '${read_file2}':
                    node.text = data_lst[1]
                if node.text == '${write_file}':
                    node.text = out_path

            tmp_graph = join(graphs_dir, "mosaic_02_datatakes_tmp.xml")
            tree.write(tmp_graph)
            procCmd = f'"{gpt_exe}" "{tmp_graph}"'
            print(procCmd)
            subprocess.run(procCmd)
            # os.system(procCmd)

            os.remove(tmp_graph)