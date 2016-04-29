"""
defaults
===============
This module fills the plots with values specified in defaults
and fills the remaining options with placeholders so that
existence checks will not be needed later.

..moduleauthor:: David Fallis

"""

import numpy as np
import constants
from matplotlib.colors import LogNorm

DEFAULTS = {'plotprojection': 'mercator',
            'data_type': 'climatology',
            'set_yscale': 'log',
            'frequency': 'mon',
            'realization': 'r1i1p1',
            'scale': 1,
            'shift': 0,
            'pdf': True,
            'png': False,
            'ps': False,
            'eps': False,
            'comp_flag': None,
            'remap': 'remapdis',
            'remap_grid': 'r360x180',
            'alpha': 0.05,
            'sigma': 0.05,
            'cdostring': None,
            'units': None,
            'divergent': False,
            'yearmean': False,
            'extra_variables': [],
            'extra_obs': [],
            'external_function': None,
            'external_function_args': {},
            }


MODELS = ['bcc-csm1-1',
          'CanAM4',
          'CanESM2',
          'CMCC-CESM',
          'CMCC-CM',
          'CMCC-CMS',
          'CNRM-CM5',
          'CNRM-CM5-2',
          'CFSv2-2011',
          'ACCESS1-0',
          'ACCESS1-3',
          'CSIRO-Mk3.6.0',
          'EC-EARTH',
          'FIO-ESM',
          'BNU-ESM',
          'INM-CM4',
          'IPSL-CM5a-LR',
          'IPSL-CM5A-MR',
          'IPSL-CM5B-LR',
          'FGOALS-g2',
          'FGOALS-gl',
          'FGOALS-s2',
          'MIROC4h',
          'MIROC5',
          'MIROC-ESM',
          'MIROC-ESM-CHEM',
          'HadCM3',
          'HadCM3Q',
          'HadGEM2-A'
          'HadGEM2-CC',
          'HadGEM2-ES',
          'MPI-ESM-LR',
          'MPI-ESM-MR',
          'MPI-ESM-P',
          'MRI-AGCM3.2H',
          'MRI-AGCM3.2S',
          'MRI-CGCM3',
          'MRI-ESM1',
          'GISS-E2-H',
          'GISS-E2-H-CC',
          'GISS-E2-R',
          'GISS-E2-R-CC',
          'GEOS-5',
          'CCSM4',
          'NorESM1-M',
          'NorESM-ME',
          'NICAM.09',
          'HadGEM2-AO',
          'GFDL-CM2p1',
          'GFDL-CM3',
          'GFDL-ESM2G',
          'GFDL-ESM2M',
          'GFDL-HIRAM-C180',
          'GFDL-HIRAM-C360',
          'CESM1',
          ]

piControl = {'dates': {'start_date': '2900-01',
                       'end_date': '3000-01'},
             }
historical = {'dates': {'start_date': '1986-01',
                        'end_date': '2005-01'},
              }
rcp = {'dates': {'start_date': '2081-01',
                 'end_date': '2100-01'},
       }                        

norms = {'lognorm': LogNorm()}


def fill(plots, run, experiment, defaults={}):
    """   
    Fills the blank spaces in plots with default values.
         
    Parameters
    ----------
    plots : list of dictionaries
    model_run : string
                run ID
    experiment : string
                 experiment name
    defaults : dictionary
               values to fill plots

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
        if p['comp_cmips'] == None:
            p['comp_cmips'] = []
        if 'comp_ids' not in p:
            p['comp_ids'] = []
        if p['comp_ids'] == None:
            p['comp_ids'] = []
        if 'comp_obs' not in p:
            p['comp_obs'] = []
        if p['comp_obs'] == None:
            p['comp_obs'] = []
        if 'data1' not in p:
            p['data1'] = {}
        if 'data2' not in p:
            p['data2'] = {}
        if 'comp' not in p:
            p['comp'] = {}

        if 'depths' not in p:
            p['depths'] = [""]
        if 'seasons' not in p:
            p['seasons'] = ['DJF', 'MAM', 'JJA', 'SON']
        if 'comp_seasons' not in p:
            p['comp_seasons'] = p['seasons']
        if 'months' not in p:
            p['months'] = [1,2,3,4,5,6,7,8,9,10,11,12]
        if 'comp_months' not in p:
            p['comp_months'] = p['months']
        p['months'] = [str(i) for i in p['months']]
        p['comp_months'] = [str(i) for i in p['comp_months']]
        if 'cmip5_file' not in p:
            p['cmip5_file'] = None 
        if 'cmip5_files' not in p:
            p['cmip5_files'] = []                    
        if p['comp_models'] == 'all':
            p['comp_models'] = list(MODELS)
        if p['comp_cmips'] == 'all':
            p['comp_cmips'] = list(MODELS)
        if 'comp_scale' not in p:
            p['comp_scale'] = p['scale']
        if 'comp_shift' not in p:
            p['comp_shift'] = p['shift']
        if 'extra_scales' not in p:
            p['extra_scales'] = [1] * len(p['extra_variables'])
        if 'extra_comp_scales' not in p:
            p['extra_comp_scales'] = p['extra_scales']
        if 'extra_shifts' not in p:
            p['extra_shifts'] = [0] * len(p['extra_variables'])
        if 'extra_comp_shifts' not in p:
            p['extra_comp_shifts'] = p['extra_shifts'] 

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

        if 'plot_args' not in p:
            p['plot_args'] = {}
               
        if 'comp_dates' not in p:
            p['comp_dates'] = p['dates']
          
        p['model_ID'] = run
        p['experiment'] = experiment
        p['plot_depth'] = 0
        
        def _default_plot_args(projection):
            if projection == 'global_map':
                return {'latmin': 50, 'latmax': 50, 'lonmin': 0, 'lonmax': 360}
            if projection == 'mercator':
                return {'latmin': -80, 'latmax': 80, 'lonmin': 0, 'lonmax': 360}
            if projection == 'polar_map':
                return {'latmin': 45, 'latmax': 80, 'lonmin': 0, 'lonmax': 360, 'lon_0': 180}
            if projection == 'polar_map_south':
                return {'latmin': -80, 'latmax': -45, 'lonmin': 0, 'lonmax': 360, 'lon_0': 180}
            return {}
        default_pargs = _default_plot_args(p['plot_projection'])
        for key in default_pargs:
            if key not in p['plot_args']:
                p['plot_args'][key] = default_pargs[key]
        
        def _fill_args(data):
            p[data]['pcolor_flags'] = []
            p[data]['ax_flags'] = {}
            if 'ax_args' not in p[data]:
                p[data]['ax_args'] = {}
            if 'pcolor_args' not in p[data]:
                p[data]['pcolor_args'] = {}
            if 'title' not in p[data]['ax_args']:
                p[data]['title_flag'] = False
            else:
                p[data]['title_flag'] = True
            
            for key in p[data]['pcolor_args']:
                p[data]['pcolor_flags'].append(key)

            if 'norm' in p[data]['pcolor_args']:
                try:
                    p[data]['pcolor_args']['norm'] = norms[p[data]['pcolor_args']['norm']]
                except:
                    pass 
              

        _fill_args('data1')
        _fill_args('data2')
        _fill_args('comp')
        if 'ncols' not in p['comp']:
            p['comp']['ncols'] = 11        
         

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
    if pl['realm'] == 'atmos':
        pl[datanumber]['ax_args']['ylabel'] = 'Pressure'
    else:
        pl[datanumber]['ax_args']['ylabel'] = 'Depth'

def _zonal_labels(datanumber, pl):
    pl[datanumber]['ax_args']['xlabel'] = 'Latitude'
    pl[datanumber]['ax_args']['xticks'] = np.arange(-80, 81, 20)
        
def filltitle(p):
    def fill(comp):
        if not p['data1']['title_flag']:
            p['data1']['ax_args']['title'] = p['variable'] + ' ' + p['data_type'] + ' ' + p['model_ID'] + ' ' + p['dates']['start_date'] + ' - ' + p['dates']['end_date']
        if not p['data2']['title_flag']:
            p['data2']['ax_args']['title'] = p['variable'] + ' ' + p['data_type'] + ' ' + comp + ' ' + p['comp_dates']['start_date'] + ' - ' + p['comp_dates']['end_date']
        if not p['comp']['title_flag']:
            p['comp']['ax_args']['title'] = p['variable'] + ' ' + p['data_type'] + ' ' + p['model_ID'] + '-' + comp
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
            
    if p['plot_projection'] == 'section':
        _section_labels('data1', p)
        _section_labels('data2', p)
        _section_labels('comp', p)
    if p['plot_projection'] == 'zonal_mean':
        _zonal_labels('data1', p)
        _zonal_labels('data2', p)
        _zonal_labels('comp', p)    
