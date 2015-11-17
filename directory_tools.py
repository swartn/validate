"""
directory_tools
===============

.. moduleauthor:: David Fallis
"""



import os
import cdo; cdo = cdo.Cdo()
       
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
        if p['climatology'] or p['compare_climatology']:
            if 'climatology_dates' in p:
                if 'start_date' in p['climatology_dates']:
                    start_dates[p['variable']].append(p['climatology_dates']['start_date'])
            else:
                start_dates[p['variable']].append('0')
        if p['trends'] or p['compare_trends']:
            if 'trends_dates' in p:
                if 'start_date' in p['trends_dates']:
                    start_dates[p['variable']].append(p['trends_dates']['start_date'])
            else:
                start_dates[p['variable']].append('0')
        
    for var in start_dates:
        start_dates[var] = [int(date[:4]) for date in start_dates[var]]
        start_dates[var] = min(start_dates[var])
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
        if p['climatology'] or p['compare_climatology']:
            if 'climatology_dates' in p:
                if 'end_date' in p['climatology_dates']:
                    end_dates[p['variable']].append(p['climatology_dates']['end_date'])
            else:
                end_dates[p['variable']].append('3000')
        if p['trends'] or p['compare_trends']:
            if 'trends_dates' in p:
                if 'end_date' in p['trends_dates']:
                    end_dates[p['variable']].append(p['trends_dates']['end_date'])
            else:
                end_dates[p['variable']].append('3000')
        
    for var in end_dates:
        end_dates[var] = [int(date[:4]) for date in end_dates[var]]
        end_dates[var] = max(end_dates[var])
    return end_dates    

def _traverse(root):
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
    mkthedir('fldmeanfiles')
    mkthedir('remapfiles')  
    mkthedir('trendfiles')
    mkthedir('mask')
    mkthedir('plots')
    mkthedir('zonalfiles')
        
def _load_masks(run):
    """Loads the land and sea masks for a specified run
    
    Parameters
    ----------
    run : string
          the model run
    """
    os.system('ln -s /raid/rc40/data/ncs/historical-' + run + '/fx/ocean/sftof/r0i0p0/*.nc ./mask/ocean')
    os.system('ln -s /raid/rc40/data/ncs/historical-' + run + '/fx/atmos/sftlf/r0i0p0/sftlf_fx_DevAM4-2_historical-edr_r0i0p0.nc ./mask/land')  
    
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
                if int(sd) > int (end_dates[d[1]]) or int(ed) < int(start_dates[d[1]]):
                    filedict[d].remove(infile)
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
    for d in filedict:
        if len(filedict[d]) > 1:
            count += 1
            outfile = 'ncstore/merged' + filedict[d][0].rsplit('/',1)[1]
            infiles = ' '.join(filedict[d])
            print d
            print infiles
            os.system('cdo mergetime ' + infiles + ' ' + outfile)
            print 'done merge' 
            filedict[d] = (outfile)
        else:
            filedict[d] = filedict[d][0]
    return filedict

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
    x = f.rsplit('/',1)
    x = x[1].rsplit('.',1)
    x = x[0].rsplit('_',1)
    x = x[1].split('-',1)
    return x[0][:4], x[1][:4] 
                   
def getvariable(f):
    """ Returns the years from a filename and directory path
        This is dependant on the cmip naming convention
    Parameters
    ----------
    string : name of file including path
    
    Returns
    -------
    string of start year
    string of end year
    """
    x = f.rsplit('/',1)
    x = x[1].split('_',1)
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
    x = f.rsplit('/',4)
    x = x[0].rsplit('/',1)
    return x[1]

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
    x = f.rsplit('/',1)
    x = x[1].rsplit('_',2)
    x = x[1].split('_',1)
    x = x[0][1:2]
    return x

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
    x = f.rsplit('/',3)
    x = x[0].rsplit('/',1)
    return x[1]
    
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
            
def getfiles(plots, run):
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
    files = _traverse('/raid/rc40/data/ncs/historical-' + run)   
    _load_masks(run)
    
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
    for key in vf.keys():
        if key not in fvr:
            del vf[key]
    startdates = min_start_dates(plots)
    enddates = max_end_dates(plots)
    filedict = _remove_files_out_of_date_range(vf, startdates, enddates)
    filedict = _cat_file_slices(filedict)  
    for p in plots:
        if 'ifile' not in p:
            p['ifile'] = filedict[(p['frequency'], p['variable'], str(p['realization']))] 
        p['realm'] = realms[p['variable']]
        p['realm_cat'] = getrealmcat(p['realm'])
        if 'plot_args' not in p:
            p['plot_args'] = {}
        if 'fill_continents' not in p['plot_args']:
            if p['realm_cat'] == 'ocean':
                p['plot_args']['fill_continents'] = True

def remfiles(del_fldmeanfiles=True, del_mask=True, del_ncstore=True, del_remapfiles=True, del_trendfiles=True, del_zonalfiles=True, **kwargs):
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
    if del_fldmeanfiles:
        os.system('rm -rf fldmeanfiles')
    if del_mask:
        os.system('rm -rf mask')
    if del_ncstore:
        os.system('rm -rf ncstore')
    if del_remapfiles:
        os.system('rm -rf remapfiles')        
    if del_trendfiles:
        os.system('rm -rf trendfiles')        
    if del_zonalfiles:
        os.system('rm -rf zonalfiles')        
        
def getobsfiles(plots, obsroot):
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
    obsfiles = _traverse(obsroot)
    variables = _variable_dictionary(plots)
    for f in obsfiles:
        var = getvariable(f)
        if var in variables:
            variables[var].append(f)
    for p in plots:
        if p['compare_climatology'] or p['compare_trends']:
            if 'comp_file' not in p:
                try:
                    p['comp_file'] = variables[p['variable']][0]
                except:
                    print 'No observations file was found for ' + p['variable']
                    p['compare_climatology'] = False
                    p['compare_trends'] = False                                    
    
if __name__ == "__main__": 
    plots =[ 
         {
          'compare_climatology': False, 
          'compare_trends': True,                      
          'variable': 'tas',
          'plot_projection': 'zonal_mean',
          'trends': False,
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000]                              
          },                                
         { 
          'compare_climatology': False, 
          'compare_trends': True,            
          'variable': 'va',
          'plot_projection': 'mercator',
          'depth_type': 'plev',
          'depths':[20000, 85000, 100000]                              
          }, 
          
          ]   
    for p in getobsfiles(plots):
        if p['compare_climatology'] or p['compare_trends']:
            print p['comp_file']
