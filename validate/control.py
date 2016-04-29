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
import constants
          
def execute(options, **kwargs):
    """ Gets the configuration and contains the function that
        calls modules required to find the data,
        process the data, and output the plots and figures.

    """
    def plot(run=None, experiment='historical', direct_data_root= "", data_root="", observations_root=".", cmip5_root="", processed_cmip5_root="", output_root=None, cmip5_means='', ignorecheck=False, external_root="", debugging=False, plots=[], defaults={}, delete={}, obs={}, **kwargs):
        """Calls modules required to find the data,
           process the data, and output the plots and figures
        """
        constants.run = run
        constants.experiment = experiment
        constants.direct_data_root = direct_data_root
        constants.data_root = data_root
        constants.observations_root = observations_root
        constants.cmip5_root = cmip5_root
        constants.processed_cmip5_root = processed_cmip5_root
        constants.output_root = output_root
        constants.cmip5_means = cmip5_means
        constants.external_root = external_root
        constants.debugging = debugging

#        check_inputs() needs to be updated to match the latest changes to the configuration
#        if not ignorecheck:
#            # check that the configuartion is valid
#            check_inputs(plots, run, experiment, observations_root, cmip5_root, obs, defaults, delete)

        # fill options not specified using the defaults
        print 'applying default values...'
        fill(plots, run, experiment, defaults)
        
        # find and modify if necessary the files for the model and experiment
        print 'finding model files...'
        getfiles(plots, direct_data_root, data_root, run, experiment)
        
        # find the observations files
        print 'finding observed files...'
        getobsfiles(plots, observations_root)
        
        # find the cmip5 files
        print 'finding cmip5 files...'
        cmip(plots, cmip5_root, cmip5_means, experiment)
        
        # find the files from other runIds for comparison
        print 'finding other model files...'
        getidfiles(plots, data_root, experiment)
        
        # THIS IS WHERE THE PLOTS ARE CREATED
        print 'creating plots...'
        plotnames = loop(plots, debugging)
        
        # cleanup files and directories created during processing
        print 'cleaning up...'
        remfiles(**delete)
        
        # organize plots in joined.pdf file
        print 'merging plots...'
        arrange(plotnames)
        
        #create tarfile and move to output
        move_tarfile(output_root, run, experiment)


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
        print 'WARNING: No configuration file was found in the current directory. Using default.'
    
    # overwrite the configuration with input given in the execution arguments
    for key in options:
        settings[key] = options[key]
    if 'realization' in options:
        try:
            settings['defaults']['realization'] = options['realization']
        except KeyError:
            settings['defaults'] = {}
            settings['defaults']['realization'] = options['realization']
    
    plot(**settings)
