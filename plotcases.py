import plotload as pl
import plotregions as pr
import numpy as np
import matplotlib.pyplot as plt

def global_map_climatology(plot):
    print 'plotting global map of ' + plot['variable']
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'])    
    if data.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(min(depth))
            print('global_map: plot_depth not specified for ' +
                  plot['variable'] + ', using ' + str(plot['plot_depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  p['plot_depth'] + ' for ' + v)

        data = data[depth_ind, :, :]
        
    pr.global_map(lon, lat, data, ax_args=plot['data1_args']['ax_args'],
                  pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units)
                  
    plot_name = 'plots/' + plot['variable'] + '_map.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name

def section_climatology(plot):
    print 'plotting section of ' + plot['variable']
    plot['data1_args']['ax_args']['xlabel'] = 'Latitude'
    plot['data1_args']['ax_args']['xticks'] = np.arange(-80, 81, 20)
    plot['data1_args']['ax_args']['ylabel'] = 'Depth'
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'])

    try:
        if data.ndim == 3:
            zonmean = data.mean(axis=2)
        elif data.ndim == 2:
             zonmean = data.mean(axis=1)
    except:
        print 'proc_plot cannot zonal mean for section ' + plot['ifile'] + ' ' + plot['variable']
        
    pr.section(lat, depth, zonmean, ax_args=plot['data1_args']['ax_args'],
               pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units)
    plot_name = 'plots/' + plot['variable'] + '_section.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name

def polar_map_climatology(plot):
    print 'plotting polar map of ' + plot['variable']
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'])    
    #print depth
    if data.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(min(depth))
            print('global_map: plot_depth not specified for ' +
                  plot['variable'] + ', using ' + str(plot['plot_depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  p['plot_depth'] + ' for ' + v)

        data = data[depth_ind, :, :]
        
    pr.polar_map(lon, lat, data, ax_args=plot['data1_args']['ax_args'],
                  pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units)
                  
    plot_name = 'plots/' + plot['variable'] + '_polar_map.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name    

def polar_map_south_climatology(plot):
    print 'plotting polar map of ' + plot['variable']
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'])    
    print depth
    if data.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(min(depth))
            print('global_map: plot_depth not specified for ' +
                  plot['variable'] + ', using ' + str(plot['plot_depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  p['plot_depth'] + ' for ' + v)

        data = data[depth_ind, :, :]
        
    pr.polar_map_south(lon, lat, data, ax_args=plot['data1_args']['ax_args'],
                  pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units)
                  
    plot_name = 'plots/' + plot['variable'] + '_polar_map_south.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name 
    
def mercator_climatology(plot): 
    print 'plotting meractor projection of ' + plot['variable']
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'])    
    #print depth
    if data.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(min(depth))
            print('global_map: plot_depth not specified for ' +
                  plot['variable'] + ', using ' + str(plot['plot_depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  p['plot_depth'] + ' for ' + v)

        data = data[depth_ind, :, :]
        
    pr.mercator(lon, lat, data, ax_args=plot['data1_args']['ax_args'],
                  pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units,
                  **plot['position'])
                  
    plot_name = 'plots/' + plot['variable'] + '_mercator.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name 
       
def global_map_comparison(plot):
    print 'plotting global map comparison of ' + plot['variable']
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'])    
    obsdata, units, lon, lat, depth = pl.timeaverage_load(plot['comp_file'], plot['variable']) 
    if data.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(depth.min())
            print('global_map: plot_depth not specified for ' +
                  plot['variable'] + ', using ' + str(plot['plot_depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  p['plot_depth'] + ' for ' + plot['variable'])

        data = data[depth_ind, :, :]
        
    if obsdata.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(depth.min())

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  p['plot_depth'] + ' for ' + plot['variable'])

        obsdata = obsdata[depth_ind, :, :]  
    if data.shape != obsdata.shape:
        raise ValueError('data1.shape != data2.shape, cannot make anomaly')
    else:
        anom =  obsdata - data
    
    fig, (axl, axm, axr) = plt.subplots(3,1, figsize=(8,8))
              
    pr.global_map(lon, lat, data, ax=axl, ax_args=plot['data1_args']['ax_args'],
                  pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units)
    pr.global_map(lon, lat, obsdata, ax=axm, ax_args=plot['data2_args']['ax_args'],
                  pcolor_args=plot['data2_args']['pcolor_args'], cblabel=units)
    pr.global_map(lon, lat, anom, ax=axr, ax_args=plot['comp_args']['ax_args'],
                  pcolor_args=plot['comp_args']['pcolor_args'], cblabel=units)
                                                      
    plot_name = 'plots/' + plot['variable'] + '_map_comparison.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name
    
def section_comparison(plot):
    print 'plotting section comparison of ' + plot['variable']
    plot['data1_args']['ax_args']['xlabel'] = 'Latitude'
    plot['data1_args']['ax_args']['xticks'] = np.arange(-80, 81, 20)
    plot['data1_args']['ax_args']['ylabel'] = 'Depth'
    plot['data2_args']['ax_args']['xlabel'] = 'Latitude'
    plot['data2_args']['ax_args']['xticks'] = np.arange(-80, 81, 20)
    plot['data2_args']['ax_args']['ylabel'] = 'Depth'    
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'])
    obsdata, units, lon, lat, depth = pl.timeaverage_load(plot['comp_file'], plot['variable'])
    try:
        if data.ndim == 3:
            zonmean = data.mean(axis=2)
        elif data.ndim == 2:
             zonmean = data.mean(axis=1)
    except:
        print 'proc_plot cannot zonal mean for section ' + plot['ifile'] + ' ' + plot['variable']
    try:
        if obsdata.ndim == 3:
            obszonmean = obsdata.mean(axis=2)
        elif obsdata.ndim == 2:
             obszonmean = obsdata.mean(axis=1)
    except:
        print 'proc_plot cannot zonal mean for section ' + plot['comp_file'] + ' ' + plot['variable'] 
        
    if zonmean.shape != obszonmean.shape:
        raise ValueError('data1.shape != data2.shape, cannot make anomaly')
    else:
        anom =  obszonmean - zonmean
        
    fig, (axl, axm, axr) = plt.subplots(3,1, figsize=(8,8))
                   
    pr.section(lat, depth, zonmean, ax=axl, ax_args=plot['data1_args']['ax_args'],
               pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units)
    pr.section(lat, depth, obszonmean, ax=axm, ax_args=plot['data2_args']['ax_args'],
               pcolor_args=plot['data2_args']['pcolor_args'], cblabel=units)
    pr.section(lat, depth, anom, ax=axr, ax_args=plot['comp_args']['ax_args'],
               pcolor_args=plot['comp_args']['pcolor_args'], cblabel=units)
    plot_name = 'plots/' + plot['variable'] + '_section_comparison.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name

def polar_map_comparison(plot):
    print 'plotting global map comparison of ' + plot['variable']
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'])    
    obsdata, units, lon, lat, depth = pl.timeaverage_load(plot['comp_file'], plot['variable']) 
    if data.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(depth.min())
            print('global_map: plot_depth not specified for ' +
                  plot['variable'] + ', using ' + str(plot['plot_depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  p['plot_depth'] + ' for ' + plot['variable'])

        data = data[depth_ind, :, :]
        
    if obsdata.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(depth.min())

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  p['plot_depth'] + ' for ' + plot['variable'])

        obsdata = obsdata[depth_ind, :, :]  
    if data.shape != obsdata.shape:
        raise ValueError('data1.shape != data2.shape, cannot make anomaly')
    else:
        anom =  obsdata - data
    
    fig, (axl, axm, axr) = plt.subplots(3,1, figsize=(8,8))
              
    pr.global_map(lon, lat, data, ax=axl, ax_args=plot['data1_args']['ax_args'],
                  pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units)
    pr.global_map(lon, lat, obsdata, ax=axm, ax_args=plot['data2_args']['ax_args'],
                  pcolor_args=plot['data2_args']['pcolor_args'], cblabel=units)
    pr.global_map(lon, lat, anom, ax=axr, ax_args=plot['comp_args']['ax_args'],
                  pcolor_args=plot['comp_args']['pcolor_args'], cblabel=units)
                                                      
    plot_name = 'plots/' + plot['variable'] + '_polar_map_comparison.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name

def _trend_units(data, units, plot):
    dates = plot['trends_dates']
    if dates:
        syear = dates['start_date'][:4] 
        smonth = dates['start_date'][5:7]
        eyear = dates['end_date'][:4] 
        emonth = dates['end_date'][5:7]
        months = (int(eyear)*12 + int(emonth)) - (int(syear)*12 + int(smonth))
    else:
        pass
    data = data*120    
    units = units + '/decade'
    return data, units
    
    
def global_map_trends(plot):
    print 'plotting global map trends of ' + plot['variable']
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['trends_dates'])    
    if data.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(min(depth))
            print('global_map: plot_depth not specified for ' +
                  plot['variable'] + ', using ' + str(plot['plot_depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  p['plot_depth'] + ' for ' + v)

        data = data[depth_ind, :, :]

    data, units = _trend_units(data, units, plot)
            
    pr.global_map(lon, lat, data, ax_args=plot['data1_args']['ax_args'],
                  pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units)
                  
    plot_name = 'plots/' + plot['variable'] + '_trends.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name    

def section_trends(plot):
    print 'plotting section trends of ' + plot['variable']
    plot['data1_args']['ax_args']['xlabel'] = 'Latitude'
    plot['data1_args']['ax_args']['xticks'] = np.arange(-80, 81, 20)
    plot['data1_args']['ax_args']['ylabel'] = 'Depth'
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['trends_dates'])
    try:
        if data.ndim == 3:
            zonmean = data.mean(axis=2)
        elif data.ndim == 2:
             zonmean = data.mean(axis=1)
    except:
        print 'proc_plot cannot zonal mean for section ' + plot['ifile'] + ' ' + plot['variable']
    print zonmean
    data, units = _trend_units(data, units, plot)
       
    pr.section(lat, depth, zonmean, ax_args=plot['data1_args']['ax_args'],
               pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units)
    plot_name = 'plots/' + plot['variable'] + '_section_trends.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name

def polar_map_trends(plot):
    print 'plotting polar map trends of ' + plot['variable']
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['trends_dates'])    
    if data.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(min(depth))
            print('global_map: plot_depth not specified for ' +
                  plot['variable'] + ', using ' + str(plot['plot_depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  p['plot_depth'] + ' for ' + v)

        data = data[depth_ind, :, :]

    data, units = _trend_units(data, units, plot)
            
    pr.polar_map(lon, lat, data, ax_args=plot['data1_args']['ax_args'],
                  pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units)
                  
    plot_name = 'plots/' + plot['variable'] + '_polar_map_trends.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name    

def polar_map_south_trends(plot):
    print 'plotting south polar map trends of ' + plot['variable']
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['trends_dates'])    
    if data.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(min(depth))
            print('global_map: plot_depth not specified for ' +
                  plot['variable'] + ', using ' + str(plot['plot_depth']))
        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  str(plot['plot_depth']) + ' for ' + plot['variable'])

        data = data[depth_ind, :, :]

    data, units = _trend_units(data, units, plot)
            
    pr.polar_map_south(lon, lat, data, ax_args=plot['data1_args']['ax_args'],
                  pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units)
                  
    plot_name = 'plots/' + plot['variable'] + '_polar_map_south_trends.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name 

def mercator_trends(plot):
    print 'plotting mercator trends of ' + plot['variable']
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['trends_dates'])    
    if data.ndim > 2:
        if 'depth' in plot:
            plot['plot_depth'] = np.round(plot['depth'])
        else:
            plot['plot_depth'] = np.round(min(depth))
            print('global_map: plot_depth not specified for ' +
                  plot['variable'] + ', using ' + str(plot['plot_depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' +  p['plot_depth'] + ' for ' + v)

        data = data[depth_ind, :, :]
        print data.shape


    data, units = _trend_units(data, units, plot)
            
    pr.mercator(lon, lat, data, ax_args=plot['data1_args']['ax_args'],
                  pcolor_args=plot['data1_args']['pcolor_args'], cblabel=units,
                  **plot['position'])
                  
    plot_name = 'plots/' + plot['variable'] + '_mercator_trends.pdf'
    plt.savefig(plot_name, bbox_inches='tight')
    return plot_name 
