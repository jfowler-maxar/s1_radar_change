import os
from os.path import *
from osgeo import gdal
import numpy as np
import time

work_dir = r"E:\work\s1_change"
tile = 'n39w077'
relorb = '4'
tile_dir = join(work_dir, tile)
stack_dir = join(tile_dir,'multi_temp_stack')
temp_slope_dir = join(tile_dir,'temp_slope')
chang_dir = join(tile_dir, 'change')

start_time = time.time()
for stack in os.listdir(stack_dir):
    if '_stack.' in stack:
        bxstack = join(stack_dir,stack)
        ds = gdal.Open(bxstack)
        srs_prj = ds.GetProjection()
        geoTransform = ds.GetGeoTransform()
        xsize = ds.RasterXSize
        ysize = ds.RasterYSize
        num_bands = ds.RasterCount

        out = stack[:-9]+'date_num.tif'
        out_path = join(chang_dir,out)
        print(f'working on {out_path}')

        drv = gdal.GetDriverByName("GTiff")
        dst_ds = drv.Create(out_path,
                            xsize,
                            ysize,
                            1,
                            gdal.GDT_Byte,
                            )
        dst_ds.SetGeoTransform(geoTransform)
        dst_ds.SetProjection(srs_prj)
        dst_band = dst_ds.GetRasterBand(1)

        print('chipping')
        block_xsize = 512
        block_ysize = 512
        minx = geoTransform[0]
        miny = geoTransform[3]
        step_x = geoTransform[1]
        step_y = geoTransform[5]
        count_x = 0
        count_y = 0
        for x in range(0, xsize, block_xsize):
            # print(f'block x: {x}')
            if x + block_xsize < xsize:
                cols = block_xsize
                x_off = minx + (count_x * step_x)
                count_x = count_x + block_xsize
            else:
                cols = xsize - x
                x_off = minx + (count_x * step_x)
                count_x = count_x + x
            count_y = 0
            for y in range(0, ysize, block_ysize):
                print(f'block xy: {x} {y}')
                if y + block_ysize < ysize:
                    rows = block_ysize
                    y_off = miny + (count_y * step_y)
                    count_y = count_y + block_ysize
                else:
                    rows = ysize - y
                    y_off = miny + (count_y * step_y)
                    count_y = count_y + y

                # this is where calculations/data maniuplations happen
                array_layers = []
                for i in range(1, num_bands + 1):
                    band = ds.GetRasterBand(i).ReadAsArray(x, y, cols, rows).astype('float32')
                    array_layers.append(band)

                mean_arr0 = np.nanmean(array_layers,axis=0)#getting errors with all Nan slices
                mean_arr = np.where(mean_arr0 <= -9999, 0, mean_arr0) #if every band = nan then avg will be nan, so this sets it to 0

                for k in range(len(array_layers)):
                    array_layers[k][np.isnan(array_layers[k])] = mean_arr[np.isnan(array_layers[k])]

                diff_arr = np.diff(array_layers, axis=0)
                diff_abs = np.abs(diff_arr) #getting absolute value

                max_arg = np.nanargmax(diff_arr, axis=0)+2 #return value is index 0 = b2-b1, 1 = b3-b2, 2 = b4-b3, etc
                #so +2 should be the band number where change first appears
                dst_band.WriteArray(max_arg, x, y)
print("--- %s seconds ---" % (time.time() - start_time))
