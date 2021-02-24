import glob
import xarray as xr
import os.path


def reduce_tropomi_NO2(fname_in, fname_out):
    '''
    Reduce each TROPOMI NO2 orbit file
    only keep desired variables
    '''
    # first group
    group_name = 'PRODUCT'
    ds_group1 = xr.open_dataset(fname_in, group=group_name)

    desired_vars = ['qa_value',
                    'nitrogendioxide_tropospheric_column',
                    'nitrogendioxide_tropospheric_column_precision']

    ds_output = xr.Dataset(coords=ds_group1.coords)

    for ivar in desired_vars:
        ds_output[ivar] = ds_group1[ivar].copy()

    # second group
    group_name = 'PRODUCT/SUPPORT_DATA/DETAILED_RESULTS'
    # fname = '/geos/d21/sat_data/TROPOMI/NO2/EU/2020/04/tmp/test.nc'
    ds_group2 = xr.open_dataset(fname_in, group=group_name)

    desired_vars = ['cloud_fraction_crb_nitrogendioxide_window',
                    'cloud_radiance_fraction_nitrogendioxide_window']

    for ivar in desired_vars:
        ds_output[ivar] = ds_group2[ivar].copy()
        del ds_output[ivar].attrs['coordinates']
        # have to remove this attribute, otherwise incompatible

    # save as netcdf file
    ds_output.to_netcdf(fname_out)

    return


# iterate over all of them
year = '2020'
months = ['04', '05', '06', '07']

top_dir = '/geos/d21/sat_data/TROPOMI/NO2/EU/'

for imonth in months:
    one_month_dir = top_dir + year + '/' + imonth + '/'

    # all of the TROPOMI files in this directory
    fnames = glob.glob(one_month_dir + "*.nc")

    for fname_in in fnames:
        # prepare fname_out
        index = fname_in.find('.nc')
        fname_out_tmp = fname_in[:index] + '.reduced' + fname_in[index:]
        index = fname_out_tmp.find('/2020/')
        fname_out = fname_out_tmp[:index] + '/reduced' + fname_out_tmp[index:]

        if os.path.isfile(fname_out):
            continue
        else:
            reduce_tropomi_NO2(fname_in, fname_out)
            print('reduced ', fname_in, ' to: ', fname_out)
