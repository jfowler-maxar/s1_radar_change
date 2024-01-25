# s1_radar_change

Not used to creating README's so apologies if missing information 

Requirements: 
ESA's SNAP, Copernicus Browser account

Python modules: 
pandas, geopandas, osgeo, 

General information
Hardcoded paths for creating Dirs, hardcoded Copernicus Browser Credentials

Workflow

1. access_sentinel_data\search_for_gran.py
requires Copernicus Browser account for downloading Sentinel 1 scenes
Search parameters: data_collection, productType, 1x1 tile, start/end dates

Outputs: monthly csv's and concatenated {tile}_id.csv


2. access_sentinel_data\find_rel_orbs.py
Finds all relative orbits for AOI
Currently only uses S1-BA, because S1-B went down a couple years ago 
input: {tile}_id.csv from (1)
output: {tile}_relorb_{orb_num}.csv


3. access_sentinel_data\download_sentinel.py
editing/removing csv (2) before generally recommended    
Downloads S1 zips to local
Copernicus Browser can only download 3 scenes at a time, so requires rerurnning...
Need to update/fix this  
input: pick a csv from (2)
output: S1 zip files


4. snap_gpt_prepro.py
Geocoding: transforms from SAR geometry into a map projection
Graph from ESA SNAP tutorials includes: Thermal Noise Removal, Calibration, Terrain-Correction, Linear to from db, Subset
input: S1 zip files from (3)
output: geocoded images, in absolute orbit dir's 


5. mosaic_day.py
Mosaic scenes in absolute orbit together for AOI
input: geocoded images from(4)
output:ready for analysis mosaiced images 


6. multi_temp_stack.py
Take mosaics from (5) and put in vrt stack
input: mosaics from (5)
output: {tile}_relorb{relorb}_stack.vrt


7. radar_temporal_slope.py
Create linear regression slope
input: {tile}_relorb{relorb}_stack.vrt from (6)
output: {tile}_relorb{relorb}_tempslope.tif 


8. radar_std_slope.py
takes temporal slope and outputs standard deviation, to be used for thresholding later
input: {tile}_relorb{relorb}_tempslope.tif (7)
output: {tile}_relorb{relorb}_tempslope_std.tif


9. radar_step_time.py
Get date of largest step.
To be combined with tempslope_std(9) later
input: {tile}_relorb{relorb}_stack.vrt from (6)
output: {tile}_relorb{relorb}_date_num.tif


10. radar_change_layer.py
Take tempslope_std > |3| and return date_num 
input: {tile}_relorb{relorb}_tempslope_std.tif(8) and {tile}_relorb{relorb}_date_num.tif'(9)
output: {tile}_relorb{relorb}_ch_tmp.tif

11. radar_ch_layer_sieve.py
gdal_sieve to remove single pixels
input: {tile}_relorb{relorb}_ch_tmp.tif(10)
output: {tile}_relorb{relorb}_ch.tif


12. radar_vectorize.py
Take change raster and export to vector
input: {tile}_relorb{relorb}_ch.tif(11)
output: {tile}_relorb{relorb}_ch_tmp.shp

13. radar_vec_attrib.py
Change date added to vec
tempslope_std added to attributes
input: {tile}_relorb{relorb}_ch_tmp.shp (12)
output: {tile}_relorb{relorb}_ch_final.shp
