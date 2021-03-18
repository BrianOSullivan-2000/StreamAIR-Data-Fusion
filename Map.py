# In[1]

import numpy as np
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
import s5a as s5a
import warnings
warnings.filterwarnings('ignore')

def open_ncfile(filename):
    # Open file and extract longitudes and latitudes

    # ds = nc.Dataset(filename)
    # ds = s5a.load_ncfile(filename)
    ds = xr.open_dataset(filename)
    # qa = np.array(ds['qa_value'])

    return ds

ds = open_ncfile("Test_NetCDF_file.nc")


# In[2]

#Get NO2 & qa_value column data
ds_NO2 = ds.nitrogendioxide_tropospheric_column
ds_qa = ds.qa_value

#Set longitude and latitude bounds
lon_b = (-25, 29)
lat_b = (35, 68)
ROI_lon_b = (-11, -5)
ROI_lat_b = (51.2, 55.8)

#Convert to dataframe
df = ds_NO2.to_dataframe()

#Add qa_value column & filter out qa < 0.5
df_qa = ds_qa.to_dataframe()
df["qa_value"] = df_qa.qa_value.values
df = df[df["qa_value"] > 0.5]

#Drop NaN values
df = df.dropna()
ROI_df = df


# In[3]

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


# In[4]

#Set geometry with latitudes and longitudes
df_lon = df.longitude.values
df_lat = df.latitude.values
geometry = gpd.points_from_xy(df_lon, df_lat)

#Set geometry for Ireland map
ROI_df_lon = ROI_df.longitude.values
ROI_df_lat = ROI_df.latitude.values
ROI_geometry = gpd.points_from_xy(ROI_df_lon, ROI_df_lat)

#Convert DataFrame to GeoDataFrame
gdf = gpd.GeoDataFrame(df, columns=['nitrogendioxide_tropospheric_column'], geometry=geometry, crs={'init' :'epsg:4326'})
ROI_gdf = gpd.GeoDataFrame(ROI_df, geometry=ROI_geometry, crs={'init' :'epsg:4326'})

# In[5]

#Function for plotting values
def map_plot(gdf, variable, markersize):

    #World map overlay
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    #Plot formatting
    plt.rcParams["font.serif"] = "Times New Roman"
    fig, ax = plt.subplots(1, 1, figsize=(8, 8), dpi=100)
    ax = plt.axes(projection=ccrs.PlateCarree())
    gdf.plot(column=variable, cmap='rainbow', marker=',', markersize=markersize , ax=ax, legend=True)
    ax.coastlines()


#Plot for Western Europe
map_plot(gdf, "nitrogendioxide_tropospheric_column", 4)
plt.title("NO2 Concentration (mol m^2) March 1st 2020")
plt.xlim(lon_b)
plt.ylim(lat_b)
plt.show()

# In[6]

#Function for plotting values
def map_plot(gdf, variable, markersize):

    #World map overlay
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    #Plot formatting
    plt.rcParams["font.serif"] = "Times New Roman"
    fig, ax = plt.subplots(1, 1, figsize=(8, 8), dpi=100)
    ax = plt.axes(projection=ccrs.PlateCarree())
    gdf.plot(column=variable, cmap='rainbow', marker=',', markersize=markersize , ax=ax, legend=True)
    ax.coastlines()

lon_b = (-25, 29)
lat_b = (35, 68)

#Files can now be quickly read into GeoDataFrames
ROI_gdf = gpd.read_file("Europe - April/" + "Sentinel-5P_Apr_14.json")

# In[7]

#Plot for Ireland
map_plot(ROI_gdf, "nitrogendioxide_tropospheric_column", 15)
plt.title("NO2 Concentration (mol m^2) April 2nd 2020")
plt.xlim(lon_b)
plt.ylim(lat_b)
plt.show()
