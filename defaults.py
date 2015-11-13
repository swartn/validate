def fill(plots, obs, defaults):
    # fills the blank spaces in plots with default values and returns the list
    for p in plots:
        for key in defaults:
            if key not in p:
                p[key] = defaults[key]
        if 'variable' not in p:
            plots.remove(p)
            print p
            print 'deleted: no variable provided'    
        if 'plot_projection' not in p:
            p['plot_projection'] = 'global_map'
        if 'climatology' not in p:
            p['climatology'] = False
        if 'climatology_dates' not in p:
            p['climatology_dates'] = None
        if 'compare_climatology' not in p:
            p['compare_climatology'] = False
        if 'trends' not in p:
            p['trends'] = False
        if 'trends_dates' not in p:
            p['trends_dates'] = None
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

            
        if p['compare_climatology'] or p['compare_trends']:
            if 'comp_file' not in p:
                try:
                    lvar = p['variable'].lower()
                    p['comp_file'] = obs[lvar]
                except:
                    uvar = p['variable'].upper()
                    p['comp_file'] = obs[uvar]    
        
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
                      
        _fill_args('data1')
        _fill_args('data2')
        _fill_args('comp')
        
                                             
    return plots

def filltitle(p, t, d, depth):
    if 'Climatology' in t:
        if not p[d + '_args']['climatology_args']['title_flag']:
            p[d + '_args']['climatology_args']['ax_args']['title'] = p['variable'] + ' ' + t 
            if p['climatology_dates']:
                p[d + '_args']['climatology_args']['ax_args']['title'] = p[d + '_args']['climatology_args']['ax_args']['title'] + ' ' + p['climatology_dates']['start_date'] + '_' + p['climatology_dates']['end_date']
            if depth:
                p[d + '_args']['climatology_args']['ax_args']['title'] = p[d + '_args']['climatology_args']['ax_args']['title'] + ' ' + p['depth_type'] + ': ' + depth        
    elif 'Trends' in t:
        if not p[d + '_args']['trends_args']['title_flag']:
            p[d + '_args']['trends_args']['ax_args']['title'] = p['variable'] + ' Trends'
            if p['trends_dates']:
                p[d + '_args']['trends_args']['ax_args']['title'] = p[d + '_args']['trends_args']['ax_args']['title'] + ' ' + p['trends_dates']['start_date'] + '_' + p['trends_dates']['end_date']              
            if depth:
                p[d + '_args']['trends_args']['ax_args']['title'] = p[d + '_args']['trends_args']['ax_args']['title'] + ' ' + p['depth_type'] + ': ' + depth
    return p 
    

