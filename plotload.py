import os
from netCDF4 import Dataset, num2date
import cdo; cdo = cdo.Cdo()
import numpy as np
import datetime

def timeaverage_load(ifile, var, depth_type, dates, realm):

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
    
    #lon = np.linspace(0,359, 360)
    #lat = np.linspace(-90,90,180)
    lon = nc.variables['lon'][:].squeeze()
    lat = nc.variables['lat'][:].squeeze()
    depth = np.round(depth)
    return data, units, lon, lat, depth

def timeaverage_load_comp(ifile, var, depth_type, dates, realm):

    path, ifile = os.path.split(ifile)

    if dates:
        if not os.path.isfile('remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc'):
            cdo.selvar(var, input=path + '/' + ifile, output='remapfiles/selvar.nc')
            out='remapfiles/selvar.nc'
            cdo.remapdis('r360x180', input='-setctomiss,0 -timmean -seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + out, output='remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc')
        nc = Dataset('remapfiles/remap_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', 'r')
    else:
        if not os.path.isfile('remapfiles/remap_' + ifile):
            cdo.selvar(var, input=path + '/' + ifile, output='remapfiles/selvar.nc')
            out='remapfiles/selvar.nc'
            cdo.remapdis('r360x180', input='-timmean ' + 'remapfiles/selvar.nc', output='remapfiles/remap_' + ifile)
        nc = Dataset('remapfiles/remap_' + ifile, 'r')
    
    
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
    
    #lon = np.linspace(0,359, 360)
    #lat = np.linspace(-90,90,180)
    lon = nc.variables['lon'][:].squeeze()
    lat = nc.variables['lat'][:].squeeze()
    depth = np.round(depth)
    return data, units, lon, lat, depth    
def trends_load(ifile, var, depth_type, dates):
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
    
    ncvar = nc.variables[var]
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
    #lon = np.linspace(0, 359, 360)
    #lat = np.linspace(-90,90,180)
    lon = nc.variables['lon'][:].squeeze()
    lat = nc.variables['lat'][:].squeeze()

    depth = np.round(depth)
    return data, units, lon, lat, depth    
    
def timeseries_load(ifile, var, depth_type, dates):
    path, ifile = os.path.split(ifile)
    if not os.path.isfile('fldmeanfiles/fldmean_' + ifile):
        cdo.fldmean(input=path + '/' + ifile, output='fldmeanfiles/fldmean_' + ifile)
    
    if dates:           
        if not os.path.isfile('fldmeanfiles/fldmean_' + ifile +  str(dates['start_date']) + str(dates['end_date']) + '.nc'):
            cdo.fldmean(input='-seldate,' + str(dates['start_date']) + ',' +str(dates['end_date']) + ' ' + path + '/' + ifile, output='fldmeanfiles/fldmean_'  + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc')
        nc = Dataset('fldmeanfiles/fldmean_' + ifile + str(dates['start_date']) + str(dates['end_date']) + '.nc', 'r')
    else:
        if not os.path.isfile('fldmeanfiles/fldmean_' + ifile):
            cdo.fldmean(input=path + '/' + ifile, output='fldmeanfiles/fldmean_' + ifile)
        nc = Dataset('fldmeanfiles/fldmean_' + ifile, 'r')

    

   
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
    
    nc_time = nc.variables['time']
    try: 
        cal = nc_time.calendar
    except:
        cal = 'standard'
    x = num2date(nc_time[:], nc_time.units, cal)
    x = [datetime.datetime(*item.timetuple()[:6]) for item in x]
    x = np.array(x)

    depth = np.round(depth)
    return data, units, x, depth    

if __name__ == "__main__":
    ifile = '/raid/rc40/data/ncs/historical-edr/mon/atmos/ta/r1i1p1/ta_Amon_DevAM4-2_historical-edr_r1i1p1_185001-200012.nc'
    timeseries_load(ifile,'ta','plev')        
