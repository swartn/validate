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
            'climatology': False,
            'climatology_dates': {'start_date': '1850-01', 'end_date': '2000-01'},
            'compare_climatology': True,

            'trends': False,
            'trends_dates': {'start_date': '1991-01', 'end_date': '2000-01'},
            'compare_trends': True,

            'realization': '1',
            'scale': 1,
            #'plot_args': {'fill_continents': True}
            'pdf': True,
            }

plots = [
 
         {    
          'variable': 'ta',
          'plot_projection': 'section',
#          'depth_type': 'plev',
#          'depths':[20000, 8500, 10000],
          'compare': {'cmip5': True,
                      'model': True,
                      'obs': True,},
          'comp_models': ['CanCM4', 'NorESM1-M'],
          'frequency': 'mon'
          },          
        ]

delete = {
          'del_fldmeanfiles': True,
          'del_mask': True,
          'del_ncstore': True,
          'del_remapfiles': True,
          'del_trendfiles': True,
          'del_zonalfiles': True,
          'del_ENS_MEAN_cmipfiles': True,
          'del_ENS_STD_cmipfiles': True,
          'del_cmipfiles': False,
          }
          
obsroot = '/raid/rc40/data/ncs/obs4comp'               
cmiproot = '/raid/ra40/CMIP5_OTHER_DOWNLOADS/'
        
if __name__ == "__main__":
       plots_with_files = con.execute(plots, model_run, obsroot, cmiproot, defaults, delete, , debugging=True)
