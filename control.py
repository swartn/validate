"""
control
===============

.. moduleauthor:: David Fallis
"""



from directory_tools import getfiles, remfiles, getobsfiles
from plotter import loop
from pdforganize import arrange
from defaults import fill

def execute(plots, run, obsroot, defaults, delete):
    """ Calls modules required to find the data, 
        process the data, and output the plots and figures
        
    Parameters
    ----------
    plots : list of dictionaries
    run : string
          model run
    obs : dictionary
          maps variable to name of file with observations
    defaults : dictionary
               any keys will be added to each plot if they are not present
    delete : dictionary
             maps directory name to boolean, will delete the directoy if True
    """
                  
    filled_plots = fill(plots, obs, defaults)
    plots_with_files = getfiles(filled_plots, run) 
    plots_with_obs = getobsfiles(plots_with_files, obsroot)   
    plotnames = loop(plots_with_obs)
    remfiles(**delete)
    arrange(plotnames)
    
        
