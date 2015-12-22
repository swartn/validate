"""
control
===============
This module has one function 'execute()' which calls functions
from various modules to produce the plots layed out in conf.yaml


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
    """ Gets the configuration and contains the function that
        calls modules required to find the data,
        process the data, and output the plots and figures.

    """
    def plot(run=None, experiment='historical', observations_root="", cmip5_root="", loadcmip5=False, ignorecheck=False, debugging=False, plots=[], defaults={}, delete={}, obs={}, **kwargs):
        """Calls modules required to find the data,
           process the data, and output the plots and figures
        """
        if not ignorecheck:
            # check that the configuartion is valid
            check_inputs(plots, run, experiment, observations_root, cmip5_root, obs, defaults, delete)
        
        # fill options not specified using the defaults
        fill(plots, defaults, run, experiment)
        
        # find and modify if necessary the files for the model and experiment
        getfiles(plots, run, experiment)
        
        # find the observations files
        getobsfiles(plots, observations_root)
        
        # find the cmip5 files
        cmip(plots, cmip5_root, experiment, loadcmip5)
        
        # find the files from other runIds fir comparison
        getidfiles(plots, experiment)
        
        # THIS IS WHERE THE PLOTS ARE CREATED
        plotnames = loop(plots, debugging)
        
        # cleanup files and directories created during processing
        remfiles(**delete)
        
        # organize plots in joined.pdf file
        arrange(plotnames)


    # if conf.yaml exists in the current directory use that for the configuration
    try:
        with open('conf.yaml', 'r') as f:
            settings = yaml.load(f)
    # if it does not exist then use the default file in the package
    except IOError:
        import pkg_resources
        path = os.path.join('configure', 'conf.yaml')
        confile = pkg_resources.resource_filename('validate', path)
        with open(confile, 'r') as f:
            settings = yaml.load(f)
    
    # overwrite the configuration with input given in the exection arguments
    for key in options:
        settings[key] = options[key]
    
    plot(**settings)
