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
            'climatology': False,
            'climatology_dates': {'start_date': '1991-01', 'end_date': '2000-01'},
            'compare_climatology': False,
            
            'trends': False,
            'trends_dates': {'start_date': '1991-01', 'end_date': '2000-01'},
            'compare_trends': True,
            
            'realization': '1',
            'scale': 1,
            #'plot_args': {'fill_continents': True}
            }

plots = [
 
         {    
          'variable': 'ta',
          'plot_projection': 'section',
          'depth_type': 'plev',                             
          }, 
                                                      
        ]

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
       plots_with_files = con.execute(plots, model_run, obs, defaults)
