import control as con


model_run = 'aaa'


defaults = {
            'climatology': True,
            'climatology_dates': {'start_date': '1920-01-01', 'end_date': '1990-01-01'},
            'compare_climatology': False,
            
            'trends': True,
            'trends_dates': {'start_date': '1920-01-01', 'end_date': '1990-01-01'},
            'compare_trends': False,
            
            'realization': '1',
            }
plots = [ 


         {    
          'variable': 'no3',
          'plot_projection': 'mercator',
          'data1_args': {'pcolor_args':{'vmin': 0.02, 'vmax': 0.1}},                                
          },                                                                                       
        ]
        
obs_root = '/raid/ra40/data/ncs/nemo_out/obs4comp/'
obs = {'NO3' : obs_root + 'uncs_orca2_data_data_n_an_nomask.nc',
       'DIC' : obs_root + 'uncs_orca2_data_data_TCO2_nomask.nc',
       'NCHL': obs_root + 'uncs_seawifs_mean_1998_2005.nc',
       }

if __name__ == "__main__":
       plots_with_files = con.execute(plots, model_run, obs, defaults)
