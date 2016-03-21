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
import matplotlib as mpl
mpl.use('AGG')
from directory_tools import getfiles, remfiles, getobsfiles, getidfiles, cmip, move_tarfile
from plot_iterator import loop
from pdf_organizer import arrange
from defaults import fill
from syntax_check import check_inputs
          
def execute(options, **kwargs):
    """ Gets the configuration and contains the function that
        calls modules required to find the data,
        process the data, and output the plots and figures.

    """
    def plot(run=None, experiment='historical', direct_data_root= "", data_root="", observations_root="", cmip5_root="", output_root=None, cmip5_means='', loadcmip5=False, ignorecheck=False, debugging=False, plots=[], defaults={}, delete={}, obs={}, **kwargs):
        """Calls modules required to find the data,
           process the data, and output the plots and figures
        """
#        if not ignorecheck:
#            # check that the configuartion is valid
#            check_inputs(plots, run, experiment, observations_root, cmip5_root, obs, defaults, delete)
        
        # fill options not specified using the defaults
        fill(plots, run, experiment, defaults)
        
        # find and modify if necessary the files for the model and experiment
        getfiles(plots, direct_data_root, data_root, run, experiment)
        
        # find the observations files
        getobsfiles(plots, observations_root)
        
        # find the cmip5 files
        cmip(plots, cmip5_root, cmip5_means, experiment, loadcmip5)
        
        # find the files from other runIds for comparison
        getidfiles(plots, data_root, experiment)
        
        # THIS IS WHERE THE PLOTS ARE CREATED
        plotnames = loop(plots, debugging)
        
        # cleanup files and directories created during processing
        remfiles(**delete)
        
        # organize plots in joined.pdf file
        arrange(plotnames)
        
        #create tarfile and move to output
        move_tarfile(output_root)


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
    
    # overwrite the configuration with input given in the execution arguments
    for key in options:
        settings[key] = options[key]
    
    plot(**settings)
