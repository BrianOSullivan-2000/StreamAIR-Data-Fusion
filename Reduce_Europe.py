# In[1]

import numpy as np
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
import os
import fiona
import json

import warnings
warnings.filterwarnings('ignore')

# In[2]

#Set longitude and latitude bounds
lon_b = (-25, 29)
lat_b = (35, 68)


def open_ncfile(filename):
    # Open file and extract longitudes and latitudes
    ds = xr.open_dataset(filename)

    return ds


def reduce(ds):

    #reduce file to useful data in Western Europe
    ds_NO2 = ds.nitrogendioxide_tropospheric_column
    ds_qa = ds.qa_value
    ds_NO2_precision = ds.nitrogendioxide_tropospheric_column_precision
    ds_cloud_fraction = ds.cloud_fraction_crb_nitrogendioxide_window
    ds_cloud_radiance = ds.cloud_radiance_fraction_nitrogendioxide_window

    #Convert to dataframe
    df = ds_NO2.to_dataframe()

    #Add auxiliary values
    df_NO2_precision = ds_NO2_precision.to_dataframe()
    df_cloud_fraction = ds_cloud_fraction.to_dataframe()
    df_cloud_radiance = ds_cloud_radiance.to_dataframe()

    #Add values as columns to dataframe
    df["nitrogendioxide_tropospheric_column_precision"] = df_NO2_precision.nitrogendioxide_tropospheric_column_precision.values
    df["cloud_fraction_crb_nitrogendioxide_window"] = df_cloud_fraction.cloud_fraction_crb_nitrogendioxide_window.values
    df["cloud_radiance_fraction_nitrogendioxide_window"] = df_cloud_radiance.cloud_radiance_fraction_nitrogendioxide_window.values

    #Add qa_value column & filter out qa < 0.5
    df_qa = ds_qa.to_dataframe()
    df["qa_value"] = df_qa.qa_value.values
    df = df[df["qa_value"] > 0.5]

    #Drop NaN values & ground_pixel, scanline coords
    df = df.dropna()
    df = df.reset_index()
    df = df.drop(["scanline", "ground_pixel"], axis=1)

    #Set boundaries for dataframe
    df = df[df["longitude"] > lon_b[0]]
    df = df[df["longitude"] < lon_b[1]]
    df = df[df["latitude"] > lat_b[0]]
    df = df[df["latitude"] < lat_b[1]]

    #Set geometry with latitudes and longitudes
    df_lon = df.longitude.values
    df_lat = df.latitude.values
    geometry = gpd.points_from_xy(df_lon, df_lat)

    #Convert DataFrame to GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs={'init' :'epsg:4326'})

    #Fix formatting issue with time
    gdf['time'] = gdf['time'].dt.strftime('%Y-%m-%d')

    return gdf

# In[3]

#Extract filtered lists indexing useful files
def get_correct_files(Month, number):

    #Loop over files evaluated with Filter.py
    with open("Good files.txt") as f:
        lines = f.readlines()

        for line in lines:
            if (lines.index(line) + 1) / 2 == number:

                #Split into values and remove "[]" from beginning and end
                list = (line.split(", "))
                list[0], list[-1] = list[0][1:], list[-1][:-2]

                for i in list:
                    Month.append(int(i))

April, May, June = [], [], []

#Note April==1, May==2, June==3
#Compile lists of indexes for useful files
get_correct_files(April, 1)
get_correct_files(May, 2)
get_correct_files(June, 3)

# In[4]

#Open files according to get_correct_files(), reduce them and write to Europe directories
i = 1

#Loop through files in reduced/, files moved afterwards due to lack of space
for filename in os.listdir("reduced/2020/06/"):

    if i in June:

        #Extract and reduce file data
        raw_file = open_ncfile("reduced/2020/06/" + filename)
        file = reduce(raw_file)
        raw_file.close()

        #Save reduced file in .json format
        file.to_file("Europe - June/" + "Sentinel-5P_June_{}.json".format(i), driver='GeoJSON')


    i += 1

# In[5]

#Files can now be quickly read into GeoDataFrames
file = gpd.read_file("Europe - April/" + "Sentinel-5P_Apr_6.json")
file
