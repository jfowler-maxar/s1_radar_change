import os
from os.path import *
from osgeo import gdal, ogr, osr

work_dir = r"E:\work\s1_change"
tile = 'n39w077'
relorb = '4'
tile_dir = join(work_dir, tile)
stack_dir = join(tile_dir, 'multi_temp_stack')
temp_slope_dir = join(tile_dir, 'temp_slope')
chang_dir = join(tile_dir, 'change')
vec_dir = join(tile_dir, 'vec')
if not exists(vec_dir):
    os.mkdir(vec_dir)

in_name = f'{tile}_relorb{relorb}_ch.tif'
in_path = join(chang_dir, in_name)
if not exists(in_path):
    print('oh no')
    exit()
polygonize = r'C:\Program Files\QGIS 3.28.1\apps\Python39\Scripts\gdal_polygonize.py'

out_name = f'{tile}_relorb{relorb}_ch_tmp.shp'
output_path = join(vec_dir, out_name)

#  get raster datasource
src_ds = gdal.Open(in_path)
srs_prj = src_ds.GetProjection()
geoTransform = src_ds.GetGeoTransform()
print(srs_prj)
#
srcband = src_ds.GetRasterBand(1)
dst_layername = f'{tile}_relorb{relorb}_ch'
drv = ogr.GetDriverByName("ESRI Shapefile")
dst_ds = drv.CreateDataSource(output_path)

sp_ref = osr.SpatialReference()
sp_ref.ImportFromWkt(srs_prj)
# sp_ref.SetFromUserInput('EPSG:4326')

dst_layer = dst_ds.CreateLayer(dst_layername, srs=sp_ref)

fld = ogr.FieldDefn("date", ogr.OFTInteger)
dst_layer.CreateField(fld)
dst_field = dst_layer.GetLayerDefn().GetFieldIndex("date")

# this works, but still includes values=0
# gdal.Polygonize(srcband, None, dst_layer, dst_field, [], callback=None)

# using input band as mask layer, prevents values of 0 getting called!
gdal.Polygonize(srcband, srcband, dst_layer, dst_field, [], callback=None)

del src_ds
del dst_ds
