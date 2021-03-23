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
    ds = s5a.load_ncfile(filename)
    ds = s5a.filter_by_quality(ds)
    #ds = xr.open_dataset(filename)
    # qa = np.array(ds['qa_value'])

    return ds

df = open_ncfile("data/S5P_OFFL_L2__CO_____20201001T221937_20201002T000107_15387_01_010302_20201003T120351.nc.tmp")


# In[2]

#Set longitude and latitude bounds
lon_b = (-11, 36)
lat_b = (36, 64)
ROI_lon_b = (-11, -5)
ROI_lat_b = (51.2, 55.8)

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
geometry = gpd.points_from_xy(df.longitude, df.latitude)

#Set geometry for Ireland map
ROI_geometry = gpd.points_from_xy(ROI_df.longitude, ROI_df.latitude)

#Convert DataFrame to GeoDataFrame
gdf = gpd.GeoDataFrame(df, columns=['value'], geometry=geometry, crs={'init' :'epsg:4326'})
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
map_plot(gdf, "value", 4)
plt.title("NO2 Concentration (mol m^2) March 1st 2020")
plt.xlim(lon_b)
plt.ylim(lat_b)
plt.show()
