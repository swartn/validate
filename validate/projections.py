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
from matplotlib.colors import LogNorm
import cdo
cdo = cdo.Cdo()
plt.close('all')
font = {'size': 9}
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


def worldmap(projection, lon, lat, data, pvalues=None, cvalues=None, alpha=None, ax=None,
              ax_args=None, pcolor_args=None, cblabel='', anom=False, rmse=False,
              latmin=-80, latmax=80, lonmin=0, lonmax=360, lon_0=180, draw_contour=False,
              label=None,
              fill_continents=False, draw_parallels=True, draw_meridians=False,
              plot={}):
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    else:
        fig = plt.gcf()
    
    if not pcolor_args:
        pcolor_args = default_pcolor_args(data, anom)

    for key, value in default_pcolor_args(data).iteritems():
        if key not in pcolor_args or (pcolor_args[key] is None):
            pcolor_args[key] = value

    if projection == 'global_map':
        m = Basemap(projection='kav7', llcrnrlat=latmin, urcrnrlat=latmax, 
                    llcrnrlon=lonmin, urcrnrlon=lonmax, 
                    lon_0=-180, resolution='c', ax=ax)
        a, b = (9000000, -1000000)
        parallel_labels = [1, 0, 0, 0]
        meridian_labels = [0, 0, 0, 0]
    if projection == 'mercator':
        m = Basemap(projection='merc', llcrnrlat=latmin, urcrnrlat=latmax, 
                    llcrnrlon=lonmin, urcrnrlon=lonmax, 
                    lat_ts=20, resolution='c', ax=ax)
        a, b = m(lonmin + 2, latmin - 2)
        parallel_labels = [0, 0, 0, 0]
        meridian_labels = [0, 0, 0, 0]
    if projection == 'polar_map':
        m = Basemap(projection='npstere', boundinglat=latmin, 
                    lon_0=lon_0, resolution='c', round=True, ax=ax)
        a, b = m(135, 20)
        parallel_labels = [0, 0, 0, 0]
        meridian_labels = [0, 0, 0, 0]
    if projection == 'polar_map_south':
        m = Basemap(projection='spstere', boundinglat=latmax, 
                    lon_0=lon_0, resolution='c', round=True, ax=ax)
        a, b = m(-135, -20) 
        parallel_labels = [0, 0, 0, 0]
        meridian_labels = [0, 0, 0, 0]  

    lons, lats = np.meshgrid(lon, lat)
    x, y = m(lons, lats)
    cot = m.pcolormesh(x, y, data, **pcolor_args)
    
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
        m.drawparallels(np.arange(-80, 81, 20), labels=parallel_labels, ax=ax, fontsize=9)
    if draw_meridians:
        print 'here'
        m.drawmeridians(np.arange(0, 360, 90), labels=meridian_labels, yoffset=0.5e6, ax=ax, fontsize=9)

    if pvalues is not None:
        draw_stipple(pvalues, lon, lat, m, alpha)

    if cvalues is not None:
        draw_trend_stipple(data, cvalues, lon, lat, m)

    cbar = m.colorbar(mappable=cot, location='right', label=cblabel)
    cbar.solids.set_edgecolor("face") 
    if label is not None:
        ax.text(a, b, label, fontsize=7)

def section(x, z, data, ax=None, rmse=False, pvalues=None, alpha=None, ax_args=None, pcolor_args=None, plot={}, cblabel='', anom=False, cbaxis=None):
    """Pcolor a var in a section, using ax if supplied"""
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

    cot = ax.pcolormesh(x, z, data, shading='gouraud', **pcolor_args)
    if plot['variable'] == 'msftmyz':
        cts = np.around(np.arange(-25,25, 2), decimals=1)
        cs = ax.contour(x, z, data, cts, colors=['k'], vmin=pcolor_args['vmin'],
                   vmax=pcolor_args['vmax'])
        plt.clabel(cs,  inline=True, fmt='%r', fontsize= 3)
    else:
        ax.contour(x, z, data, colors=['k'], vmin=pcolor_args['vmin'],
                   vmax=pcolor_args['vmax'])
               

    ax.invert_yaxis()
    ax.autoscale(True, axis='both', tight='both')

    ax.set_yscale(plot['set_yscale'])

    if ax_args:
        plt.setp(ax, **ax_args)

    if pvalues is not None:
        slons = []
        sdepths = []
        for index, value in np.ndenumerate(pvalues):
            if index[1]%4 == 0:
                if value < alpha:
                    slons.append(x[index[1]])
                    sdepths.append(z[index[0]])
        ax.plot(slons, sdepths, '.', markersize=0.2, color='k')

    box = ax.get_position()
    if cbaxis:
        fig.colorbar(cot, cax=cbaxis, label=cblabel)
    else:
        tl = fig.add_axes([box.x1 + box.width * 0.05, box.y0, 0.02, box.height])
        fig.colorbar(cot, cax=tl, label=cblabel)

    vals = [str(np.round(data.min(), 1)), str(np.round(data.max(), 1))]
    plot['stats'] = {'min': float(vals[0]),
                     'max': float(vals[1]),
                     }
    snam = ['min: ', 'max: ']    
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


def zonalmean(x, data, ax=None, ax_args={}, label='model', plot={}, color=None, zorder=None):
    """ Makes a zonal mean line plot, using ax if supplied
    """
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    else:
        fig = plt.gcf()
    ax.plot(x, data, label=label, color=color, zorder=zorder)
    plt.xlim(-90, 90)
    if ax_args:
        plt.setp(ax, **ax_args)
    plot['stats'] = 'N/A'


def taylordiagram(refdata, labelled_data, unlabelled_data, fig=None, ax_args=None, plot={}):

    flatrefdata = refdata.flatten()
    refstd = refdata.std(ddof=1)
    for i, (d, n, c) in enumerate(labelled_data):
        labelled_data[i] = d.flatten(), n, c

    plot['stats'] = {'obserations': {'standard deviation': float(refstd)}}
    
    for i, (d, n) in enumerate(unlabelled_data):
        unlabelled_data[i] = d.flatten(), n

    labelled_samples = [[m.std(ddof=1), np.ma.corrcoef(flatrefdata, m)[0, 1], n, c] for m, n, c in labelled_data]
    unlabelled_samples = [[m.std(ddof=1), np.ma.corrcoef(flatrefdata, m)[0,1], n] for m, n in unlabelled_data]
    
    if not fig:
        fig = plt.figure()
    else:
        fig = plt.gcf()

    stdrange = max(labelled_samples, key=itemgetter(1))[0] * 1.3 / refstd
    if stdrange <= refstd * 1.5 / refstd:
        stdrange = refstd * 1.5 / refstd

    dia = TaylorDiagram(refstd, fig=fig, label=plot['comp_obs'][0], srange=(0, stdrange))
#    colors = plt.matplotlib.cm.jet(np.linspace(0, 1, len(samples)))
    
    for i, (stddev, corrcoef, n, c) in enumerate(labelled_samples):
        if corrcoef < 0:
            corrcoef = 0
        plot['stats'][n] = {'standard deviation': float(stddev),
                            'correlation coefficient': float(corrcoef)} 
        dia.add_sample(stddev, corrcoef,
                       marker='.', ms=12, ls='',
                       mfc=c, mec=c,
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

def taylor_from_stats(labelled_data, unlabelled_data, obs_label='observation', fig=None, label=None, ax_args=None):
    if not fig:
        fig = plt.figure()
    else:
        fig = plt.gcf()

    stdrange = max([item['std'] for item in labelled_data]) * 1.3
    if stdrange <= 1.5:
        stdrange = 1.5
 
    dia = TaylorDiagram(1, fig=fig, label=obs_label, srange=(0, stdrange))
    handles_dictionary = {}
    for i, sample in enumerate(labelled_data):
        if sample['corrcoef'] < 0:
            sample['corrcoef'] = 0
        if 'color' not in sample:
            dia.add_sample(sample['std'], sample['corrcoef'],
                       marker=sample['marker'], ms=8, ls='',
                       zorder=sample['zorder'],
                       label=sample['name'])
        else:
            dia.add_sample(sample['std'], sample['corrcoef'],
                       marker=sample['marker'], ms=8, ls='',
                       mfc=sample['color'], mec=sample['color'],
                       zorder=sample['zorder'],
                       label=sample['name'])        
        handles_dictionary[sample['name']] = sample['color']
    handles = [mpatches.Patch(color=color, label=name) for name, color in handles_dictionary.iteritems()]
    handles = [mpatches.Patch(color='b')] + handles
    labels = [obs_label] + handles_dictionary.keys()   
  
    fig.legend(handles, labels, numpoints=1, loc='upper right')

    for sample in unlabelled_data:         
        if sample['corrcoef'] < 0:
            sample['corrcoef'] = 0
        if 'color' not in sample:
            dia.add_sample(sample['std'], sample['corrcoef'],
                       marker=sample['marker'], ms=8, ls='',
                       zorder=sample['zorder']-1,
                       label=sample['name'])
        else:         
            dia.add_sample(sample['std'], sample['corrcoef'],
                       marker=sample['marker'], ms=8, ls='',
                       mfc=sample['color'], mec=sample['color'],
                       zorder=sample['zorder']-1,
                       label=sample['name'])

    dia.add_grid(True, axis='x', linestyle='--', alpha=0.6,
                 color='0.5', zorder=0)
                  
    contours = dia.add_contours(colors='0.5')
    plt.clabel(contours, inline=1, fontsize=10)

    if 'title' in ax_args:
        plt.title(ax_args['title'])    
    if label is not None:
         fig.text(0.1, 0, label, fontsize=7)       
          
           
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
    for sample in values:
        plt.axvline(sample['data'], label=sample['name'], linewidth=4,
                    color=sample['color'])
    plt.setp(ax, **ax_args)
    if 'title' in ax_args:
        plt.title(ax_args['title'])
    
    ax.legend(loc='best')
    
def scatter(data, data2, ax=None, ax_args=None, plot={}):
    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    else:
        fig = plt.gcf()
    x = data.flatten()
    y = data2.flatten()
    ax.scatter(x, y, marker='.', c='0.5', s=0.3)
    if ax_args:
        plt.setp(ax, **ax_args)  

if __name__ == "__main__":
    pass
