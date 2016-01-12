.. _mercator:

Mercator Projection
===================

For this example we want to make a color map comparison between
the edr run ID and CanESM2 for the atmospheric surface temperature
climatology between 1980 and 1995.

.. image:: images/tas_mercator_climatology_comparison_CanESM20.png

First use the command:

.. code-block:: bash

    validate-configure

Then edit the conf.yaml file to the following:

.. code-block:: yaml

    run: 'edr'
    experiment: 'historical'

    defaults:
                climatology_dates:
                  start_date: '1980-01'
                  end_date: '1995-01'
                png: True

    plots:    
            - variable: 'tas'
              plot_projection: 'mercator'
              climatology: False
              compare_climatology: True
              compare: 
                  model: True
              comp_models: 
                - CanESM2

    delete:
              del_fldmeanfiles: True
              del_mask: True
              del_ncstore: True
              del_remapfiles: True
              del_trendfiles: True
              del_zonalfiles: True
              del_ENS_MEAN_cmipfiles: True
              del_ENS_STD_cmipfiles: True
              del_cmipfiles: False
             
    observations_root: '/raid/rc40/data/ncs/obs4comp'
    cmip5_root: '/raid/ra40/CMIP5_OTHER_DOWNLOADS/'

Save the file and then use the command:

.. code-block:: bash

    validate-configure
