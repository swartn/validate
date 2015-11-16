# output log
# Taylor
# compare section
# document
# traverse obs directory
# some funny titles
# min depth for sections



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
          'depths':[20000, 85000, 100000]                              
          }, 
         {    
          'variable': 'ta',
          'plot_projection': 'zonal_mean',
          'trends': False,
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000]                              
          },                                
         {    
          'variable': 'hus',
          'plot_projection': 'mercator',
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
          'variable': 'thetao',
          'plot_projection': 'global_map',
          'depth_type': 'lev',
          'depths': [0,200,500,2000,5000]                                        
          },  
         {    
          'variable': 'so',
          'plot_projection': 'mercator',
          'depth_type': 'lev',
          'depths': [0,200,500,2000,5000],                                        
          }, 
         {    
          'variable': 'thetao',
          'plot_projection': 'section',
          'depth_type': 'lev',                                        
          },         
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
        ]

delete = {
          'del_fldmeanfiles': True,
          'del_mask': True,
          'del_ncstore': True,
          'del_remapfiles': True,
          'del_trendfiles': True,
          'del_zonalfiles': True,
          }
          
obs_root = '/raid/ra40/data/ncs/nemo_out/obs4comp/'
obs = {'tas': './tas_Amon_CanESM2_historical_r1i1p1_185001-200512.nc',
       'ta': '/raid/rc40/data/ncs/obs4comp/20CR/mon/ta_Amon_20CR_historical_ens-mean_187101-201212.nc',
       'tauu': '/raid/rc40/data/ncs/obs4comp/20CR/mon/tauu_Amon_20CR_historical_ens-mean_187101-201212.nc',
       'tauv': '/raid/rc40/data/ncs/obs4comp/20CR/mon/tauv_Amon_20CR_historical_ens-mean_187101-201212.nc',
       'thetao': '/raid/rc40/data/ncs/obs4comp/observations/ocean/woa09/thetao_Omon_WOA09_historical.nc',
       'pr': '/raid/rc40/data/ncs/obs4comp/20CR/mon/pr_Amon_20CR_historical_ens-mean_187101-201212.nc',
       'psl': '/raid/rc40/data/ncs/obs4comp/20CR/mon/psl_Amon_20CR_historical_ens-mean_187101-201212.nc',
       'ua': '/raid/rc40/data/ncs/obs4comp/20CR/mon/ua_Amon_20CR_historical_ens-mean_187101-201212.nc',
       'va': '/raid/rc40/data/ncs/obs4comp/20CR/mon/va_Amon_20CR_historical_ens-mean_187101-201212.nc',
       'chl': '/raid/rc40/data/ncs/obs4comp/observations/ocean/chl_Omon_SEAWIFS_historical_198801-200512-mean.nc',
       'tos': '/raid/rc40/data/ncs/obs4comp/observations/ocean/tos_Omon_NOAA-OI-SST_historical_198101-201502.nc',
       'no3': '/raid/rc40/data/ncs/obs4comp/observations/ocean/woa09/no3_OcnBgchem_WOA09_historical.nc',
       'so': '/raid/rc40/data/ncs/obs4comp/observations/ocean/woa09/so_Omon_WOA09_historical.nc',      
       }                 
         
if __name__ == "__main__":
       plots_with_files = con.execute(plots, model_run, obs, defaults, delete)
