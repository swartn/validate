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
         'climatology' : Boolean to produce climatology plot.
         'compare_climatology' : Boolean to produce climatology comparison.
         'trends' : Boolean to produce trends plot.
         'compare_trends' : Boolean to produce trends comparison.
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
         'comp_file' : Can be used to specify a filename, including the directory path, 
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


.. moduleauthor:: David Fallis
"""


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
          'variable': 'ta',
          'plot_projection': 'global_map',
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000]                              
          },           
         {    
          'variable': 'hus',
          'plot_projection': 'global_map',
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000]                              
          },
         {    
          'variable': 'ua',
          'plot_projection': 'global_map',
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000]                              
          },           
         {    
          'variable': 'va',
          'plot_projection': 'global_map',
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000]                              
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
          'variable': 'ua',
          'plot_projection': 'section',
          'depth_type': 'plev',                  
          },           
         {    
          'variable': 'va',
          'plot_projection': 'section',
          'depth_type': 'plev',                   
          },
         {    
          'variable': 'tas',
          'plot_projection': 'global_map',                             
          }, 
         {    
          'variable': 'huss',
          'plot_projection': 'global_map',                             
          }, 
         {    
          'variable': 'uas',
          'plot_projection': 'global_map',                             
          }, 
         {    
          'variable': 'vas',
          'plot_projection': 'global_map',                             
          }, 
         {    
          'variable': 'sfcWind',
          'plot_projection': 'global_map',                             
          }, 
#         {    
#          'variable': 'pr',
#          'plot_projection': 'global_map',                             
#          }, 
         {    
          'variable': 'psl',
          'plot_projection': 'global_map',                             
          }, 


         {    
          'variable': 'thetao',
          'plot_projection': 'global_map',
          'depth_type': 'lev',
          'depths': [0,200,500,2000,5000]                                        
          },  
         {    
          'variable': 'so',
          'plot_projection': 'global_map',
          'depth_type': 'lev',
          'depths': [0,200,500,2000,5000],                                        
          }, 
         {    
          'variable': 'uo',
          'plot_projection': 'global_map',
          'depth_type': 'lev',
          'depths': [0,200,500,2000,5000],                                        
          }, 
         {    
          'variable': 'vo',
          'plot_projection': 'global_map',
          'depth_type': 'lev',
          'depths': [0,200,500,2000,5000],                                        
          },  
          
          
         {    
          'variable': 'thetao',
          'plot_projection': 'section',
          'depth_type': 'lev',                                       
          },  
         {    
          'variable': 'so',
          'plot_projection': 'section',
          'depth_type': 'lev',                                     
          }, 
         {    
          'variable': 'uo',
          'plot_projection': 'section', 
          'depth_type': 'lev',                                      
          }, 
         {    
          'variable': 'vo',
          'plot_projection': 'section', 
          'depth_type': 'lev',                                      
          }, 
          
          
         {    
          'variable': 'intdic',
          'plot_projection': 'global_map',
          'depth_type': 'lev',
          'depths': [0,200,500,2000,5000],                                        
          },  
         {    
          'variable': 'no3',
          'plot_projection': 'global_map',
          'depth_type': 'lev',
          'depths': [0,200,500,2000,5000],                                        
          }, 
         {    
          'variable': 'ph',
          'plot_projection': 'global_map',
          'depth_type': 'lev',
          'depths': [0,200,500,2000,5000],                                        
          }, 
         {    
          'variable': 'talk',
          'plot_projection': 'global_map',
          'depth_type': 'lev',
          'depths': [0,200,500,2000,5000],                                        
          }, 

#         {    
#          'variable': 'intdic',
#          'plot_projection': 'section',
#          'depth_type': 'lev',                                       
#          },  
#         {    
#          'variable': 'no3',
#          'plot_projection': 'section',
#          'depth_type': 'lev',                                     
#          }, 
#         {    
#          'variable': 'ph',
#          'plot_projection': 'section',
#          'depth_type': 'lev',                                       
#          }, 
#         {    
#          'variable': 'talk',
#          'plot_projection': 'section',
#          'depth_type': 'lev',                                       
#          }, 



         {    
          'variable': 'zooc',
          'plot_projection': 'global_map',                                        
          },  
         {    
          'variable': 'phyc',
          'plot_projection': 'global_map',                                       
          },
#         {    
#          'variable': 'zooc',
#          'plot_projection': 'section',                                       
#          }, 
#         {    
#          'variable': 'phyc',
#          'plot_projection': 'section',                                       
#          }, 
 
 
         {    
          'variable': 'chl',
          'plot_projection': 'global_map',                                       
          },  
         {    
          'variable': 'epc100',
          'plot_projection': 'global_map',                                      
          }, 
         {    
          'variable': 'fgco2',
          'plot_projection': 'global_map',                                       
          }, 
         {    
          'variable': 'dpco2',
          'plot_projection': 'global_map',                                       
          }, 
          
          
          
          
         {    
          'variable': 'cLeaf',
          'plot_projection': 'global_map',                                       
          },  
         {    
          'variable': 'cLitter',
          'plot_projection': 'global_map',                                      
          }, 
         {    
          'variable': 'cRoot',
          'plot_projection': 'global_map',                                       
          }, 
         {    
          'variable': 'cSoil',
          'plot_projection': 'global_map',                                       
          },          
         {    
          'variable': 'cVeg',
          'plot_projection': 'global_map',                                       
          },  
         {    
          'variable': 'cWood',
          'plot_projection': 'global_map',                                      
          }, 
         {    
          'variable': 'evspsblsoi',
          'plot_projection': 'global_map',                                       
          }, 
         {    
          'variable': 'evspsblveg',
          'plot_projection': 'global_map',                                       
          }, 
         {    
          'variable': 'fLitterSoil',
          'plot_projection': 'global_map',                                       
          },  
         {    
          'variable': 'fVegLitter',
          'plot_projection': 'global_map',                                      
          }, 
         {    
          'variable': 'gpp',
          'plot_projection': 'global_map',                                       
          }, 
         {    
          'variable': 'lai',
          'plot_projection': 'global_map',                                       
          }, 
         {    
          'variable': 'mrfso',
          'plot_projection': 'global_map',                                       
          },  
         {    
          'variable': 'mrlsl',
          'plot_projection': 'global_map',                                      
          }, 
         {    
          'variable': 'mrro',
          'plot_projection': 'global_map',                                       
          }, 
         {    
          'variable': 'mrros',
          'plot_projection': 'global_map',                                       
          }, 
         {    
          'variable': 'nbp',
          'plot_projection': 'global_map',                                       
          },  
         {    
          'variable': 'nep',
          'plot_projection': 'global_map',                                      
          }, 
         {    
          'variable': 'npp',
          'plot_projection': 'global_map',                                       
          }, 
         {    
          'variable': 'prveg',
          'plot_projection': 'global_map',                                       
          },           
         {    
          'variable': 'ra',
          'plot_projection': 'global_map',                                       
          },  
         {    
          'variable': 'rGrowth',
          'plot_projection': 'global_map',                                      
          }, 
         {    
          'variable': 'rh',
          'plot_projection': 'global_map',                                       
          }, 
         {    
          'variable': 'rMaint',
          'plot_projection': 'global_map',                                       
          },
         {    
          'variable': 'tran',
          'plot_projection': 'global_map',                                       
          }, 
         {    
          'variable': 'tsl',
          'plot_projection': 'global_map',                                       
          }, 
          
#         {    
#          'variable': 'sic',
#          'plot_projection': 'polar_map',                                       
#          }, 
#         {    
#          'variable': 'sic',
#          'plot_projection': 'polar_map_south',                                       
#          }, 
         {    
          'variable': 'sit',
          'plot_projection': 'polar_map', 
          'plot_args': {'fill_continents': True}                                                
          }, 
         {    
          'variable': 'sit',
          'plot_projection': 'polar_map_south',
          'plot_args': {'fill_continents': True}                                       
          }, 
#         {    
#          'variable': 'snd',
#          'plot_projection': 'polar_map',                                       
#          }, 
#         {    
#          'variable': 'snd',
#          'plot_projection': 'polar_map_south',                                       
#          }, 
         {    
          'variable': 'tsice',
          'plot_projection': 'polar_map', 
          'plot_args': {'fill_continents': True}                                                  
          }, 
         {    
          'variable': 'tsice',
          'plot_projection': 'polar_map_south',  
          'plot_args': {'fill_continents': True}                                                 
          },                                                                                                                                                                                                                    
        ]

delete = {
          'del_fldmeanfiles': True,
          'del_mask': True,
          'del_ncstore': True,
          'del_remapfiles': True,
          'del_trendfiles': True,
          'del_zonalfiles': False,
          'del_cmipfiles': False,
          'del_ENS_MEAN_cmipfiles': True,
          'del_ENS_STD_cmipfiles': True,
          }
                  
obsroot = '/raid/ra40/data/ncs/nemo_out/obs4comp/'
obs = {'NO3' : obs_root + 'uncs_orca2_data_data_n_an_nomask.nc',
       'DIC' : obs_root + 'uncs_orca2_data_data_TCO2_nomask.nc',
       'NCHL': obs_root + 'uncs_seawifs_mean_1998_2005.nc',
       'tas': './tas_Amon_CanESM2_historical_r1i1p1_185001-200512.nc'
       }

output = {'pdf': True,
          'png': True,}       

if __name__ == "__main__":
       plots_with_files = con.execute(plots, model_run, obs, defaults, delete, output)
