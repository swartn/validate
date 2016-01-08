"""
defaults
===============
This module fills the plots with values specified in defaults
and fills the remaining options with placeholders so that
existence checks will not be needed later.

.. moduleauthor:: David Fallis
"""

DEFAULTS = {'plotprojection': 'global_map',
            'climatology': False,
            'compare_climatology': False,
            'trends': False,
            'compare_trends': False,
            'frequency': 'mon',
            'realization': 1,
            'depths': [0],
            'scale': 1,
            'pdf': True,
            'png': False,
            'comp_flag': None,
            'remap': 'remapdis',
            'remap_grid': 'r180x360',
            }


def fill(plots, defaults, model_run, experiment):
    """ Fills the blank spaces in plots with default values and returns the list

    Parameters
    ----------
    plots : list of dictionaries
    defaults : dictionary
               values to fill plots
    model_run : string
                run ID
    experiment : string
                 experiment name

    Returns
    -------
    list of dictionaries
    """
    for p in plots:

        # fill plots with the defaults given in conf.yaml
        for key in defaults:
            if key not in p:
                p[key] = defaults[key]
 
        # fill plots with global DEFAULTS
        for key in DEFAULTS:
            if key not in p:
                p[key] = DEFAULTS[key]
                
        # remove plot from list if no variable is provided
        if 'variable' not in p:
            plots.remove(p)
            print p
            print 'deleted: no variable provided'

        p['model_ID'] = model_run
        p['plot_depth'] = 0
        if 'compare' not in p:
            p['compare'] = {'cmip5': False,
                            'model': False,
                            'runid': False,
                            'obs': True,
                            }
        else:
            if 'cmip5' not in p['compare']:
                p['compare']['cmip5'] = False
            if 'model' not in p['compare']:
                p['compare']['model'] = False
            if 'obs' not in p['compare']:
                p['compare']['obs'] = False
            if 'runid' not in p['compare']:
                p['compare']['runid'] = False
                
        def _fill_args(data):
            if data + '_args' not in p:
                p[data + '_args'] = {}
            if 'climatology_args' not in p[data + '_args']:
                p[data + '_args']['climatology_args'] = {}
            if 'trends_args' not in p[data + '_args']:
                p[data + '_args']['trends_args'] = {}

            if 'pcolor_args' not in p[data + '_args']['climatology_args']:
                p[data + '_args']['climatology_args']['pcolor_args'] = {}
            if 'ax_args' not in p[data + '_args']['climatology_args']:
                p[data + '_args']['climatology_args']['ax_args'] = {}

            if 'pcolor_args' not in p[data + '_args']['trends_args']:
                p[data + '_args']['trends_args']['pcolor_args'] = {}
            if 'ax_args' not in p[data + '_args']['trends_args']:
                p[data + '_args']['trends_args']['ax_args'] = {}

            if 'title' not in p[data + '_args']['climatology_args']['ax_args']:
                p[data + '_args']['climatology_args']['title_flag'] = False
            else:
                p[data + '_args']['climatology_args']['title_flag'] = True
            if 'title' not in p[data + '_args']['trends_args']['ax_args']:
                p[data + '_args']['trends_args']['title_flag'] = False
            else:
                p[data + '_args']['trends_args']['title_flag'] = True

            if 'vmin' not in p[data + '_args']['climatology_args']['pcolor_args']:
                p[data + '_args']['climatology_args']['pcolor_flag'] = False
            else:
                p[data + '_args']['climatology_args']['pcolor_flag'] = True
            if 'vmin' not in p[data + '_args']['trends_args']['pcolor_args']:
                p[data + '_args']['trends_args']['pcolor_flag'] = False
            else:
                p[data + '_args']['trends_args']['pcolor_flag'] = True

        _fill_args('data1')
        _fill_args('data2')
        _fill_args('comp')


def filltitle(p):
    def fill(comp):
        if not p['data1_args']['climatology_args']['title_flag']:
            p['data1_args']['climatology_args']['ax_args']['title'] = (p['variable'] + ' Climatology ' + p['model_ID'] + ' ' +
                                                                       p['climatology_dates']['start_date'] + '-' +
                                                                       p['climatology_dates']['end_date'] +
                                                                       ' Depth: ' + str(p['plot_depth']))
        if not p['data2_args']['climatology_args']['title_flag']:
            p['data2_args']['climatology_args']['ax_args']['title'] = (p['variable'] + ' Climatology ' + comp + ' ' +
                                                                       p['climatology_dates']['start_date'] + '-' +
                                                                       p['climatology_dates']['end_date'] +
                                                                       ' Depth: ' + str(p['plot_depth']))
        if not p['comp_args']['climatology_args']['title_flag']:
            p['comp_args']['climatology_args']['ax_args']['title'] = (p['variable'] + ' Climatology ' + p['model_ID'] + '-' + comp + ' ' +
                                                                      p['climatology_dates']['start_date'] + '-' +
                                                                      p['climatology_dates']['end_date'] +
                                                                      ' Depth: ' + str(p['plot_depth']))

        if not p['data1_args']['trends_args']['title_flag']:
            p['data1_args']['trends_args']['ax_args']['title'] = (p['variable'] + ' Trends ' + p['model_ID'] + ' ' +
                                                                  p['trends_dates']['start_date'] + '-' +
                                                                  p['trends_dates']['end_date'] +
                                                                  ' Depth: ' + str(p['plot_depth']))
        if not p['data2_args']['trends_args']['title_flag']:
            p['data2_args']['trends_args']['ax_args']['title'] = (p['variable'] + ' Trends ' + comp + ' ' +
                                                                  p['trends_dates']['start_date'] + '-' +
                                                                  p['trends_dates']['end_date'] +
                                                                  ' Depth: ' + str(p['plot_depth']))
        if not p['comp_args']['trends_args']['title_flag']:
            p['comp_args']['trends_args']['ax_args']['title'] = (p['variable'] + ' Trends ' + p['model_ID'] + '-' + comp + ' ' +
                                                                 p['trends_dates']['start_date'] + '-' +
                                                                 p['trends_dates']['end_date'] +
                                                                 ' Depth: ' + str(p['plot_depth']))
    if p['comp_flag'] == 'model':
        fill(p['comp_model'])
    elif p['comp_flag'] == 'runid':
        fill(p['comp_model'])
    else:
        if p['comp_flag']:
            fill(p['comp_flag'])
        else:
            fill("")
