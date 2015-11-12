import plotload as pl
import plotregions as pr
import numpy as np
import matplotlib.pyplot as plt
import defaults as dft
import datetime


def map_climatology(plot, func):
    print 'plotting map of ' + plot['variable']
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['realm_cat'])
    plot['plot_depth'] = 0   
    if data.ndim > 2:
        plot['plot_depth'] = min(depth, key=lambda x:abs(x-plot['depth']))
        try:
            depth_ind = np.where(np.round(depth) == np.round(plot['plot_depth']))[0][0]
        except:
            print('Failed to extract depth ' +  plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data = data[depth_ind, :, :]
    
    plot = dft.filltitle(plot, 'Climatology', 'data1', str(plot['plot_depth']))    
    func(lon, lat, data, ax_args=plot['data1_args']['climatology_args']['ax_args'],
         pcolor_args=plot['data1_args']['climatology_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
                  
    plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_climatology' + str(plot['plot_depth']) + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name    

def map_climatology_comparison(plot, func):
    print 'plotting comparison map of ' + plot['variable']
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['realm_cat'])
    plot['plot_depth'] = 0       
    if data.ndim > 2:
        plot['plot_depth'] = min(depth, key=lambda x:abs(x-plot['depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data = data[depth_ind, :, :]
    
    data2, units, lon, lat, depth = pl.timeaverage_load_comp(plot['comp_file'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['realm_cat']) 
    
  
    if data2.ndim > 2:
        plot['plot_depth'] = min(depth, key=lambda x:abs(x-plot['depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data2 = data2[depth_ind, :, :]    

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
        
def section_climatology(plot, func):    
    print 'plotting section of ' + plot['variable']
    plot['data1_args']['climatology_args']['ax_args']['xlabel'] = 'Latitude'
    plot['data1_args']['climatology_args']['ax_args']['xticks'] = np.arange(-80, 81, 20)
    plot['data1_args']['climatology_args']['ax_args']['ylabel'] = plot['depth_type']
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['climatology_dates'], plot['realm_cat'])
    try:
        if data.ndim == 3:
            zonmean = data.mean(axis=2)
        elif data.ndim == 2:
            zonmean = data.mean(axis=1)
    except:
        print 'proc_plot cannot zonal mean for section ' + plot['ifile'] + ' ' + plot['variable']

    plot = dft.filltitle(plot, 'Climatology', 'data1', '')        
    func(lat, depth, zonmean, ax_args=plot['data1_args']['climatology_args']['ax_args'],
               pcolor_args=plot['data1_args']['climatology_args']['pcolor_args'], cblabel=units)
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_climatology' + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    
    plot['plot_depth'] = 0
    return plot_name
    
def section_climatology_comparison(plot, func):
    pass

def _trend_units(data, units, plot):
    if plot['frequency'] == 'day':
        data = data*3652.5
    if plot['frequency'] == 'mon':
        data = data*120
    if plot['frequency'] == 'year':
        data = data*10
    units = units + '/decade'
    return data, units
    
def map_trends(plot, func):    
    print 'plotting trends map of ' + plot['variable']
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['trends_dates'])  
    plot['plot_depth'] = 0  
    if data.ndim > 2:
        plot['plot_depth'] = min(depth, key=lambda x:abs(x-plot['depth']))

        try:
            depth_ind = np.where(np.round(depth) == np.round(plot['plot_depth']))[0][0]
        except:
            print('Failed to extract depth ' +  plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data = data[depth_ind, :, :]

    data, units = _trend_units(data, units, plot)

    plot = dft.filltitle(plot, 'Trends', 'data1', str(plot['plot_depth']))            
    func(lon, lat, data, anom=True, ax_args=plot['data1_args']['trends_args']['ax_args'],
                  pcolor_args=plot['data1_args']['trends_args']['pcolor_args'], cblabel=units,
                  **plot['plot_args'])
                  
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_trends' + str(plot['plot_depth']) + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name 

def section_trends(plot, func):
    print 'plotting section trends of ' + plot['variable']
    plot['data1_args']['trends_args']['ax_args']['xlabel'] = 'Latitude'
    plot['data1_args']['trends_args']['ax_args']['xticks'] = np.arange(-80, 81, 20)
    plot['data1_args']['trends_args']['ax_args']['ylabel'] = plot['depth_type']
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['trends_dates'])
    try:
        if data.ndim == 3:
            zonmean = data.mean(axis=2)
        elif data.ndim == 2:
            zonmean = data.mean(axis=1)
    except:
        print 'proc_plot cannot zonal mean for section ' + plot['ifile'] + ' ' + plot['variable']

    zonmean, units = _trend_units(zonmean, units, plot)
    plot = dft.filltitle(plot, 'Trends', 'data1', '')        
    func(lat, depth, zonmean, anom=True, ax_args=plot['data1_args']['trends_args']['ax_args'],
               pcolor_args=plot['data1_args']['trends_args']['pcolor_args'], cblabel=units)
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_trends' + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')

    plot['plot_depth'] = 0    
    return plot_name
def timeseries(plot, func):
    print 'plotting timeseries of ' + plot['variable']


    data, units, x, depth = pl.timeseries_load(plot['ifile'], plot['variable'], plot['depth_type'], plot['climatology_dates'])
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
   
    plot = dft.filltitle(plot, 'Climatology', 'data1', plot['plot_depth'])        
    func(x, data, ax_args=plot['data1_args']['climatology_args']['ax_args'])
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_climatology' + str(plot['depth']) + '.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name
    
      
