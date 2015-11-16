import control as con
import os

model_run = 'edr'

#os.system('ln -s /raid/ra40/CMIP5_OTHER_DOWNLOADS/tas/tas_Amon_CanESM2_historical_r1i1p1_185001-200512.nc .')

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
          }
                  
obs_root = '/raid/ra40/data/ncs/nemo_out/obs4comp/'
obs = {'NO3' : obs_root + 'uncs_orca2_data_data_n_an_nomask.nc',
       'DIC' : obs_root + 'uncs_orca2_data_data_TCO2_nomask.nc',
       'NCHL': obs_root + 'uncs_seawifs_mean_1998_2005.nc',
       'tas': './tas_Amon_CanESM2_historical_r1i1p1_185001-200512.nc'
       }
       

if __name__ == "__main__":
       plots_with_files = con.execute(plots, model_run, obs, defaults, delete)
