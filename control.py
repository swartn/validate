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
                  
    fill(plots, defaults)
    getfiles(plots, run) 
    getobsfiles(plots, obsroot)   
    plotnames = loop(plots)
    remfiles(**delete)
    arrange(plotnames)
    
        
