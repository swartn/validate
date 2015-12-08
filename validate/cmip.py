"""
cmip
===============

.. moduleauthor:: David Fallis
"""


import cmipdata as cd
import cdo; cdo = cdo.Cdo()
import os
from directory_tools import traverse, max_end_dates, min_start_dates


def importcmip(directory='/raid/ra40/CMIP5_OTHER_DOWNLOADS/'):
    try:
        os.makedirs('cmipfiles')
    except:
        pass
    files = traverse(directory)

    print len(files)    
    for f in files:
        if '.nc' not in f:
            files.remove(f)
    print len(files)
    for f in files:
        newfile = f.rsplit('/',1)[1] 
        os.system('ln -s ' + f + ' ./cmipfiles/' + newfile)  
    
def model_average(var, model, frequency):
    new = 'ENS-MEAN_cmipfiles/' + var + '_' + model + '.nc'
    if not os.path.isfile(new):
        ens = cd.mkensemble('cmipfiles/' + var + '_*' + model + '_*historical_*.nc', prefix='cmipfiles/')
        ens = cd.cat_exp_slices(ens)
        means, stdevs = cd.ens_stats(ens, var)
        new = 'ENS-MEAN_cmipfiles/' + var + '_' + model + '.nc'
        os.rename(means[0], new)
    return new

def models(var, model):
    ens = cd.mkensemble('cmipfiles/' + var + '_*' + model + '_*historical_*.nc', prefix='cmipfiles/')
    ens.fulldetails()
    ens = cd.cat_exp_slices(ens)
    return ens.lister('ncfile')
    
def cmipaverage(var, model_file, sd, ed):    
    out = 'ENS-MEAN_cmipfiles/' + var + '_' + 'cmip5.nc'
    if not os.path.isfile(out):
        filelist = list(set(model_file.values()))
        newfilelist = []
        newerfilelist = []
        for f in filelist:
            time = f.replace('.nc', '_time.nc')
#            try:
            os.system('cdo -L seldate,' + sd + ',' + ed + ' -selvar,' + var + ' ' + f + ' ' + time)
#            cdo.seldate(sd+','+ed, options = '-L', input='-selvar,' + var + ' ' + f, output=time)
#            except:
#                pass
#            else: 
            newfilelist.append(time)  
        for f in newfilelist:
            remap = f.replace('.nc', '_remap.nc')
 #           try:
            cdo.remapdis('r360x180', input=f, output=remap)
#            except:
#                pass
#            else: 
            newerfilelist.append(remap)
              
        filestring = ' '.join(newerfilelist)
        cdo.ensmean(input = filestring, output = out)
    return out


#def cmips(var):
#    ens = cd.mkensemble('cmipfiles/' + var + '_*historical_*.nc', prefix='cmipfiles/')
#    models = ens.lister('model')
#    print models
#    model_averages = []
#    for m in models:
#        model_averages.append(model_average(var, m))
#    print model_averages    
#    return model_averages


def getfiles(plots):
    startdates = min_start_dates(plots)
    enddates = max_end_dates(plots)    
    cmip5_variables = {}
    for p in plots:
        p['model_files'] = {}
        p['model_file'] = {}
        p['cmip5_files'] = {}
        p['cmip5_file'] = {}
        comp = p['compare']
        if comp['model'] or comp['cmip5']:
            for model in p['comp_models'][:]:
                try:
                    p['model_file'][model] = model_average(p['variable'], model, p['frequency'])
                except:
                    with open('logs/log.txt', 'a') as outfile:
                        outfile.write('No cmip5 files were found for ' + p['variable'] + ': ' + model + '\n\n')
                    print 'No cmip5 files were found for ' + p['variable'] + ': ' + model
                    p['comp_models'].remove(model)
    for p in plots:
        if p['compare']['cmip5']:
            try:
                p['cmip5_file'] = cmipaverage(p['variable'], p['model_file'], str(startdates[p['variable']]) + '-01', str(enddates[p['variable']])+ '-01')
            except:
                p['compare']['cmip5'] = False
                   
def cmip(plots, cmipdir, load):
    for p in plots:
        if p['compare']['cmip5'] == True or p['compare']['model'] == True:            
            if (not os.path.exists('cmipfiles')) or load:
                importcmip(cmipdir)
            getfiles(plots)
            break
            

                              

if __name__=="__main__":
    plots = [

        ]
    
    cmip(plots, '/raid/ra40/CMIP5_OTHER_DOWNLOADS/')
    for p in plots:
        print p['cmip5_files']
        print p['model_files']
        print p['model_file']
        print p['cmip5_file']
    
