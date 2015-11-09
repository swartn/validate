import control as con
import os

model_run = 'edr'

defaults = {
            'climatology': True,
            'climatology_dates': {'start_date': '1991-01', 'end_date': '2000-01'},
            'compare_climatology': False,
            
            'trends': True,
            'trends_dates': {'start_date': '1991-01', 'end_date': '2000-01'},
            'compare_trends': False,
            
            'realization': '1',
            #'plot_args': {'fill_continents': True}
            }

plots = [

         {    
          'variable': 'sic',
          'plot_projection': 'polar_map',                     
          },                                
        ]

obs_root = '/raid/ra40/data/ncs/nemo_out/obs4comp/'
obs = {'NO3' : obs_root + 'uncs_orca2_data_data_n_an_nomask.nc',
       'DIC' : obs_root + 'uncs_orca2_data_data_TCO2_nomask.nc',
       'NCHL': obs_root + 'uncs_seawifs_mean_1998_2005.nc',
       'tas': './tas_Amon_CanESM2_historical_r1i1p1_185001-200512.nc'
       }                 
         
if __name__ == "__main__":
       plots_with_files = con.execute(plots, model_run, obs, defaults)
