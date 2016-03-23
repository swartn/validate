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
from .functions import external
import cdo
cdo = cdo.Cdo()

preprocessed_data_root = ''

def silent_remove(name):
    try: 
        os.remove(name)
    except OSError:
        pass

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


def _ncvar(ds, var):
    try:
        ncvar = ds.variables[var]
    except:
        varu = var.upper()
        ncvar = ds.variables[varu]
    return ncvar

def _units(ncvar, scale, shift):
    try:
        units = ncvar.units
    except:
        units = ''

    if shift < 0:
        units = '(' + units + ' - ' + str(abs(shift)) + ')'
    if shift > 0:
        units = '(' + units + ' + ' + str(shift) + ')'   
    if scale != 1:
        units = units + ' * ' + str(scale)
       
    return units

def _depth(ds, ncvar):
    for dimension in ncvar.dimensions:
        try:
            if ds.variables[dimension].axis == 'Z':
                depth = ds.variables[dimension][:]
                break
        except:
            # keep looping if the dimension doen't have an 'axis' attribute
            pass
    else:
        depth = [0]
    return np.round(depth)

def _lon_lat(ds):
    try:
        lon = ds.variables['lon'][:].squeeze()
    except:
        try:
            lon = ds.variables['x'][:].squeeze()
        except:
            lon = None
    try:
        lat = ds.variables['lat'][:].squeeze()
    except:
        try:
            lat = ds.variables['y'][:].squeeze()
        except:
            lat = None
    return lon, lat


def _time(ds):
    nc_time = ds.variables['time']
    try:
        cal = nc_time.calendar
    except:
        cal = 'standard'
    try:
        x = num2date(nc_time[:], nc_time.units, cal)
        x = [datetime.datetime(*item.timetuple()[:6]) for item in x]
        x = np.array(x)
    except:
        x = None
    return x

def get_external_function(name):
    def external_functions(function_name):
        return {'sample': external.sample,
               }[function_name]
    return external_functions(name)
    
def dataload(ifile, var, dates, realm='atmos', scale=1, shift=0, 
             remapf='remapdis', remapgrid='r360x180', seasons=None,
             datatype='full', depthneeded=None, section=False, fieldmean=False, gridweights=False,
             cdostring=None, external_function=None, external_function_args={}):

    time_averaged_bool = _check_dates(ifile, dates)
    
    sel_var_file = sel_var(ifile, var)
    masked_file = mask(sel_var_file, realm)
    c_file = setc(masked_file, realm)
    
    if cdostring is not None:
        c_file = cdos(c_file, cdostring)

    remapped_file = remap(c_file, remapf, remapgrid)
    seasonal_file = season(remapped_file, seasons)
    ofile = sel_date(seasonal_file, dates['start_date'], dates['end_date'], time_averaged_bool)

    if external_function is not None:
        ofile = get_external_function(external_function)(ofile, **external_function_args)        
            
    if datatype == 'climatology':
        ofile = time_mean(ofile, time_averaged_bool)
    elif datatype == 'trends':
        ofile = trend(ofile)
    elif datatype == 'detrend':
        ofile = detrend(ofile)
    
    if depthneeded:
        ofile = intlevel(ofile, depthneeded)
    
    if section:
        ofile = zonal_mean(ofile)

    if fieldmean:
        ofile = field_mean(ofile)
    


    dataset = Dataset(ofile, 'r')
    ncvar = _ncvar(dataset, var)
    rawdata = ncvar[:].squeeze()
    data = (rawdata + shift) * scale
    units = _units(ncvar, scale, shift)
    depth = _depth(dataset, ncvar)
    lon, lat = _lon_lat(dataset)
    time = _time(dataset)

    if gridweights:
        gfile = grid_weights(ofile)    
        gdataset = Dataset(gfile, 'r')
        gncvar = _ncvar(gdataset, 'cell_weights')
        weights = gncvar[:].squeeze()
    else:
        weights = None
    return data, lon, lat, depth, units, time, weights


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
                silent_remove(out)
                return name
        elif realm == 'land':
            try:
                cdo.ifthen(input='mask/land ' + name, output=out) 
            except:
                with open('logs/log.txt', 'a') as outfile:
                    outfile.write('WARNING: Ocean data was not masked\n')
                silent_remove(out)
                return name
        else:
            out = name
    return out

def time_mean(name, time_average=False):
    if time_average:
       return name
    out = 'netcdf/climate_' + split(name)
    if not os.path.isfile(out):
        cdo.timmean(input=name, output=out)
    return out  

def trend(name):
    out = 'netcdf/slope_' + split(name)
    outintercept = 'netcdf/intercept_' + split(name)
    if not os.path.isfile(out):
        cdo.trend(input=name, output=outintercept + ' ' + out)
    return out

def detrend(name):
    out = 'netcdf/detrend_' + split(name)
    if not os.path.isfile(out):
        cdo.detrend(input=name, output=out)
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
    out = 'netcdf/' + remapname + '-' + remapgrid + '_' + split(name)
    if not os.path.isfile(out):
        remap = get_remap_function(remapname)
        try:
            remap(remapgrid, input=name, output=out)
        except:
            try:
                os.remove(out)
            except:
                pass
            return name
    return out

def field_mean(name):
    out = 'netcdf/fldmean_' + split(name)
    if not os.path.isfile(out):
        cdo.fldmean(input=name, output=out)
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

def grid_weights(name):
    out = 'netcdf/gridweights_' + split(name)
    if not os.path.isfile(out):
        cdo.gridweights(input=name, output=out)
    return out

def already_calculated(name):
    if os.path.isfile(name):
        return name
    precalc = preprocessed_data_root + '/' + split(name)
    if os.path.isfile(precalc):
        return precalc
    return None
    
if __name__ == "__main__":
    pass
