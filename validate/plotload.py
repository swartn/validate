"""
plotload
===============

THis module contains functions that will load data from
netCDF files needed to produce plots. It uses various cdo
commands to manipulate the netCDF files if they need to be
processed before the data is extracted.

.. moduleauthor:: David Fallis
"""

import os
from netCDF4 import Dataset, num2date, date2num
import numpy as np
import datetime
import cdo
cdo = cdo.Cdo()


def _check_averaged(ifile):
    nc = Dataset(ifile, 'r')
    time = nc.variables['time'][:].squeeze()
    return time.size == 1


def year_mon_day(datestring):
    year = datestring.split('-')[0]
    try:
        mon = datestring.split('-')[1]
    except:
        mon = '01'
    try:
        day = datestring.split('-')[2]
    except:
        day = '01'
    return int(year), int(mon), int(day)


def _check_dates_outside(ifile, start_date, end_date):
    nc = Dataset(ifile, 'r')
    time = nc.variables['time_bnds'][:].squeeze()
    nc_time = nc.variables['time']
    try:
        cal = nc_time.calendar
    except:
        cal = 'standard'
    start = datetime.datetime(*year_mon_day(start_date))
    end = datetime.datetime(*year_mon_day(end_date))
    start = date2num(start, nc_time.units)
    end = date2num(end, nc_time.units)
    compstart = nc_time[:][0]
    compend = nc_time[:][-1]
    if compstart > end or compend < start:
        return True
    elif compstart > start or compend < end:
        with open('logs/log.txt', 'a') as outfile:
            outfile.write('WARNING: Comparison data does not cover entire time period... Used subset\n')
    return False


def _check_dates(ifile, dates):
    if _check_averaged(ifile):
        with open('logs/log.txt', 'a') as outfile:
            outfile.write('WARNING: Comparison data is time averaged\n')
        return False
    elif _check_dates_outside(ifile, **dates):
        with open('logs/log.txt', 'a') as outfile:
            outfile.write('WARNING: Comparison data is not from time period\n')
        raise Exception


def _scale_units(units, scale):
    """ Corrects the units to match the scale applied to the data

    Parameters
    ----------
    units : string
    scale : int

    Returns
    -------
    string
    """
    if scale != 1:
        units = units + ' * ' + str(scale)
    return units


def _load(nc, var):
    """ Extracts the data from a netCDF4 Dataset along
        with the units and associated depths

    Parameters
    ----------
    nc : netCDF4.Dataset
    var : string
    depth_type : string

    Returns
    -------
    numpy array
    string
    list
    """
    try:
        ncvar = nc.variables[var]
    except:
        varu = var.upper()
        ncvar = nc.variable[varu]
    data = ncvar[:].squeeze()

    try:
        units = ncvar.units
    except:
        units = ''

    depth = [0]
    for dimension in ncvar.dimensions:
        try:
            if nc.variables[dimension].axis == 'Z':
                depth = nc.variables[dimension][:]
                break
        except:
            pass

    return data, units, depth


def _load2(data, nc, units, depth, scale):
    """ Extracts the data from a netCDF4 Dataset along
        with the units and associated depths

    Parameters
    ----------
    data : numpy array
    nc : netCDF4.Dataset
    units : string
    depth : numpy array
    scale : int

    Returns
    -------
    numpy array
    numpy array
    numpy array
    numpy array
    string
    """
    lon = nc.variables['lon'][:].squeeze()
    lat = nc.variables['lat'][:].squeeze()
    depth = np.round(depth)
    units = _scale_units(units, scale)
    data = data * scale
    return data, lon, lat, depth, units

def get_remap_function(remap):
    if remap == 'remapdis':
        return cdo.remapdis
    def cdoremap(r):
        return {'remapbil': cdo.remapbil,
                'remapbic': cdo.remapbic,
                'remapdis': cdo.remapdis,
                'remapnn': cdo.remapnn,
                'remapcon': cdo.remapcon,
                'remapcon2': cdo.remapcon2,
                'remapplaf': cdo.remaplaf,
                }[r]  
    return cdoremap(remap)  
    
    
def timeaverage_load(ifile, var, dates, realm, scale, remapf='remapdis', remapgrid='r360x180'):
    """ Loads the data from a file and remaps it.
        Applies a time average over specified dates and scales the data.

    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    dates : dictionary
            maps 'start_date' and 'end_date' to date string with formay 'yyyy-mm'
    realm : string
            either 'ocean', 'land' or 'atmos'
    scale : int
            scale the data by this factor

    Returns
    -------
    numpy array
    string
    numpy array
    numpy array
    numpy array
    """
    _check_dates(ifile, dates)
    path, sfile = os.path.split(ifile)
    remap = get_remap_function(remapf)
    finalout = 'remapfiles/' + remapf + remapgrid + '_' + sfile + str(dates['start_date']) + str(dates['end_date']) + '.nc'
    if not os.path.isfile(finalout):
        out = 'remapfiles/remapfile.nc'
        if realm == 'ocean':
            cdo.ifthen(input='mask/ocean ' + ifile, output=out)
        elif realm == 'land':
            cdo.ifthen(input='mask/land ' + ifile, output=out)
        else:
            out = ifile
        cdo.selvar(var, input=out, output='remapfiles/selvar.nc')
        out = 'remapfiles/selvar.nc'
        cdo.timmean(input='-seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + out, output='remapfiles/seldate.nc')
        remap(remapgrid, options='-L', input='-setctomiss,0 remapfiles/seldate.nc', output=finalout)
    nc = Dataset(finalout, 'r')

    data, units, depth = _load(nc, var)
    data, lon, lat, depth, units = _load2(data, nc, units, depth, scale)

    return data, units, lon, lat, depth


def timeaverage_load_comp(ifile, var, dates, realm, depthneeded, scale, remapf='remapdis', remapgrid='r360x180'):
    """ Loads the data from a file and remaps it to 360x180.
        Also remaps the vertical axis to specified depths for easy comparison
        Applies a time average over specified dates and scales the data.

    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    dates : dictionary
            maps 'start_date' and 'end_date' to date string with formay 'yyyy-mm'
    realm : string
            either 'ocean', 'land' or 'atmos'
    depthneeded : numpy array
    scale : int
            scale the data by this factor

    Returns
    -------
    numpy array
    string
    numpy array
    numpy array
    numpy array
    """
    depthneeded = ["%.2f" % number for number in depthneeded]
    for i in xrange(len(depthneeded)):
        depthneeded[i] = str(depthneeded[i])
    depthneededstr = ','.join(depthneeded)
    
    _check_dates(ifile, dates)    
    path, sfile = os.path.split(ifile)
    remap = get_remap_function(remapf)
    finalout = 'remapfiles/' + remapf + remapgrid + '_' + sfile + str(dates['start_date']) + str(dates['end_date']) + '.nc'
    if not os.path.isfile(finalout):
        out = 'remapfiles/selvar.nc'    
        cdo.selvar(var, input=ifile, output=out)
        remap(remapgrid, options='-L', input='-setctomiss,0 -timmean -seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + out, output=finalout)
    try:
        cdo.intlevelx(str(depthneededstr), input=finalout, output=finalout + str(depthneeded[0]) + '.nc')
        nc = Dataset(finalout + str(depthneeded[0]) + '.nc', 'r')
    except:
        nc = Dataset(finalout, 'r')

    data, units, depth = _load(nc, var)
    data, lon, lat, depth, units = _load2(data, nc, units, depth, scale)
    return data, units, lon, lat, depth


def trends_load(ifile, var, dates, scale, remapf='remapdis', remapgrid='r360x180'):
    """ Loads the trend data over specified dates from a file
        Remaps and scales the data.

    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    dates : dictionary
            maps 'start_date' and 'end_date' to date string with formay 'yyyy-mm'
    scale : int
            scale the data by this factor

    Returns
    -------
    numpy array
    string
    numpy array
    numpy array
    numpy array
    """
    _check_dates(ifile, dates)
    path, sfile = os.path.split(ifile)
    remap = get_remap_function(remapf)
    finalout = 'trendfiles/slope_' + remapf + remapgrid + '_' + sfile + str(dates['start_date']) + str(dates['end_date']) + '.nc'
    slopefile = 'trendfiles/slope_' + sfile + str(dates['start_date']) + str(dates['end_date']) + '.nc'
    if not os.path.isfile(finalout):
        cdo.trend(input='-seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + ifile,
                  output='trendfiles/intercept_' + sfile + ' ' + slopefile)
        remap(remapgrid, input='-setctomiss,0 ' + slopefile,
                  output=finalout)
    nc = Dataset(finalout, 'r')

    data, units, depth = _load(nc, var)
    data, lon, lat, depth, units = _load2(data, nc, units, depth, scale)

    return data, units, lon, lat, depth


def trends_load_comp(ifile, var, dates, depthneeded, scale, remapf='remapdis', remapgrid='r360x180'):
    """ Loads the trend data over specified dates from a file
        Remaps and scales the data. Also remaps the vertical axis to
        specified depths for easy comparison.

    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    dates : dictionary
            maps 'start_date' and 'end_date' to date string with formay 'yyyy-mm'
    depthneeded : numpy array
    scale : int
            scale the data by this factor

    Returns
    -------
    numpy array
    string
    numpy array
    numpy array
    numpy array
    """
    depthneeded = ["%.2f" % number for number in depthneeded]
    for i in xrange(len(depthneeded)):
        depthneeded[i] = str(depthneeded[i])
    depthneededstr = ','.join(depthneeded)

    _check_dates(ifile, dates)
    path, sfile = os.path.split(ifile)
    remap = get_remap_function(remapf)
    finalout = 'trendfiles/slope_' + remapf + remapgrid + sfile + str(dates['start_date']) + str(dates['end_date']) + '.nc'
    trendfile = 'trendfiles/slope_' + sfile + str(dates['start_date']) + str(dates['end_date']) + '.nc'
    if not os.path.isfile(finalout):
        cdo.selvar(var, input=ifile, output='trendfiles/selvar.nc')
        out = 'trendfiles/selvar.nc'
        cdo.trend(input='-seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + out,
                  output='trendfiles/intercept_' + sfile + ' ' + trendfile)
        remap(remapgrid, options='-L', input='-setctomiss,0 ' + trendfile,
                  output=finalout)
    try:
        cdo.intlevelx(str(depthneededstr), input=finalout, output=finalout + str(depthneeded[0]) + '.nc')
        nc = Dataset(finalout + str(depthneeded[0]) + '.nc', 'r')
    except:
        nc = Dataset(finalout, 'r')

    data, units, depth = _load(nc, var)
    data, lon, lat, depth, units = _load2(data, nc, units, depth, scale)
    return data, units, lon, lat, depth


def timeseries_load(ifile, var, dates, realm, scale):
    """ Loads the field mean data over specified dates from a file.
        Remaps and scales the data.

    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    dates : dictionary
            maps 'start_date' and 'end_date' to date string with formay 'yyyy-mm'
    scale : int
            scale the data by this factor

    Returns
    -------
    numpy array
    string
    numpy array
    numpy array
    """
    _check_dates(ifile, dates)    
    path, sfile = os.path.split(ifile)
    finalout = 'fldmeanfiles/fldmean_' + sfile + str(dates['start_date']) + str(dates['end_date']) + '.nc'

    if not os.path.isfile(finalout):
        out = 'fldmeanfiles/fldmean.nc'
        if realm == 'ocean':
            cdo.ifthen(input='mask/ocean ' + ifile, output=out)
        elif realm == 'land':
            cdo.ifthen(input='mask/land ' + ifile, output=out)
        else:
            out = ifile

        cdo.fldmean(input='-setctomiss,0 -seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + out, output=finalout)
   
    nc = Dataset(finalout, 'r')

    data, units, depth = _load(nc, var)
    nc_time = nc.variables['time']
    try:
        cal = nc_time.calendar
    except:
        cal = 'standard'
    x = num2date(nc_time[:], nc_time.units, cal)
    x = [datetime.datetime(*item.timetuple()[:6]) for item in x]
    x = np.array(x)

    depth = np.round(depth)
    units = _scale_units(units, scale)
    data = data * scale
    return data, units, x, depth


def timeseries_load_comp(ifile, var, dates, depthneeded, scale):
    """ Loads the field mean data over specified dates from a file.
        Remaps and scales the data.

    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    dates : dictionary
            maps 'start_date' and 'end_date' to date string with formay 'yyyy-mm'
    scale : int
            scale the data by this factor

    Returns
    -------
    numpy array
    string
    numpy array
    numpy array
    """
    depthneeded = ["%.2f" % number for number in depthneeded]
    for i in xrange(len(depthneeded)):
        depthneeded[i] = str(depthneeded[i])
    depthneededstr = ','.join(depthneeded)
    
    _check_dates(ifile, dates)
    path, sfile = os.path.split(ifile)
    finalout = 'fldmeanfiles/fldmean_' + sfile + str(dates['start_date']) + str(dates['end_date']) + '.nc'
    if not os.path.isfile(finalout):
        out = 'fldmeanfiles/selvar.nc'
        cdo.selvar(var, input=ifile, output=out)
        cdo.fldmean(options='-L', input='-seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + out, output=finalout)
    try:
        cdo.intlevelx(str(depthneededstr), input=finalout, output=finalout + str(depthneeded[0]) + '.nc')
        nc = Dataset(finalout + str(depthneeded[0]) + '.nc', 'r')
    except:
        nc = Dataset(finalout, 'r')

    data, units, depth = _load(nc, var)
    nc_time = nc.variables['time']
    try:
        cal = nc_time.calendar
    except:
        cal = 'standard'
    x = num2date(nc_time[:], nc_time.units, cal)
    x = [datetime.datetime(*item.timetuple()[:6]) for item in x]
    x = np.array(x)

    depth = np.round(depth)
    units = _scale_units(units, scale)
    data = data * scale
    return data, units, x, depth


def zonal_load(ifile, var, dates, realm, scale):
    """ Loads the zonal mean data over specified dates from a file.
        Remaps and scales the data.

    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    dates : dictionary
            maps 'start_date' and 'end_date' to date string with formay 'yyyy-mm'
    depthneeded : numpy array
    scale : int
            scale the data by this factor

    Returns
    -------
    numpy array
    string
    numpy array
    numpy array
    """
    _check_dates(ifile, dates)    
    path, sfile = os.path.split(ifile)

    finalout = 'zonalfiles/zonmean_' + sfile + str(dates['start_date']) + str(dates['end_date']) + '.nc'
    if not os.path.isfile(finalout):
        out = 'zonalfiles/zonmean.nc'
        if realm == 'ocean':
            cdo.ifthen(input='mask/ocean ' + ifile, output=out)
        elif realm == 'land':
            cdo.ifthen(input='mask/land ' + ifile, output=out)
        else:
            out = ifile
        cdo.zonmean(options='-L', input='-timmean -setctomiss,0 -seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + out, output=finalout)
    nc = Dataset(finalout, 'r')
    
    data, units, depth = _load(nc, var)
    x = nc.variables['lat'][:].squeeze()

    depth = np.round(depth)
    units = _scale_units(units, scale)
    data = data * scale
    return data, units, x, depth


def zonal_load_comp(ifile, var, dates, depthneeded, scale):
    """ Loads the zonal mean data over specified dates from a file.
        Remaps and scales the data.

    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    dates : dictionary
            maps 'start_date' and 'end_date' to date string with formay 'yyyy-mm'
    scale : int
            scale the data by this factor

    Returns
    -------
    numpy array
    string
    numpy array
    numpy array
    """
    depthneeded = ["%.2f" % number for number in depthneeded]
    for i in xrange(len(depthneeded)):
        depthneeded[i] = str(depthneeded[i])
    depthneededstr = ','.join(depthneeded)
    
    _check_dates(ifile, dates)    
    path, sfile = os.path.split(ifile)
    finalout = 'zonalfiles/zonmean_' + sfile + str(dates['start_date']) + str(dates['end_date']) + '.nc'

    if not os.path.isfile(finalout):
        out = 'zonalfiles/selvar.nc'
        cdo.selvar(var, input=ifile, output=out)
        out2 = 'zonalfiles/selvarremap.nc'
        cdo.remapdis('r360x180', input=out, output=out2)
        cdo.zonmean(options='-L', input='-timmean -seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + out2, output=finalout)
    try:
        cdo.intlevelx(str(depthneededstr), input=finalout, output=finalout + str(depthneeded[0]) + '.nc')
        nc = Dataset(finalout + str(depthneeded[0]) + '.nc', 'r')
    except:
        nc = Dataset(finalout, 'r')

    data, units, depth = _load(nc, var)

    x = nc.variables['lat'][:].squeeze()

    depth = np.round(depth)
    units = _scale_units(units, scale)
    data = data * scale
    return data, units, x, depth


if __name__ == "__main__":
    pass
