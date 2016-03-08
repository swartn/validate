"""
plotregions
===============
This module contains the functions that will produce the plots
using matplotlib.

.. moduleauthor:: David Fallis
"""

import matplotlib as mpl
import subprocess
import os
import glob
import numpy as np
from numpy import mean, sqrt, square
from mpl_toolkits.basemap import Basemap, addcyclic, maskoceans
import matplotlib.pyplot as plt
import brewer2mpl
from discrete_cmap import discrete_cmap
from netCDF4 import Dataset
from colormaps import viridis
from taylor import TaylorDiagram
from operator import itemgetter
from math import ceil
import matplotlib.patches as mpatches
import cdo
cdo = cdo.Cdo()
plt.close('all')
font = {'size': 12}
plt.rc('font', **font)


def default_pcolor_args(data, anom=False):
    """Returns a dict with default pcolor params as key:value pairs

    Parameters
    ----------
    data : numpy array
    anom : boolean
           True if positive/negative display is wanted

    Returns
    -------
    dictionary
    """
    # Set 3-std range for colorbar to exclude outliers.
    if anom:
        # For anomalies, center range around 0
        anom_max = abs(data).mean() + abs(data).std() * 3.0
        vmin = -1 * anom_max
        vmax = anom_max
        # Anomaly cmap
        cmap = anom_cmap()

    else:
        mean = data.mean()
        std = data.std()
        dmax = data.max()
        dmin = data.min()       
        # otherwise, center around the mean
        vmin = mean - std * 3.0
        vmax = mean + std * 3.0
        print dmax
        print dmin
        print vmin
        print vmax
        
        if vmax > dmax and vmin < dmin:
            vmax = dmax
            vmin = dmin
        elif vmin < dmin:
            vmax = vmax + dmin - vmin
            if vmax > dmax:
                vmax = dmax
            vmin = dmin
        elif vmax > dmax:
            vmin = vmin + dmax - vmax
            if vmin < dmin:
                vmin = dmin
            vmax = dmax            
        print vmin
        print vmax    
        # Use true min/max if they are closer to the mean than the 3.0-std spread.
#        if vmax > dmax:
#            vmax = dmax
#        if vmin < dmin:
#            vmin = dmin()
        # New mpl, colorblind friendly, continuously varying, default cmap
        cmap = viridis

    d = {'vmin': vmin,
         'vmax': vmax,
         'cmap': cmap,
         'rasterized': True
         }

    return d


def anom_cmap():
    """return a discrete blue-red cmap from colorbrewer"""
    ncols = 11
    cmap_anom = brewer2mpl.get_map('RdBu', 'diverging', ncols,
                                   reverse=True).mpl_colormap
    cmap_anom = discrete_cmap(ncols, cmap_anom)
    return cmap_anom


def stats(plot, data, rmse):
    if rmse:
        vals = [str(np.round(data.min(), 1)), str(np.round(data.max(), 1)), str(np.round(sqrt(mean(square(data))), 1))]
        snam = ['min: ', 'max: ', 'rmse: ']
        plot['stats'] = {'rmse': float(vals[2]),
                         'min': float(vals[0]),
                         'max': float(vals[1]),
                         }
    else:
        vals = [str(np.round(data.min(), 1)), str(np.round(data.max(), 1)), str(np.round(data.mean(), 1))]
        snam = ['min: ', 'max: ', 'mean: ']
        plot['stats'] = {'mean': float(vals[2]),
                         'min': float(vals[0]),
                         'max': float(vals[1]),
                         }
    return vals, snam

def draw_stipple(pvalues, lon, lat, m, alpha):
        slons = []
        slats = []
        for index, value in np.ndenumerate(pvalues):
            if index[1]%4 == 0 and index[0]%2 == 0:
                if value < alpha:    
                    slons.append(lon[index[1]])
                    slats.append(lat[index[0]])
        a,b = m(slons, slats)
        m.plot(a,b, '.', markersize=0.3, color='k', zorder=1)

def draw_trend_stipple(data, cvalues, lon, lat, m):        
        slons = []
        slats = []
        for index, value in np.ndenumerate(cvalues):
            if index[1]%4 == 0 and index[0]%2 == 0:
                if abs(value) < data[index[0]][index[1]]:             
                    slons.append(lon[index[1]])
                    slats.append(lat[index[0]])
        a,b = m(slons, slats)
        m.plot(a,b, '.', markersize=0.3, color='k', zorder=1)      
  
def global_map(lon, lat, data, pvalues=None, cvalues=None, alpha=None, ax=None, ax_args=None, pcolor_args=None, cblabel='', anom=False, rmse=False,
               latmin=-50, latmax=50, lonmin=0, lonmax=360, draw_contour=False,
               fill_continents=False, fill_oceans=False, draw_parallels=True, draw_meridians=False, plot={}):
    """Pcolor a var in a global map, using ax if supplied"""
    # setup a basic global map
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    else:
        fig = plt.gcf()

    if not pcolor_args:
        pcolor_args = default_pcolor_args(data, anom)

    for key, value in default_pcolor_args(data).iteritems():
        if key not in pcolor_args or (pcolor_args[key] is None):
            pcolor_args[key] = value

    m = Basemap(projection='kav7', llcrnrlat=latmin, urcrnrlat=latmax, llcrnrlon=lonmin, urcrnrlon=lonmax, lon_0=-180, resolution='c', ax=ax)
    lons, lats = np.meshgrid(lon, lat)
    x, y = m(lons, lats)

    cot = m.pcolor(x, y, data, **pcolor_args)

    if ax_args:
        plt.setp(ax, **ax_args)
    if draw_contour:
        m.contour(x, y, data, colors=['k'], 
                   vmin=pcolor_args['vmin'], vmax=pcolor_args['vmax'])
    ax.autoscale(enable=True, axis='both', tight=True)
    m.drawcoastlines(linewidth=1.25, ax=ax)

    if fill_continents:
        m.fillcontinents(color='0.8', ax=ax, zorder=2)
    if draw_parallels:
        m.drawparallels(np.arange(-80, 81, 20), labels=[1, 0, 0, 0], linewidth=0, ax=ax)
    if draw_meridians:
        m.drawmeridians(np.arange(0, 360, 90), labels=[0, 0, 0, 1], linewidth=0, yoffset=0.5e6, ax=ax)
    if fill_oceans:
        m.drawlsmask(ocean_color='0.7')

    if alpha:
        draw_stipple(pvalues, lon, lat, m, alpha)

    if cvalues is not None:
        draw_trend_stipple(data, cvalues, lon, lat, m)
    
    m.colorbar(mappable=cot, location='right', label=cblabel)

    vals, snam = stats(plot, data, rmse)
    val = [s + v for s, v in zip(snam, vals)]
    x, y = (9000000, -800000)
    ax.text(x, y, '  '.join(val), fontsize=7)


def polar_map(lon, lat, data, pvalues=None, cvalues=None, alpha=None, ax=None, ax_args=None, pcolor_args=None, cblabel='', anom=False, rmse=False,
              latmin=40, latmax=80, lonmin=0, lonmax=360, lon_0=180, draw_contour=False,
              fill_continents=False, fill_oceans=False, draw_parallels=True, draw_meridians=True, plot={}):
    """Pcolor a var in a north polar map, using ax if supplied"""
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    else:
        fig = plt.gcf()

    if not pcolor_args:
        pcolor_args = default_pcolor_args(data, anom)

    for key, value in default_pcolor_args(data).iteritems():
        if key not in pcolor_args or (pcolor_args[key] is None):
            pcolor_args[key] = value

    m = Basemap(projection='npstere', boundinglat=latmin, lon_0=lon_0, resolution='c', round=True, ax=ax)

    lons, lats = np.meshgrid(lon, lat)
    x, y = m(lons, lats)

    cot = m.pcolor(x, y, data, **pcolor_args)

    if ax_args:
        plt.setp(ax, **ax_args)

    if draw_contour:
        m.contour(x, y, data, colors=['k'], 
                   vmin=pcolor_args['vmin'], vmax=pcolor_args['vmax'])
    m.drawcoastlines()
    if fill_continents:
        m.fillcontinents(color='0.8', ax=ax, zorder=2)
    if draw_parallels:
        m.drawparallels(np.arange(-80., 81., 20.))
    if draw_meridians:
        m.drawmeridians(np.arange(-180., 181., 20.))
    m.drawmapboundary()

    if alpha:
        draw_stipple(pvalues, lon, lat, m, alpha)    

    if cvalues is not None:
        draw_trend_stipple(data, cvalues, lon, lat, m)
            
    m.colorbar(mappable=cot, location='right', label=cblabel)

    vals, snam = stats(plot, data, rmse)
    val = [s + v for s, v in zip(snam, vals)]
    x, y = m(135, 20)
    ax.text(x, y, '  '.join(val), fontsize=7)


def polar_map_south(lon, lat, data, pvalues=None, cvalues=None, alpha=None, ax=None, ax_args=None, pcolor_args=None, cblabel='', anom=False, rmse=False,
                    latmin=-80, latmax=-40, lonmin=0, lonmax=360, lon_0=180, draw_contour=False,
                    fill_continents=False, fill_oceans=False, draw_parallels=True, draw_meridians=True, plot={}):
    """Pcolor a var in a south polar map, using ax if supplied"""
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    else:
        fig = plt.gcf()

    if not pcolor_args:
        pcolor_args = default_pcolor_args(data, anom)

    for key, value in default_pcolor_args(data).iteritems():
        if key not in pcolor_args or (pcolor_args[key] is None):
            pcolor_args[key] = value

    m = Basemap(projection='spstere', boundinglat=latmax, lon_0=lon_0, resolution='c', round=True, ax=ax)

    lons, lats = np.meshgrid(lon, lat)
    x, y = m(lons, lats)

    cot = m.pcolor(x, y, data, **pcolor_args)

    if ax_args:
        plt.setp(ax, **ax_args)

    if draw_contour:
        m.contour(x, y, data, colors=['k'], 
                   vmin=pcolor_args['vmin'], vmax=pcolor_args['vmax'])
                   
    m.drawcoastlines()
    if fill_continents:
        m.fillcontinents(color='0.8', ax=ax, zorder=2)
    if draw_parallels:
        m.drawparallels(np.arange(-80., 81., 20.))
    if draw_meridians:
        m.drawmeridians(np.arange(-180., 181., 20.))
    if fill_oceans:
        m.drawlsmask(ocean_color='0.7')
    m.drawmapboundary()
 
    if alpha:
        draw_stipple(pvalues, lon, lat, m, alpha)

    if cvalues is not None:
        draw_trend_stipple(data, cvalues, lon, lat, m)
           
    m.colorbar(mappable=cot, location='right', label=cblabel)
    vals, snam = stats(plot, data, rmse)
    val = [s + v for s, v in zip(snam, vals)]
    x, y = m(-135, -20)
    ax.text(x, y, '  '.join(val), fontsize=7)


def mercator(lon, lat, data, pvalues=None, cvalues=None, alpha=None, ax=None, ax_args=None, pcolor_args=None, cblabel='', anom=False, rmse=False, plot={},
             latmin=-80, latmax=80, lonmin=0, lonmax=360, draw_contour=False,
             fill_continents=False, fill_oceans=False, draw_parallels=False, draw_meridians=False):
    """Pcolor a var in a mercator plot, using ax if supplied"""
    if not pcolor_args:
        pcolor_args = default_pcolor_args(data, anom)
    for key, value in default_pcolor_args(data).iteritems():
        if key not in pcolor_args or (pcolor_args[key] is None):
            pcolor_args[key] = value

    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    else:
        fig = plt.gcf()
    m = Basemap(projection='merc', llcrnrlat=latmin, urcrnrlat=latmax, llcrnrlon=lonmin, urcrnrlon=lonmax, lat_ts=20, resolution='c', ax=ax)

    lons, lats = np.meshgrid(lon, lat)
    x, y = m(lons, lats)

    cot = m.pcolor(x, y, data, **pcolor_args)
    if ax_args:
        plt.setp(ax, **ax_args)

    if draw_contour:
        m.contour(x, y, data, colors=['k'], 
                  vmin=pcolor_args['vmin'], vmax=pcolor_args['vmax'])
                   
    m.drawcoastlines()
    if fill_continents:
        m.fillcontinents(color='0.8', ax=ax, zorder=2)
    if draw_parallels:
        m.drawparallels(np.arange(-80., 81., 20.))
    if draw_meridians:
        m.drawmeridians(np.arange(-180., 181., 20.))
    m.drawmapboundary()
    
    if alpha:
        draw_stipple(pvalues, lon, lat, m, alpha)

    if cvalues is not None:
        draw_trend_stipple(data, cvalues, lon, lat, m)
   
    m.colorbar(mappable=cot, location='right', label=cblabel)
    vals, snam = stats(plot, data, rmse)
    val = [s + v for s, v in zip(snam, vals)]
    x, y = m(lonmin + 2, latmin - 2)
    ax.text(x, y, '  '.join(val), fontsize=7)


def _fix_1Ddata(z, data, ax_args):
    """ Extends section data if it is in only on dimension
    """
    newdata = range(0, 5)
    for n in range(0, 5):
        newdata[n] = data
    ax_args['ylabel'] = ''
    ax_args['yticks'] = []
    return np.array(range(0, 5)), np.array(newdata), ax_args


def section(x, z, data, ax=None, rmse=False, pvalues=None, alpha=None, ax_args=None, pcolor_args=None, plot={}, cblabel='', anom=False, cbaxis=None):
    """Pcolor a var in a section, using ax if supplied"""
    if len(data.shape) == 1:
        z, data, ax_args = _fix_1Ddata(z, data, ax_args)
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        fig.subplots_adjust(top=0.8, right=0.8)
    else:
        fig = plt.gcf()

    if not pcolor_args:
        pcolor_args = default_pcolor_args(data, anom)
    for key, value in default_pcolor_args(data).iteritems():
        if key not in pcolor_args or (pcolor_args[key] is None):
            pcolor_args[key] = value

    cot = ax.pcolormesh(x, z, data, **pcolor_args)
    if plot['variable'] == 'msftmyz':
        cts = np.arange(-25,25, 1)
        ax.contour(x, z, data, cts, colors=['k'], vmin=pcolor_args['vmin'],
                   vmax=pcolor_args['vmax'])
    else:
        ax.contour(x, z, data, colors=['k'], vmin=pcolor_args['vmin'],
                   vmax=pcolor_args['vmax'])
               

    ax.invert_yaxis()
    ax.autoscale(True, axis='both', tight='both')

    ax.set_yscale(plot['set_yscale'])

    if ax_args:
        plt.setp(ax, **ax_args)

    if alpha:
        slons = []
        sdepths = []
        for index, value in np.ndenumerate(pvalues):
            if index[1]%4 == 0:
                if value < alpha:
                    slons.append(x[index[1]])
                    sdepths.append(z[index[0]])
        ax.plot(slons, sdepths, '.', markersize=0.2, color='k')
#    plt.show()
    box = ax.get_position()
    if cbaxis:
        fig.colorbar(cot, cax=cbaxis, label=cblabel)
    else:
        tl = fig.add_axes([box.x1 + box.width * 0.05, box.y0, 0.02, box.height])
        fig.colorbar(cot, cax=tl, label=cblabel)

    if rmse:
        vals = [str(np.round(data.min(), 1)), str(np.round(data.max(), 1)), str(np.round(sqrt(mean(square(data))), 1))]
        plot['stats'] = {'rmse': float(vals[2]),
                         'min': float(vals[0]),
                         'max': float(vals[1]),
                         }
        snam = ['min: ', 'max: ', 'rmse: '] 
    else:
        vals = [str(np.round(data.min(), 1)), str(np.round(data.max(), 1)), str(np.round(data.mean(), 1))]
        plot['stats'] = {'mean': float(vals[2]),
                         'min': float(vals[0]),
                         'max': float(vals[1]),
                         }
        snam = ['min: ', 'max: ', 'mean: ']
    val = [s + v for s, v in zip(snam, vals)]
    ax.text(.75, -.2, '  '.join(val), horizontalalignment='left', verticalalignment='bottom', fontsize=7, transform = ax.transAxes) 

def timeseries(x, data, ax=None, ax_args=None, label='model', plot={}, color=None, zorder=None):
    """ Makes a timeseries line plot, using ax if supplied
    """
    if data.shape != x.shape:
        data = data[:x.shape[0]]
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    else:
        fig = plt.gcf()

    ax.plot(x, data, label=label, color=color, zorder=zorder)

    plt.setp(ax, **ax_args)
    plot['stats'] = 'N/A'


def zonalmean(x, data, ax=None, ax_args=None, label='model', plot={}, color=None, zorder=None):
    """ Makes a zonal mean line plot, using ax if supplied
    """
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    else:
        fig = plt.gcf()
    ax.plot(x, data, label=label, color=color, zorder=zorder)

    plt.setp(ax, **ax_args)
    plot['stats'] = 'N/A'


def taylordiagram(refdata, plotdata, unlabelled_data, fig=None, ax_args=None, plot={}):

    flatrefdata = refdata.flatten()
    refstd = refdata.std(ddof=1)
    for i, (d, n) in enumerate(plotdata):
        plotdata[i] = d.flatten(), n

    plot['stats'] = {'obserations': {'standard deviation': float(refstd)}}
    
    for i, (d, n) in enumerate(unlabelled_data):
        unlabelled_data[i] = d.flatten(), n

    samples = [[m.std(ddof=1), np.ma.corrcoef(flatrefdata, m)[0, 1], n] for m, n in plotdata]
    unlabelled_samples = [[m.std(ddof=1), np.ma.corrcoef(flatrefdata, m)[0,1], n] for m, n in unlabelled_data]
    
    if not fig:
        fig = plt.figure()
    else:
        fig = plt.gcf()

    stdrange = max(samples, key=itemgetter(1))[0] * 1.3 / refstd
    if stdrange <= refstd * 1.5 / refstd:
        stdrange = refstd * 1.5 / refstd

    dia = TaylorDiagram(refstd, fig=fig, label=plot['comp_obs'][0], srange=(0, stdrange))
    colors = plt.matplotlib.cm.jet(np.linspace(0, 1, len(samples)))
    
    for i, (stddev, corrcoef, n) in enumerate(samples):
        if corrcoef < 0:
            corrcoef = 0
        plot['stats'][n] = {'standard deviation': float(stddev),
                            'correlation coefficient': float(corrcoef)} 
        dia.add_sample(stddev, corrcoef,
                       marker='.', ms=12, ls='',
                       mfc=colors[i], mec=colors[i],
                       label=n, zorder=2)
    fig.legend(dia.samplePoints,
               [p.get_label() for p in dia.samplePoints],
               numpoints=1, prop=dict(size='small'), loc='upper right')
    
    for i, (stddev, corrcoef, n) in enumerate(unlabelled_samples):
        if corrcoef <= 0:
            continue
        plot['stats'][n] = {'standard deviation': float(stddev),
                            'correlation coefficient': float(corrcoef)}         
        dia.add_sample(stddev, corrcoef,
                       marker='.', ms=5, ls='',
                       mfc='grey', mec='grey',
                       label=None, zorder=1) 
                       

   
    dia.add_grid()

    contours = dia.add_contours(colors='0.5')
    plt.clabel(contours, inline=1, fontsize=10)

    if 'title' in ax_args:
        plt.title(ax_args['title'])

def histogram(data, values, ax=None, ax_args=None, plot={}):
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    else:
        fig = plt.gcf()
    
    n, bins, patches = plt.hist(data, 10, facecolor='grey', alpha=0.75)
    ymax = int(ceil(1.2 * max(n)))
    ax.set_ylim(0, ymax)
    
#    colormap = plt.cm.gist_rainbow
#    ax.set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, len(values))])
    for key in values:
        plt.axvline(values[key], label=key, linewidth=4,
                    color=next(ax._get_lines.color_cycle))
    plt.setp(ax, **ax_args)
    if 'title' in ax_args:
        plt.title(ax_args['title'])
    
    ax.legend(loc='best')
    

if __name__ == "__main__":
    pass
