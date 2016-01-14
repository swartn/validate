"""
plotcase
===============

This module contains functinos for different cases of
plots. The functinos will load the appropriate data. Do
any manipulations needed for the data and direct the data
to the correct plot.

.. moduleauthor:: David Fallis
"""

import dataload as pl
import plotregions as pr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import defaults as dft
import datetime
from plotregions import default_pcolor_args


def _depth_data(data, depth, plot):
    """ Makes a numpy array only containing data at the desired depth

    Parameters
    ----------
    data : numpy array
    depth : numpy array
            the depth needed
    plot : dictionary

    Returns
    -------
    dictionary
    """
    if data.ndim > 2:
        plot['plot_depth'] = min(depth, key=lambda x: abs(x - plot['depth']))
        try:
            depth_ind = np.where(np.round(depth) == np.round(plot['plot_depth']))[0][0]
        except:
            print('Failed to extract depth ' + plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data = data[depth_ind, :, :]
    else:
        plot['plot_depth'] = ''
    return data


def _section_data(data, plot):
    """ Averages the data for each latitude

    Parameters
    ----------
    data : numpy array
    plot : dictionary

    Returns
    -------
    numpy array
    """
    try:
        if data.ndim == 3:
            zonmean = data.mean(axis=2)
        elif data.ndim == 2:
            zonmean = data.mean(axis=1)
    except:
        print 'proc_plot cannot zonal mean for section ' + plot['ifile'] + ' ' + plot['variable']
        return data
    return zonmean


def _pcolor(data, plot, ptype, anom=False):
    if not plot['data1_args'][ptype + '_args']['pcolor_flag']:
        plot['data1_args'][ptype + '_args']['pcolor_args'] = default_pcolor_args(data, anom)


def _comp_pcolor(data, obs, plot, ptype, anom=False):
    """ Gives the data and observations the same colorbar
        for comparison

    Parameters
    ----------
    data : numpy array
    obs : numpy array
    plot : dictionary
    ptype : string
            'climatology' or 'trends'
    """
    if not plot['data1_args'][ptype + '_args']['pcolor_flag'] and not plot['data2_args'][ptype + '_args']['pcolor_flag']:
        d1pca = default_pcolor_args(data, anom)
        d2pca = default_pcolor_args(obs, anom)

        vmin = np.min([d1pca['vmin'], d2pca['vmin']])
        vmax = np.max([d1pca['vmax'], d2pca['vmax']])

        d1pca['vmin'] = vmin
        d1pca['vmax'] = vmax

        plot['data1_args'][ptype + '_args']['pcolor_args'] = d1pca
        plot['data2_args'][ptype + '_args']['pcolor_args'] = d1pca


def savefigures(plotname, png=False, pdf=False, **kwargs):
    pdfname = plotname + '.pdf'
    pngname = plotname + '.png'
    if png:
        plt.savefig(pngname, bbox_inches='tight')
    if pdf:
        plt.savefig(pdfname, bbox_inches='tight')


def map_climatology(plot, func):
    """ Loads and plots the data for a time averaged map

    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map

    Returns
    -------
    string : name of the plot
    """
    print 'plotting map of ' + plot['variable']
    # load data from netcdf file
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], plot['remap'], plot['remap_grid'])
    

    # get data at correct depth
    data = _depth_data(data, depth, plot)

    dft.filltitle(plot)
    _pcolor(data, plot, 'climatology', anom=False)
    
    # make plot
    func(lon, lat, data, ax_args=plot['data1_args']['climatology_args']['ax_args'],
         pcolor_args=plot['data1_args']['climatology_args']['pcolor_args'], cblabel=units, plot=plot,
         **plot['plot_args'])

    plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_climatology' + str(plot['plot_depth'])
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name


def climatology_comparison_name(plot):
    if plot['comp_flag'] == 'obs':
        plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_climatology_comparison_obs' + str(plot['plot_depth'])
    if plot['comp_flag'] == 'cmip5':
        plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_climatology_comparison_cmip5_' + str(plot['plot_depth'])
    if plot['comp_flag'] == 'model':
        plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_climatology_comparison_' + plot['comp_model'] + str(plot['plot_depth'])
    if plot['comp_flag'] == 'runid':
        plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_climatology_comparison_' + plot['comp_model'] + str(plot['plot_depth'])
    return plot_name


def trends_comparison_name(plot):
    if plot['comp_flag'] == 'obs':
        plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_trends_comparison_obs' + str(plot['plot_depth'])
    if plot['comp_flag'] == 'cmip5':
        plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_trends_comparison_cmip5_' + str(plot['plot_depth'])
    if plot['comp_flag'] == 'model':
        plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_trends_comparison_' + plot['comp_model'] + str(plot['plot_depth'])
    if plot['comp_flag'] == 'runid':
        plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_trends_comparison_' + plot['comp_model'] + str(plot['plot_depth'])
    return plot_name


def map_climatology_comparison(plot, func):
    """ Loads and plots the data for a time averaged map.
        Loads and plots the data for comparison and plots the
        difference between the data and the comparison data.

    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map

    Returns
    -------
    string : name of the plot
    """
    print 'plotting comparison map of ' + plot['variable']
    # load data from netcdf file
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], plot['remap'], plot['remap_grid'])

    
    # get data at correct depth
    data = _depth_data(data, depth, plot)

    # get comparison data from netcdf file
    data2, units, lon, lat, depth = pl.timeaverage_load(plot['comp_file'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], plot['remap'], plot['remap_grid'], [plot['plot_depth']])

    # get comparison data at correct depth
    data2 = _depth_data(data2, depth, plot)

    compdata = data - data2
    _comp_pcolor(data, data2, plot, 'climatology')
    fig, (axl, axm, axr) = plt.subplots(3, 1, figsize=(8, 8))

    dft.filltitle(plot)

    # make plots of data, comparison data, data - comparison data
    func(lon, lat, data, plot=plot, ax=axl, ax_args=plot['data1_args']['climatology_args']['ax_args'],
         pcolor_args=plot['data1_args']['climatology_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lon, lat, data2, plot=plot, ax=axm, ax_args=plot['data2_args']['climatology_args']['ax_args'],
         pcolor_args=plot['data2_args']['climatology_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lon, lat, compdata, anom=True, rmse=True, plot=plot, ax=axr, ax_args=plot['comp_args']['climatology_args']['ax_args'],
         pcolor_args=plot['comp_args']['climatology_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    
    plot_name = climatology_comparison_name(plot)
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name


def _section_labels(datanumber, plot):
    """ Gives the axes of a section appropriate labels

    Parameters
    ----------
    datanumber : string
                 name of the data
    plot : dictionary

    Returns
    -------
    dictionary
    """
    plot[datanumber]['climatology_args']['ax_args']['xlabel'] = 'Latitude'
    plot[datanumber]['climatology_args']['ax_args']['xticks'] = np.arange(-80, 81, 20)
    plot[datanumber]['climatology_args']['ax_args']['ylabel'] = 'Depth'
    return plot


def section_climatology(plot, func):
    """ Loads and plots the data for a time average section map.

    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map

    Returns
    -------
    string : name of the plot
    """
    print 'plotting section of ' + plot['variable']
    
    plot = _section_labels('data1_args', plot)
    
    # load data from netcdf file
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], plot['remap'], plot['remap_grid'])

    # calculate the zonal mean of the data
    zonmean = _section_data(data, plot)

    dft.filltitle(plot)
    _pcolor(data, plot, 'climatology', anom=False)
    
    # plot the data
    func(lat, depth, zonmean, plot=plot, ax_args=plot['data1_args']['climatology_args']['ax_args'],
         pcolor_args=plot['data1_args']['climatology_args']['pcolor_args'], cblabel=units)
    
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_climatology'
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name


def section_climatology_comparison(plot, func):
    """ Loads and plots the data for a time averaged section map.
        Loads and plots the data for comparison and plots the
        difference between the data and the comparison data.

    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map

    Returns
    -------
    string : name of the plot
    """
    print 'plotting section comparison of ' + plot['variable']
    _section_labels('data1_args', plot)
    _section_labels('data2_args', plot)
    _section_labels('comp_args', plot)

    # load data from netcdf file
    #data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], plot['remap'], plot['remap_grid'])
    zonmean, units, x, depth = pl.zonal_load(plot['ifile'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'])
    print zonmean.shape
    # calculate the zonal mean
    #zonmean = _section_data(data, plot)
    
    # load comparison data from netcdf file
    #data2, units2, lon2, lat2, depth2 = pl.timeaverage_load(plot['comp_file'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], depthneeded=depth)
    zonmean2, units2, x2, depth2 = pl.zonal_load(plot['comp_file'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], depthneeded=depth)
    print zonmean2.shape
    # calculate the zonal mean of the comparison data
    #zonmean2 = _section_data(data2, plot)
    
    dft.filltitle(plot)
    _comp_pcolor(zonmean, zonmean2, plot, 'climatology')
    compdata = zonmean - zonmean2
    
    # make plots of data, comparison data, data - comparison data
    fig = plt.figure(figsize=(6, 8))
    gs = gridspec.GridSpec(3, 2, width_ratios=[20, 1])
    func(x, depth, zonmean, plot=plot, ax=plt.subplot(gs[0, 0]), ax_args=plot['data1_args']['climatology_args']['ax_args'],
         pcolor_args=plot['data1_args']['climatology_args']['pcolor_args'], cblabel=units, cbaxis=plt.subplot(gs[0, 1]))
    func(x, depth, zonmean2, plot=plot, ax=plt.subplot(gs[1, 0]), ax_args=plot['data2_args']['climatology_args']['ax_args'],
         pcolor_args=plot['data2_args']['climatology_args']['pcolor_args'], cblabel=units, cbaxis=plt.subplot(gs[1, 1]))
    func(x, depth, compdata, anom=True, rmse=True, plot=plot, ax=plt.subplot(gs[2, 0]), ax_args=plot['comp_args']['climatology_args']['ax_args'],
         pcolor_args=plot['comp_args']['climatology_args']['pcolor_args'], cblabel=units, cbaxis=plt.subplot(gs[2, 1]))

    plt.tight_layout()
    plot_name = climatology_comparison_name(plot)
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name


def _trend_units(data, units, plot):
    """ Multiplies the data by a scalar factor based on the frequency

    Parameters
    ----------
    data : numpy array
    units : string
    plot : dictionary

    Returns
    -------
    numpy array
    string
    """
    if plot['frequency'] == 'day':
        data = data * 365
    if plot['frequency'] == 'mon':
        data = data * 120
    if plot['frequency'] == 'year':
        data = data * 10
    units = units + '/decade'
    return data, units


def map_trends(plot, func):
    """ Loads and plots the trend data on a map.

    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map

    Returns
    -------
    string : name of the plot
    """
    print 'plotting trends map of ' + plot['variable']
    
    # load trends data from netcdf file
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['trends_dates'], plot['scale'], plot['remap'], plot['remap_grid'])

    # get data at correct depth
    data = _depth_data(data, depth, plot)
    
    # scale data based on frequency
    data, units = _trend_units(data, units, plot)

    _pcolor(data, plot, 'trends', anom=True)
    dft.filltitle(plot)
    
    # make plot
    func(lon, lat, data, anom=True, plot=plot, ax_args=plot['data1_args']['trends_args']['ax_args'],
         pcolor_args=plot['data1_args']['trends_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])

    plot_name = 'plots/' + plot['variable'] + '_' + plot['plot_projection'] + '_trends' + str(plot['plot_depth'])
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name


def map_trends_comp(plot, func):
    """ Loads and plots the trend data on a map.
        Loads and plots the data for comparison and plots the
        difference between the data and the comparison data.

    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map

    Returns
    -------
    string : name of the plot
    """
    print 'plotting trends map comparison of ' + plot['variable']
    
    # load trends data from netcdf file
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['trends_dates'], plot['scale'], plot['remap'], plot['remap_grid'])

    # get data at correct depth
    data = _depth_data(data, depth, plot)

    # scale data based on frequency
    data, units = _trend_units(data, units, plot)

    # load trends comparison data from netcdf file
    data2, units2, lon2, lat2, depth2 = pl.trends_load(plot['comp_file'], plot['variable'], plot['trends_dates'], plot['scale'], plot['remap'], plot['remap_grid'], depthneeded=[plot['plot_depth']])

    # get comparison data at correct depth
    if data2.ndim > 2:
        data2 = data2[depth_ind, :, :]
        
    # scale data based on frequency
    data2, units2 = _trend_units(data2, units2, plot)
    compdata = data - data2

    dft.filltitle(plot)
    _comp_pcolor(data, data2, plot, 'trends', anom=True)

    # make trends plots of data, comparison data, data - comparison data    
    fig, (axl, axm, axr) = plt.subplots(3, 1, figsize=(8, 8))
    func(lon, lat, data, ax=axl, anom=True, plot=plot, ax_args=plot['data1_args']['trends_args']['ax_args'],
         pcolor_args=plot['data1_args']['trends_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lon, lat, data2, ax=axm, anom=True, plot=plot, ax_args=plot['data2_args']['trends_args']['ax_args'],
         pcolor_args=plot['data2_args']['trends_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lon, lat, compdata, ax=axr, anom=True, rmse=True, plot=plot, ax_args=plot['comp_args']['trends_args']['ax_args'],
         pcolor_args=plot['comp_args']['trends_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
         
    plot_name = trends_comparison_name(plot)
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name


def section_trends(plot, func):
    """ Loads and plots the trend data for a section map.

    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map

    Returns
    -------
    string : name of the plot
    """
    print 'plotting section trends of ' + plot['variable']
    _section_labels('data1_args', plot)

    # load trends data from netcdf file
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['trends_dates'], plot['scale'], plot['remap'], plot['remap_grid'])
    
    # get zonal mean data
    zonmean = _section_data(data, plot)
    
    # scale data based on frequency
    zonmean, units = _trend_units(zonmean, units, plot)
    
    dft.filltitle(plot)
    _pcolor(zonmean, plot, 'trends', anom=True)
    
    # make plot
    func(lat, depth, zonmean, anom=True, plot=plot, ax_args=plot['data1_args']['trends_args']['ax_args'],
         pcolor_args=plot['data1_args']['trends_args']['pcolor_args'], cblabel=units)

    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_trends_'
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name


def section_trends_comp(plot, func):
    """ Loads and plots the trend data for a section map.
        Loads and plots the data for comparison and plots the
        difference between the data and the comparison data.

    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map

    Returns
    -------
    string : name of the plot
    """
    print 'plotting section trends of ' + plot['variable']
    _section_labels('data1_args', plot)
    _section_labels('data2_args', plot)
    _section_labels('comp_args', plot)

    # load trends data from netcdf file
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['trends_dates'], plot['scale'], plot['remap'], plot['remap_grid'])
    
    # get zonal mean of data
    zonmean = _section_data(data, plot)

    # load comparison data from netcdf file
    data2, units2, lon2, lat2, depth2 = pl.trends_load(plot['comp_file'], plot['variable'], plot['trends_dates'], plot['scale'], plot['remap'], plot['remap_grid'], depthneeded=depth)
    
    # get zonal mean of comparison data
    zonmean2 = _section_data(data2, plot)

    # scale data based on frequency
    zonmean, units = _trend_units(zonmean, units, plot)
    zonmean2, units2 = _trend_units(zonmean2, units2, plot)

    compdata = zonmean - zonmean2
    dft.filltitle(plot)
    _comp_pcolor(zonmean, zonmean2, plot, 'trends', anom=True)
    
    # make trends plots of data, comparison data, data - comparison data    
    fig, (axl, axm, axr) = plt.subplots(3, 1, figsize=(8, 8))
    func(lat, depth, zonmean, ax=axl, anom=True, plot=plot, ax_args=plot['data1_args']['trends_args']['ax_args'],
         pcolor_args=plot['data1_args']['trends_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lat, depth, zonmean2, ax=axm, anom=True, plot=plot, ax_args=plot['data2_args']['trends_args']['ax_args'],
         pcolor_args=plot['data2_args']['trends_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lat, depth, compdata, ax=axr, anom=True, rmse=True, plot=plot, ax_args=plot['comp_args']['trends_args']['ax_args'],
         pcolor_args=plot['comp_args']['trends_args']['pcolor_args'], cblabel=units,
         **plot['plot_args'])

    plot_name = trends_comparison_name(plot)
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name

def timeseriesdata(plot, compfile, depth):
    data, units, x, depth = pl.timeseries_load(compfile, plot['variable'], plot['climatology_dates'], plot['realm'], plot['scale'], depthneeded=depth)

    if data.ndim > 1:
        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' + plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data = data[:, depth_ind]
    return data, x


def timeseries_comparison(plot, func):
    print 'plotting timeseries comparison of ' + plot['variable']

    # Load time series data from netcdf file
    data, units, x, depth = pl.timeseries_load(plot['ifile'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'])

    plot['data1_args']['climatology_args']['ax_args']['xlabel'] = 'Time'
    plot['data1_args']['climatology_args']['ax_args']['ylabel'] = units
    
    # get data at the correct depth 
    plot['plot_depth'] = plot['depth']
    if data.ndim > 1:
        plot['plot_depth'] = min(depth, key=lambda x: abs(x - plot['depth']))

        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' + plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data = data[:, depth_ind]

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    dft.filltitle(plot)
    
    # make plot
    func(x, data, plot=plot, ax=ax, ax_args=plot['data1_args']['climatology_args']['ax_args'])

    # plot comparison data on the same axis
    if plot['compare']['cmip5']:
        plot['comp_model'] = 'cmip5'
        data, x = timeseriesdata(plot, plot['cmip5_file'], depth)
        func(x, data, plot=plot, ax=ax, label=plot['comp_model'], ax_args=plot['data1_args']['climatology_args']['ax_args'])
    if plot['compare']['obs']:
        plot['comp_model'] = 'Observations'
        data, x = timeseriesdata(plot, plot['obs_file'], depth)
        func(x, data, plot=plot, ax=ax, label=plot['comp_model'], ax_args=plot['data1_args']['climatology_args']['ax_args'])
    if plot['compare']['model']:
        for model in plot['comp_models']:
            plot['comp_model'] = model
            data, x = timeseriesdata(plot, plot['model_file'][model], depth)
            func(x, data, plot=plot, ax=ax, label=plot['comp_model'], ax_args=plot['data1_args']['climatology_args']['ax_args'])
    if plot['compare']['runid']:
        for i in plot['comp_ids']:
            plot['comp_model'] = i
            data, x = timeseriesdata(plot, plot['id_file'][i], depth)
            func(x, data, plot=plot, ax=ax, label=plot['comp_model'], ax_args=plot['data1_args']['climatology_args']['ax_args'])

    ax.legend(loc='best')
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_climatology_timeseries_comparison' + str(plot['plot_depth'])
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name

def zonalmeandata(plot, compfile, ax, depth, func):
    data2, units2, x2, depth2 = pl.zonal_load_comp(compfile, plot['variable'], plot['climatology_dates'], depth, plot['scale'])
    if data2.ndim > 1:
        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' + plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data2 = data2[depth_ind, :]
    func(x2, data2, plot=plot, ax=ax, label=plot['comp_model'], ax_args=plot['data1_args']['climatology_args']['ax_args'])


def zonalmean_comparison(plot, func):
    """ Loads and plots a time average of the zonal means
        for each latitude. Loads and plots the data for comparison.

    Parameters
    ----------
    plot : dictionary
    func : a method that will plot the data on a specified map

    Returns
    -------
    string : name of the plot
    """
    print 'plotting zonal mean of ' + plot['variable']
    
    # Load zonal mean data from netcdf file
    data, units, x, depth = pl.zonal_load(plot['ifile'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'])

    plot['data1_args']['climatology_args']['ax_args']['xlabel'] = 'Latitude'
    plot['data1_args']['climatology_args']['ax_args']['ylabel'] = units

    # get data at the correct depth 
    plot['plot_depth'] = plot['depth']
    print data.shape
    if data.ndim > 1:
        plot['plot_depth'] = min(depth, key=lambda x: abs(x - plot['depth']))
        try:
            depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
        except:
            print('Failed to extract depth ' + plot['plot_depth'] + ' for ' + plot['variable'])
            depth_ind = 0
        data = data[depth_ind, :]

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    dft.filltitle(plot)
    
    # make plot
    func(x, data, plot=plot, ax=ax, ax_args=plot['data1_args']['climatology_args']['ax_args'])

    # plot comparison data on the same axis
    if plot['compare']['cmip5']:
        plot['comp_model'] = 'cmip5'
        zonalmeandata(plot, plot['cmip5_file'], ax, depth, func)
    if plot['compare']['obs']:
        plot['comp_model'] = 'Observations'
        zonalmeandata(plot, plot['obs_file'], ax, depth, func)
    if plot['compare']['model']:
        for model in plot['comp_models']:
            plot['comp_model'] = model
            zonalmeandata(plot, plot['model_file'][model], ax, depth, func)
    if plot['compare']['runid']:
        for i in plot['comp_ids']:
            plot['comp_model'] = i
            zonalmeandata(plot, plot['id_file'][i], ax, depth, func)

    ax.legend(loc='best')
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_climatology_zonalmean_comparison' + str(plot['plot_depth'])
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name


def taylor_full(plot, func):
    print 'plotting taylor diagram of ' + plot['variable']
    plot['plot_depth'] = plot['depth']
    
    # load data from netcdf file
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'])

    # start list of tuples to be plotted
    plotdata = [(data, plot['model_ID'])]

    # load observations data
    data, units, lon, lat, depth = pl.timeaverage_load(plot['obs_file'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], depthneeded=[plot['plot_depth']])
    
    dft.filltitle(plot)
    
    # get data from models and cmip and append to plotdata list
    if plot['compare']['cmip5'] == True:
        plot['comp_model'] = 'cmip5'
        data, units, lon, lat, depth = pl.timeaverage_load(plot['cmip5_file'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], depthneeded=[plot['plot_depth']])
        plotdata.append((data, 'cmip5'))
    if plot['compare']['model'] == True:
        for model in plot['comp_models']:
            plot['comp_model'] = model
            data, units, lon, lat, depth = pl.timeaverage_load(plot['model_file'][model], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], depthneeded=[plot['plot_depth']])
            plotdata.append((data, model))
    if plot['compare']['runid'] == True:
        for i in plot['comp_ids']:
            plot['comp_model'] = i
            data, units, lon, lat, depth = pl.timeaverage_load(plot['id_file'][i], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], depthneeded=[plot['plot_depth']])
            plotdata.append((data, i))
            
    # make plot
    pr.taylordiagram(refdata, plotdata, plot=plot, ax_args=plot['data1_args']['climatology_args']['ax_args'])
    
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_climatology_taylor' + str(plot['plot_depth'])
    plt.tight_layout()
    savefigures(plot_name, **plot)
    plot['units'] = units
    plot['comp_file'] = plot['obs_file']
    return plot_name
    
def taylor(plot, func):
    if not plot['is_depth']:
        return taylor_full(plot, func)

    print 'plotting taylor diagram of ' + plot['variable']
    plot['plot_depth'] = plot['depth']
    
    # load data from netcdf file
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'])
    
    # get data at correct depth
    data = _depth_data(data, depth, plot)
    

    # start list of tuples to be plotted
    plotdata = [(data, plot['model_ID'])]

    # load observations data
    data, units, lon, lat, depth = pl.timeaverage_load(plot['obs_file'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], depthneeded=[plot['plot_depth']])
    
    # get observations data at correct depth
    refdata = _depth_data(data, depth, plot)
    
    dft.filltitle(plot)
    
    # get data from models and cmip and append to plotdata list
    if plot['compare']['cmip5'] == True:
        plot['comp_model'] = 'cmip5'
        data, units, lon, lat, depth = pl.timeaverage_load(plot['cmip5_file'], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], depthneeded=[plot['plot_depth']])
        plotdata.append((_depth_data(data, depth, plot), 'cmip5'))
    if plot['compare']['model'] == True:
        for model in plot['comp_models']:
            plot['comp_model'] = model
            data, units, lon, lat, depth = pl.timeaverage_load(plot['model_file'][model], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], depthneeded=[plot['plot_depth']])
            plotdata.append((_depth_data(data, depth, plot), model))
    if plot['compare']['runid'] == True:
        for i in plot['comp_ids']:
            plot['comp_model'] = i
            data, units, lon, lat, depth = pl.timeaverage_load(plot['id_file'][i], plot['variable'], plot['climatology_dates'], plot['realm_cat'], plot['scale'], depthneeded=[plot['plot_depth']])
            plotdata.append((_depth_data(data, depth, plot), i))
            
    # make plot
    pr.taylordiagram(refdata, plotdata, plot=plot, ax_args=plot['data1_args']['climatology_args']['ax_args'])
    
    plot_name = 'plots/' + plot['variable'] + plot['plot_projection'] + '_climatology_taylor' + str(plot['plot_depth'])
    plt.tight_layout()
    savefigures(plot_name, **plot)
    plot['units'] = units
    plot['comp_file'] = plot['obs_file']
    return plot_name
  
