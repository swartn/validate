# output log
# Taylor
# document
# min depth for sections
# cmip
# tests

import control as con
import os

model_run = 'edr'

defaults = {
            'climatology': True,
            'climatology_dates': {'start_date': '1991-01', 'end_date': '2000-01'},
            'compare_climatology': True,

            'trends': True,
            'trends_dates': {'start_date': '1991-01', 'end_date': '2000-01'},
            'compare_trends': True,

            'realization': '1',
            'scale': 1,
            #'plot_args': {'fill_continents': True}
            }

plots = [
         {    
          'variable': 'ta',         
          'plot_projection': 'mercator',
          'climatology': True,
          'climatology_dates': {'start_date': '1985-01', 'end_date': '2000-01'}, 
          'trends': True,
          'trends_dates': {'start_date': '1991-01', 'end_date': '2000-01'},                   
          'compare_climatology': True,   
          'compare_trends': True, 
          'realization': '1',
          'data1_args': {'climatology_args': {'pcolor_args': {'vmin': 250, 'vmax': 300},
                                              'ax_args': {'title': 'The title'}},
                         'trends_args':      {}},
          'data2_args': {},
          'comp_args': {},
          'plot_args': {'fill_continents': True},                                                       
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000],
          'frequency': 'mon'                             
          }, 
         {    
          'variable': 'ta',
          'plot_projection': 'time_series',
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000],  
          'compare_climatology': False,
          'trends': False,  
          'compare_trends': False,                                                
          }, 
         {    
          'variable': 'ta',
          'plot_projection': 'zonal_mean',
          'trends': False,
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000], 
          'compare_climatology': False,
          'trends': False,  
          'compare_trends': False,                                        
          },                                
         {    
          'variable': 'hus',
          'plot_projection': 'mercator',
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000] ,                             
          }, 
        
         {    
          'variable': 'ta',
          'plot_projection': 'section',
          'depth_type': 'plev',                            
          },           
         {    
          'variable': 'hus',
          'plot_projection': 'section',
          'depth_type': 'plev',                  
          },  
          
         {    
          'variable': 'thetao',
          'plot_projection': 'global_map',
          'depth_type': 'lev',
          'depths': [0,2000,5000],  
          'compare_climatology': False, 
          'compare_trends': False,                                         
          },  
         {    
          'variable': 'so',
          'plot_projection': 'mercator',
          'depth_type': 'lev',
          'depths': [0,2000,5000], 
          'compare_climatology': False,
          'compare_trends': False,                                                     
          }, 
         {    
          'variable': 'thetao',
          'plot_projection': 'section',
          'depth_type': 'lev', 
          'compare_climatology': False, 
          'compare_trends': False,                                                     
          },         
         {    
          'variable': 'sit',
          'plot_projection': 'polar_map', 
          'plot_args': {'fill_continents': True},
          'compare_climatology': False,
          'compare_trends': False,                                                              
          }, 
         {    
          'variable': 'sit',
          'plot_projection': 'polar_map_south',
          'plot_args': {'fill_continents': True} ,
          'compare_climatology': False, 
          'compare_trends': False,                                                    
          }, 
        ]

delete = {
          'del_fldmeanfiles': True,
          'del_mask': True,
          'del_ncstore': True,
          'del_remapfiles': True,
          'del_trendfiles': True,
          'del_zonalfiles': True,
          }
          
obsroot = '/raid/rc40/data/ncs/obs4comp'               
         
if __name__ == "__main__":
       plots_with_files = con.execute(plots, model_run, obsroot, defaults, delete)
