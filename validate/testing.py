"""
configure
===============
This module is used to configure the output of running the validation package.
Several parameters can be defined to be passed to the control.py module.

model_run : A three letter string associated with the model to be tested.             
            
            example:             
                model_run = 'edr'

plots : A list of dictionaries specifying the plots to be produced. At a minimum
        to produce a plot, the dictionary must have a 'variable' and 'plot_projection'
        specified. The rest of the keys are options for customizing the plots.
        Possible keys:
         'variable' : The variable to be plotted.
                      ex. 'ta'
         'plot_projection' : The plot to be made.
                             options:
                              'global_map'
                              'mercator'
                              'polar_map'
                              'polar_map_south'
                              'section'
                              'time_series'
                              'zonal_mean'
                              'taylor'
         'climatology' : Boolean to produce climatology plot.
         'compare_climatology' : Boolean to produce climatology comparison.
         'trends' : Boolean to produce trends plot.
         'compare_trends' : Boolean to produce trends comparison.
         'compare' : A dictionary mapping comparison options
                     'obs'
                     'cmip5',
                     'model'
                     'runid'
                     to booleans
         'comp_models' : A list of strings of cmip5 model names to compare
         'comp_ids' : A list of strings of run IDs to compare
         'climatology_dates' : A dictionary mapping
                               'start_date'
                               'end_date'
                               to the dates to use in the climatology plots.
                               Should be of the form 'yyyy-mm-dd' or 'yyyy-mm'
                               ex. {'start_date': '1970-01-01', 'end_date': '1990-01'}
         'trends_dates' : A dictionary mapping
                          'start_date'
                          'end_date'
                          to the dates to use in the trends plots.
                          Should be of the form 'yyyy-mm-dd' or 'yyyy-mm'
                          ex. {'start_date': '1970-01-01', 'end_date': '1990-01'}
         'realization' : integer or string of realizaion number
                         ex. '1'
         'depth_type' : string of the depth type used for the variable in the netCDF file.
                        required for depths to be specified and for section plots
                        ex 'plev'
         'depths' : list of integers of the depths to be plotted in the units specified
                    under 'depth_type'
                    ex. [10000, 2500, 1000]
         'frequency' : time interval of data
                       ex. 'mon'
         'scale' : float
                   the data is mulitiplied by the scalar value
         'plot_args' : dictionary with some boolean options for the map plots
                       options:
                        'fill_continents'
                        'draw_parallels'
                        'draw_meridians'
                       ex. {'fill_continents': True}
         'data1_args' : A dictionary specifying the arguments for the model data plot
         'data2_args' : A dictionary specifying the arguments for the observations data plot.
                        It uses the came keys as 'data1_args'
         'comp_args' : A dictionary specifying the arguments for the comparsson plot of
                       the model and observations. It uses the same keys as 'data1_args'
         'ifile' : Can be used to specify a netCDF filename, including the directoy path
                   to be used for this plot.
         'obs_file' : Can be used to specify a filename, including the directory path, 
                       to be used for the observation data.
                        
                        
                        
         
                               

delete : A dictionary mapping directories to booleans. The booleans are set
         to True if the temporary files should be deleted afeter the plots
         have been produced. Any keys not specified will be treated as True.
         Possible keys:
          'del_fldmeanfiles'
          'del_mask'
          'del_ncstore'
          'del_remapfiles'
          'del_trendfiles'
          'del_zonalfiles'
         
         example:
             delete = {
                 'del_fldmeanfiles': True,
                 'del_mask': True,
                 'del_ncstore': False,
             }             

obs : A dictionary mapping the name of the variable to the name of a netCDF
      file with observations data for that variable. The name must include
      the filepath. This will be overwritten if a file is specified in the 
      plot dictionary within plots.
      
      example:
          obs = {
              'no3' : '/raid/ra40/data/ncs/obs4comp/uncs_orca2_data_data_n_an_nomask.nc',
       }          

obsroot : A string naming the directory where netCDF observation files can 
           be found if they were not specifically specified in the plot or the
           obs dictionary. To be found the files in the directory can be within 
           subdirectories, but the filenames must begin with the variable
           name followed by an underscore: 'var_*'
           
           example:
               obsroot = '/raid/ra40/data/ncs/obs4comp/'                        
                      

"""

import control as con
import os

model_run = 'edr'

defaults = {
            'climatology': True,
            'climatology_dates': {'start_date': '1980-01', 'end_date': '2000-01'},
            'compare_climatology': True,

            'trends': False,
            'trends_dates': {'start_date': '1991-01', 'end_date': '2000-01'},
            'compare_trends': False,

            'realization': '1',
            'scale': 1,
            #'plot_args': {'fill_continents': True}
            'pdf': True,
            }

plots = [
 
         {    
          'variable': 'ta',
          'plot_projection': 'zonal_mean',
          'depth_type': 'plev',
          'depths':[20000, 8500, 100000],
          'compare': {'cmip5': False,
                      'model': False,
                      'obs': True,
                      'runid': True,},
          'comp_models': ['CanCM4', 'NorESM1-M'],
          'comp_ids': ['cvu'],
          'frequency': 'mon',
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
       plots_with_files = con.execute(plots, model_run, obsroot, cmiproot, defaults, delete, debugging=True)
