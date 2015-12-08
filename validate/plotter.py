"""
plotter
===============

This module contains functions needed to efficiently loop
through all of the specified plots that will be produced.

.. moduleauthor:: David Fallis
"""

import os
import glob

import plotregions as pr
import defaults as dft
import plotcase as pc
import matplotlib.pyplot as plt
from yamllog import log

DEBUGGING = False

def climatology(plot):
    """ Calls the appropriate functions to output the plot
    """
    print 'climatology plot'
    def pregion_standard(pl):
        return {'global_map': (pr.global_map, pc.map_climatology),
                'section': (pr.section, pc.section_climatology),
                'polar_map': (pr.polar_map, pc.map_climatology),
                'polar_map_south': (pr.polar_map_south, pc.map_climatology),
                'mercator': (pr.mercator, pc.map_climatology),
                'time_series': (pr.timeseries, pc.timeseries),
                'zonal_mean': (pr.zonalmean, pc.zonalmean),                
                }[pl]
    func_region, func_case = pregion_standard(plot['plot_projection']) 
    return func_case(plot, func_region) 

    
def compare_climatology(plot):
    """ Calls the appropriate functions to output the plot
    """
    print 'climatology comparison plot'    
    def pregion_comp(pl):
        return {'global_map': (pr.global_map, pc.map_climatology_comparison),
                'section': (pr.section, pc.section_climatology_comparison),
                'polar_map': (pr.polar_map, pc.map_climatology_comparison),
                'polar_map_south': (pr.polar_map_south, pc.map_climatology_comparison),
                'mercator': (pr.mercator, pc.map_climatology_comparison),
                'time_series': (pr.timeseries, pc.timeseries_comparison),
                'zonal_mean': (pr.zonalmean, pc.zonalmean_comparison), 
                'taylor': (pr.taylordiagram, pc.taylor),
                }[pl]
    func_region, func_case = pregion_comp(plot['plot_projection']) 
    return func_case(plot, func_region)
    
def trends(plot):
    """ Calls the appropriate functions to output the plot
    """
    print 'trend plot'
    def pregion_trends(pl):
        return {'global_map': (pr.global_map, pc.map_trends),
                'section': (pr.section, pc.section_trends),
                'polar_map': (pr.polar_map, pc.map_trends),
                'polar_map_south': (pr.polar_map_south, pc.map_trends),
                'mercator': (pr.mercator, pc.map_trends),
                }[pl]
    func_region, func_case = pregion_trends(plot['plot_projection']) 
    return func_case(plot, func_region)   
    
def compare_trends(plot):
    """ Calls the appropriate functions to output the plot
    """
    print 'trend comparison plot'
    def pregion_ct(pl):
        return {'global_map': (pr.global_map, pc.map_trends_comp),
                'section': (pr.section, pc.section_trends_comp),
                'polar_map': (pr.polar_map, pc.map_trends_comp),
                'polar_map_south': (pr.polar_map_south, pc.map_trends_comp),
                'mercator': (pr.mercator, pc.map_trends_comp),
                }[pl]
    func_region, func_case = pregion_ct(plot['plot_projection']) 
    return func_case(plot, func_region)

def _remove_plots():
    """ Removes old plots
    """
    plots_out = []
    old_plots = glob.glob('plots/*.pdf')    
    for f in old_plots:
        os.remove(f)
    old_plots = glob.glob('plots/*.png')    
    for f in old_plots:
        os.remove(f)
        
def makeplot(p, plotnames, func):
    p['plot_type'] = func.__name__
    try:    
        plot_name = func(p)
    except:
        with open('logs/log.txt', 'a') as outfile:
            outfile.write('Failed to plot ' + p['variable'] + ', ' + p['plot_projection'] + ', ' + p['plot_type'] + ', ' + p['comp_model'] + ', at depth:' + str(p['depth']) + '\n\n')
    else:
        p['plot_name'] = plot_name + '.pdf'
        p['png_name'] = plot_name + '.png'    
        if p['pdf']:
            plotnames.append(dict(p))
            log(p)
        if p['png']:
            p['plot_name'] = p['png_name']
            log(p)
        with open('logs/log.txt', 'a') as outfile:
            outfile.write('Successfully plotted ' + p['variable'] + ', ' + p['plot_projection'] + ', ' + p['plot_type'] + ', ' + p['comp_model'] + ', at depth:' + str(p['depth']) + '\n\n')    
    
def makeplot_without_catching(p, plotnames, func):
    p['plot_type'] = func.__name__
    plot_name = func(p)
    p['plot_name'] = plot_name + '.pdf'
    p['png_name'] = plot_name + '.png'

    if p['pdf']:
        plotnames.append(dict(p))
        log(p) 
    if p['png']:
        p['plot_name'] = p['png_name']
        log(p)

def calltheplot(plot, plotnames, ptype):
    funcs = {'climatology': climatology,
             'trends': trends,
             'compare_climatology': compare_climatology,
             'compare_trends': compare_trends,}
    if DEBUGGING:
        makeplot_without_catching(plot, plotnames, funcs[ptype])
    else:
        makeplot(plot, plotnames, funcs[ptype])           

def comp_loop(plot, plotnames, ptype):
    comp = plot['compare']
    if comp['obs']:
        plot['comp_model'] = 'Observations'
        plot['comp_flag'] = 'obs'
        plot['comp_file'] = plot['obs_file']
        calltheplot(plot, plotnames, ptype)
    if comp['cmip5']:
        plot['comp_flag'] = 'cmip5'
        plot['comp_model'] = 'cmip5'
        plot['comp_file'] = plot['cmip5_file']
        calltheplot(plot, plotnames, ptype)
    if comp['model']:
        plot['comp_flag'] = 'model'
        for model in plot['comp_models']:
            plot['comp_model'] = model
            plot['comp_file'] = plot['model_file'][model]
            calltheplot(plot, plotnames, ptype)
    if comp['runid']:
        plot['comp_flag'] = 'runid'
        for i in plot['id_file']:
            plot['comp_model'] = i
            plot['comp_file'] = plot['id_file'][i]
            calltheplot(plot, plotnames, ptype)  
                      
def loop_plot_types(plot, plotnames):
    types = ['climatology', 'trends', 'compare_climatology', 'compare_trends']
    comptypes = ['compare_climatology', 'compare_trends']
    funcs = {'climatology': climatology,
             'trends': trends,
             'compare_climatology': compare_climatology,
             'compare_trends': compare_trends,}
    if plot['plot_projection'] == 'time_series' or plot['plot_projection'] == 'zonal_mean' or plot['plot_projection'] == 'taylor':
        plot['comp_model'] = 'Model'
        calltheplot(plot, plotnames, 'compare_climatology')   
    else:
        for ptype in types:
            if plot[ptype]:
                if ptype in comptypes:
                    comp_loop(plot, plotnames, ptype)
                else:
                    plot['comp_model'] = 'Model'
                    calltheplot(plot, plotnames, ptype)              
            
            
def loop(plots, debug):
    """ Loops though the list of plots and the depths within
        the plots and outputs each to a pdf
        
    Parameters
    ----------
    plots : list of dictionaries
    
    Returns
    -------
    list of tuples with (plotname, plot dictionary, plot type)
    """
    
    global DEBUGGING
    DEBUGGING = debug
    
    #remove old plots
    _remove_plots()
            
    plotnames = []
    for p in plots:
        if p['depths'] == []:
            p['depths'] = [0]
        for d in p['depths']:
            p['depth'] = int(d) 
            loop_plot_types(p, plotnames)
        plt.close('all')             
    return plotnames

        
if __name__ == "__main__":
    pass
