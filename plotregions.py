import subprocess
import os
import glob
import numpy as np
from mpl_toolkits.basemap import Basemap, addcyclic, maskoceans
import matplotlib.pyplot as plt
import matplotlib as mpl
import brewer2mpl
from discrete_cmap import discrete_cmap
plt.close('all')
font = {'size'   : 12}
plt.rc('font', **font)
from netCDF4 import Dataset
import cdo; cdo = cdo.Cdo()
from colormaps import viridis
def default_pcolor_args(data, anom=False):
    """Returns a dict with default pcolor params as key:value pairs"""

    # Set 3-std range for colorbar to exclude outliers.
    if anom:
        # For anomalies, center range around 0
        anom_max = abs(data).mean() + abs(data).std()*3.0
        vmin = -1*anom_max
        vmax = anom_max
        # Anomaly cmap
        cmap = anom_cmap()
    else:
        # otherwise, center around the mean
        vmin = data.mean() - data.std()*3.0
        vmax = data.mean() + data.std()*3.0
        # Use true min/max if they are closer to the mean than the 3-std spread.
        if vmax > data.max() : vmax = data.max()
        if vmin < data.min() : vmin = data.min()
        # New mpl, colorblind friendly, continuously varying, default cmap
        cmap = viridis

    d = {'vmin' : vmin,
         'vmax' : vmax,
         'cmap' : cmap,
         'rasterized' : True
         }

    return d

def anom_cmap():
    """return a discrete blue-red cmap from colorbrewer"""
    ncols = 11
    cmap_anom = brewer2mpl.get_map('RdBu', 'diverging', ncols,
                                   reverse=True).mpl_colormap
    cmap_anom = discrete_cmap(ncols, cmap_anom)
    return cmap_anom
    
def global_map(lon, lat, data, ax=None, ax_args=None, pcolor_args=None, cblabel='', anom = False,
               latmin=-50, latmax=50, lonmin=0, lonmax=360, 
               fill_continents=False, fill_oceans=False, draw_parallels=True, draw_meridians=False):
    """Pcolor a var in a global map, using ax if supplied"""
    # setup a basic global map
    if not ax:
        fig, ax = plt.subplots(1,1, figsize=(8,8))
    else:
        fig = plt.gcf()

    if not pcolor_args : pcolor_args = default_pcolor_args(data, anom)

    for key, value in default_pcolor_args(data).iteritems():
        if key not in pcolor_args or (pcolor_args[key] is None):
            pcolor_args[key] = value

    m = Basemap(projection='kav7',llcrnrlat=latmin,urcrnrlat=latmax,llcrnrlon=lonmin,urcrnrlon=lonmax, lon_0=-180,resolution='c', ax=ax)
    lons, lats = np.meshgrid(lon, lat)
    x, y = m(lons, lats)

    cot = m.pcolor(x, y, data, **pcolor_args)

    if ax_args:
        plt.setp(ax, **ax_args)

    ax.autoscale(enable=True, axis='both', tight=True)
    m.drawcoastlines(linewidth=1.25, ax=ax)
    
    if fill_continents:
        m.fillcontinents(color='0.8',ax=ax, zorder=2)
    if draw_parallels:
        m.drawparallels(np.arange(-80,81,20),labels=[1,0,0,0], linewidth=0, ax=ax)
    if draw_meridians:
        m.drawmeridians(np.arange(0,360,90),labels=[0,0,0,1], linewidth=0,yoffset=0.5e6, ax=ax)
    if fill_oceans:
        m.drawlsmask(ocean_color='0.7')
        
    m.colorbar(mappable=cot, location='right', label=cblabel)
    vals = [data.min(), data.max(), data.mean()]
    snam = ['min: ', 'max: ', 'mean: ']   
    vals = [s + str(np.round(v,1)) for s, v in zip(snam, vals)]
    x, y = m(10, -88)
    ax.text(x, y, '  '.join(vals), fontsize=8)

def polar_map(lon, lat, data, ax=None, ax_args=None, pcolor_args=None, cblabel='', anom = False,
              latmin=30, latmax=80, lonmin=0, lonmax=360,
              fill_continents=True, fill_oceans = False, draw_parallels=True, draw_meridians=True):


    if not ax:
        fig, ax = plt.subplots(1,1, figsize=(8,8))
    else:
        fig = plt.gcf()
        
    if not pcolor_args : pcolor_args = default_pcolor_args(data, anom)
    
    for key, value in default_pcolor_args(data).iteritems():
        if key not in pcolor_args or (pcolor_args[key] is None):
            pcolor_args[key] = value  


    m = Basemap(projection='npstere',boundinglat=latmin,lon_0=270,resolution='c', ax=ax)
    
    lons, lats = np.meshgrid(lon, lat)
    x, y = m(lons, lats)

    cot = m.pcolor(x, y, data, **pcolor_args)

    if ax_args:
        plt.setp(ax, **ax_args)    
        
    m.drawcoastlines()
    if fill_continents:
        m.fillcontinents(color='0.8',ax=ax)
    if draw_parallels:
        m.drawparallels(np.arange(-80.,81.,20.))
    if draw_meridians:
        m.drawmeridians(np.arange(-180.,181.,20.))
    m.drawmapboundary()
    m.colorbar(mappable=cot, location='right', label=cblabel)
    vals = [data.min(), data.max(), data.mean()]
    snam = ['min: ', 'max: ', 'mean: ']

    vals = [s + str(np.round(v,1)) for s, v in zip(snam, vals)]
    x, y = m(-135, 12)
    ax.text(x, y, '  '.join(vals), fontsize=8)

def polar_map_south(lon, lat, data, ax=None, ax_args=None, pcolor_args=None, cblabel='', anom = False,
                    latmin=-90, latmax=-30, lonmin=0, lonmax=360,
                    fill_continents=True, fill_oceans = False, draw_parallels=True, draw_meridians=True):


    if not pcolor_args : pcolor_args = default_pcolor_args(data, anom)
    
    for key, value in default_pcolor_args(data).iteritems():
        if key not in pcolor_args or (pcolor_args[key] is None):
            pcolor_args[key] = value  

    if not ax:
        fig, ax = plt.subplots(1,1, figsize=(8,8))
    else:
        fig = plt.gcf()
    m = Basemap(projection='spstere',boundinglat=latmax,lon_0=270,resolution='c')
    
    lons, lats = np.meshgrid(lon, lat)
    x, y = m(lons, lats)

    cot = m.pcolor(x, y, data, **pcolor_args)

    if ax_args:
        plt.setp(ax, **ax_args)    
        
    m.drawcoastlines()
    if fill_continents:
        m.fillcontinents(color='0.8',ax=ax)
    if draw_parallels:
        m.drawparallels(np.arange(-80.,81.,20.))
    if draw_meridians:
        m.drawmeridians(np.arange(-180.,181.,20.))
    if fill_oceans:
        m.drawlsmask(ocean_color='0.7')
    m.drawmapboundary()
    m.colorbar(mappable=cot, location='right', label=cblabel)
    vals = [data.min(), data.max(), data.mean()]
    snam = ['min: ', 'max: ', 'mean: ']
    vals = [s + str(np.round(v,1)) for s, v in zip(snam, vals)]
    x, y = m(-45, -12)
    ax.text(x, y, '  '.join(vals), fontsize=8)

def mercator(lon, lat, data, ax=None, ax_args=None, pcolor_args=None, cblabel='', anom=False,
             latmin=-80, latmax=80, lonmin=0, lonmax=360,
             fill_continents=False, fill_oceans=False, draw_parallels=True, draw_meridians=True):

    if not pcolor_args : pcolor_args = default_pcolor_args(data, anom)
    for key, value in default_pcolor_args(data).iteritems():
        if key not in pcolor_args or (pcolor_args[key] is None):
            pcolor_args[key] = value  

    if not ax:
        fig, ax = plt.subplots(1,1, figsize=(8,8))
    else:
        fig = plt.gcf()
    m = Basemap(projection='merc',llcrnrlat=latmin,urcrnrlat=latmax,llcrnrlon=lonmin,urcrnrlon=lonmax,lat_ts=20,resolution='c')
    
    lons, lats = np.meshgrid(lon, lat)
    x, y = m(lons, lats)
                    
                
         
        
    cot = m.pcolor(x, y, data, **pcolor_args)

    if ax_args:
        plt.setp(ax, **ax_args)    
    
    m.drawcoastlines()
    if fill_continents:
        m.fillcontinents(color='0.8',ax=ax)
    if draw_parallels:
        m.drawparallels(np.arange(-80.,81.,20.))
    if draw_meridians:
        m.drawmeridians(np.arange(-180.,181.,20.))
    m.drawmapboundary()

    m.colorbar(mappable=cot, location='right', label=cblabel)
    vals = [data.min(), data.max(), data.mean()]
    snam = ['min: ', 'max: ', 'mean: ']
    vals = [s + str(np.round(v,1)) for s, v in zip(snam, vals)]
    x, y = m(lonmin + 1, latmin + 1)
    ax.text(x, y, '  '.join(vals), fontsize=8)

    
def _fix_1Ddata(z, data, ax_args):
    newdata = range(0,5)
    for n in range(0,5):
        newdata[n] = data
    ax_args['ylabel'] = ''
    ax_args['yticks'] = []
    return np.array(range(0,5)), np.array(newdata), ax_args
    
                                                                
def section(x, z, data, ax=None, ax_args=None, pcolor_args=None, cblabel='', anom=False):
    if len(z) == 1:
       z, data, ax_args = _fix_1Ddata(z, data, ax_args)
    if not ax:
        fig, ax = plt.subplots(1,1, figsize=(8,8))
        fig.subplots_adjust(top=0.8, right=0.8)
    else:
        fig = plt.gcf()

    if not pcolor_args : pcolor_args = default_pcolor_args(data, anom)
    for key, value in default_pcolor_args(data).iteritems():
        if key not in pcolor_args or (pcolor_args[key] is None):
            pcolor_args[key] = value


    cot = ax.pcolormesh(x, z, data, **pcolor_args)
    ax.contour(x, z, data, colors=['k'], vmin=pcolor_args['vmin'],
               vmax=pcolor_args['vmax'])
    ax.invert_yaxis()
    ax.autoscale(True, axis='both', tight='both')
    if ax_args:
        plt.setp(ax, **ax_args)

    box = ax.get_position()
    tl = fig.add_axes([box.x1 + box.width * 0.05, box.y0, 0.02, box.height])
    fig.colorbar(cot, cax=tl, label=cblabel)

def timeseries(x, data, ax=None, ax_args=None,):
    if not ax:
        fig, ax = plt.subplots(1,1, figsize=(8,8))
    else:
        fig = plt.gcf()
    
    ax.plot(x, data)

    plt.setp(ax, **ax_args)    
    
    
    
if __name__ == "__main__":
    global_map(lon, lat, data, ax=None, ax_args=None, pcolor_args=None, cblabel='')

