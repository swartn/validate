"""
plotter
===============

.. moduleauthor:: David Fallis
"""

import os
import glob

import plotregions as pr
import defaults as dft
import plotcase as pc
import matplotlib.pyplot as plt

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
                'time_series': (pr.timeseries, pc.timeseries)
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

def makeplot(p, plotnames, func):
    p['plot_type'] = func.__name__
    try:    
        p['plot_name'] = func(p)
    except:
        with open('logs/log.txt', 'a') as outfile:
            outfile.write('Failed to plot ' + p['variable'] + ', ' + p['plot_projection'] + ', ' + p['plot_type'] + ', at depth:' + str(p['depth']) + '\n\n')
    else:

        plotnames.append(dict(p))
        with open('logs/log.txt', 'a') as outfile:
            outfile.write('Successfully plotted ' + p['variable'] + ', ' + p['plot_projection'] + ', ' + p['plot_type'] + ', at depth:' + str(p['depth']) + '\n\n')    
    
def makeplot_without_catching(p, plotnames, func):
    p['plot_type'] = func.__name__
    p['plot_name'] = func(p)
    plotnames.append(dict(p))
    
def loop_plot_types(plot, plotnames):
    types = ['climatology', 'trends', 'compare_climatology', 'compare_trends']
    funcs = {'climatology': climatology,
             'trends': trends,
             'compare_climatology': compare_climatology,
             'compare_trends': compare_trends,}
    for ptype in types:
        if plot[ptype]:
            makeplot(plot, plotnames, funcs[ptype])
            #makeplot_without_catching(plot, plotnames, funcs[ptype])
            
            
def loop(plots):
    """ Loops though the list of plots and the depths within
        the plots and outputs each to a pdf
        
    Parameters
    ----------
    plots : list of dictionaries
    
    Returns
    -------
    list of tuples with (plotname, plot dictionary, plot type)
    """
    
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
    ifile_ptrc = ('/raid/ra40/data/ncs/nemo_out/nue/' +
                  'mc_nue_1m_20000101_20001231_ptrc_t.nc.001')    
    plots = [
         {'ifile': ifile_ptrc,
          'variable': 'DIC',
          'plot_projection': 'global_map',
          'plot_type': 'standard',
          'plot _args': {'data1_args': {'pcolor_args': {'vmin' : 1800, 'vmax' : 2300}}
                         }                       
          },

         {'ifile' : ifile_ptrc,
          'variable' : 'NO3',
          'plot_projection' : 'global_map',
          'plot_type': 'comparison',          
          },
         ]
    loop(plots)

