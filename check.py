"""
check
===============

.. moduleauthor:: David Fallis
"""
import os
import re

def check_variable(var):
    if type(var) is not str:
        raise TypeError("variable: " + str(var) + " needs to be 'str' type")

def check_plot_projection(pp):
    if type(pp) is not str:
        raise TypeError("plot_projection: " + str(pp) + " needs to be 'str' type")
    possible_values = ['global_map',
                       'mercator',
                       'polar_map',
                       'polar_map_south',
                       'section',
                       'time_series',
                       'zonal_mean',]
    if pp not in possible_values:
        raise ValueError("plot_projection: " + pp + " is not a valid 'plot_projection'")

def check_section(plot):
    if plot['plot_projection'] is 'section':
        if 'depth_type' not in plot:
             raise Exception("'depth_type' must be specified to plot a section")

def check_bool(thebool, thekey):
    if type(thebool) is not bool:
        raise TypeError("'" + thekey + "' must be 'bool' type")

def check_date(date):
    redate1 = re.compile(r'\b[0-9][0-9][0-9][0-9]\b')
    redate2 = re.compile(r'\b[0-9][0-9][0-9][0-9]-[0-9][0-9]\b')
    redate3 = re.compile(r'\b[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\b')
    if redate1.match(date) or redate2.match(date) or redate3.match(date):
        return True
    return False
    

def check_dates(dates, thekey):
    if type(dates) is not dict:
        raise TypeError("'" + thekey +"' must be 'dict' type")
    for key in dates:
        if key is not 'start_date' and key is not 'end_date':
            raise ValueError("'" + thekey + "' key's must be either 'start_date' or 'end_date'")
    if 'start_date' in dates:
        if not check_date(dates['start_date']):
            raise ValueError("'" + thekey + "': 'start_date' must of from yyyy-mm or yyyy-mm-dd")
    if 'end_date' in dates:
        if not check_date(dates['end_date']):
            raise ValueError("'" + thekey + "': 'end_date' must of from yyyy-mm or yyyy-mm-dd")    

def check_realization(real):
    if type(real) is str:
        try:
            int(real)
        except ValueError:
            raise ValueError("'realization' should be 'int' type")
        else:
            return
    if type(real) is int:
        return
    else:
        raise TypeError("Realization should be 'int' type")

def check_depth_type(dt):
    if type(dt) is not str:
        raise TypeError("'depth_type' must be 'str' type")

def check_depth(plot):
    if 'depth_type' not in plot:
        raise Exception("'depth_type' must be specified to plot specific depths")

def check_depths(depths):
    if type(depths) is not list:
        raise TypeError("'depths' must be 'list' type")
    for depth in depths:
        if type(depth) is not int:
            raise TypeError("the depths in 'depths' must be 'int' type")

def check_frequency(freq):
    if type(freq) is not str:
        raise TypeError("'frequency' must be 'str' type")
    possible_values = ['day','mon','yr']
    if freq not in posible_values:
        raise ValueError("'frequency' must be one of 'day', 'mon', or 'yr'")

def check_scale(scale):
    if type(scale) is not int and type(scale) is not float:
        raise TypeError("'scale' must be 'int' or 'float' type")

def check_plot_args(pargs):
    if type(pargs) is not dict:
        raise TypeError("'plot_args' must be 'dict' type")
    possible_keys = ['fill_continents',
                     'draw_parallels',
                     'draw_meridians',]
    for key in pargs:
        if type(key) is not str:
            raise TypeError("Keys in 'plot_args' must be 'str' type")
        if key not in possible_keys:
            raise ValueError("Keys in 'plot_args' must be one of 'fill_continents', 'draw_parallels', or 'draw_meridians'")

def check_dict(dargs, data):
    if type(dargs) is not dict:
        raise TypeError("'" + data + "' must be 'dict' type")

def check_projection_args(pargs, data):
    if type(pargs) is not dict:
        raise TypeError("'" + data + "' must be 'dict' type")
    possible_keys = ['pcolor_args',
                     'ax_args',]
    for key in pargs:
        if type(key) is not str:
            raise TypeError("'" + data + "' keys must be 'str' type")
        if key not in possible_keys:
            raise ValueError("'" + data + "' keys must be either 'pcolor_args' or 'ax_args'")
    if 'pcolor_args' in pargs:
        check_dict(pargs['pcolor_args'], 'pcolor_args')
    if 'ax_args' in pargs:
        check_dict(pargs['ax_args'], 'ax_args')
        
                     
def check_data_args(dargs, data):
    if type(dargs) is not dict:
       raise TypeError("'" + data + "' must be 'dict' type")
    possible_keys = ['climatology_args',
                     'trends_args']
    for key in dargs:
        if type(key) is not str:
            raise TypeError("'" + data + "' keys must be 'str' type")
        if key not in possible_keys:
            raise ValueError("'" + data + "' keys must be either 'climatology_args' or 'trends_args'")
    if 'climatology_args' in dargs:
        check_projection_args(dargs['climatology_args'], 'climatology_args')
    if 'trends_args' in dargs:
        check_projection_args(dargs['trends_args'], 'trends_args')
        
    
 
def check_plot(plot):
    possible_keys = ['variable',
                     'plot_projection',
                     'climatology',
                     'compare_climatology',
                     'trends',
                     'compare_trends',
                     'climatology_dates',
                     'trends_dates',
                     'realization',
                     'depth_type',
                     'depths',
                     'frequency',
                     'scale',
                     'data1_args',
                     'data2_args',
                     'comp_args',
                     'plot_args',]  
    for key in plot:
        if key not in possible_keys:
            raise ValueError(str(key) + ' is not a valid key for a dictionary in plot')
    if 'variable' in plot:
        check_variable(plot['variable'])
    if 'plot_projection' in plot:
        check_plot_projection(plot['plot_projection'])
        check_section(plot)
    if 'climatology' in plot:
        check_bool(plot['climatology'], 'climatology')
    if 'compare_climatology' in plot:
        check_bool(plot['compare_climatology'], 'compare_climatology')
    if 'trends' in plot:
        check_bool(plot['trends'], 'trends')
    if 'compare_trends' in plot:
        check_bool(plot['trends'], 'compare_trends')
    if 'climatology_dates' in plot:
        check_dates(plot['climatology_dates'], 'climatology_dates')
    if 'trends_dates' in plot:
        check_dates(plot['trends_dates'], 'trends_dates')
    if 'realization' in plot:
        check_realization(plot['realization'])
    if 'depth_type' in  plot:
        check_depth_type(plot['depth_type'])
    if 'depths' in plot:
        check_depth(plot)
        check_depths(plot['depths'])
    if 'frequency' in plot:
        check_frequency(plot['frequency'])
    if 'scale' in plot:
        check_scale(plot['scale'])
    if 'plot_args' in plot:
        check_plot_args(plot['plot_args'])
    if 'data1_args' in plot:
        check_data_args(plot['data1_args'], 'data1_args')
    if 'data2_args' in plot:
        check_data_args(plot['data2_args'], 'data2_args')
    if 'comp_args' in plot:
        check_data_args(plot['comp_args'], 'comp_args')
    
    
        

def check_plots(plots):
    if type(plots) is not list:
        raise TypeError("plots needs to be 'list' type")
    for plot in plots:
        if type(plot) is not dict:
            raise TypeError("plot in plots needs to be 'dict' type")
    for plot in plots:
        check_plot(plot) 
    

def check_model_run(model_run):
    if type(model_run) is not str:
        raise TypeError("'model_run' needs to be 'str' type")
    if not os.path.exists('/raid/rc40/data/ncs/historical-' + model_run):
        raise ValueError("No data found for model '" + model_run)
        

def check_obsroot(obsroot):
    if type(obsroot) is not str:
        raise TypeError("'obs_root' needs to be 'str' type")
    if not os.path.exists(obsroot):
        raise ValueError("obsroot: " + obsroot + " does not exist")

def check_obs(obs):
    if type(obs) is not dict:
        raise TypeError("'obs' needs to be 'dict' type")
    for key in obs:
        if type(key) is not str:
            raise TypeError("obs key '" + str(key) + "' needs to be 'str' type")
        if type(obs[key]) is not str:
            raise TypeError("obs[" + key + "] needs to be 'str' type")
        if not os.path.isfile(obs[key]):
            raise ValueError("obs[" + key + "] '" + obs[key] + "' does not exist")

def check_delete(delete):
    possible_keys = ['del_fldmeanfiles',
                     'del_mask',
                     'del_ncstore',
                     'del_remapfiles',
                     'del_trendfiles',
                     'del_zonalfiles',]
    for key in delete:
        if key not in possible_keys:
            raise ValueError(str(key) + ' is not a valid key for delete{}')
        if type(delete[key]) is not bool:
            raise TypeError('delete[' + key + "] needs to be 'bool' type")
        
        

def check_input(plots, model_run, obsroot, obs, defaults, delete):
    check_plots(plots)
    check_model_run(model_run)
    check_obsroot(obsroot)
    check_obs(obs)
    check_plot(defaults)
    check_delete(delete)
    
    
if __name__ == "__main__":
 model_run = 'edr'

 defaults = {
            'climatology': True,
            #'climatology_dates': {'start_date': '1881-01', 'end_date': '1890-01'},
            'compare_climatology': True,

            'trends': False,
            'trends_dates': {'start_date': '1991-01', 'end_date': '2000-01'},
            'compare_trends': False,

            'realization': '1',
            'scale': 1,
            #'plot_args': {'fill_continents': True}
            }

 plots = [

         {    
          'variable': 'ta',
          'plot_projection': 'time_series',
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000], 
          'realization': '1'                                              
          }, 
         {}
        ]
 delete = {
          'del_fldmeanfiles': False,
          'del_mask': True,
          'del_ncstore': True,
          'del_remapfiles': True,
          'del_trendfiles': True,
          'del_zonalfiles': True,
          }
          
 obsroot = '/raid/rc40/data/ncs/obs4comp'               

 obs = {}         
 check_input(plots, model_run, obsroot, obs, defaults, delete)
