**********
Quickstart
**********

Installing
===========

**Dependencies**

Several external packages are required:

`Python 2.7x <http://www.python.org/download/>`_

`Climate Data Operators (cdo) <https://code.zmaw.de/projects/cdo>`_ v1.6 or later.

`netCDF4 <http://unidata.github.io/netcdf4-python/>`_

`numpy 1.2.1 or later 
<http://sourceforge.net/project/showfiles.php?group_id=1369&package_id=175103>`__

`matplotlib <http://sf.net/projects/matplotlib/>`_ 

`pyyaml <http://pyyaml.org/wiki/PyYAML/>`_

validate has primarily been developed and tested within the 
`anaconda <http://docs.continuum.io/anaconda/index.html>`_ python distribution on 
Linux x86/x64 and Mac OSX. Windows is not supported.

**Installation**

To install, first clone the repo from github:

.. code-block:: bash

    git clone https://github.com/fallisd/validate.git
    
then build and install:

.. code-block:: bash

    cd validate
    python setup.py install
    
You can (should) do this inside a virtual environment. In that case it will work 
without root privileges. If you are using anaconda see  
http://conda.pydata.org/docs/faq.html#env.

Using validate
==============

After a succesful installation, you should move to a working directory (preferably empty).
Be careful working in populated directories as validate may remove or modify files or 
directories with particular names.

To create a standard set of plots use the command 

.. code-block:: bash
    
    validate-execute -r [runID]

Where [runID] is the three letter runId for the experiment.

To make modifications to the standard plots use the command:

.. code-block:: bash

    validate-configure
    
Once the changes have been made, save the conf.yaml file in your working directory
and once again use the command:

.. code-block:: bash
    
    validate-execute -r [runID]

The generated plots can be found in the /plots directory and details about
the plots in the /log directory.
 


