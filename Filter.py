# In[1]

import numpy as np
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs

import warnings
warnings.filterwarnings('ignore')

# In[2]

def open_ncfile(filename):
    # Open file and extract longitudes and latitudes

    # ds = nc.Dataset(filename)
    ds = xr.open_dataset(filename)
    # qa = np.array(ds['qa_value'])

    return ds

ds = open_ncfile("reduced/2020/04/" + "S5P_OFFL_L2__NO2____20200408T121425_20200408T135555_12884_01_010302_20200410T051600.reduced.nc")

#Get NO2 column data
ds_NO2 = ds.nitrogendioxide_tropospheric_column

#Set longitude and latitude bounds
lon_b = (-22, 20)
lat_b = (42, 62)
ROI_lon_b = (-11, -5)
ROI_lat_b = (51.2, 55.8)

#Convert to dataframe and remove nan values
df = ds_NO2.to_dataframe()
df = df.dropna()
ROI_df = df

#Set boundaries for dataframe
df = df[df["longitude"] > lon_b[0]]
df = df[df["longitude"] < lon_b[1]]
df = df[df["latitude"] > lat_b[0]]
df = df[df["latitude"] < lat_b[1]]

#Set boundaries for ireland DataFrame
ROI_df = ROI_df[ROI_df["longitude"] > ROI_lon_b[0]]
ROI_df = ROI_df[ROI_df["longitude"] < ROI_lon_b[1]]
ROI_df = ROI_df[ROI_df["latitude"] > ROI_lat_b[0]]
ROI_df = ROI_df[ROI_df["latitude"] < ROI_lat_b[1]]

print(df)
