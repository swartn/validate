"""
control
===============
This module has one function 'execute()' which calls functions
from various modules to produce the plots layed out in configure.py


.. moduleauthor:: David Fallis
"""
import sys
import yaml
import os
from directory_tools import getfiles, remfiles, getobsfiles, getidfiles
from plotter import loop
from pdforganize import arrange
from defaults import fill
from check import check_inputs
from cmip import cmip
def execute(options, **kwargs):
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
    def plot(run=None, experiment='historical', observations_root="", cmip5_root="", loadcmip5=False, ignorecheck=False, debugging=False, plots=[], defaults={}, delete={}, obs={}, **kwargs):
        if not ignorecheck:
            check_inputs(plots, run, experiment, observations_root, cmip5_root, obs, defaults, delete)              
        fill(plots, defaults, run)
        getfiles(plots, run) 
        getobsfiles(plots, observations_root)
        cmip(plots, cmip5_root, experiment, loadcmip5)  
        getidfiles(plots)
        plotnames = loop(plots, debugging)
        remfiles(**delete)
        arrange(plotnames)         

    try:
        with open('configure/conf.yaml', 'r') as f:
            settings = yaml.load(f)
    except IOError:
        import pkg_resources
        path = os.path.join('configure', 'conf.yaml')
        confile = pkg_resources.resource_filename('validate', path)
        with open(confile, 'r') as f:
            settings = yaml.load(f)

    for key in settings:
        if key in options:
            setting[key] = options[key]
    plot(**settings)
