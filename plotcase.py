"""
plotcase
===============

.. moduleauthor:: David Fallis
"""

import plotload as pl
import plotregions as pr
import numpy as np
import matplotlib.pyplot as plt
import defaults as dft
import datetime

def _depth_data(data, depth, plot):
    """ Makes a numpy array only containing data at the desired depth
    
    Parameters
    ----------
    data : numpy array
    depth : numpy array
            the depth needed
    plot : dictionary
    
    Returns
    -------
    dictionary
    """
    print type(depth)
    if data.ndim > 2:
        plot['plot_depth'] = min(depth, key=lambda x:abs(x-plot['depth']))
        try:
            depth_ind = np.where(np.round(depth) == np.round(plot['plot_depth']))[0][0]
        except:
            print('Failed to extract depth ' +  plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data = data[depth_ind, :, :] 
    return data

def _section_data(data, plot):
    """ Averages the data for each latitude
    
    Parameters
    ----------
    data : numpy array
    plot : dictionary
    
    Returns
    -------
    numpy array
    """
    try:
        if data.ndim == 3:
            zonmean = data.mean(axis=2)
        elif data.ndim == 2:
            zonmean = data.mean(axis=1)
    except:
        print 'proc_plot cannot zonal mean for section ' + plot['ifile'] + ' ' + plot['variable']
        return data
    return zonmean

def map_climatology(plot, func):
    """ Loads and plots the data for a time averaged map
    
    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map
    
    Returns
    -------
    string : name of the plot
    """
    print 'plotting map of ' + plot['variable']
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['realm_cat'], plot['scale'])
    plot['plot_depth'] = 0
    
    data = _depth_data(data, depth, plot)   
    
    plot = dft.filltitle(plot, 'Climatology', 'data1', str(plot['plot_depth']))    
    func(lon, lat, data, ax_args=plot['data1_args']['climatology_args']['ax_args'],
         pcolor_args=plot['data1_args']['climatology_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
                  
    plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_climatology' + str(plot['plot_depth']) + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name    

def map_climatology_comparison(plot, func):
    """ Loads and plots the data for a time averaged map.
        Loads and plots the data for comparison and plots the 
        difference between the data and the comparison data.
    
    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map
    
    Returns
    -------
    string : name of the plot
    """
    print 'plotting comparison map of ' + plot['variable']
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['realm_cat'], plot['scale'])
    plot['plot_depth'] = 0 
    data = _depth_data(data, depth, plot)
    
    data2, units, lon, lat, depth = pl.timeaverage_load_comp(plot['comp_file'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['realm_cat'], [plot['plot_depth']], plot['scale']) 
    
    data2 = _depth_data(data2, depth, plot)
  
    compdata = data - data2    
    fig, (axl, axm, axr) = plt.subplots(3,1, figsize=(8,8))        
    
    plot = dft.filltitle(plot, 'Climatology', 'data1', str(plot['plot_depth']))
    plot = dft.filltitle(plot, 'Climatology Observations', 'data2', str(plot['plot_depth'])) 
    plot = dft.filltitle(plot, 'Climatology Model - Obs', 'comp', str(plot['plot_depth']))  
         
    func(lon, lat, data, ax=axl, ax_args=plot['data1_args']['climatology_args']['ax_args'],
         pcolor_args=plot['data1_args']['climatology_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lon, lat, data2, ax=axm, ax_args=plot['data2_args']['climatology_args']['ax_args'],
         pcolor_args=plot['data2_args']['climatology_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lon, lat, compdata, anom=True, ax=axr, ax_args=plot['comp_args']['climatology_args']['ax_args'],
         pcolor_args=plot['comp_args']['climatology_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])                              
    plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_climatology_comparison' + str(plot['plot_depth']) + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name   


def _section_labels(datanumber, plot):
    """ Gives the axes of a section appropriate labels
    
    Parameters
    ----------
    datanumber : string
                 name of the data
    plot : dictionary
    
    Returns
    -------
    dictionary
    """
    plot[datanumber]['climatology_args']['ax_args']['xlabel'] = 'Latitude'
    plot[datanumber]['climatology_args']['ax_args']['xticks'] = np.arange(-80, 81, 20)
    plot[datanumber]['climatology_args']['ax_args']['ylabel'] = plot['depth_type'] 
    return plot   
        
def section_climatology(plot, func):
    """ Loads and plots the data for a time average section map.
    
    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map
    
    Returns
    -------
    string : name of the plot
    """    
    print 'plotting section of ' + plot['variable']
    plot = _section_labels('data1_args', plot)
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['realm_cat'], plot['scale'])
    
    zonmean = _section_data(data, plot)

    plot = dft.filltitle(plot, 'Climatology', 'data1', '')        
    func(lat, depth, zonmean, ax_args=plot['data1_args']['climatology_args']['ax_args'],
               pcolor_args=plot['data1_args']['climatology_args']['pcolor_args'], cblabel=units)
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_climatology' + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    
    plot['plot_depth'] = 0
    return plot_name
    
def section_climatology_comparison(plot, func):
    """ Loads and plots the data for a time averaged section map.
        Loads and plots the data for comparison and plots the 
        difference between the data and the comparison data.
    
    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map
    
    Returns
    -------
    string : name of the plot
    """
    print 'plotting section comparison of ' + plot['variable']
    _section_labels('data1_args', plot)
    _section_labels('data2_args', plot)
    _section_labels('comp_args', plot)        
       
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['realm_cat'], plot['scale'])
    
    zonmean = _section_data(data, plot)
    
    data2, units2, lon2, lat2, depth2 = pl.timeaverage_load_comp(plot['comp_file'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['realm_cat'], depth, plot['scale'])  
    
    zonmean2 =_section_data(data2, plot)    
               
    plot = dft.filltitle(plot, 'Climatology', 'data1', '')  
    plot = dft.filltitle(plot, 'Climatology Observations', 'data2', '') 
    plot = dft.filltitle(plot, 'Climatology Model - Obs', 'comp', '')               

    compdata = zonmean - zonmean2    
    fig, (axl, axm, axr) = plt.subplots(3,1)

    func(lat, depth, zonmean, ax=axl, ax_args=plot['data1_args']['climatology_args']['ax_args'],
               pcolor_args=plot['data1_args']['climatology_args']['pcolor_args'], cblabel=units)
    func(lat, depth, zonmean2, ax=axm, ax_args=plot['data2_args']['climatology_args']['ax_args'],
               pcolor_args=plot['data2_args']['climatology_args']['pcolor_args'], cblabel=units)
    func(lat, depth, compdata, ax=axr, ax_args=plot['comp_args']['climatology_args']['ax_args'],
               pcolor_args=plot['comp_args']['climatology_args']['pcolor_args'], cblabel=units)
                              
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_climatology_comparison' + '.pdf'
    plt.tight_layout()
    plt.savefig(plot_name, bbox_inches='tight')
    
    plot['plot_depth'] = 0
    return plot_name

def _trend_units(data, units, plot):
    """ Multiplies the data by a scalar factor based on the frequency
    
    Parameters
    ----------
    data : numpy array
    units : string
    plot : dictionary
    
    Returns
    -------
    numpy array
    string
    """
    if plot['frequency'] == 'day':
        data = data*3652.5
    if plot['frequency'] == 'mon':
        data = data*120
    if plot['frequency'] == 'year':
        data = data*10
    units = units + '/decade'
    return data, units
    
def map_trends(plot, func):
    """ Loads and plots the trend data on a map.
    
    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map
    
    Returns
    -------
    string : name of the plot
    """     
    print 'plotting trends map of ' + plot['variable']
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['trends_dates'], plot['scale'])  
    plot['plot_depth'] = 0  
    
    data = _depth_data(data, depth, plot)

    data, units = _trend_units(data, units, plot)

    plot = dft.filltitle(plot, 'Trends', 'data1', str(plot['plot_depth']))            
    func(lon, lat, data, anom=True, ax_args=plot['data1_args']['trends_args']['ax_args'],
                  pcolor_args=plot['data1_args']['trends_args']['pcolor_args'], cblabel=units,
                  **plot['plot_args'])
                  
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_trends' + str(plot['plot_depth']) + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name 

def map_trends_comp(plot, func):
    """ Loads and plots the trend data on a map.
        Loads and plots the data for comparison and plots the 
        difference between the data and the comparison data.
    
    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map
    
    Returns
    -------
    string : name of the plot
    """    
    print 'plotting trends map comparison of ' + plot['variable']
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['trends_dates'], plot['scale'])  
    plot['plot_depth'] = 0 
     
    data = _depth_data(data, depth, plot)

    data, units = _trend_units(data, units, plot)

    data2, units2, lon2, lat2, depth2 = pl.trends_load_comp(plot['comp_file'], plot['variable'], plot['depth_type'], plot['trends_dates'], [plot['plot_depth']], plot['scale'])  
 
    if data2.ndim > 2:
        data2 = data2[depth_ind, :, :]

    data2, units2 = _trend_units(data2, units2, plot)

    compdata = data - data2

    plot = dft.filltitle(plot, 'Trends', 'data1', str(plot['plot_depth'])) 
    plot = dft.filltitle(plot, 'Observations Trends', 'data2', str(plot['plot_depth']))
    plot = dft.filltitle(plot, 'Trends Model - Obs', 'comp', str(plot['plot_depth']))

    fig, (axl, axm, axr) = plt.subplots(3,1, figsize=(8,8)) 
                       
    func(lon, lat, data, ax=axl, anom=True, ax_args=plot['data1_args']['trends_args']['ax_args'],
                  pcolor_args=plot['data1_args']['trends_args']['pcolor_args'], cblabel=units,
                  **plot['plot_args'])
    func(lon, lat, data2, ax=axm, anom=True, ax_args=plot['data2_args']['trends_args']['ax_args'],
                  pcolor_args=plot['data2_args']['trends_args']['pcolor_args'], cblabel=units,
                  **plot['plot_args'])
    func(lon, lat, compdata, ax=axr, anom=True, ax_args=plot['comp_args']['trends_args']['ax_args'],
                  pcolor_args=plot['comp_args']['trends_args']['pcolor_args'], cblabel=units,
                  **plot['plot_args'])                                    
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_compare_trends' + str(plot['plot_depth']) + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name 


def section_trends(plot, func):
    """ Loads and plots the trend data for a section map.
    
    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map
    
    Returns
    -------
    string : name of the plot
    """  
    print 'plotting section trends of ' + plot['variable']
    _section_labels('data1_args', plot)
    
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['trends_dates'], plot['scale'])
    zonmean = _section_data(data, plot)
    zonmean, units = _trend_units(zonmean, units, plot)
    plot = dft.filltitle(plot, 'Trends', 'data1', '')        
    func(lat, depth, zonmean, anom=True, ax_args=plot['data1_args']['trends_args']['ax_args'],
               pcolor_args=plot['data1_args']['trends_args']['pcolor_args'], cblabel=units)
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_trends' + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')

    plot['plot_depth'] = 0    
    return plot_name

def section_trends_comp(plot, func):
    """ Loads and plots the trend data for a section map.
        Loads and plots the data for comparison and plots the 
        difference between the data and the comparison data.
            
    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map
    
    Returns
    -------
    string : name of the plot
    """ 
    print 'plotting section trends of ' + plot['variable']
    _section_labels('data1_args', plot)    
    _section_labels('data2_args', plot)
    _section_labels('comp_args', plot)    
       
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['trends_dates'], plot['scale'])
    zonmean = _section_data(data, plot)

    data2, units2, lon2, lat2, depth2 = pl.trends_load_comp(plot['comp_file'], plot['variable'], plot['depth_type'], plot['trends_dates'], depth, plot['scale'])
    zonmean2 = _section_data(data2, plot)
        
    zonmean, units = _trend_units(zonmean, units, plot)
    zonmean2, units2 = _trend_units(zonmean2, units2, plot)   
    
    compdata = zonmean - zonmean2
     
    plot = dft.filltitle(plot, 'Trends', 'data1', '')   
    plot = dft.filltitle(plot, 'Observations Trends', 'data2', '')  
    plot = dft.filltitle(plot, 'Trends Model-Obs', 'comp', '')
             
    fig, (axl, axm, axr) = plt.subplots(3,1, figsize=(8,8)) 
                       
    func(lat, depth, zonmean, ax=axl, anom=True, ax_args=plot['data1_args']['trends_args']['ax_args'],
                  pcolor_args=plot['data1_args']['trends_args']['pcolor_args'], cblabel=units,
                  **plot['plot_args'])
    func(lat, depth, zonmean2, ax=axm, anom=True, ax_args=plot['data2_args']['trends_args']['ax_args'],
                  pcolor_args=plot['data2_args']['trends_args']['pcolor_args'], cblabel=units,
                  **plot['plot_args'])
    func(lat, depth, compdata, ax=axr, anom=True, ax_args=plot['comp_args']['trends_args']['ax_args'],
                  pcolor_args=plot['comp_args']['trends_args']['pcolor_args'], cblabel=units,
                  **plot['plot_args']) 
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_trends' + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')

    plot['plot_depth'] = 0    
    return plot_name


    
def timeseries(plot, func):
    """ Loads and plots a global mean timeseries.
    
    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map
    
    Returns
    -------
    string : name of the plot
    """  
    print 'plotting timeseries of ' + plot['variable']
    data, units, x, depth = pl.timeseries_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['scale'])
    plot['data1_args']['climatology_args']['ax_args']['xlabel'] = 'Time'
    plot['data1_args']['climatology_args']['ax_args']['ylabel'] = units
    
    plot['plot_depth'] = plot['depth']
    if data.ndim > 1:
        plot['plot_depth'] = min(depth, key=lambda x:abs(x-plot['depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data = data[:,depth_ind]   
   
    plot = dft.filltitle(plot, 'Climatology', 'data1', str(plot['plot_depth']))        
    func(x, data, ax_args=plot['data1_args']['climatology_args']['ax_args'])
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_climatology_timeseries' + str(plot['depth']) + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name
    
def zonalmean(plot, func): 
    """ Loads and plots a time average of the zonal means
        for each latitude. 
    
    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map
    
    Returns
    -------
    string : name of the plot
    """      
    print 'plotting zonal mean of ' + plot['variable']
    data, units, x, depth = pl.zonal_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['scale'])
    plot['data1_args']['climatology_args']['ax_args']['xlabel'] = 'Latitude'
    plot['data1_args']['climatology_args']['ax_args']['ylabel'] = units
    
    plot['plot_depth'] = plot['depth']
    if data.ndim > 1:
        plot['plot_depth'] = min(depth, key=lambda x:abs(x-plot['depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data = data[depth_ind,:]  

   
    plot = dft.filltitle(plot, 'Climatology', 'data1', str(plot['plot_depth']))        
    func(x, data, ax_args=plot['data1_args']['climatology_args']['ax_args'])
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_climatology_zonalmean' + str(plot['depth']) + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name     
