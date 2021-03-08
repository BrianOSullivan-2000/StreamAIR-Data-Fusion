# In[1]

import numpy as np
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
import os

import warnings
warnings.filterwarnings('ignore')

# In[2]



def open_ncfile(filename):
    # Open file and extract longitudes and latitudes

    # ds = nc.Dataset(filename)
    ds = xr.open_dataset(filename)
    # qa = np.array(ds['qa_value'])

    return ds

# In[3]

# Loop through files finding those which contain data in Western Europe
i = 1
good_files_Apr = []

# Loop through directory
for filename in os.listdir("reduced/2020/04/"):

    ds = open_ncfile("reduced/2020/04/" + filename)

    #Get NO2 column data
    ds_NO2 = ds.nitrogendioxide_tropospheric_column
    ds_qa = ds.qa_value

    #Set longitude and latitude bounds
    lon_b = (-22, 20)
    lat_b = (42, 62)
    ROI_lon_b = (-11, -5)
    ROI_lat_b = (51.2, 55.8)

    #Convert to dataframe and remove nan values
    df = ds_NO2.to_dataframe()

    #Add qa_value column & filter out qa < 0.5
    df_qa = ds_qa.to_dataframe()
    df["qa_value"] = df_qa.qa_value.values
    df = df[df["qa_value"] > 0.5]

    df = df.dropna()

    #Set boundaries for dataframe
    df = df[df["longitude"] > lon_b[0]]
    df = df[df["longitude"] < lon_b[1]]
    df = df[df["latitude"] > lat_b[0]]
    df = df[df["latitude"] < lat_b[1]]

    if df.empty == False:
        good_files_Apr.append(i)

    i += 1

# In[4]

# Loop through files finding those which contain data in Western Europe

i = 1
good_files_May = []

# Loop through directory
for filename in os.listdir("reduced/2020/05/"):


    ds = open_ncfile("reduced/2020/05/" + filename)

    #Get NO2 column data
    ds_NO2 = ds.nitrogendioxide_tropospheric_column
    ds_qa = ds.qa_value

    #Set longitude and latitude bounds
    lon_b = (-22, 20)
    lat_b = (42, 62)

    #Convert to dataframe and remove nan values
    df = ds_NO2.to_dataframe()

    #Add qa_value column & filter out qa < 0.5
    df_qa = ds_qa.to_dataframe()
    df["qa_value"] = df_qa.qa_value.values
    df = df[df["qa_value"] > 0.5]

    df = df.dropna()

    #Set boundaries for dataframe
    df = df[df["longitude"] > lon_b[0]]
    df = df[df["longitude"] < lon_b[1]]
    df = df[df["latitude"] > lat_b[0]]
    df = df[df["latitude"] < lat_b[1]]

    if df.empty == False:
        good_files_May.append(i)

    i += 1


# In[5]

# Loop through files finding those which contain data in Western Europe

i = 1
good_files_Jun = []

# Loop through directory
for filename in os.listdir("reduced/2020/06/"):


    ds = open_ncfile("reduced/2020/06/" + filename)

    #Get NO2 column data
    ds_NO2 = ds.nitrogendioxide_tropospheric_column
    ds_qa = ds.qa_value

    #Set longitude and latitude bounds
    lon_b = (-22, 20)
    lat_b = (42, 62)

    #Convert to dataframe and remove nan values
    df = ds_NO2.to_dataframe()

    #Add qa_value column & filter out qa < 0.5
    df_qa = ds_qa.to_dataframe()
    df["qa_value"] = df_qa.qa_value.values
    df = df[df["qa_value"] > 0.5]

    df = df.dropna()

    #Set boundaries for dataframe
    df = df[df["longitude"] > lon_b[0]]
    df = df[df["longitude"] < lon_b[1]]
    df = df[df["latitude"] > lat_b[0]]
    df = df[df["latitude"] < lat_b[1]]

    if df.empty == False:
        good_files_Jun.append(i)

    i += 1

# In[6]

print(good_files_Apr)
print(good_files_May)
print(good_files_Jun)
