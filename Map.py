# In[1]

import numpy as np
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs


def open_ncfile(filename):
    # Open file and extract longitudes and latitudes

    # ds = nc.Dataset(filename)
    ds = xr.open_dataset(filename)
    # qa = np.array(ds['qa_value'])

    return ds

ds = open_ncfile("reduced/2020/04/" + "S5P_OFFL_L2__NO2____20200401T023618_20200401T041749_12779_01_010302_20200402T184746.reduced.nc")

# In[2]

ds_NO2 = ds.nitrogendioxide_tropospheric_column
ds_lon = ds.longitude
ds_lat = ds.latitude
ds_NO2_numpy = ds_NO2.values

print(ds_NO2.data)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
# ds_NO2.plot()
plt.show()

# Potential solutions: Remove NaN values, filter out qa < 0.5, Cut down ds size (filter?)
# In[3]
