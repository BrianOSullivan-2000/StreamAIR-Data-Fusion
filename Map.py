# In[1]

import netCDF4 as nc


def open_ncfile(filename):

    ds = nc.Dataset(filename)

    print(ds['longitude'][:])
    print(ds['latitude'][:])


open_ncfile("reduced/2020/04/" + "S5P_OFFL_L2__NO2____20200401T023618_20200401T041749_12779_01_010302_20200402T184746.reduced.nc")
