"""
cmip
===============

.. moduleauthor:: David Fallis
"""

from directory_tools import traverse, max_end_dates, min_start_dates
import os
import cmipdata as cd
import cdo
cdo = cdo.Cdo()


def importcmip(directory='/raid/ra40/CMIP5_OTHER_DOWNLOADS/'):
    """ Recursively traverses the provided directory and soft links the netCDF
        files to a directory called cmipfiles in the current directory.
    """
    # try to make the cmipfiles directory
    try:
        os.makedirs('cmipfiles')
    # catch exception if the directory already exists
    except:
        pass
    
    # make list of file names found in the given directory
    files = traverse(directory)
    
    # remove non netCDF files from the list
    for f in files:
        if '.nc' not in f:
            files.remove(f)
    print len(files)
    
    # soft link files to cmipfiles
    for f in files:
        newfile = f.rsplit('/', 1)[1]
        os.system('ln -s ' + f + ' ./cmipfiles/' + newfile)


def model_average(var, model, expname, frequency):
    """ Creates and stores a netCDF file with the average data
        across the realizations for a given variable, model, and experiment
        Returns the name of the created file.
    """
    new = 'ENS-MEAN_cmipfiles/' + var + '_' + model + '.nc'
    
    # skip if the new file was already made
    if not os.path.isfile(new):
        ensstring = 'cmipfiles/' + var + '_*' + frequency + '_*' + model + '_' + expname + '_*.nc'
        print ensstring
        ens = cd.mkensemble(ensstring, prefix='cmipfiles/')
        ens = cd.cat_exp_slices(ens)
        means, stdevs = cd.ens_stats(ens, var)
        new = 'ENS-MEAN_cmipfiles/' + var + '_' + model + '.nc'
        os.rename(means[0], new)
    return new


def cmipaverage(var, model_file, sd, ed):
    """ Creates and stores a netCDF file with the average data
        across all the models provided.
        REturns the name of the created file.
    """
    out = 'ENS-MEAN_cmipfiles/' + var + '_' + 'cmip5.nc'
    # skip if the new file was already made
    if not os.path.isfile(out):
        filelist = list(set(model_file.values()))
        newfilelist = []
        newerfilelist = []
        for f in filelist:
            time = f.replace('.nc', '_time.nc')
            
            # try to select the date range
            try:
                os.system('cdo -L seldate,' + sd + ',' + ed + ' -selvar,' + var + ' ' + f + ' ' + time)
#            cdo.seldate(sd+','+ed, options = '-L', input='-selvar,' + var + ' ' + f, output=time)
            except:
                # don't append filename to the list if it was not in the date range
                pass
            else:
                newfilelist.append(time)
        for f in newfilelist:
            remap = f.replace('.nc', '_remap.nc')
            
            # try to remap the files
            try:
                cdo.remapdis('r360x180', input=f, output=remap)
            except:
                # don't append the filename if it could not be remapped
                pass
            else:
                newerfilelist.append(remap)

        filestring = ' '.join(newerfilelist)
        
        # compute the mean across the models
        cdo.ensmean(input=filestring, output=out)
    return out


def getfiles(plots, expname):
    """ Loop through the plots and create the comparison files if cdo operations are needed 
        and map the keys in the compare dictionary to the correct file names.
    """
    # get the date ranges need for each variable
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
            # map the file names of the comparison files to the model names
            for model in p['comp_models'][:]:
                try:
                    p['model_file'][model] = model_average(p['variable'], model, expname, p['frequency'])
                except:
                    with open('logs/log.txt', 'a') as outfile:
                        outfile.write('No cmip5 files were found for ' + p['variable'] + ': ' + model + '\n\n')
                    print 'No cmip5 files were found for ' + p['variable'] + ': ' + model

                    # remove the model from the list if no comparison files were found
                    p['comp_models'].remove(model)
    for p in plots:
        if p['compare']['cmip5']:
            # map the file name of the comparison file to cmip5 in compare dictionary
            try:
                p['cmip5_file'] = cmipaverage(p['variable'], p['model_file'], str(startdates[p['variable']]) + '-01', str(enddates[p['variable']]) + '-01')
            except:
                p['compare']['cmip5'] = False


def cmip(plots, cmipdir, expname, load):
    """ Import the netCDF files if needed
        and call the functions to modify and map the cmip5 files
    """
    for p in plots:
        if p['compare']['cmip5'] == True or p['compare']['model'] == True:
            # Assumes if the 'cmipfiles' directory exists then the files have been already linked
            # can be loaded anyways of the loadcimp5 flag is set in the execution
            if (not os.path.exists('cmipfiles')) or load:
                importcmip(cmipdir)
            getfiles(plots, expname)
            break


if __name__ == "__main__":
    pass
