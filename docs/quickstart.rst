**********
Quickstart
**********

Installing
===========
You can install validate with pip from pypi:

.. code-block:: bash

    pip install validate

or the latest version directly from github

.. code-block:: bash

    pip install git+https://github.com/swartn/validate.git

validate has primarily been developed and tested within the
`anaconda <http://docs.continuum.io/anaconda/index.html>`_ python distribution on
Linux x86/x64 and Mac OSX. Windows is not supported.

You can (should) do this inside a virtual environment. In that case it will work
without root privileges. If you are using anaconda see
http://conda.pydata.org/docs/faq.html#env.

**Dependencies**

The external package `Climate Data Operators (cdo) <https://code.zmaw.de/projects/cdo>`_ v1.6 or later
is required. Python dependencies are in theory handled automatically by pip, but often things go
smoother if you have these items available: 

  - `Python 2.7x <http://www.python.org/download/>`_

  - `Climate Data Operators (cdo) <https://code.zmaw.de/projects/cdo>`_ v1.6 or later.

  - `netCDF4 <http://unidata.github.io/netcdf4-python/>`_

  - `numpy 1.2.1 or later  <http://sourceforge.net/project/showfiles.php?group_id=1369&package_id=175103>`__

  - `matplotlib <http://sf.net/projects/matplotlib/>`_ 

  - `pyyaml <http://pyyaml.org/wiki/PyYAML/>`_

  - `brewer2mpl <https://github.com/jiffyclub/palettable/wiki/brewer2mpl/>`_

  - 'cmipdata <https://cmipdata.readthedocs.org/en/latest/>'_

validate has primarily been developed and tested within the 
`anaconda <http://docs.continuum.io/anaconda/index.html>`_ python distribution on 
Linux x86/x64 and Mac OSX, where dependencies were installed with conda. 
Windows is not supported.

Using validate
==============

After a succesful installation, you should move to a working directory (preferably empty).
Be careful working in populated directories as validate may remove or modify files or 
directories with particular names.

To setup the configuration file use the command:

.. code-block:: bash

    validate-configure

which will provide a conf.yaml file. Follow the examples in this file to specify the 
plots you desire, and make sure to modify the "data_root" variable to point to the 
data on your system. Once the changes have been made, save the conf.yaml file 
in your working directory and once use the command:

.. code-block:: bash
    
    validate-execute -r [runID]

The generated plots can be found in the /plots directory and details about
the plots in the /log directory.
 
