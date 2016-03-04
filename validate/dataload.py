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
    """ Returns True if there is only one timestep in the netcdf file
    """
    nc = Dataset(ifile, 'r')
    try:
        time = nc.variables['time'][:].squeeze()
    except:
        return True
    return time.size == 1


def year_mon_day(datestring):
    """ Seperates a string of from yyyy-mm-dd in to
        three integers and returns the tuple year,mon,day
    """
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
    """ Checks if the comparison data is outside of the dates for the plot
        Returns True if the dates of the data are completely outside of the
        desired dates.
        Returns False if the dates overlap at all, but prints a warning if 
        it is only a subset.
    """
    # Load data from file into Dataset object
    nc = Dataset(ifile, 'r')
    
    nc_time = nc.variables['time']
    try:
        cal = nc_time.calendar
    except:
        cal = 'standard'
    
    # convert dates to datetime object
    start = datetime.datetime(*year_mon_day(start_date))
    end = datetime.datetime(*year_mon_day(end_date))
    print start
    print end
    print nc_time.units
    print cal
    # convert datetime objects to integers
    start = date2num(start, nc_time.units, calendar=cal)
    end = date2num(end, nc_time.units, calendar=cal)
    
    # get start and end dates of file
    compstart = nc_time[:][0]
    compend = nc_time[:][-1]
    
    # make comparison
    if compstart > end or compend < start:
        return True
    elif compstart > start or compend < end:
        with open('logs/log.txt', 'a') as outfile:
            outfile.write('WARNING: Comparison data does not cover entire time period... Used subset\n')
    return False


def _check_dates(ifile, dates):
    """ Prints warnings or raises exception if the desired dates
        are not within the date bounds of the file.
    """
    try:
        if _check_averaged(ifile):
            with open('logs/log.txt', 'a') as outfile:
                outfile.write('WARNING: Comparison data is time averaged\n')
            return True
        elif _check_dates_outside(ifile, **dates):
            with open('logs/log.txt', 'a') as outfile:
                outfile.write('WARNING: Comparison data is not from time period\n')
            raise Exception
        return False
    except:
        with open('logs/log.txt', 'a') as outfile:
            outfile.write('WARNING: Comparison data time period could not be checked\n') 
        return False       


def _scale_units(units, scale, shift):
    """ Corrects the units to match the scale applied to the data

    Parameters
    ----------
    units : string
    scale : int

    Returns
    -------
    string
    """
    if shift < 0:
        units = '(' + units + ' - ' + str(abs(shift)) + ')'
    if shift > 0:
        units = '(' + units + ' + ' + str(shift) + ')'   
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
        # try to load the data for the variable
        ncvar = nc.variables[var]
    except:
        # try again with the uppercase variable
        # should almost never go here
        varu = var.upper()
        ncvar = nc.variable[varu]
    
    data = ncvar[:].squeeze()

    try:
        units = ncvar.units
    except:
        units = ''

    depth = [0]
    
    # find the name of the z-axis variable and load the depth data if it exists
    for dimension in ncvar.dimensions:
        try:
            if nc.variables[dimension].axis == 'Z':
                depth = nc.variables[dimension][:]
                break
        except:
            # keep looping if the dimension doen't have an 'axis' attribute
            pass

    return data, units, depth


def _load2(data, nc, units, depth, scale, shift):
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
    try:
        lon = nc.variables['lon'][:].squeeze()
    except:
        lon = None
    try:
        lat = nc.variables['lat'][:].squeeze()
    except:
        lat = None
    depth = np.round(depth)
    units = _scale_units(units, scale, shift)
    data = (data + shift) * scale
    return data, lon, lat, depth, units


def timeaverage_load(ifile, var, dates, realm, scale, shift, remapf='remapdis', remapgrid='r360x180', depthneeded=None, seasons=None):
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
    averaged = _check_dates(ifile, dates)
    if var == 'msftmyz':
        finalout = remap(setc(time_mean(season(sel_var(ifile, var), seasons), dates['start_date'], dates['end_date'], averaged), realm), remapf, remapgrid) 
    elif depthneeded is not None: # use is not because the truth value of an array is ambiguous
        finalout = intlevel(remap(setc(time_mean(season(sel_var(ifile, var), seasons), dates['start_date'], dates['end_date'], averaged), realm), remapf, remapgrid), depthneeded)
    else:
        finalout = remap(setc(time_mean(mask(season(sel_var(ifile, var), seasons), realm), dates['start_date'], dates['end_date'], averaged), realm), remapf, remapgrid)
    
    # load data from final netcdf file into Dataset object
    nc = Dataset(finalout, 'r')

    # extract relevent information from Dataset object
    data, units, depth = _load(nc, var)
    data, lon, lat, depth, units = _load2(data, nc, units, depth, scale, shift)

    return data, units, lon, lat, depth


def trends_load(ifile, var, dates, scale, shift, remapf='remapdis', remapgrid='r360x180', depthneeded=None, seasons=None):
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

    if depthneeded is not None:
        finalout = intlevel(setc(remap(trend(season(sel_var(ifile, var), seasons), dates['start_date'], dates['end_date']), remapf, remapgrid)), depthneeded)   
    else:
        finalout = setc(remap(trend(season(sel_var(ifile, var), seasons), dates['start_date'], dates['end_date']), remapf, remapgrid))
    
    # load data from final netcdf file into Dataset object
    nc = Dataset(finalout, 'r')

    # Extract relevent information from Dataset object
    data, units, depth = _load(nc, var)
    data, lon, lat, depth, units = _load2(data, nc, units, depth, scale, shift)

    return data, units, lon, lat, depth

def full_load(ifile, var, dates, realm, scale, shift, remapf='remapdis', remapgrid='r360x180', depthneeded=None, seasons=None):

    averaged = _check_dates(ifile, dates)
    
    if depthneeded is not None:
        finalout = intlevel(setc(remap(sel_date(season(sel_var(ifile, var), seasons), dates['start_date'], dates['end_date'], averaged), remapf, remapgrid)), depthneeded)
    else:
        finalout = setc(remap(sel_date(mask(season(sel_var(ifile, var), seasons), realm), dates['start_date'], dates['end_date'], averaged), remapf, remapgrid))
    
    nc = Dataset(finalout, 'r')
    data, units, depth = _load(nc, var)
    return data

def full_detrend(ifile, var, dates, realm, scale, shift, remapf='remapdis', remapgrid='r360x180', depthneeded=None, seasons=None):
    if depthneeded is not None:
        pass
    else:
        finalout = setc(remap(detrend(season(sel_var(ifile, var), seasons), dates['start_date'], dates['end_date']), remapf, remapgrid))
    
    nc = Dataset(finalout, 'r')
    data, units, depth = _load(nc, var)
    data = (data + shift) * scale
    return data

def timeseries_load(ifile, var, dates, realm, scale, shift, depthneeded=None, seasons=None, cdostring=None):
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
    if cdostring:
        finalout = cdos(ifile, cdostring)
    elif depthneeded is not None:
        finalout = intlevel(setc(field_mean(season(cdos(sel_var(ifile, var), cdostring), seasons), dates['start_date'], dates['end_date'])), depthneeded)
    else:
        finalout = setc(field_mean(mask(season(cdos(sel_var(ifile, var), cdostring), seasons), realm), dates['start_date'], dates['end_date']))    

    # Load data into Dataset object
    nc = Dataset(finalout, 'r')

    # Get the time data from the dataset object
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
    units = _scale_units(units, scale, shift)
    data = (data + shift) * scale
    return data, units, x, depth

def histogram_load(ifile, var, dates, realm, scale, shift, remapf='remapdis', remapgrid='r360x180', trends=False, depthneeded=None, seasons=None):
    
    _check_dates(ifile, dates)

    if trends:
        if depthneeded is not None:
            finalout = intlevel(field_mean(remap(trend(setc(season(sel_var(ifile, var), seasons)), dates['start_date'], dates['end_date']), remapf, remapgrid), dates['start_date'], dates['end_date']), depthneeded)    
        else:
            finalout = field_mean(remap(trend(setc(mask(season(sel_var(ifile, var), seasons), realm)), dates['start_date'], dates['end_date']), remapf, remapgrid), dates['start_date'], dates['end_date'])   
    else:
        if depthneeded is not None:
            finalout = intlevel(field_mean(remap(time_mean(setc(season(sel_var(ifile, var), seasons)), dates['start_date'], dates['end_date']), remapf, remapgrid)), depthneeded)    
        else:
            finalout = field_mean(remap(time_mean(setc(mask(season(sel_var(ifile, var), seasons), realm)), dates['start_date'], dates['end_date']), remapf, remapgrid))

    # Load data into Dataset object
    nc = Dataset(finalout, 'r')

    # Get the time data from the dataset object
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
    units = _scale_units(units, scale, shift)
    data = (data + shift) * scale
    return data, units, x, depth

def full_section_load(ifile, var, dates, realm, scale, shift, remapf='remapdis', remapgrid='r360x180', depthneeded=None, seasons=None):
    averaged = _check_dates(ifile, dates)
    if depthneeded is not None:
        finalout = intlevel(zonal_mean(remap(sel_date(setc(season(sel_var(ifile, var), seasons)), dates['start_date'], dates['end_date'], averaged), remapf, remapgrid)), depthneeded)    
    else:
        finalout = zonal_mean(remap(sel_date(setc(mask(season(sel_var(ifile, var), seasons), realm)), dates['start_date'], dates['end_date'], averaged), remapf, remapgrid))
 
    nc = Dataset(finalout, 'r')
    data, units, depth = _load(nc, var)
    return data
        
def zonal_load(ifile, var, dates, realm, scale, shift, remapf='remapdis', remapgrid='r360x180', trends=False, depthneeded=None, seasons=None):
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
    averaged = _check_dates(ifile, dates)  
    
    if trends:
        if depthneeded is not None:
            finalout = intlevel(zonal_mean(remap(trend(setc(season(sel_var(ifile, var)), seasons), dates['start_date'], dates['end_date']), remapf, remapgrid)), depthneeded)    
        else:
            finalout = zonal_mean(remap(trend(setc(mask(season(sel_var(ifile, var), seasons), realm)), dates['start_date'], dates['end_date']), remapf, remapgrid))   
    else:
        if depthneeded is not None:
            finalout = intlevel(zonal_mean(remap(time_mean(setc(season(sel_var(ifile, var), seasons)), dates['start_date'], dates['end_date'], averaged), remapf, remapgrid)), depthneeded)    
        else:
            finalout = zonal_mean(remap(time_mean(setc(mask(season(sel_var(ifile, var), seasons), realm)), dates['start_date'], dates['end_date'], averaged), remapf, remapgrid))
    
    nc = Dataset(finalout, 'r')

    # extract relevent data
    data, units, depth = _load(nc, var)
    x = nc.variables['lat'][:].squeeze()

    depth = np.round(depth)
    units = _scale_units(units, scale, shift)
    data = (data + shift) * scale
    return data, units, x, depth

def split(name):
    """ Returns the name of a file without the directory path
    """
    path, filename = os.path.split(name)
    return filename

def sel_date(name, start_date, end_date, time_average=False):
    if time_average:
        return name
    out = 'netcdf/seldate_' + start_date + '_' + end_date + '_' + split(name)
    if not os.path.isfile(out):
        datestring = start_date + ',' + end_date
        cdo.seldate(datestring, input=name, output=out)
    return out
    
def sel_var(name, variable):
    out = 'netcdf/sel_' + split(name)
    if not os.path.isfile(out):
        cdo.selvar(variable, input=name, output=out) 
    return out

def mask(name, realm):
    out = 'netcdf/masked_' + split(name)
    if not os.path.isfile(out):
        if realm == 'ocean':
            try:
                cdo.ifthen(input='mask/ocean ' + name, output=out)
            except:
                with open('logs/log.txt', 'a') as outfile:
                    outfile.write('WARNING: Land data was not masked\n')
                return name             
        elif realm == 'land':
            try:
                cdo.ifthen(input='mask/land ' + name, output=out) 
            except:
                with open('logs/log.txt', 'a') as outfile:
                    outfile.write('WARNING: Ocean data was not masked\n')
                return name 
        else:
            out = name
    return out

def time_mean(name, start_date, end_date, time_average=False):
    if time_average:
       return name
    out = 'netcdf/climate_' + start_date + '_' + end_date + '_' + split(name)
    if not os.path.isfile(out):
        seldatestring = '-seldate,' + start_date + ',' + end_date
        cdo.timmean(input=seldatestring + ' ' + name, output=out)
    return out  

def trend(name, start_date, end_date):
    out = 'netcdf/slope_' + start_date + '_' + end_date + '_' + split(name)
    outintercept = 'netcdf/intercept_' + start_date + '_' + end_date + '_' + split(name)
    if not os.path.isfile(out):
        seldatestring = '-seldate,' + start_date + ',' + end_date
        cdo.trend(input=seldatestring + ' ' + name, output=outintercept + ' ' + out)
    return out

def detrend(name, start_date, end_date):
    out = 'netcdf/detrend_' + start_date + '_' + end_date + '_' + split(name)
    if not os.path.isfile(out):
        seldatestring = '-seldate,' + start_date + ',' + end_date
        cdo.detrend(input=seldatestring + ' ' + name, output=out)
    return out    

def setc(name, realm='ocean'):
    if realm == 'atmos':
#        cdo.setmisstoc(0, input=name, output=out)
        return name
    out = 'netcdf/setc_' + split(name)
    if not os.path.isfile(out):
        cdo.setctomiss(0, input=name, output=out)
    return out

def get_remap_function(remap):
    """ Returns a cdo function from string of the same name.
    """
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

def remap(name, remapname, remapgrid):
    out = 'netcdf/' + remapname + '-' + remapgrid + split(name)
    if not os.path.isfile(out):
        remap = get_remap_function(remapname)
        try:
            remap(remapgrid, input=name, output=out)
        except:
            return name
    return out

def field_mean(name, start_date, end_date):
    out = 'netcdf/fldmean_' + start_date + '_' + end_date + '_' + split(name)
    if not os.path.isfile(out):
        seldatestring = '-seldate,' + start_date + ',' + end_date
        cdo.fldmean(options='-L', input=seldatestring + ' ' + name, output=out)
    return out

def zonal_mean(name):
    out = 'netcdf/zonmean_' + split(name)
    if not os.path.isfile(out):
        cdo.zonmean(input=name, output=out)
    return out
    
def depthstring(depthlist):
    depthneeded = ["%.2f" % number for number in depthlist]
    for i in xrange(len(depthneeded)):
        depthneeded[i] = str(depthneeded[i])
    return ','.join(depthneeded)
    
       
def intlevel(name, depthlist):
    if depthlist == None or depthlist == [] or depthlist == [""] or depthlist == [None]:
        return name
    depth = depthstring(depthlist)
    depthname = depth.replace(' ', '')
    if len(depthname) > 100:
        depthname = depthname[:99]
    out = 'netcdf/level-' + str(depthname) + '_' + split(name)
    if depth:
        if not os.path.isfile(out):
            try:
                cdo.intlevelx(str(depth), input=name, output=out)
            except:
                return name
    else:
        return name
    return out        
   
def season(name, seasonlist):
    if seasonlist == None or seasonlist == ['DJF', 'MAM', 'JJA', 'SON']:
        return name
    seasonstring = ','.join(seasonlist)
    outputstring = ''.join(seasonlist)
    out = 'netcdf/selseason-' + outputstring + '_' + split(name)
    if not os.path.isfile(out):
        cdo.selseas(seasonstring, input=name, output=out)
    return out

def cdos(name, string):
    if string:
        out = 'netcdf/cdo_' + split(name)
        if not os.path.isfile(out):
            s = 'cdo ' + string + ' ' + name + ' ' + out
            os.system(s)
        return out
    return name

if __name__ == "__main__":
    pass
