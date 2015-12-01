"""
cmip
===============

.. moduleauthor:: David Fallis
"""


import cmipdata as cd
import os
from directory_tools import traverse

def importcmip(directory='/raid/ra40/CMIP5_OTHER_DOWNLOADS/'):
    files = traverse(directory)

    print len(files)    
    for f in files:
        if '.nc' not in f:
            files.remove(f)
    print len(files)
    for f in files:
        newfile = f.rsplit('/',1)[1] 
        os.system('ln -s ' + f + ' ./cmipfiles/' + newfile)  
    
def model_average(var, model):
    ens = cd.mkensemble('cmipfiles/' + var + '_*' + model + '_*historical_*.nc', prefix='cmipfiles/')
    ens.fulldetails()
    ens = cd.cat_exp_slices(ens)
    ens.fulldetails()
    means, stdevs = cd.ens_stats(ens, var)
    try:
        new = means[0].replace('.nc', model + '.nc')
        os.rename(means[0], new)
    except: 
        pass
    return new

def models(var, model):
    ens = cd.mkensemble('cmipfiles/' + var + '_*' + model + '_*historical_*.nc', prefix='cmipfiles/')
    ens.fulldetails()
    ens = cd.cat_exp_slices(ens)
    return ens.lister('ncfile')
    
def cmip_average(var):
    ens = cd.mkensemble('cmipfiles/' + var + '_*historical_*.nc', prefix='cmipfiles/')
    models = ens.lister('model')
    print models
    model_averages = []
    for m in models:
        model_average = model_average(var, m)
        new = model_average.replace('.nc', var + '.nc')
        os.rename(model_average, new)
        model_averages.append(new)
    return model_averages

#def cmips(var):
#    ens = cd.mkensemble('cmipfiles/' + var + '_*historical_*.nc', prefix='cmipfiles/')
#    models = ens.lister('model')
#    print models
#    model_averages = []
#    for m in models:
#        model_averages.append(model_average(var, m))
#    print model_averages    
#    return model_averages
    
def cmip(plots, cmipdir):
    for p in plots:
        if p['compare']['cmip5'] == True or p['compare']['model'] == True:
            importcmip(cmipdir)
            break
    for p in plots:
        p['model_files'] = {}
        p['model_file'] = {}
        p['cmip5_files'] = {}
        p['cmip5_file'] = {}
        comp = p['compare']
        if comp['cmip5']:
            pass
        if comp['model']:
            for model in p['comp_models']:
                p['model_file'][model] = model_average(p['variable'], model)
            print p['model_file']

                              

if __name__=="__main__":
    plots = [
         {    
          'variable': 'no3',
          'plot_projection': 'time_series',
          'compare_climatology': True,
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000],
          'compare': {#'cmip5': True,
                      #'cmip5_average': True,
                      'model': ['CanESM2',],
                      'model_average': ['CanESM2']},                                            
          }, 
        ]
    
    cmip(plots, '/raid/ra40/CMIP5_OTHER_DOWNLOADS/')
    for p in plots:
        print p['cmip5_files']
        print p['model_files']
        print p['model_file']
        print p['cmip5_file']
    
