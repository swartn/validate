import os
from netCDF4 import Dataset
import cdo; cdo = cdo.Cdo()
import numpy as np

def timeaverage_load(ifile, var):

    path, ifile = os.path.split(ifile)
    if not os.path.isfile('remapfiles/remap_' + ifile):
        print ifile
        cdo.remapdis('r360x180', input='-timmean '
                     + path + '/' + ifile, output='remapfiles/remap_' + ifile)

    
    nc = Dataset('remapfiles/remap_' + ifile, 'r' )
    
    #for key in nc.variables:
        #print '<<' + key + '>>'
    try:
        ncvar = nc.variables[var]

    except:
        varu = var.upper()
        #print '-----------'
        #print '>>' + varu +'<<'
        #print '---------'
        ncvar = nc.variable[varu]
    data = ncvar[:].squeeze()

    try:
        units = ncvar.units
    except:
        units = ''

    try:
        for dimension in ncvar.dimensions:
            #print dimension
            if 'lev' in dimension.lower():
                depth = nc.variables[dimension][:]
                break             
            else:
                depth = [0]
    except:
        depth = [0]

    
    lon = np.linspace(0, 360, 360)
    lat = np.linspace(-90,90,180)
    #print lon
    #print lon.shape
    #print lat
    #print lat.shape
    #print data.shape
    #print depth
    #print 'SHAPE__________________________________________'

    return data, units, lon, lat, depth
    
def trends_load(ifile, var, dates):
    path, ifile = os.path.split(ifile)   
    
    if not os.path.isfile('trendfiles/slope_' + ifile):
        if dates:
            cdo.trend(input='-seldate,' + str(dates['start_date']) + ',' + str(dates['end_date']) + ' ' + path + '/' + ifile, 
                      output='trendfiles/intercept_' + ifile + ' trendfiles/slope_' + ifile)
        else:
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
        
    try:
        for dimension in ncvar.dimensions:
            if 'depth' in dimension.lower():
                    depth = nc.variables[dimension][:]
                    break
            else:
                depth = [0]
    except:
        depth = [0]
    #print data.shape      
    lon = np.linspace(0, 360, 360)
    lat = np.linspace(-90,90,180)
    #print lon
    #print lon.shape
    #print lat
    #print lat.shape
    #print data.shape
    #for n in data[0][0]:
        #print n
    #print 'DDDAAATTTAAA2'
    #for n in data[0][2]:
        #print n
    #print 'SHAPE__________________________________________'
    return data, units, lon, lat, depth            
