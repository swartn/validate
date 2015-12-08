"""
defaults
===============
This module fills the plots with values specified in defaults
and fills the remaining options with placeholders so that 
existence checks will not be needed later.

.. moduleauthor:: David Fallis
"""
def fill(plots, defaults, model_run):
    """ Fills the blank spaces in plots with default values and returns the list
    
    Parameters
    ----------
    plots : list of dictionaries
    obs : dictionary
          maps variable name to the name of observations file
    defaults : dictionary
               values to fill plots
    
    Returns
    -------
    list of dictionaries
    """
    for p in plots:
        for key in defaults:
            if key not in p:
                p[key] = defaults[key]
        if 'variable' not in p:
            plots.remove(p)
            print p
            print 'deleted: no variable provided' 
        p['model_ID'] = model_run   
        if 'plot_projection' not in p:
            p['plot_projection'] = 'global_map'
        if 'climatology' not in p:
            p['climatology'] = False
        if 'compare_climatology' not in p:
            p['compare_climatology'] = False
        if 'trends' not in p:
            p['trends'] = False
        if 'compare_trends' not in p:
            p['compare_trends'] = False
        if 'frequency' not in p:
            p['frequency'] = 'mon'
        if 'realization' not in p:
            p['realization'] = 1
        if 'depth_type' not in p:
            p['depth_type'] = ""
        if 'depths' not in p:
            p['depths'] = [0]
        if 'scale' not in p:
            p['scale'] = 1
        if 'pdf' not in p:
            p['pdf'] = True
        if 'png' not in p:
            p['png'] = False
        p['comp_flag'] = None
        if 'compare' not in p:
            p['compare'] = {'cmip5': False,
                            'model': False,
                            'obs': True,}
        else:
            if 'cmip5' not in p['compare']:
                p['compare']['cmip5'] = False
            if 'model' not in p['compare']:
                p['compare']['model'] = False        
            if 'obs' not in p['compare']:
                p['compare']['cmip5'] = False

            

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
    else:
        if p['comp_flag']:
            fill(p['comp_flag'])
        else:
            fill("")

    

