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
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from matplotlib import gridspec
import defaults as dft
import datetime
from plotregions import default_pcolor_args


def _1d_depth_data(data, depth, plot):
    if not type(data) == 'numpy.ndarray':
        plot['plot_depth'] = None
        return data
    plot['plot_depth'] = min(depth, key=lambda x: abs(x - plot['depth']))
    try:
        depth_ind = np.where(np.round(depth) == np.round(plot['plot_depth']))[0][0]
    except:
        print('Failed to extract depth ' + plot['plot_depth'] + ' for ' + plot['variable'])
        depth_ind = 0
    data = data[depth_ind]
    return data

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
        plot['plot_depth'] = None
    return data

def _full_depth_data(data, depth, plot):
    if data.ndim > 3:
        depth_ind = np.where(np.round(depth) == np.round(plot['plot_depth']))[0][0]
        data = data[:, depth_ind, :, :]
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
    if plot['variable'] == 'msftmyz':
        return data[plot['basin'], :, :]
    
    try:
        if data.ndim == 3:
            zonmean = data.mean(axis=2)
        elif data.ndim == 2:
            zonmean = data.mean(axis=1)
    except:
        print 'proc_plot cannot zonal mean for section ' + plot['ifile'] + ' ' + plot['variable']
        return data
    return zonmean


def _pcolor(data, plot, anom=False):
    if anom or plot['divergent']:
        anom = True    
    if not plot['data1']['pcolor_flag']:
        plot['data1']['pcolor_args'] = default_pcolor_args(data, anom)


def _comp_pcolor(data, obs, plot, anom=False):
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
    if anom or plot['divergent']:
        anom = True  
    if not plot['data1']['pcolor_flag'] and not plot['data2']['pcolor_flag']:
        d1pca = default_pcolor_args(data, anom)
        d2pca = default_pcolor_args(obs, anom)

        vmin = np.min([d1pca['vmin'], d2pca['vmin']])
        vmax = np.max([d1pca['vmax'], d2pca['vmax']])

        d1pca['vmin'] = vmin
        d1pca['vmax'] = vmax

        plot['data1']['pcolor_args'] = d1pca
        plot['data2']['pcolor_args'] = d1pca


def savefigures(plotname, png=False, pdf=False, **kwargs):
    pdfname = plotname + '.pdf'
    pngname = plotname + '.png'
    if png:
        plt.savefig(pngname, bbox_inches='tight')
    if pdf:
        plt.savefig(pdfname, bbox_inches='tight')

def plotname(plot):
    plotname = 'plots/'
    plotname += plot['variable']
    plotname += plot['data_type']
    plotname += '_' + plot['plot_projection']
    plotname += '_' + str(plot['plot_depth'])
    plotname += '_' + plot['dates']['start_date'] + plot['dates']['end_date']
    season = ''.join(plot['seasons'])
    plotname += season

    try: 
        plotname += '_' + str(plot['basin'])
    except:
        pass
    
    if plot['comp_flag'] == 'Model' or not plot['comp_flag']:
        return plotname
    try:
        plotname += '_' + plot['comp_model']
    except: pass
    plotname += '_' + plot['comp_dates']['start_date'] + plot['comp_dates']['end_date']
    compseason = ''.join(plot['comp_seasons'])
    plotname += compseason

    print plotname
    return plotname    
        

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
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], plot['remap'], plot['remap_grid'], seasons=plot['seasons'])
    if plot['units']:
        units = plot['units']
    # get data at correct depth
    data = _depth_data(data, depth, plot)

    dft.filltitle(plot)
    _pcolor(data, plot, anom=False)
    # make plot
    func(lon, lat, data, ax_args=plot['data1']['ax_args'],
         pcolor_args=plot['data1']['pcolor_args'], cblabel=units, plot=plot,
         **plot['plot_args'])

    plot_name = plotname(plot)
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name

def ttest(data1, data2):
    t, p = sp.stats.ttest_ind(data1, data2, axis=0, equal_var=False)
    return p

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

    
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], plot['remap'], plot['remap_grid'], seasons=plot['seasons'])
    # get data at correct depth
    data = _depth_data(data, depth, plot)
    try:
        fulldata = pl.full_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], plot['remap'], plot['remap_grid'], seasons=plot['seasons'])
        fulldata2 = pl.full_load(plot['comp_file'], plot['variable'], plot['comp_dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], plot['remap'], plot['remap_grid'], depthneeded=list(depth), seasons=plot['comp_seasons'])
  
        if len(fulldata.shape) == len(fulldata2.shape):
            fulldepthdata = _full_depth_data(fulldata, depth, plot)
            fulldepthdata2 = _full_depth_data(fulldata2, depth, plot)
            pvalues = ttest(fulldepthdata, fulldepthdata2)
        else:
            pvalues = None 
            plot['alpha'] = None
    except:
        pvalues = None
        plot['alpha'] = None
    # get comparison data from netcdf file
    data2, units2, lon2, lat2, depth = pl.timeaverage_load(plot['comp_file'], plot['variable'], plot['comp_dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], plot['remap'], plot['remap_grid'], [plot['plot_depth']], seasons=plot['comp_seasons'])
    # get comparison data at correct depth
#    data2 = _depth_data(data2, depth, plot)
    try:
        compdata = data - data2
    except:
        data2 = data2.transpose()
        compdata = data - data2
    _comp_pcolor(data, data2, plot)
    
    if plot['units']:
        units = plot['units']

    fig, (axl, axm, axr) = plt.subplots(3, 1, figsize=(8, 8))

    dft.filltitle(plot)

    # make plots of data, comparison data, data - comparison data
    func(lon, lat, data, plot=plot, ax=axl, ax_args=plot['data1']['ax_args'],
         pcolor_args=plot['data1']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lon, lat, data2, plot=plot, ax=axm, ax_args=plot['data2']['ax_args'],
         pcolor_args=plot['data2']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lon, lat, compdata, pvalues=pvalues, alpha=plot['alpha'], anom=True, rmse=True, plot=plot, ax=axr, ax_args=plot['comp']['ax_args'],
         pcolor_args=plot['comp']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    
    plot_name = plotname(plot)
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name


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
    
    
    # load data from netcdf file
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], plot['remap'], plot['remap_grid'], seasons=plot['seasons'])

    if plot['units']:
        units = plot['units']
        
    # calculate the zonal mean of the data
    zonmean = _section_data(data, plot)
    dft.filltitle(plot)
    _pcolor(data, plot, anom=False)

    fig = plt.figure(figsize=(10,3))
    gs = gridspec.GridSpec(1, 1, width_ratios=[1, 1])    
    # plot the data
    func(lat, depth, zonmean, plot=plot, ax=plt.subplot(gs[0, 0]), ax_args=plot['data1']['ax_args'],
         pcolor_args=plot['data1']['pcolor_args'], cblabel=units)
    
    plot_name = plotname(plot)

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
    # load data from netcdf file
    zonmean, units, x, depth = pl.zonal_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], seasons=plot['seasons'])

    # load comparison data from netcdf file
    zonmean2, units2, x2, depth2 = pl.zonal_load(plot['comp_file'], plot['variable'], plot['comp_dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=list(depth), seasons=plot['comp_seasons'])

    if plot['units']:
        units = plot['units']

    fulldata = pl.full_section_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], seasons=plot['seasons'])
    fulldata2 = pl.full_section_load(plot['comp_file'], plot['variable'], plot['comp_dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=list(depth), seasons=plot['comp_seasons'])
    pvalues = ttest(fulldata, fulldata2)
    
    dft.filltitle(plot)
    _comp_pcolor(zonmean, zonmean2, plot)
    compdata = zonmean - zonmean2
    
    # make plots of data, comparison data, data - comparison data
    fig = plt.figure(figsize=(6, 8))
    gs = gridspec.GridSpec(3, 2, width_ratios=[20, 1])
    func(x, depth, zonmean, plot=plot, ax=plt.subplot(gs[0, 0]), ax_args=plot['data1']['ax_args'],
         pcolor_args=plot['data1']['pcolor_args'], cblabel=units, cbaxis=plt.subplot(gs[0, 1]))
    func(x, depth, zonmean2, plot=plot, ax=plt.subplot(gs[1, 0]), ax_args=plot['data2']['ax_args'],
         pcolor_args=plot['data2']['pcolor_args'], cblabel=units, cbaxis=plt.subplot(gs[1, 1]))
    func(x, depth, compdata, anom=True, rmse=True, pvalues=pvalues, alpha=plot['alpha'], plot=plot, ax=plt.subplot(gs[2, 0]), ax_args=plot['comp']['ax_args'],
         pcolor_args=plot['comp']['pcolor_args'], cblabel=units, cbaxis=plt.subplot(gs[2, 1]))

    plt.tight_layout()
    plot_name = plotname(plot)
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
        data = data * 3650
    if plot['frequency'] == 'mon':
        data = data * 120
    if plot['frequency'] == 'year':
        data = data * 10
    units = units + '/decade'
    return data, units

def trend_significance(residuals, sigma=0.05):
    nt = len(residuals)
    count = 0
    x = len(residuals[0, :, 0])
    y = len(residuals[0, 0, :])
    rcorrs = np.empty(shape=[x, y])
    for (i,j), value in np.ndenumerate(rcorrs):
        count += 1
        r_corr,_ = sp.stats.pearsonr(residuals[: -1, i, j], residuals[1:, i, j])
        if r_corr < 0:
            r_corr = 0
        rcorrs[i][j] = r_corr
    
    cs = np.empty(shape=[x, y])    
    for (i,j), rcor in np.ndenumerate(rcorrs):
        neff = float(nt * (1-rcor) / (1 + rcor))
        #neff = nt
        a = residuals[:,i,j]
        b = a * a
        d = sum(b)
        se = np.sqrt( d / ( neff - 2 ) )
        sb = se / np.sqrt( sum( ( np.arange(nt) - np.mean( np.arange(nt) ) )**2 ) )

        tcrit = sp.stats.t.isf(sigma/2.0, nt - 2 )

        c = tcrit * sb

        cs[i][j] = c
    return cs


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
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['dates'], plot['scale'], plot['shift'], plot['remap'], plot['remap_grid'], seasons=plot['seasons'])

    # get data at correct depth
    data = _depth_data(data, depth, plot)
    
    # scale data based on frequency
    data, units = _trend_units(data, units, plot)

    fulldata = pl.full_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], plot['remap'], plot['remap_grid'], seasons=plot['seasons'])
    detrenddata = pl.full_detrend(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], plot['remap'], plot['remap_grid'], seasons=plot['seasons'])
    fulldepthdata = _full_depth_data(fulldata, depth, plot)
    fulldepthdetrenddata = _full_depth_data(detrenddata, depth, plot)
    
    slope, intercept, r_value, p_value, std_error = sp.stats.linregress(np.arange(len(fulldepthdata)), fulldepthdata[:, 0 , 0])
    siggrid = trend_significance(fulldepthdetrenddata, plot['sigma'])
    cvalues, _ = _trend_units(siggrid, units, plot)

    _pcolor(data, plot, anom=True)
    dft.filltitle(plot)

    if plot['units']:
        units = plot['units']    
    # make plot
    func(lon, lat, data, anom=True, plot=plot, cvalues=cvalues, ax_args=plot['data1']['ax_args'],
         pcolor_args=plot['data1']['pcolor_args'], cblabel=units,
         **plot['plot_args'])

    plot_name = plotname(plot)

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
    data, units, lon, lat, depth = pl.trends_load(plot['ifile'], plot['variable'], plot['dates'], plot['scale'], plot['shift'], plot['remap'], plot['remap_grid'], seasons=plot['seasons'])

    # get data at correct depth
    data = _depth_data(data, depth, plot)

    # scale data based on frequency
    data, units = _trend_units(data, units, plot)
    if plot['units']:
        units = plot['units']
        
    # load trends comparison data from netcdf file
    data2, units2, lon2, lat2, depth2 = pl.trends_load(plot['comp_file'], plot['variable'], plot['comp_dates'], plot['comp_scale'], plot['comp_shift'], plot['remap'], plot['remap_grid'], depthneeded=[plot['plot_depth']], seasons=plot['comp_seasons'])

    # get comparison data at correct depth
    if data2.ndim > 2:
        data2 = data2[depth_ind, :, :]
        
    # scale data based on frequency
    data2, units2 = _trend_units(data2, units2, plot)
    compdata = data - data2

    dft.filltitle(plot)
    _comp_pcolor(data, data2, plot, anom=True)

    # make trends plots of data, comparison data, data - comparison data    
    fig, (axl, axm, axr) = plt.subplots(3, 1, figsize=(8, 8))
    func(lon, lat, data, ax=axl, anom=True, plot=plot, ax_args=plot['data1']['ax_args'],
         pcolor_args=plot['data1']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lon, lat, data2, ax=axm, anom=True, plot=plot, ax_args=plot['data2']['ax_args'],
         pcolor_args=plot['data2']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
    func(lon, lat, compdata, ax=axr, anom=True, rmse=True, plot=plot, ax_args=plot['comp']['ax_args'],
         pcolor_args=plot['comp']['pcolor_args'], cblabel=units,
         **plot['plot_args'])
         
    plot_name = plotname(plot)
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

    # load trends data from netcdf file
    zonmean, units, x, depth = pl.zonal_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], plot['remap'], plot['remap_grid'], trends=True, seasons=plot['seasons'])    
    
    # scale data based on frequency
    zonmean, units = _trend_units(zonmean, units, plot)
    if plot['units']:
        units = plot['units']
    
    dft.filltitle(plot)
    _pcolor(zonmean, plot, anom=True)
    fig = plt.figure(figsize=(10,3))
    gs = gridspec.GridSpec(1, 1, width_ratios=[1, 1])   
    # make plot
    func(x, depth, zonmean, anom=True, plot=plot, ax=plt.subplot(gs[0, 0]), ax_args=plot['data1']['ax_args'],
         pcolor_args=plot['data1']['pcolor_args'], cblabel=units)

    plot_name = plotname(plot)
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

    zonmean, units, x, depth = pl.zonal_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], plot['remap'], plot['remap_grid'], trends=True, seasons=plot['seasons'])

    zonmean2, units2, x2, depth2 = pl.zonal_load(plot['comp_file'], plot['variable'], plot['comp_dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], plot['remap'], plot['remap_grid'], trends=True, depthneeded=list(depth), seasons=plot['comp_seasons'])

    # scale data based on frequency
    zonmean, units = _trend_units(zonmean, units, plot)
    zonmean2, units2 = _trend_units(zonmean2, units2, plot)
    if plot['units']:
        units = plot['units']

    compdata = zonmean - zonmean2
    dft.filltitle(plot)
    _comp_pcolor(zonmean, zonmean2, plot, anom=True)
    
    # make plots of data, comparison data, data - comparison data
    fig = plt.figure(figsize=(6, 8))
    gs = gridspec.GridSpec(3, 2, width_ratios=[20, 1])
    func(x, depth, zonmean, anom=True, plot=plot, ax=plt.subplot(gs[0, 0]), ax_args=plot['data1']['ax_args'],
         pcolor_args=plot['data1']['pcolor_args'], cblabel=units, cbaxis=plt.subplot(gs[0, 1]))
    func(x, depth, zonmean2, anom=True, plot=plot, ax=plt.subplot(gs[1, 0]), ax_args=plot['data2']['ax_args'],
         pcolor_args=plot['data2']['pcolor_args'], cblabel=units, cbaxis=plt.subplot(gs[1, 1]))
    func(x, depth, compdata, anom=True, rmse=True, plot=plot, ax=plt.subplot(gs[2, 0]), ax_args=plot['comp']['ax_args'],
         pcolor_args=plot['comp']['pcolor_args'], cblabel=units, cbaxis=plt.subplot(gs[2, 1]))

    plt.tight_layout()
    plot_name = plotname(plot)
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name

def histogram(plot, func):
    values = {}
    fdata, units, x, depth = pl.histogram_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], trends=True, depthneeded=None, seasons=plot['seasons'])  
    # scale data based on frequency
    fdata, units = _trend_units(fdata, units, plot)
    if not plot['units']:
        plot['units'] = units
    fdata = _1d_depth_data(fdata, depth, plot)
    values[plot['model_ID']] = fdata
    for o in plot['comp_obs']:
        data, units, x, depth = pl.histogram_load(plot['obs_file'][o], plot['variable'], plot['comp_dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], trends=True, depthneeded=plot['plot_depth'], seasons=plot['seasons'])
        data, units = _trend_units(data, units, plot)
        data = _1d_depth_data(data, depth, plot)
        values[o] = data
    for i in plot['comp_ids']:  
        data, units, x, depth = pl.histogram_load(plot['id_file'][i], plot['variable'], plot['comp_dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], trends=True, depthneeded=plot['plot_depth'], seasons=plot['seasons'])
        data, units = _trend_units(data, units, plot)
        data = _1d_depth_data(data, depth, plot)
        values[i] = data
    for m in plot['comp_models']:  
        data, units, x, depth = pl.histogram_load(plot['model_file'][m], plot['variable'], plot['comp_dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], trends=True, depthneeded=plot['plot_depth'], seasons=plot['seasons'])
        data, units = _trend_units(data, units, plot)
        data = _1d_depth_data(data, depth, plot)
        values[m] = data 
    cmipdata = []
    for f in plot['cmip5_files']:
        data, units, x, depth = pl.histogram_load(f, plot['variable'], plot['comp_dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], trends=True, depthneeded=plot['plot_depth'], seasons=plot['seasons'])
        data, units = _trend_units(data, units, plot)
        data = _1d_depth_data(data, depth, plot)
        cmipdata.append(data)
    
    
    dft.filltitle(plot)
    plot['data1']['ax_args']['xlabel'] = 'Trends ' + plot['comp_dates']['start_date'][:4] + '-' + plot['comp_dates']['end_date'][:4] + ' (' + units + ')'
    plot['data1']['ax_args']['ylabel'] = '# Realizations'
    pr.histogram(cmipdata, values, ax_args=plot['data1']['ax_args'], plot=plot)
    plot_name = plotname(plot)
    savefigures(plot_name, **plot)
    plot['units'] = units
    return plot_name
    
def timeseriesdata(plot, compfile, depth):
    data, units, x, depth = pl.timeseries_load(compfile, plot['variable'], plot['dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=plot['plot_depth'], seasons=plot['comp_seasons'], cdostring=plot['cdostring'])

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
    data, units, x, depth = pl.timeseries_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], seasons=plot['seasons'], cdostring=plot['cdostring'])

    plot['data1']['ax_args']['xlabel'] = 'Time'
    if 'ylabel' not in plot['data1']['ax_args']:
        if plot['units']:
            plot['data1']['ax_args']['ylabel'] = plot['units']
        else:
            plot['data1']['ax_args']['ylabel'] = units
            plot['units'] = units
    #plot['data1']['ax_args']['ylabel'] = 'mols-1'
    # get data at the correct depth 
    plot['plot_depth'] = None
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
    func(x, data, plot=plot, ax=ax, label=plot['model_ID'], ax_args=plot['data1']['ax_args'], color='b', zorder=6)
    handles = [mpatches.Patch(color='b', label=plot['model_ID'])]

    # plot comparison data on the same axis
    if plot['cmip5_file']:
        plot['comp_model'] = 'cmip5'
        data, x = timeseriesdata(plot, plot['cmip5_file'], depth)
        func(x, data, plot=plot, ax=ax, label=plot['comp_model'], ax_args=plot['data1']['ax_args'], color='g', zorder=4)
        handles.append(mpatches.Patch(color='g', label=str(plot['comp_model'])))
    for o in plot['comp_obs']:
        plot['comp_model'] = o
        data, x = timeseriesdata(plot, plot['obs_file'][o], depth)
        func(x, data, plot=plot, ax=ax, label=plot['comp_model'], ax_args=plot['data1']['ax_args'], color='k', zorder=5)
        handles.append(mpatches.Patch(color='k', label=str(plot['comp_model'])))
    for model in plot['comp_models']:
        plot['comp_model'] = model
        data, x = timeseriesdata(plot, plot['model_file'][model], depth)
        func(x, data, plot=plot, ax=ax, label=plot['comp_model'], ax_args=plot['data1']['ax_args'], color='r', zorder=2)
        handles.append(mpatches.Patch(color='r', label=str(plot['comp_model'])))
    for f in plot['cmip5_files']:
        try:
            plot['comp_model'] = 'cmip'
            data, x = timeseriesdata(plot, f, depth)
            func(x, data, plot=plot, ax=ax, label=None, ax_args=plot['data1']['ax_args'], color='0.75', zorder=1)
        except:
            pass 
    for i in plot['comp_ids']:
        plot['comp_model'] = i
        data, x = timeseriesdata(plot, plot['id_file'][i], depth)
        func(x, data, plot=plot, ax=ax, label=plot['comp_model'], ax_args=plot['data1']['ax_args'], color='y', zorder=3)
        handles.append(mpatches.Patch(color='y', label=str(plot['comp_model'])))

    ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1, 0.5))
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    plot_name = plotname(plot)
    savefigures(plot_name, **plot)
    return plot_name

def zonalmeandata(plot, compfile, ax, depth, func, color, zorder):
    try:
        data2, units2, x2, depth2 = pl.zonal_load(compfile, plot['variable'], plot['comp_dates'], depth, plot['comp_scale'], plot['comp_shift'], seasons=plot['comp_seasons'])
        if data2.ndim > 1:
            try:
                depth_ind = np.where(np.round(depth) == plot['plot_depth'])[0][0]
            except:
                print('Failed to extract depth ' + plot['plot_depth'] + ' for ' + plot['variable'])
                depth_ind = 0
            data2 = data2[depth_ind, :]
        func(x2, data2, plot=plot, ax=ax, label=plot['comp_model'], ax_args=plot['data1']['ax_args'], color=color, zorder=zorder)
    except: pass

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
    data, units, x, depth = pl.zonal_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], seasons=plot['seasons'])

    plot['data1']['ax_args']['xlabel'] = 'Latitude'
    if 'ylabel' not in plot['data1']['ax_args']:
        if plot['units']:
            plot['data1']['ax_args']['ylabel'] = plot['units']
        else:
            plot['data1']['ax_args']['ylabel'] = units
            plot['units'] = units
    # get data at the correct depth 
    plot['plot_depth'] = None

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
    func(x, data, plot=plot, ax=ax, ax_args=plot['data1']['ax_args'], color='r', zorder=6)
    handles = [mpatches.Patch(color='b', label=plot['model_ID'])] 
    
    # plot comparison data on the same axis
    if plot['comp_cmips']:
        plot['comp_model'] = 'cmip5'
        zonalmeandata(plot, plot['cmip5_file'], ax, depth, func, color='k', zorder=4)
        handles.append(mpatches.Patch(color='g', label='cmip5')) 
    for o in plot['comp_obs']:
        plot['comp_model'] = o
        zonalmeandata(plot, plot['obs_file'][o], ax, depth, func, color='b', zorder=5)
        handles.append(mpatches.Patch(color='k', label=str(plot['comp_model'])))
    for model in plot['comp_models']:
        plot['comp_model'] = model
        zonalmeandata(plot, plot['model_file'][model], ax, depth, func, color='g', zorder=2)        
        handles.append(mpatches.Patch(color='r', label=str(plot['comp_model'])))        
    for f in plot['cmip5_files']:
        plot['comp_model'] = 'cmip'
        zonalmeandata(plot, f, ax, depth, func, color='0.75', zorder=1)
    for i in plot['comp_ids']:
        plot['comp_model'] = i
        zonalmeandata(plot, plot['id_file'][i], ax, depth, func, color='y', zorder=3)
        handles.append(mpatches.Patch(color='y', label=str(plot['comp_model'])))
        
    ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1, 0.5))
    plot_name = plotname(plot)
    savefigures(plot_name, **plot)
    return plot_name


def taylor_full(plot, func):
    print 'plotting taylor diagram of ' + plot['variable']
#    plot['plot_depth'] = plot['depth']
    
    # load data from netcdf file
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], seasons=plot['seasons'])

    # start list of tuples to be plotted
    plotdata = [(data, plot['model_ID'])]

    # load observations data
    
    refdata, units, lon, lat, depth = pl.timeaverage_load(plot['obs_file'][plot['comp_obs'][0]], plot['variable'], plot['dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=list(depth), seasons=plot['comp_seasons']) 
 
    dft.filltitle(plot)
    cmip5data = []

    for f in plot['cmip5_files']:
        plot['comp_model'] = f
        data, units, lon, lat, depth = pl.timeaverage_load(f, plot['variable'], plot['dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=list(depth), seasons=plot['comp_seasons'])
        cmip5data.append((data, f))
    # get data from models and cmip and append to plotdata list
    if plot['cmip5_file']:
        plot['comp_model'] = 'cmip5'
        data, units, lon, lat, depth = pl.timeaverage_load(plot['cmip5_file'], plot['variable'], plot['dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=list(depth), seasons=plot['comp_seasons'])
        plotdata.append((data, 'cmip5'))
    for model in plot['comp_models']:
        plot['comp_model'] = model
        data, units, lon, lat, depth = pl.timeaverage_load(plot['model_file'][model], plot['variable'], plot['dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=list(depth), seasons=plot['comp_seasons'])
        plotdata.append((data, model))
    for i in plot['comp_ids']:
        plot['comp_model'] = i
        data, units, lon, lat, depth = pl.timeaverage_load(plot['id_file'][i], plot['variable'], plot['dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=list(depth), seasons=plot['comp_seasons'])
        plotdata.append((data, i))

            
    # make plot
    pr.taylordiagram(refdata, plotdata, cmip5data, plot=plot, ax_args=plot['data1']['ax_args'])
    
    plot_name = plotname(plot)
    plt.tight_layout()
    savefigures(plot_name, **plot)
    if not plot['units']:
        plot['units'] = units
    plot['comp_file'] = plot['obs_file']
    return plot_name
    
def taylor(plot, func):
    if not plot['is_depth']:
        return taylor_full(plot, func)

    print 'plotting taylor diagram of ' + plot['variable']
    plot['plot_depth'] = plot['depth']
    
    # load data from netcdf file
    data, units, lon, lat, depth = pl.timeaverage_load(plot['ifile'], plot['variable'], plot['dates'], plot['realm_cat'], plot['scale'], plot['shift'], seasons=plot['seasons'])
    
    # get data at correct depth
    data = _depth_data(data, depth, plot)
    

    # start list of tuples to be plotted
    plotdata = [(data, plot['model_ID'])]

    # load observations data
    data, units, lon, lat, depth = pl.timeaverage_load(plot['obs_file'][plot['comp_obs'][0]], plot['variable'], plot['dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=[plot['plot_depth']], seasons=plot['comp_seasons'])
    
    # get observations data at correct depth
    refdata = _depth_data(data, depth, plot)
    
    dft.filltitle(plot)
    cmip5data = []

    for f in plot['cmip5_files']:
        plot['comp_model'] = f
        data, units, lon, lat, depth = pl.timeaverage_load(f, plot['variable'], plot['dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=list(depth), seasons=plot['comp_seasons'])
        cmip5data.append((data, f))    
    # get data from models and cmip and append to plotdata list
    if plot['cmip5_file']:
        plot['comp_model'] = 'cmip5'
        data, units, lon, lat, depth = pl.timeaverage_load(plot['cmip5_file'], plot['variable'], plot['dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=[plot['plot_depth']], seasons=plot['comp_seasons'])
        plotdata.append((_depth_data(data, depth, plot), c))
    for model in plot['comp_models']:
        plot['comp_model'] = model
        data, units, lon, lat, depth = pl.timeaverage_load(plot['model_file'][model], plot['variable'], plot['dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=[plot['plot_depth']], seasons=plot['comp_seasons'])
        plotdata.append((_depth_data(data, depth, plot), model))
    for i in plot['comp_ids']:
        plot['comp_model'] = i
        data, units, lon, lat, depth = pl.timeaverage_load(plot['id_file'][i], plot['variable'], plot['dates'], plot['realm_cat'], plot['comp_scale'], plot['comp_shift'], depthneeded=[plot['plot_depth']], seasons=plot['comp_seasons'])
        plotdata.append((_depth_data(data, depth, plot), i))
            
    # make plot
    pr.taylordiagram(refdata, plotdata, cmip5data, plot=plot, ax_args=plot['data1']['ax_args'])
    
    plot_name = plotname(plot)
    plt.tight_layout()
    savefigures(plot_name, **plot)
    if not plot['units']:
        plot['units'] = units
    plot['comp_file'] = plot['obs_file']
    return plot_name
 
