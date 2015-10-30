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
            p['climatology_dates'] = {}
        if 'compare_climatology' not in p:
            p['compare_climatology'] = False
        if 'trends' not in p:
            p['trends'] = False
        if 'trends_dates' not in p:
            p['trends_dates'] = {}
        if 'compare_trends' not in p:
            p['compare_trends'] = False
        if 'frequency' not in p:
            p['frequency'] = 'mon'
        if 'realization' not in p:
            p['realization'] = '1'
        if 'position' not in p:
            p['position'] = {}
        if p['compare_climatology'] or p['compare_trends']:
            if 'comp_file' not in p:
                try:
                    lvar = p['variable'].lower()
                    p['comp_file'] = obs[lvar]
                except:
                    uvar = p['variable'].upper()
                    p['comp_file'] = obs[uvar]
                
        if 'data1_args' not in p:
            p['data1_args'] = {}
        if 'pcolor_args' not in p['data1_args']:
            p['data1_args']['pcolor_args'] = None       
        if 'ax_args' not in p['data1_args']:
            p['data1_args']['ax_args'] = {} 
        if 'data2_args' not in p:
            p['data2_args'] = {}            
        if 'pcolor_args' not in p['data2_args']:
            p['data2_args']['pcolor_args'] = None 
        if 'ax_args' not in p['data2_args']:
            p['data2_args']['ax_args'] = {}            
        if 'comp_args' not in p:
            p['comp_args'] = {}                   
        if 'pcolor_args' not in p['comp_args']:
            p['comp_args']['pcolor_args'] = None
        if 'ax_args' not in p['comp_args']:
            p['comp_args']['ax_args'] = {}            
                                          
    return plots

def filltitle(p, t):
    p['data1_args']['ax_args']['title'] = p['variable'] + ' ' + t
    p['data2_args']['ax_args']['title'] = p['variable'] + ' ' + t 
    p['comp_args']['ax_args']['title'] = p['variable'] + ' ' + t
    return p 
    

