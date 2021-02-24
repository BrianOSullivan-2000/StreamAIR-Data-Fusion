#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy
import pandas as pd
import subprocess
import json
import os

# In[2]:


def write_download_script(fname_in, fname_out, download_dir):
    with open(fname_in) as f:
        file_info = json.load(f)

    # Find number of separate entries
    nfiles = len(file_info['feed']["entry"])

    # Extract uuid from each entry
    uuids = []
    for xi in range(nfiles):
        uuids.append(file_info['feed']["entry"][xi]["id"])

    # Write uuids to download script
    wget_str1 = "wget -nc --content-disposition --continue --user=s5pguest --password=s5pguest"
    wget_str12 = " -P " + download_dir
    wget_str13 = """ "https://s5phub.copernicus.eu/dhus/odata/v1/Products('"""

    wget_str2 = r"""')/\$value" """
    file = open(fname_out, "w")
    file.write("#!/bin/bash \n")
    for uuid in uuids:
        file.write(wget_str1 + wget_str12 + wget_str13 + uuid + wget_str2 + "\n")

    file.close()

    return nfiles


# In[3]:


start_date = "20200401"
end_date = "20200701"

wget_fname = "wget_loop.scr"

query_fname = "query_results.txt"
download_fname = "download_day.scr"

# 1. Create template text for wget query script
wget_txt1 = "wget --no-check-certificate --user=s5pguest --password=s5pguest --output-document=" + query_fname + " "

# global
# wget_txt2 = "'https://s5phub.copernicus.eu/dhus/search?q=(beginposition:["
# regional, VERIFY EU domain
lon1 = -11
lon2 = 36
lat1 = 36
lat2 = 64
polygon_string = str(lon1) + ' ' + str(lat1) + ',' + str(lon2) + ' ' + str(lat1) + ',' + str(lon2) + ' ' + str(lat2) + ',' + str(lon1) + ' ' + str(lat2) + ',' + str(lon1) + ' ' + str(lat1)
print(polygon_string)

wget_txt2 = "'https://s5phub.copernicus.eu/dhus/search?q=footprint:" + \
    '"intersects(POLYGON((' + polygon_string + ')))"' + " AND beginposition:["

# 2019-01-01T00:00:00.000Z TO 2019-04-30T23:59:59.999Z
wget_txt4 = "] AND producttype:L2__NO2___&rows=100&start=0&format=json'"


# In[4]:
# 2. Loop through dates
dates = pd.date_range(start=start_date, end=end_date)
# print(dates)
for date in dates:

    # 3. Write wget query script
    file = open(wget_fname, "w")
    file.write("#!/bin/bash \n")
    file.write("USERNAME=s5pguest \n")
    file.write("PASSWORD=s5pguest \n")

    date_str = date.strftime("%Y-%m-%d")
    wget_date_str = date_str + "T00:00:00.000Z TO " + date_str + \
        "T23:59:59.999Z"
    wget_line = wget_txt1 + wget_txt2 + wget_date_str + wget_txt4

    file.write(wget_line + " \n")

    file.close()

    # 4. Run the wget script
    subprocess.call(["chmod", "u+x", wget_fname])
    subprocess.call(["./" + wget_fname])

    # Need to check if this was successful somehow...maybe by cleaning up\
    # previous versions

    year = date_str[:4]
    month = date_str[5:7]
    download_dir = "/geos/d21/sat_data/TROPOMI/NO2/EU/" + year + "/" + month + "/"
    if os.path.isfile(query_fname):

        # 5. Run the write download script part:
        nfiles = write_download_script(query_fname, download_fname, download_dir)

    #  # 6. Run the download script from the shell
        subprocess.call(["chmod", "u+x", download_fname])
        subprocess.call(["./" + download_fname])
    ##
    else:
        print(query_fname + " does not exist")


# In[5]:
