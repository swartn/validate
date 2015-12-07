"""
control
===============
This module has one function 'execute()' which calls functions
from various modules to produce the plots layed out in configure.py


.. moduleauthor:: David Fallis
"""



from directory_tools import getfiles, remfiles, getobsfiles
from plotter import loop
from pdforganize import arrange
from defaults import fill
from check import check_inputs
from cmip import cmip

def execute(plots, run, obsroot=None, cmiproot=None, defaults={}, delete={}, obs={}, load_cmip5=False, check_input=True, debugging=False):
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
    if check_input:
        check_inputs(plots, run, obsroot, cmiproot, obs, defaults, delete)              
    fill(plots, defaults, run)
    getfiles(plots, run) 
    getobsfiles(plots, obsroot)
    cmip(plots, cmiproot, load_cmip5)   
    plotnames = loop(plots, debugging)
    remfiles(**delete)
    arrange(plotnames)
    
        
