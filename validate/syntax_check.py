"""
syntax_check
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
    """ Raises TypeError exception if the argument is not a string. 
    """
    if type(var) is not str:
        raise TypeError("variable: " + str(var) + " needs to be 'str' type")


def check_plot_projection(pp):
    """ Raises TypeError exception if the argument is not a string.
        Raises ValueError exception if the argument is not in the
        list of possible values. 
    """
    if type(pp) is not str:
        raise TypeError("plot_projection: " + str(pp) +
                        " needs to be 'str' type")
    possible_values = ['global_map',
                       'mercator',
                       'polar_map',
                       'polar_map_south',
                       'section',
                       'time_series',
                       'zonal_mean',
                       'taylor',
                       'multivariable_taylor',
                       'histogram'
                       ]
    if pp not in possible_values:
        raise ValueError("plot_projection: " + pp +
                         " is not a valid 'plot_projection'")

def check_data_type(dt):
    if dt is None:
        return
    if type(dt) is not str:
        raise TypeError("data_type must be a 'str' type")
    possible_values = ['climatology',
                       'trends',
                       'external'
                       ]
    if dt not in possible_values:
        raise ValueError ("'data_type' must be None, climatology, or trends')
    

def check_bool(thebool, thekey):
    """ Raises TypeError exception if the argument is not a boolean. 
    """
    if type(thebool) is not bool:
        raise TypeError("'" + thekey + "' must be 'bool' type")


def check_date(date):
    """ Returns True if the argument matches the pattern
        yyyy or yyyy-mm or yyyy-mm-dd.
        Returns False otherwise.
    """
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
    """ Raises TypeError exception if the argument is not a dictionary.
        Raises ValuError exception if the dictionary keys are not one
        of 'start_date' or 'end_date'.
        Raises TypeError if the provided dates are not strings.
        Raises ValueError if the dates are not correctly formatted.
    """
    if type(dates) is not dict:
        raise TypeError("'" + thekey + "' must be 'dict' type")
    for key in dates:
        if key != 'start_date' and key != 'end_date':
            raise ValueError("'" + thekey +
                             "' key's must be either 'start_date' or 'end_date'")
    if 'start_date' in dates:
        if type(dates['start_date']) is not str:
            raise TypeError("'" + thekey +
                            "': 'start_date must be 'str' type")
        if not check_date(dates['start_date']):
            raise ValueError("'" + thekey +
                             "': 'start_date' must of form yyyy-mm or yyyy-mm-dd")
    if 'end_date' in dates:
        if type(dates['end_date']) is not str:
            raise TypeError("'" + thekey +
                            "': 'end_date must be 'str' type")
        if not check_date(dates['end_date']):
            raise ValueError("'" + thekey +
                             "': 'end_date' must of form yyyy-mm or yyyy-mm-dd")


def check_realization(real):
    """ Raises TypeError if the argument is not a string or integer.
        Raises ValueError if the argument can not be cast to an integer. 
    """
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
    """ Raises TypeError if the argument is not a list.
        Raises TypeError if the elements of the list are not integers. 
    """
    if type(depths) is not list:
        raise TypeError("'depths' must be 'list' type")
    for depth in depths:
        if type(depth) is not int:
            raise TypeError("the depths in 'depths' must be 'int' type")


def check_frequency(freq):
    """ Raises TypeError if the argument is not a string.
        Raises ValueError exception if the argument is not in the
        list of possible values.
    """
    if type(freq) is not str:
        raise TypeError("'frequency' must be 'str' type")
    possible_values = ['day', 'mon', 'yr']
    if freq not in possible_values:
        raise ValueError("'frequency' must be one of 'day', 'mon', or 'yr'")


def check_scale(scale):
    """ Raises TypeError if the argument is not an integer or a float.
    """
    if type(scale) is not int and type(scale) is not float:
        raise TypeError("'scale' must be 'int' or 'float' type")


def check_plot_args(pargs):
    """ Raises TypeError if the argument is not a dictionary.
        Raises TypeError if the keys in the dictionary are not strings.
        Raises ValueError if the keys are not in the list of 
        possible values.
    """
    if type(pargs) is not dict:
        raise TypeError("'plot_args' must be 'dict' type")
    possible_keys = ['fill_continents',
                     'draw_parallels',
                     'draw_meridians',
                     ]
    for key in pargs:
        if type(key) is not str:
            raise TypeError("Keys in 'plot_args' must be 'str' type")
        if key not in possible_keys:
            raise ValueError("Keys in 'plot_args' must be one of 'fill_continents', 'draw_parallels', or 'draw_meridians'")


def check_dict(dargs, data):
    """ Raises TypeError if the first argument is not a dictionary.
    """
    if type(dargs) is not dict:
        raise TypeError("'" + data + "' must be 'dict' type")

def check_int(theint, name)
    if type(theint) is not int:
        raise TypeError("{} must be 'int' type".format(name))

def check_data_args(dargs, data):
    """ Raises TypeError if the first argument is not a dictionary.
        Raises TypeError if the keys in the dictionary are not strings.
        Raises ValueError if the keys are not in the list of 
        possible keys.
        Raises exception if the items in the dictionary are not valid.
    """
    if type(dargs) is not dict:
        raise TypeError("'" + data + "' must be 'dict' type")
    possible_keys = ['climatology_args',
                     'trends_args',
                     'ncols',
                     ]
    for key in dargs:
        if type(key) is not str:
            raise TypeError("'" + data + "' keys must be 'str' type")
        if key not in possible_keys:
            raise ValueError("'" + data + "' keys must be either 'pcolor_args', 'ax_args', or 'ncols'")
    if 'pcolor_args' in dargs:
        check_dict(dargs['pcolor_args'], 'pcolor_args')
    if 'trends_args' in dargs:
        check_dict(dargs['ax_args'], 'ax_args')
    if 'ncols' in dargs:
        check_int(dargs['ncols'], 'ncols')

def check_compare(comp):
    """ Raises TypeError if the argument is not a dictionary.
        Raises TypeError if the keys in the dictionary are not strings.
        Raises ValueError if the keys are not in the list of 
        possible keys.
        Raises exception if the items in the dictionary are not valid.
    """
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
    """ Raises TypeError if the argument is not a list.
        Raises TypeError if the elements of the list are not strings. 
    """
    if type(models) is not list:
        raise TypeError("'comp_models' must be 'list' type")
    for model in models:
        if type(model) is not str:
            raise TypeError("models in 'comp_models' must be 'str' type")


def check_obs_file(f):
    """ Raises TypeError if the argument is not a string.
        Raises ValueError if the filename for the string provided
        does not exist. 
    """
    if type(f) is not str:
        raise TypeError("'obs_file' must be 'str' type")
    if not os.path.isfile(f):
        raise ValueError("'obs_file': " + f + " is not a file")


def check_ifile(f):
    """ Raises TypeError if the argument is not a string.
        Raises ValueError if the filename for the string provided
        does not exist. 
    """
    if type(f) is not str:
        raise TypeError("'ifile' must be 'str' type")
    if not os.path.isfile(f):
        raise ValueError("'ifile': " + f + " is not a file")


def check_comp_ids(ids):
    """ Raises TypeError if the argument is not a list.
        Raises TypeError if the elements of the list are not strings. 
    """
    if type(ids) is not list:
        raise TypeError("'comp_ids' must be 'list' type")
    for i in ids:
        if type(i) is not str:
            raise TypeError("run IDs in 'comp_ids' must be 'str' type")

def check_remap(rm):
    """ Raises TypeError if the argument is not a string.
        Raises ValueError if the string is not in thelist of 
        possible values.
    """
    if type(rm) is not str:
        raise TypeError("'remap' must be 'str' type")
    possible_values = ['remapbil',
                       'remapbic',
                       'remapdis',
                       'remapnn',
                       'remapcon',
                       'remapcon2',
                       'remapplaf',
                       ]    
    if rm not in possible_values:
        raise ValueError("'remap' " + rm + " is not a valid 'remap'")

def check_remap_grid(rmg):
    """ Raises ValueError if the keys in the dictionary are not in
        the list of possible keys.
        Raises exception if the items in the dictionary are not valid.
    """
    if type(rmg) is not str:
        raise TypeError("'remap_grid' must be 'str' type")
        
def check_plot(plot):
    """ Raises TypeError if the argument is not a string.
    """   
    possible_keys = ['variable',
                     'plot_projection',
                     'data_type',
                     'dates',
                     'comp_dates',
                     'data1',
                     'data2',
                     'comp',
                     'plot_args',
                     'comp_models',
                     'comp_cmips',
                     'comp_ids',
                     'comp_obs',
                     'realization',
                     'frequency',
                     'scale',
                     'comp_scale',
                     'shift',
                     'comp_shift',
                     'months',
                     'comp_months',
                     'seasons',
                     'comp_seasons',
                     'log_depth_axis',
                     'divergent',
                     'depths',
                     'remap',
                     'remap_grid',
                     'extra_variables',
                     'extra_ifiles',
                     'extra_realms',
                     'extra_scales',
                     'extra_comp_scales',
                     'extra_shifts',
                     'extra_comp_shifts',
                     'ifile',
                     'id_file',
                     'obs_file',
                     'model_files',
                     'cmip5_file',
                     'pdf',
                     'png',
                     'ps',
                     'eps',
                     ]
    for key in plot:
        if key not in possible_keys:
            raise ValueError(str(key) + ' is not a valid key for a dictionary in plots')
    if 'variable' in plot:
        check_variable(plot['variable'])
    if 'plot_projection' in plot:
        check_plot_projection(plot['plot_projection'])
    if 'data_type' in plot:
        check_data_type(plot['data_type'])
    if 'dates' in plot:
        check_dates(plot['dates'], 'dates')
    if 'comp_dates' in plot:
        check_dates(plot['comp_dates'], 'comp_dates')

    if 'data1' in plot:
        check_data_args(plot['data1'], 'data1')
    if 'data2' in plot:
        check_data_args(plot['data2'], 'data2')
    if 'comp' in plot:
        check_data_args(plot['comp'], 'comp')
    ##here
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
    if 'remap' in plot:
        check_remap(plot['remap'])
    if 'remap_grid' in plot:
        check_remap_grid(plot['remap_grid'])

def check_plots(plots):
    """ Raises TypeError if the argument is not a list.
        Raises TypeError if the elements of the list are not dictionaries.
        Raises exception if the dictionaries in the list are not valid. 
    """
    if type(plots) is not list:
        raise TypeError("plots needs to be 'list' type")
    for plot in plots:
        if type(plot) is not dict:
            raise TypeError("plot in plots needs to be 'dict' type")
    for plot in plots:
        check_plot(plot)


def check_run(model_run):
    """ Raises TypeError if the argument is not a string.
    """
    if type(model_run) is not str:
        raise TypeError("'model_run' needs to be 'str' type")


def check_experiment(exp):
    """ Raises TypeError if the argument is not a string.
    """
    if type(exp) is not str:
        raise TypeError("'experiment' needs to be 'str' type")

def check_root(name, root):
    """ Raises TypeError if root is not a string.
        Raises ValueError if root is not a valid directory path.
    """ 
    if type(root) is not str:
        raise TypeError("{} needs to be 'str' type".format(name))
    if not os.path.exists(cmiproot):
        raise ValueError("{}: {} is not a valid directory path".format(name, root))

def check_delete(delete):
    """ Raises TypeError if the argument is not a dictionary.
        Raises ValueError if the keys in the dictionary are not in
        the list of possible keys.
        Raises TypeError if the items in the dictionary are not booleans.
    """
    if type(delete) is not dict:
        raise TypeError("'delete' needs to be 'dict' type")
    possible_keys = ['del_netcdf',
                     'del_mask',
                     'del_ncstore',
                     'del_cmipfiles',
                     ]
    for key in delete:
        if key not in possible_keys:
            raise ValueError('{} is not a valid key for delete'.format(key))
        if type(delete[key]) is not bool:
            raise TypeError('delete[' + key + "] needs to be 'bool' type")


def check_defaults(defaults):
    """ Raises TypeError if the argument is not a dictionary.
        Raises exception if the dictionary is not valid.
    """
    if type(defaults) is not dict:
        raise TypeError("'defaults' must be 'dict' type")
    check_plot(defaults)


def check_inputs(run, experiment, direct_data_root, data_root, observations_root, cmip5_root, processed_cmip5_root, output_root, cmip5_means, external_root, plots, defaults, delete, **kwargs):
    """ Checks the configuration inputs and 
        raises exceptions if they do not make sense.
    """
    check_run(run)
    check_experiment(experiment)
    if direct_data_root:
        check_root('direct_data_root', direct_data_root):
    if data_root:
        check_root('data_root', data_root)
    if observations_root:
        check_root('observations_root', observations_root)
    if cmip5_root:
        check_root('cmip5_root', cmip5_root)
    if processed_cmip5_root:
        check_root('processed_cmip5_root', processed_cmip5_root)
    if output_root:
        check_root('output_root', output_root)
    if cmip5_means:
        check_root('cmip5_means', cmip5means)
    if external_root:
        check_root('external_root', external_root)
    check_delete(delete)

    check_plots(plots)

    check_defaults(defaults)



if __name__ == "__main__":
    pass
