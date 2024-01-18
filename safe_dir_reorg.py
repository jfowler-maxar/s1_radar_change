import os
from os.path import *
#from osgeo import gdal
from zipfile import ZipFile
import shutil


#setup work dir's
work_dir = r'E:\work\s1_change'
gran = "n38w078"
gran_dir = join(work_dir,gran)
text_dir = join(gran_dir,'text')

for z in os.listdir(gran_dir):
    if z.endswith(".zip"):
        #print(z)
        date = z.split("_")[4][0:8]
        #print(date)
        date_dir = join(gran_dir,date)
        if os.path.exists(date_dir) ==False:
            print("creating {}".format(date_dir))
            os.mkdir(date_dir)
        if os.path.exists(join(date_dir,z[:-3]+"safe")) == False:
            with ZipFile(join(gran_dir,z),'r') as zObject:
                print("Unzipping: {}".format(z))
                zObject.extractall(date_dir)
            zObject.close()
        else:
            print("no need to unzip {}".format(z))

for date in os.listdir(gran_dir):
    if len(date) == 8 and date.startswith('2'):
        print("Going into {} dir's".format(date))
        date_dir = join(gran_dir, date)
        for i in os.listdir(date_dir):
            if i.endswith(".SAFE"):
                #need to create date dir's
                date = i.split("_")[4][0:8]
                date_dir = join(date_dir,date)
                safe_dir = join(date_dir,i)
                ann = 'annotation'
                ann_copy = join(date_dir, ann)
                for j in os.listdir(safe_dir):
                    ann_dir = join(safe_dir,ann)
                    measure_dir = join(safe_dir,'measurement')
                    if not exists(ann_copy):
                        if exists(ann_dir):
                            shutil.copytree(ann_dir,ann_copy)
                        else:
                            print(f'looks like {ann_dir} dne')
                    for tiff in os.listdir(measure_dir):
                        if '-vv-' in tiff:
                            shutil.copy2(tiff,date_dir)
                print("Done with {}".format(date_dir))

#i could add a part to delete the .zip's, that's easy, but gonna hold on to them for now cause testing
#I'll go ahead and delete the .SAFE's cause why not
for date in os.listdir(gran_dir):
    if len(date) == 8 and date.startswith('2'):
        print("Going into {} dir's".format(date))
        date_dir = join(gran_dir, date)
        for i in os.listdir(date_dir):
            if i.endswith(".SAFE"):
                print('deleting {} .SAFEs'.format(date))
                shutil.rmtree(join(date_dir,i))

print("its done!")

