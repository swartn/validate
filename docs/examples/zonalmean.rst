.. _zonalmean:

Zonal Mean Plot
===================

For this example we want to make a color map of a zonal mean 
cross section of the atmospheric temperature of the climatology
from 1980 to 2000 for the edr run ID.

.. image:: images/tasection_climatology.png

First use the command:

.. code-block:: bash

    validate-configure

Then edit the conf.yaml file to the following:

.. code-block:: yaml

    run: 'edr'
    experiment: 'historical'

    defaults:
                climatology: True
                climatology_dates:
                  start_date: '1980-01'
                  end_date: '2000-01'
                png: True

    plots:    
            - variable: 'tas'
              plot_projection: 'zonal_mean'

    delete:
              del_netcdf: False
              del_mask: True
              del_ncstore: True
              del_cmipfiles: False

    direct_data_root: '/raid/rc40/data/ncs/historical-edr/'        
    observations_root: '/raid/rc40/data/ncs/obs4comp'
    cmip5_root: '/raid/ra40/CMIP5_OTHER_DOWNLOADS/'

Save the file and then use the command:

.. code-block:: bash

    validate-configure
