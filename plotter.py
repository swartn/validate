import os
import glob

import plotregions as pr
import defaults as dft
import plotcase as pc
import matplotlib.pyplot as plt

def _climatology(plot):
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
    return func_case(plot, func_region), 

    
def _compare_climatology(plot):
    print 'climatology comparison plot'    
    def pregion_comp(pl):
        return {'global_map': (pr.global_map, pc.map_climatology_comparison),
                'section': (pr.section, pc.section_climatology_comparison),
                'polar_map': (pr.polar_map, pc.map_climatology_comparison),
                'polar_map_south': (pr.polar_map_south, pc.map_climatology_comparison),
                'mercator': (pr.mercator, pc.map_climatology_comparison),
                }[pl]
    func_region, func_case = pregion_comp(plot['plot_projection']) 
    return func_case(plot, func_region),
    
def _trends(plot):
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
    return func_case(plot, func_region),   
    
def _compare_trends(plot):
    print 'trend comparison plot'
    def pregion_ct(pl):
        return {'global_map': (pr.global_map, pc.map_trends_comp),
                #'section': (pr.section, pc.section_trends_comp),
                'polar_map': (pr.polar_map, pc.map_trends_comp),
                'polar_map_south': (pr.polar_map_south, pc.map_trends_comp),
                'mercator': (pr.mercator, pc.map_trends_comp),
                }[pl]
    func_region, func_case = pregion_ct(plot['plot_projection']) 
    return func_case(plot, func_region),

def loop(plots):
    #outputs the plots as pdfs
    
    #remove old plots
    plots_out = []
    old_plots = glob.glob('plots/*.pdf')    
    for f in old_plots:
        os.remove(f)
            
    plotnames = []
    for p in plots:
        if p['depths'] == []:
            p['depth'] = 0
            if p['climatology'] == True:
                plotnames.append((_climatology(p), dict(p), 'climatology'))
            if p['trends'] == True:
                plotnames.append((_trends(p), dict(p), 'trends'))
            if p['compare_climatology'] == True:
                plotnames.append((_compare_climatology(p), dict(p), 'compare_climatology'))
            if p['compare_trends'] == True:
                plotnames.append((_compare_trends(p), dict(p), 'compare_trends'))
        else:
            for d in p['depths']:
                p['depth'] = int(d)
                if p['climatology'] == True:
                    plotnames.append((_climatology(p), dict(p), 'climatology'))
                if p['trends'] == True:
                    plotnames.append((_trends(p), dict(p), 'trends'))
                if p['compare_climatology'] == True:
                    plotnames.append((_compare_climatology(p), dict(p), 'compare_climatology'))
                if p['compare_trends'] == True:
                   plotnames.append((_compare_trends(p), dict(p), 'compare_trends'))                
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

