import os
from netCDF4 import Dataset, num2date
import cdo; cdo = cdo.Cdo()
import numpy as np
import datetime


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
       
def _load(nc, var, depth_type):
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
    if depth_type != "":
        try:
            for dimension in ncvar.dimensions:
                if depth_type in dimension.lower():
                    depth = nc.variables[dimension][:]
                    break
        except:
            depth = [0]
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
    data = data*scale    
    return data, lon, lat, depth, units
    
def timeaverage_load(ifile, var, depth_type, dates, realm, scale):
    """ Loads the data from a file and remaps it.
        Applies a time average over specified dates and scales the data.
        
    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    depth_type : string
                 the name the depth is labelled as in the file
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
    path, ifile = os.path.split(ifile)
    if dates:
        if not os.path.isfile('remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc'):
            out='remapfiles/remapfile.nc'
            if realm == 'ocean':
                cdo.mul(input='-divc,100 mask/ocean ' + path + '/' + ifile, output=out)
            elif realm == 'land':
                cdo.mul(input='-divc,100 mask/land ' + path + '/' + ifile, output=out)
            else:
                out = path + '/' + ifile
            cdo.remapdis('r360x180', input='-setctomiss,0 -timmean -seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + out, output='remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc')
        nc = Dataset('remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', 'r')
    else:
        if not os.path.isfile('remapfiles/remap_' + ifile):
            cdo.remapdis('r360x180', input='-timmean ' + path + '/' + ifile, output='remapfiles/remap_' + ifile)
        nc = Dataset('remapfiles/remap_' + ifile, 'r')
    
    data, units, depth = _load(nc, var, depth_type)    
    
    data, lon, lat, depth, units = _load2(data, nc, units, depth, scale)

    return data, units, lon, lat, depth

def timeaverage_load_comp(ifile, var, depth_type, dates, realm, depthneeded, scale):
    """ Loads the data from a file and remaps it to 360x180.
        Also remaps the vertical axis to specified depths for easy comparison
        Applies a time average over specified dates and scales the data.
        
    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    depth_type : string
                 the name the depth is labelled as in the file
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
    path, ifile = os.path.split(ifile)

    if dates:
        if not os.path.isfile('remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc'):
            cdo.selvar(var, input=path + '/' + ifile, output='remapfiles/selvar.nc')
            out='remapfiles/selvar.nc'
            cdo.remapdis('r360x180', options='-L', input='-setctomiss,0 -timmean -seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + out, output='remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc')
        try:    
            cdo.intlevelx(str(depthneededstr), input='remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', output='remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + str(depthneeded[0]) + '.nc')
            nc = Dataset('remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + str(depthneeded[0]) + '.nc', 'r')
        except:
            nc = Dataset('remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', 'r')
    else:
        if not os.path.isfile('remapfiles/remap_' + ifile):
            cdo.selvar(var, input=path + '/' + ifile, output='remapfiles/selvar.nc')
            out='remapfiles/selvar.nc'
            cdo.remapdis('r360x180', input='-timmean ' + 'remapfiles/selvar.nc', output='remapfiles/remap_' + ifile)
            try:
                cdo.intlevelx(str(depthneeded) + ',10000', input='remapfiles/remap_' + ifile, output='remapfiles/remap_' + ifile + str(depthneeded) + '.nc')
                nc = Dataset('remapfiles/remap_' + ifile + str(depthneeded) + '.nc', 'r')
            except:
                nc = Dataset('remapfiles/remap_' + ifile, 'r')          

    data, units, depth = _load(nc, var, 'level') 
    data, lon, lat, depth, units = _load2(data, nc, units, depth, scale)
    return data, units, lon, lat, depth    

def trends_load(ifile, var, depth_type, dates, scale):
    """ Loads the trend data over specified dates from a file 
        Remaps and scales the data.
        
    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    depth_type : string
                 the name the depth is labelled as in the file
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
    path, ifile = os.path.split(ifile)
    if dates:   
        if not os.path.isfile('trendfiles/slope_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc'):
            cdo.trend(input='-seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + path + '/' + ifile, 
                      output='trendfiles/intercept_' + ifile + ' trendfiles/slope_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc')
            cdo.remapdis('r360x180', input='-setctomiss,0 ' + 'trendfiles/slope_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', 
                         output='trendfiles/slope_remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc')
        nc = Dataset('trendfiles/slope_remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', 'r' )
    else:
        if not os.path.isfile('trendfiles/slope_' + ifile):
            cdo.trend(input=path + '/' + ifile, 
                      output='trendfiles/intercept_' + ifile + ' trendfiles/slope_' + ifile) 
            cdo.remapdis('r360x180', input='-setctomiss,0 '
                         + 'trendfiles/slope_' + ifile, output='trendfiles/slope_remap_' + ifile) 
        nc = Dataset('trendfiles/slope_remap_' + ifile, 'r' )   
    
    data, units, depth = _load(nc, var, depth_type) 
      
    data, lon, lat, depth, units = _load2(data, nc, units, depth, scale)
    
    return data, units, lon, lat, depth    

def trends_load_comp(ifile, var, depth_type, dates, depthneeded, scale):
    """ Loads the trend data over specified dates from a file 
        Remaps and scales the data. Also remaps the vertical axis to 
        specified depths for easy comparison.
                
    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    depth_type : string
                 the name the depth is labelled as in the file
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
    
    path, ifile = os.path.split(ifile)
    if dates:   
        if not os.path.isfile('trendfiles/slope_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc'):
            cdo.selvar(var, input=path + '/' + ifile, output='trendfiles/selvar.nc')
            out='trendfiles/selvar.nc'        
            cdo.trend(input='-seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + out, 
                      output='trendfiles/intercept_' + ifile + ' trendfiles/slope_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc')
            cdo.remapdis('r360x180', options='-L', input='-setctomiss,0 ' + 'trendfiles/slope_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', 
                         output='trendfiles/slope_remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc')
        try:
            cdo.intlevelx(str(depthneededstr), input='trendfiles/slope_remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', output='trendfiles/slope_remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + str(depthneeded[0]) + '.nc')
            nc = Dataset('trendfiles/slope_remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + str(depthneeded[0]) + '.nc', 'r' )
        except:
            nc = Dataset('trendfiles/slope_remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', 'r' )
    else:
        if not os.path.isfile('trendfiles/slope_' + ifile):
            cdo.trend(input=path + '/' + ifile, 
                      output='trendfiles/intercept_' + ifile + ' trendfiles/slope_' + ifile) 
            cdo.remapdis('r360x180', input='-setctomiss,0 '
                         + 'trendfiles/slope_' + ifile, output='trendfiles/slope_remap_' + ifile) 
        nc = Dataset('trendfiles/slope_remap_' + ifile, 'r' )   
    
    data, units, depth = _load(nc, var, 'level')    
    data, lon, lat, depth, units = _load2(data, nc, units, depth, scale)
    return data, units, lon, lat, depth  

   
def timeseries_load(ifile, var, depth_type, dates, scale):
    """ Loads the field mean data over specified dates from a file.
        Remaps and scales the data. 
                
    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    depth_type : string
                 the name the depth is labelled as in the file
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
    path, ifile = os.path.split(ifile)
#    if not os.path.isfile('fldmeanfiles/fldmean_' + ifile):
#        cdo.fldmean(input=path + '/' + ifile, output='fldmeanfiles/fldmean_' + ifile)
    
    if dates:           
        if not os.path.isfile('fldmeanfiles/fldmean_' + ifile +  str(dates['start_date']) + str(dates['end_date']) + '.nc'):
            cdo.fldmean(input='-seldate,' + str(dates['start_date']) + ',' +str(dates['end_date']) + ' ' + path + '/' + ifile, output='fldmeanfiles/fldmean_'  + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc')
        nc = Dataset('fldmeanfiles/fldmean_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', 'r')
    else:
        if not os.path.isfile('fldmeanfiles/fldmean_' + ifile):
            cdo.fldmean(input=path + '/' + ifile, output='fldmeanfiles/fldmean_' + ifile)
        nc = Dataset('fldmeanfiles/fldmean_' + ifile, 'r')
   
    data, units, depth = _load(nc, var, depth_type) 
    
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
    return data*scale, units, x, depth    


def zonal_load(ifile, var, depth_type, dates, scale):
    """ Loads the zonal mean data over specified dates from a file.
        Remaps and scales the data. 
                
    Parameters
    ----------
    ifile : string
            filename to load data from
    var : string
    depth_type : string
                 the name the depth is labelled as in the file
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
    path, ifile = os.path.split(ifile)
    
    if dates:           
        if not os.path.isfile('zonalfiles/zonmean_' + ifile +  str(dates['start_date']) + str(dates['end_date']) + '.nc'):
            cdo.zonmean(input='-timmean -seldate,' + str(dates['start_date']) + ',' +str(dates['end_date']) + ' ' + path + '/' + ifile, output='zonalfiles/zonmean_'  + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc')
        nc = Dataset('zonalfiles/zonmean_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', 'r')
    else:
        if not os.path.isfile('zonalfiles/zonmean_' + ifile):
            cdo.zonmean(input='-timmean' + path + '/' + ifile, output='zonalfiles/zonmean_' + ifile)
        nc = Dataset('zonalfiles/zonmean_' + ifile, 'r')   
    data, units, depth = _load(nc, var, depth_type) 
    
    x = nc.variables['lat'][:].squeeze()

    depth = np.round(depth)
    units = _scale_units(units, scale)
    return data*scale, units, x, depth    

if __name__ == "__main__":
    ifile = '/raid/rc40/data/ncs/historical-edr/mon/atmos/ta/r1i1p1/ta_Amon_DevAM4-2_historical-edr_r1i1p1_185001-200012.nc'
    timeseries_load(ifile,'ta','plev')        
