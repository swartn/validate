"""
directory_tools
===============

This module contains several functions associated with traversing
directories and gathering information from files.

.. moduleauthor:: David Fallis
"""
import os
from netCDF4 import Dataset, num2date, date2num
import datetime
import itertools
import tarfile
import cmipdata as cd
import validate
import cdo
cdo = cdo.Cdo()

MEANDIR = None

def _variable_dictionary(plots):
    """ Creates a dictionary with the variable names as keys
        mapped to empty lists

    Parameters
    ----------
    plots : list of dictionaries with 'variable' key

    Returns
    -------
    dictionary
    """
    variables = {}
    for p in plots:
        variables[p['variable']] = []
        for evar in p['extra_variables']:
            variables[evar] = []
    return variables


def min_start_dates(plots):
    """ Returns a dictionary which maps the variable names
        to the earliest year needed for that variable in all of the plots

    Parameters
    ----------
    plots : list of dictionaries

    Returns
    -------
    dictionary
    """
    start_dates = _variable_dictionary(plots)
    for p in plots:
        try:
            start_dates[p['variable']].append(p['dates']['start_date'])
        except: pass
        try:
            start_dates[p['variable']].append(p['comp_dates']['start_date'])
        except: pass
        
    for var in start_dates:
        start_dates[var] = [int(date[:4]) for date in start_dates[var]]
        try:
            start_dates[var] = min(start_dates[var])
        except:
            start_dates[var] = None
    return start_dates


def max_end_dates(plots):
    """ Returns a dictionary which maps the variable names
        to the latest year needed for that variable in all of the plots

    Parameters
    ----------
    plots : list of dictionaries

    Returns
    -------
    dictionary
    """
    end_dates = _variable_dictionary(plots)
    for p in plots:
        try:
            end_dates[p['variable']].append(p['dates']['end_date'])
        except: pass
        try:
            end_dates[p['variable']].append(p['comp_dates']['end_date'])
        except: pass

    for var in end_dates:
        end_dates[var] = [int(date[:4]) for date in end_dates[var]]
        try:
            end_dates[var] = max(end_dates[var])
        except:
            end_dates[var] = None
    return end_dates


def traverse(root):
    """ Returns a list of all filenames including the path
        within a directory or any subdirectories

    Parameters
    ----------
    root : string
           directory path

    Returns
    -------
    list of strings

    """
    files = []
    for dirname, subdirlist, filelist in os.walk(root):
        for f in filelist:
            files.append(dirname + '/' + f)
    return files


def _mkdir():
    """ Tries to make directories used to store processed *.nc files
    """
    try:
        os.makedirs('ncstore')
    except:
        try:
            os.system('rm ncstore/*.nc')
        except:
            pass

    def mkthedir(name):
        try:
            os.makedirs(name)
        except:
            pass
    mkthedir('mask')
    mkthedir('plots')
    mkthedir('logs')
    mkthedir('netcdf')
    mkthedir('cmipfiles')


def _logfile(run, experiment):
    with open('logs/log.txt', 'w') as outfile:
        outfile.write('Validate version: ' + validate.__version__ + '\n')
        outfile.write('Run ID: ' + run + '\n')
        outfile.write('Experiment: ' + experiment + '\n\n')

    with open('logs/log.yml', 'w') as outfile:
        outfile.write('Validate version: ' + validate.__version__ + '\n')
        outfile.write('Run ID: ' + run + '\n')
        outfile.write('Experiment: ' + experiment + '\n\n')


def _load_masks(files):
    """Loads the land and sea masks for a specified run

    Parameters
    ----------
    files : list
            file names
    """
    for f in files:
        var = getvariable(f)
        if var == 'sftof':
            print f
            print 'found ocean'
            os.system('ln -s ' + f + ' ./mask/ocean')
        if var == 'sftlf':
            os.system('ln -s ' + f + ' ./mask/land')
            print f
            print 'found land'
        fxvars = ['areacello',
                  'basin',
                  'deptho',
                  'thkcello',
                  'volcello',
                  'areacella',
                  'orog',
                  'orograw',
                  'mrsofc',
                  'rootd',
                  'sftgif',
                  ]
        if var in fxvars:
            os.system('ln -s ' + f + ' ./mask/' + var)          

#    used to be hard coded for known directory path
#    os.system('ln -s /raid/rc40/data/ncs/historical-' + run + '/fx/ocean/sftof/r0i0p0/*.nc ./mask/ocean')
#    os.system('ln -s /raid/rc40/data/ncs/historical-' + run + '/fx/atmos/sftlf/r0i0p0/sftlf_fx_DevAM4-2_historical-edr_r0i0p0.nc ./mask/land')


def _remove_files_out_of_date_range(filedict, start_dates, end_dates):
    """ Removes file names from a dictionary which will not be needed because
        they are outside the date range

    Parameters
    ----------
    filedict : dictionary
               maps tuple to a list of file names
    start_dates : dictionary
                  maps variable name to ealiest year needed
    end_dates : dictionary
                maps variable name to latest year needed

    Returns
    -------
    dictionary with some file names removed
    """
    for d in filedict:
        if len(filedict[d]) > 1:
            for infile in filedict[d][:]:
                sd, ed = getdates(infile)
                if end_dates[d[1]]:
                    if int(sd) > int(end_dates[d[1]]):
                        filedict[d].remove(infile)
                if start_dates[d[1]]:
                    if int(ed) < int(start_dates[d[1]]):
                        try:
                            filedict[d].remove(infile)
                        except:
                            pass
    return filedict


def _cat_file_slices(filedict):
    """ Catenates the list of files under each key
        the dictionary now maps to the new filename

    Parameters
    ----------
    filedict : dictionary
               maps tuple to a list of file names

    Returns
    -------
    dictionary mapping to new file name
    """
    count = 0
    cat_file_dict = {}
    for d in filedict:
        if len(filedict[d]) > 1:
            count += 1
            outfile = 'ncstore/merged' + filedict[d][0].rsplit('/', 1)[1]
            infiles = ' '.join(filedict[d])
            os.system('cdo mergetime ' + infiles + ' ' + outfile)
            cat_file_dict[d] = (outfile)
        else:
            cat_file_dict[d] = filedict[d][0]
    return cat_file_dict


def getdates(f):
    """ Returns the years from a filename and directory path

    Parameters
    ----------
    string : name of file including path

    Returns
    -------
    string of start year
    string of end year
    """
    nc = Dataset(f, 'r')
    time = nc.variables['time_bnds'][:].squeeze()
    nc_time = nc.variables['time']
    try:
        cal = nc_time.calendar
    except:
        cal = 'standard'
    start = nc_time[:][0]
    end = nc_time[:][-1]
    start = num2date(start, nc_time.units, cal)
    end = num2date(end, nc_time.units, cal)
    start = start.year
    end = end.year
    return start, end


def getvariable(f):
    """ Returns the variable from a filename and directory path

    Parameters
    ----------
    string : name of file including path

    Returns
    -------
    string of var
    """
    x = f.rsplit('/', 1)
    x = x[1].split('_', 1)
    return x[0]


def getfrequency(f):
    """ Returns the frequency from a filename and directory path.
        ex. 'day', 'mon', 'yr', 'fx'
        This is dependant on a specific directory organization

    Parameters
    ----------
    string : name of file including path

    Returns
    -------
    string of frequency
    """
    nc = Dataset(f, 'r')
    try: 
        frequency = str(nc.__getattribute__('frequency'))
    except:
        frequency = 'unknown'
    return frequency

def getexperiment(f):
    nc = Dataset(f, 'r')
    try:
        experiment = str(nc.__getattribute__('experiment'))
    except:
        experiment = ''
    return experiment
    
def getrealization(f):
    """ Returns the realization from a filename and directory path.
        This is dependant on the cmip naming convention

    Parameters
    ----------
    string : name of file including path

    Returns
    -------
    string of realization number
    """
    nc = Dataset(f, 'r')
    try:
        realization = str(nc.__getattribute__('realization'))
    except:
        realization = 'r1i1p1'
    return realization


def getrealm(f):
    """ Returns the realm from a filename and directory path.
        This is dependant on a specific directory organization

    Parameters
    ----------
    string : name of file including path

    Returns
    -------
    string of realm
    """
    nc = Dataset(f, 'r')
    try:
        realm = str(nc.__getattribute__('modeling_realm'))
    except:
        realm = 'atmos' # set realm to atmos, so nothing will be masked
    if 'seaIce' in realm:
        realm = 'seaIce'
    return realm


def getrealmcat(realm):
    """ Returns the category of the realm

    Parameters
    ----------
    string : realm

    Returns
    -------
    string of realm category
    """
    if realm == 'aerosol' or realm == 'atmos' or realm == 'seaIce':
        realm_cat = 'atmos'
    elif realm == 'land' or realm == 'landIce':
        realm_cat = 'land'
    else:
        realm_cat = 'ocean'
    return realm_cat


def getfiles(plots, directroot, root, run, experiment):
    """ For every plot in the dictionary of plots
        maps the key 'ifile' to the name of the file
        needed to make the plot

    Parameters
    ----------
    plots : list of dictionaries
    run : string
          name of model run

    """
    _mkdir()
    _logfile(run, experiment)
    if directroot:
        files = traverse(directroot)
    else:
        files = traverse(root + '/' + experiment + '-' + run)
    _load_masks(files)

    realms = {}
    for f in files:
       realms[getvariable(f)] = getrealm(f)

    vf = {}
    fvr = []
    for f in files:
        vf[(getfrequency(f), getvariable(f), getrealization(f))] = []
    for f in files:
        vf[(getfrequency(f), getvariable(f), getrealization(f))].append(f)
    for p in plots:
        fvr.append((p['frequency'], p['variable'], str(p['realization'])))
        for evar in p['extra_variables']:
            fvr.append((p['frequency'], evar, str(p['realization'])))
    for key in vf.keys():
        if key not in fvr:
            del vf[key]
    startdates = min_start_dates(plots)
    enddates = max_end_dates(plots)
    uncat_filedict = _remove_files_out_of_date_range(vf, startdates, enddates)
    filedict = _cat_file_slices(uncat_filedict)
    for p in plots:
        if 'ifile' in p:
            p['ifiles_for_log'] = [p['ifile']]
        else:
            p['ifiles_for_log'] = uncat_filedict[(p['frequency'], p['variable'], str(p['realization']))]    
        if 'ifile' not in p:
            try:
                p['ifile'] = filedict[(p['frequency'], p['variable'], str(p['realization']))]
            except:
                with open('logs/log.txt', 'a') as outfile:
                    outfile.write('No file was found for ' + p['variable'] + '\n\n')
                print 'No file was found for ' + p['variable']
        if 'ifile' not in p:
            continue
        if 'realm' not in p:        
            p['realm'] = getrealm(p['ifile'])
        p['realm_cat'] = getrealmcat(p['realm'])
        p['extra_ifiles'] = {}
        p['extra_realms'] = {}
        p['extra_realm_cats'] = {}
        for evar in p['extra_variables']:
            p['extra_ifiles'][evar] = filedict[(p['frequency'], evar, str(p['realization']))]
            if evar not in p['extra_realms']:
                p['extra_realms'][evar] = realms[evar]
            p['extra_realm_cats'][evar] = getrealmcat(p['extra_realms'][evar])
        
        if 'fill_continents' not in p['plot_args']:
            if p['realm_cat'] == 'ocean':
                p['plot_args']['fill_continents'] = True
    for p in plots[:]:
        if 'ifile' not in p:
            plots.remove(p)
      


def getidfiles(plots, root, experiment):
    """ Get the files for run IDs for comparison.

    Parameters
    ----------
    plots : list of dictionaries
    experiment : string
                 name of experiment

    """
    ids = []
    for p in plots:
        if p['comp_ids']:
            ids.extend(p['comp_ids'])
        p['id_file'] = {}
    ids = list(set(ids))
    startdates = min_start_dates(plots)
    enddates = max_end_dates(plots)
    for i in ids:
        files = traverse(root + experiment + '-' + i)
        vf = {}
        fvr = []
        for f in files:
            vf[(getfrequency(f), getvariable(f), getrealization(f))] = []
        for f in files:
            vf[(getfrequency(f), getvariable(f), getrealization(f))].append(f)
        for p in plots:
            fvr.append((p['frequency'], p['variable'], str(p['realization'])))
        for key in vf.keys():
            if key not in fvr:
                del vf[key]
        uncat_filedict = _remove_files_out_of_date_range(vf, startdates, enddates)
        filedict = _cat_file_slices(uncat_filedict)
        for p in plots:
            p['idfiles_for_log'] = {}
            if i in p['comp_ids']:
                if i in p['id_file']:
                    p['idfiles_for_log'][i] = p['id_file'][i] 
                else:
                    p['id_file'][i] = filedict[(p['frequency'], p['variable'], str(p['realization']))]
                    p['idfiles_for_log'] = uncat_filedict[(p['frequency'], p['variable'], str(p['realization']))]


def remfiles(del_mask=True, del_ncstore=True, del_netcdf=True, del_cmipfiles=True, **kwargs):
    """ Option to delete the directories used to store processed .nc files

    Paremeters
    ----------
    del_fldmeanfiles : boolean
    del_mask : boolean
    del_ncstore : boolean
    del_remapfiles : boolean
    del_trendfiles : boolean
    del_zonalfiles : boolean
    """
    if del_mask:
        os.system('rm -rf mask')
    if del_ncstore:
        os.system('rm -rf ncstore')
    if del_netcdf:
        os.system('rm -rf netcdf')
    if del_cmipfiles:
        os.system('rm -rf cmipfiles')



def getobsfiles(plots, obsroot):
    obsdirectories = [o for o in os.listdir(obsroot) if os.path.isdir(os.path.join(obsroot,o))]
    for o in obsdirectories:
        getobs (plots, obsroot + o, o)


def getobs(plots, obsroot, o):
    """ For every plot in the dictionary of plots
        if an observations file is needed it
        maps the key 'comp_file' to a file containg observations.
        If no observations file is found it changes the comparison
        plots to false and prints out a warning.

    Parameters
    ----------
    plots : list of dictionaries
    obsroot : string
              directory path to find observations
    """
    obsfiles = traverse(obsroot)
    variables = _variable_dictionary(plots)
    for f in obsfiles:
        var = getvariable(f)
        if var in variables:
            variables[var].append(f)
    for p in plots:
        if 'obs_file' not in p:
            p['obs_file'] = {}
        p['obsfiles_for_log'] = {}
        if o in p['comp_obs']:
            if o not in ['obs_file']:
                try:
                    p['obs_file'][o] = variables[p['variable']][0]
                    p['obsfiles_for_log'][o] = p['obs_file'][o]
                except:
                    with open('logs/log.txt', 'a') as outfile:
                        outfile.write('No observations file was found for ' + p['variable'] + '\n\n')
                    print 'No ' + o + ' file was found for ' + p['variable']
                    p['comp_obs'].remove(o)
            else:
                p['obsfiles_for_log'][o] = p['obs_file'][o]
            
        if o in p['extra_obs']:
            if 'extra_obs_files' not in p:
                p['extra_obs_files'] = {}
            for i, name in enumerate(p['extra_obs'][:]):
               if name == o:
                   try:
                       p['extra_obs_files'][p['extra_variables'][i]] = variables[p['extra_variables'][i]][0]
                   except:
                       with open('logs/log.txt', 'a') as outfile:
                           outfile.write('No observations file was found for ' + p['extra_variables'][i] + '\n\n')
                       print 'No ' + o + ' file was found for ' + p['extra_variables'][i]
                       p['extra_variables'].pop(i)
                       p['extra_scales'].pop(i)
                       p['extra_comp_scales'].pop(i)
                       p['extra_shifts'].pop(i)
                       p['extra_comp_shifts'].pop(i)                       
                       p['extra_obs'].pop(i)
        
                                          
def model_files(var, model, expname, frequency, cmipdir):
    prefix = cmipdir + '/' + var + '/'
    ensstring = prefix + var + '_*' + frequency + '_*' + model + '_' + expname + '_*.nc'
    ens = cd.mkensemble(ensstring, prefix=prefix)
    ens = cd.cat_exp_slices(ens, delete=False, output_prefix='cmipfiles/')
    mfiles = ens.lister('ncfile')
    return mfiles, ens

    
def model_average(ens, var, model):
    """ Creates and stores a netCDF file with the average data
        across the realizations for a given variable, model, and experiment
        Returns the name of the created file.
    """
    new = 'cmipfiles/' + var + '_' + model + '.nc'
    
    # skip if the new file was already made
    if not os.path.isfile(new):
        means, stdevs = cd.ens_stats(ens, var)
        os.rename(means[0], new)
        os.remove(stdevs[0])
    return new


def cmip_files(model_files):
    files = list(model_files.values())
    allfiles = [item for sublist in files for item in sublist]
    return list(set(allfiles))


def get_cmip_average(plots, directory):
    averagefiles = traverse(directory)

    variables = _variable_dictionary(plots)
    for f in averagefiles:
        var = getvariable(f)
        if var in variables:
            variables[var].append(f)
    for p in plots:
        if 'cmip5_file' in p:
            p['cmipmeanfile_for_log'] = p['cmip5_file']
            continue
        if p['comp_cmips']:
            for cfile in variables[p['variable']]:
                if getfrequency(cfile) == p['frequency'] and getexperiment(cfile) == p['experiment']:
                    p['cmip5_file'] = cfile
                    p['cmipmeanfile_for_log'] = cfile
                    break
            else:
                p['cmip5_file'] = None
                p['cmipmeanfile_for_log'] = None
    

    
def cmip_average(var, frequency, files, sd, ed, expname):
    """ Creates and stores a netCDF file with the average data
        across all the models provided.
        Returns the name of the created file.
    """
    averagefiles = traverse(MEANDIR)
    
    out = 'ENS-MEAN_cmipfiles/' + var + '_' + 'cmip5.nc'
    # skip if the new file was already made
    if not os.path.isfile(out):
        newfilelist = []
        newerfilelist = []
        for f in files:
            time = f.replace('.nc', '_time.nc')
            # try to select the date range
#            try:
            os.system('cdo -L seldate,' + sd + ',' + ed + ' -selvar,' + var + ' ' + f + ' ' + time)
#            cdo.seldate(sd+','+ed, options = '-L', input='-selvar,' + var + ' ' + f, output=time)
#            except:
                # don't append filename to the list if it was not in the date range
#                pass
#            else:
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

def getcmipfiles(plots, expname, cmipdir):
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
        p['cmip5_files'] = []
        p['cmip5_file'] = None
        if p['comp_models'] or p['comp_cmips']:
            # map the file names of the comparison files to the model names
            for model in p['comp_models'][:]:
                p['modelfiles_for_log'] = {}
                try:
                    if model not in p['model_files']:
                        p['model_files'][model], ens = model_files(p['variable'], model, expname, p['frequency'], cmipdir)
                    else:
                        ens = cd.mkensemble('', filenames=p['model_files'][model])
                    p['model_file'][model] = model_average(ens, p['variable'], model)
                    p['modelfiles_for_log'][model] = p['model_files'][model]
                except:
                    with open('logs/log.txt', 'a') as outfile:
                        outfile.write('No cmip5 files were found for ' + p['variable'] + ': ' + model + '\n\n')
                    print 'No cmip5 files were found for ' + p['variable'] + ': ' + model
                    p['comp_models'].remove(model)
                    try:
                         p['comp_cmips'].remove(model)
                    except: 
                        pass
                    
            for model in p['comp_cmips'][:]:
                if model not in p['comp_models']:
                    try:
                        p['model_files'][model], ens = model_files(p['variable'], model, expname, p['frequency'], cmipdir)
                    except:
                        with open('logs/log.txt', 'a') as outfile:
                            outfile.write('No cmip5 files were found for ' + p['variable'] + ': ' + model + '\n\n')
                        print 'No cmip5 files were found for ' + p['variable'] + ': ' + model
                        # remove the model from the list if no comparison files were found
                        p['comp_cmips'].remove(model)

    get_cmip_average(plots, MEANDIR)
                        
    for p in plots:
        if p['comp_cmips']:
            # map the file name of the comparison file to cmip5 in compare dictionary
            try:
                files = {}
                for f in p['comp_cmips']:
                    files[f] = p['model_files'][f]                         
                p['cmip5_files'] = cmip_files(files)
#                p['cmip5_file'] = cmip_average(p['variable'], p['frequency'], p['cmip5_files'], str(startdates[p['variable']]) + '-01', str(enddates[p['variable']]) + '-01', expname)
            except:
                p['comp_cmips'] = []


def cmip(plots, cmipdir, cmipmeandir, expname):
    """ Import the netCDF files if needed
        and call the functions to modify and map the cmip5 files
    """
    global MEANDIR 
    MEANDIR = cmipmeandir
    for p in plots:
        if p['comp_cmips'] or p['comp_models']:
            getcmipfiles(plots, expname, cmipdir)
            break

def make_ensemble(files):
    ens = cd.mkensemble()


def datetime_string():
    return datetime.datetime.now().strftime("%Y_%m_%d_%H-%M-%S")

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
 
        
def move_tarfile(location, run='', experiment=''):
    if location is not None:
        date = datetime_string()
        plot_tar_name = ('{}-{}_plots_{}.tar.gz').format(experiment, run, date)
        log_tar_name = ('{}-{}_logs_{}.tar.gz').format(experiment, run, date) 
        make_tarfile(plot_tar_name, 'plots')
        make_tarfile(log_tar_name, 'logs')
        plots_new_name = os.path.join(location, plot_tar_name)
        logs_new_name = os.path.join(location, log_tar_name)
        os.system('scp {} {}'.format(plot_tar_name, plots_new_name))
        os.system('scp {} {}'.format(log_tar_name, logs_new_name))      
            

if __name__ == "__main__":
    pass
