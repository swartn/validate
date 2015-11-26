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
            'compare_climatology': False,

            'trends': False,
            'trends_dates': {'start_date': '1991-01', 'end_date': '2000-01'},
            'compare_trends': False,

            'realization': '1',
            'scale': 1,
            #'plot_args': {'fill_continents': True}
            'pdf': True,
            'png': True,
            }

plots = [

         {    
          'variable': 'ta',
          'plot_projection': 'mercator',
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000],                                               
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
