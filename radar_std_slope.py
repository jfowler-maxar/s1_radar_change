import os
from os.path import *
from osgeo import gdal
import numpy as np

work_dir = r"E:\work\s1_change"
tile = 'n39w077'
relorb = '4'
tile_dir = join(work_dir, tile)
stack_dir = join(tile_dir,'multi_temp_stack')
temp_slope_dir = join(tile_dir,'temp_slope')
chang_dir = join(tile_dir, 'change')
if not exists(chang_dir):
    os.mkdir(chang_dir)

for slope in os.listdir(temp_slope_dir):
    if join(temp_slope_dir,slope).endswith('tempslope.tif'):
        bx_stack = join(temp_slope_dir,slope)
        outname = slope[:-4] + "_std.tif"
        output_path = join(chang_dir,outname)
        if not exists(output_path):
            ds = gdal.Open(bx_stack)
            srs_prj = ds.GetProjection()
            geoTransform = ds.GetGeoTransform()
            xsize = ds.RasterXSize
            ysize = ds.RasterYSize
            num_bands = ds.RasterCount

            drv = gdal.GetDriverByName("GTiff")
            dst_ds = drv.Create(output_path,
                                xsize,
                                ysize,
                                1,
                                gdal.GDT_Float32,
                                )
            dst_ds.SetGeoTransform(geoTransform)
            dst_ds.SetProjection(srs_prj)
            dst_band = dst_ds.GetRasterBand(1)
            dst_band.SetNoDataValue(-32768)

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
                    band = ds.GetRasterBand(1).ReadAsArray(x, y, cols, rows).astype('float32')
                    #arr = np.where(band <= -100, 0, band)
                    arr_std = np.nanstd(band)  # this gives one std value for entire raster
                    # now will compare this arr_std to all other pixels to see how many std's off it is
                    out_arr = band / arr_std

                    dst_band.WriteArray(out_arr, x, y)
