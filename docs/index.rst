.. validate documentation master file, created by
   sphinx-quickstart on Mon Jan  4 17:03:27 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to validate's documentation!
====================================

Contents
========

.. toctree::
   :maxdepth: 2

   quickstart
   examples/index.rst
   api
   
Introduction
============

**validate** is a python package used to produce visulizations and summary statistics
of climate model ouput, and its comparison to observations. A set of desired plots and
analyses is specified in a simple configuration file. When run validate produces a set
of image files, a merged PDF file of all images (fully indexed), as well as a file of
summary statistics and a log for reproducibility. Validate is designed to use
data in the netCDF file format, specifically as used in the Coupled Model
Intercomparison Project (CMIP).

Standard available plots include various maps projections, 2D sections, 1D time-series
or line plots, scatter plots and Taylor diagrams. "Comparison" plots compute and display
the anomaly between a model run and a specified set of observations. Options such as
colorbars, axis limits are assigned by default, but can be easily customized by the user.
Currently, validate will compute climatologies and trends over user-specified periods.
Validate can be extended to perform any advanced analysis through specification
of a user defined external function, which may be written in any language
(as long as netCDF is returned).

At the Canadian Centre for Climate Modelling and Analysis (CCCma), validate is used
in batch mode to automatically produce a large set of standard summary diagnostic
plots at the conclusion of each model run.


Contributors
------------
David Fallis: davidwfallis@gmail.com

Neil Swart: neil.swart@canada.ca

Pull requests and comments are welcome.

LICENSE
-------

See the LICENSE.txt file in the validate package. validate is distributed
under the GNU General Public License version 2, and the Open Government 
License - Canada (http://data.gc.ca/eng/open-government-licence-canada)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

