"""
check
===============
This module is used to check to the validity of the options setup
in configure.py. Exceptions will be raised if the options are
incorrectly formatted. This gives the user the opportunity to make 
the corrections before producing the plots.

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
                       'zonal_mean',
                       'taylor',]
    if pp not in possible_values:
        raise ValueError("plot_projection: " + pp + " is not a valid 'plot_projection'")

def check_bool(thebool, thekey):
    if type(thebool) is not bool:
        raise TypeError("'" + thekey + "' must be 'bool' type")

def check_date(date):
    redate1 = re.compile(r'\b[0-9][0-9][0-9][0-9]\b')
    redate2 = re.compile(r'\b[0-9][0-9][0-9][0-9]-[0-9][0-9]\b')
    redate3 = re.compile(r'\b[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]\b')
    if redate1.match(date) and len(date) == 4:
        return True
    if redate2.match(date) and len(date) == 7: 
        return True
    if redate3.match(date) and len(date) == 10:
        return True
    return False

def check_dates(dates, thekey):
    if type(dates) is not dict:
        raise TypeError("'" + thekey +"' must be 'dict' type")
    for key in dates:
        if key != 'start_date' and key != 'end_date':
            raise ValueError("'" + thekey + "' key's must be either 'start_date' or 'end_date'")
    if 'start_date' in dates:
        if type(dates['start_date']) is not str:
            raise TypeError("'" + thekey + "': 'start_date must be 'str' type")
        if not check_date(dates['start_date']):
            raise ValueError("'" + thekey + "': 'start_date' must of formm yyyy-mm or yyyy-mm-dd")
    if 'end_date' in dates:
        if type(dates['end_date']) is not str:
            raise TypeError("'" + thekey + "': 'end_date must be 'str' type")
        if not check_date(dates['end_date']):
            raise ValueError("'" + thekey + "': 'end_date' must of form yyyy-mm or yyyy-mm-dd")    

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
    if freq not in possible_values:
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

def check_compare(comp):
    if type(comp) is not dict:
        raise TypeError("'compare' must be 'dict' type")
    possible_keys = ['cmip5',
                     'model',
                     'obs',
                     'runid']
    for key in comp:
        if type(key) is not str:
            raise TypeError("'compare' keys must be 'str' type")
        if key not in possible_keys:
            raise ValueError("'compare' keys must be either one of 'cmip5', 'model', or 'obs'")
    for key in comp:
        check_bool(comp[key], "'compare': " + key)

def check_comp_models(models):
    if type(models) is not list:
        raise TypeError("'comp_models' must be 'list' type")
    for model in models:
        if type(model) is not str:
            raise TypeError("models in 'comp_models' must be 'str' type") 

def check_obs_file(f):
    if type(f) is not str:
        raise TypeError("'obs_file' must be 'str' type")
    if not os.path.isfile(f):
        raise ValueError("'obs_file': " + f + " is not a file")        

def check_ifile(f):
    if type(f) is not str:
        raise TypeError("'ifile' must be 'str' type")
    if not os.path.isfile(f):
        raise ValueError("'ifile': " + f + " is not a file") 

def check_comp_ids(ids):
    if type(ids) is not list:
        raise TypeError("'comp_ids' must be 'list' type")
    for i in ids:
        if type(i) is not str:
            raise TypeError("run IDs in 'comp_ids' must be 'str' type")    
         
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
                     'depths',
                     'frequency',
                     'scale',
                     'data1_args',
                     'data2_args',
                     'comp_args',
                     'plot_args',
                     'pdf',
                     'png',
                     'compare',
                     'comp_models',
                     'obs_file',
                     'ifile',
                     'comp_ids',]  
    for key in plot:
        if key not in possible_keys:
            raise ValueError(str(key) + ' is not a valid key for a dictionary in plots')
    if 'variable' in plot:
        check_variable(plot['variable'])
    if 'plot_projection' in plot:
        check_plot_projection(plot['plot_projection'])
    if 'climatology' in plot:
        check_bool(plot['climatology'], 'climatology')
    if 'compare_climatology' in plot:
        check_bool(plot['compare_climatology'], 'compare_climatology')
    if 'trends' in plot:
        check_bool(plot['trends'], 'trends')
    if 'compare_trends' in plot:
        check_bool(plot['compare_trends'], 'compare_trends')
    if 'climatology_dates' in plot:
        check_dates(plot['climatology_dates'], 'climatology_dates')
    if 'trends_dates' in plot:
        check_dates(plot['trends_dates'], 'trends_dates')
    if 'realization' in plot:
        check_realization(plot['realization'])
    if 'depths' in plot:
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
    if 'pdf' in plot:
        check_bool(plot['pdf'], 'pdf')
    if 'png' in plot:
        check_bool(plot['png'], 'pdf')
    if 'compare' in plot:
        check_compare(plot['compare'])
    if 'comp_models' in plot:
        check_comp_models(plot['comp_models'])
    if 'obs_file' in plot:
        check_obs_file(plot['obs_file'])
    if 'ifile' in plot:
        check_ifile(plot['_file'])
    if 'comp_ids' in plot:
        check_comp_ids(plot['comp_ids'])     
        
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

def check_experiment(exp):
    if type(exp) is not str:
        raise TypeError("'experiment' needs to be 'str' type")    
        

def check_obsroot(obsroot):
    if type(obsroot) is not str:
        raise TypeError("'obs_root' needs to be 'str' type")   
    if not os.path.exists(obsroot):
        raise ValueError("obsroot: " + obsroot + " does not exist")

def check_cmiproot(cmiproot):
    if type(cmiproot) is not str:
        raise TypeError("'cmiproot_root' needs to be 'str' type")   
    if not os.path.exists(cmiproot):
        raise ValueError("cmiproot: " + cmiproot + " does not exist")

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
    if type(delete) is not dict:
        raise TypeError("'delete' needs to be 'dict' type")
    possible_keys = ['del_fldmeanfiles',
                     'del_mask',
                     'del_ncstore',
                     'del_remapfiles',
                     'del_trendfiles',
                     'del_zonalfiles',
                     'del_cmipfiles',
                     'del_ENS_MEAN_cmipfiles',
                     'del_ENS_STD_cmipfiles',]
    for key in delete:
        if key not in possible_keys:
            raise ValueError(str(key) + ' is not a valid key for delete{}')
        if type(delete[key]) is not bool:
            raise TypeError('delete[' + key + "] needs to be 'bool' type")
        
def check_defaults(defaults):
    if type(defaults) is not dict:
       raise TypeError("'defaults' must be 'dict' type")
    check_plot(defaults)        

def check_inputs(plots, model_run, experiment, obsroot, cmiproot, obs, defaults, delete):
    check_plots(plots)
    check_model_run(model_run)
    check_experiment(experiment)
    if obsroot:
        check_obsroot(obsroot)
    if cmiproot:
        check_cmiproot(cmiproot)
    check_obs(obs)
    check_defaults(defaults)
    check_delete(delete)
    
    
    
if __name__ == "__main__":
    pass
