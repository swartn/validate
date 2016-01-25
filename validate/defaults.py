"""
defaults
===============
This module fills the plots with values specified in defaults
and fills the remaining options with placeholders so that
existence checks will not be needed later.

.. moduleauthor:: David Fallis
"""
import numpy as np

OLD=_DEFAULTS = {'plotprojection': 'global_map',
            'climatology': False,
            'compare_climatology': False,
            'trends': False,
            'compare_trends': False,
            'frequency': 'mon',
            'realization': 1,
            'depths': [0],
            'scale': 1,
            'pdf': True,
            'png': False,
            'comp_flag': None,
            'remap': 'remapdis',
            'remap_grid': 'r360x180',
            }
DEFAULTS = {'plotprojection': 'mercator',
            'data_type': 'climatology',
            'set_yscale': 'log',
            'frequency': 'mon',
            'realization': 1,
            'scale': 1,
            'pdf': True,
            'png': False,
            'comp_flag': None,
            'remap': 'remapdis',
            'remap_grid': 'r360x180',
            'seasons': ['DJF', 'MAM', 'JJA', 'SON'],
            'comp_seasons': ['DJF', 'MAM', 'JJA', 'SON'],
            'alpha': 0.01,
            'sigma': 0.05,
            }

piControl = {'dates': {'start_date': '2900-01',
                       'end_date': '3000-01'},
             }
historical = {'dates': {'start_date': '2900-01',
                        'end_date': '3000-01'},
              }
rcp = {'dates': {'start_date': '2900-01',
                 'end_date': '3000-01'},
       }                        

def fill(plots, model_run, experiment, defaults={}):
    """ Fills the blank spaces in plots with default values and returns the list

    Parameters
    ----------
    plots : list of dictionaries
    defaults : dictionary
               values to fill plots
    model_run : string
                run ID
    experiment : string
                 experiment name

    Returns
    -------
    list of dictionaries
    """
    if not defaults:
        defaults = {}
    for p in plots:

        # fill plots with the defaults given in conf.yaml
        for key in defaults:
            if key not in p:
                p[key] = defaults[key]
 
        # fill plots with immutable global DEFAULTS
        for key in DEFAULTS:
            if key not in p:
                p[key] = DEFAULTS[key]
        
        # fill plots with mutable global defaults
        if 'comp_models' not in p:
            p['comp_models'] = []
        if 'comp_cmips' not in p:
            p['comp_cmips'] = []
        if 'comp_ids' not in p:
            p['comp_ids'] = []
        if 'comp_obs' not in p:
            p['comp_obs'] = []
        if 'data1' not in p:
            p['data1'] = {}
        if 'data2' not in p:
            p['data2'] = {}
        if 'comp' not in p:
            p['comp'] = {}
        if 'plot_args' not in p:
            p['plot_args'] = {}
        if 'depths' not in p:
            p['depths'] = [""]
        if 'seasons' not in p:
            p['seasons'] = ['DJF', 'MAM', 'JJA', 'SON']
        if 'comp_seasons' not in p:
            p['comp_seasons'] = ['DJF', 'MAM', 'JJA', 'SON']
              
        # remove plot from list if no variable is provided
        if 'variable' not in p:
            plots.remove(p)
            print p
            print 'deleted: no variable provided'
        
        # add dates based on experiment
        if 'piControl' in experiment:
            for key in piControl:
                if key not in p:
                    p[key] = piControl[key]            
        elif 'rcp' in experiment:
            for key in piControl:
                if key not in p:
                    p[key] = rcp[key]          
        else:
            for key in piControl:
                if key not in p:
                    p[key] = historical[key]
        
        if 'comp_dates' not in p:
            p['comp_dates'] = p['dates']
          
        p['model_ID'] = model_run
        p['plot_depth'] = 0
        
        def _fill_args(data):
            if 'ax_args' not in p[data]:
                p[data]['ax_args'] = {}
            if 'pcolor_args' not in p[data]:
                p[data]['pcolor_args'] = {}
            if 'title' not in p[data]['ax_args']:
                p[data]['title_flag'] = False
            else:
                p[data]['title_flag'] = True
            if 'vmin' not in p[data]['pcolor_args']:
                p[data]['pcolor_flag'] = False
            else:
                p[data]['pcolor_flag'] = True

        _fill_args('data1')
        _fill_args('data2')
        _fill_args('comp')
        

        if p['plot_projection'] == 'section':
            _section_labels('data1', p)
            _section_labels('data2', p)
            _section_labels('comp', p)
         

def _section_labels(datanumber, pl):
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
    pl[datanumber]['ax_args']['xlabel'] = 'Latitude'
    pl[datanumber]['ax_args']['xticks'] = np.arange(-80, 81, 20)
    pl[datanumber]['ax_args']['ylabel'] = 'Depth'
    pass 

def filltitle(p):
    def fill(comp):
        if not p['data1']['title_flag']:
            p['data1']['ax_args']['title'] = p['variable'] + ' Model: ' + p['model_ID']
        if not p['data2']['title_flag']:
            p['data2']['ax_args']['title'] = p['variable'] + ' Model: ' + comp
        if not p['comp']['title_flag']:
            p['comp']['ax_args']['title'] = p['variable'] + ' Model: ' + p['model_ID'] + '-' + comp
#        if p['is_depth']:
#           p['data1']['ax_args']['title'] += ' Depth: ' + str(p['plot_depth'])
#           p['data2']['ax_args']['title'] += ' Depth: ' + str(p['plot_depth'])
#           p['comp']['ax_args']['title'] += ' Depth: ' + str(p['plot_depth'])

    if p['comp_flag'] == 'model':
        fill(p['comp_model'])
    elif p['comp_flag'] == 'runid':
        fill(p['comp_model'])
    else:
        if p['comp_flag']:
            fill(p['comp_flag'])
        else:
            fill("")
