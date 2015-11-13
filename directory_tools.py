import os
import cdo; cdo = cdo.Cdo()
       
def _variable_dictionary(plots):
    variables = {}
    for p in plots:
        variables[p['variable']] = []
    return variables

def min_start_dates(plots):
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

def _traverse(root, plots):
    files = []
    directories = []
    for dirname, subdirlist, filelist in os.walk(root):
        for f in filelist:
            files.append(dirname + '/' + f)
            directories.append(dirname + '/')
    return files, directories

def _mkdir():
    try:
        os.makedirs('ncstore')
    except:
        try:
            os.system('rm ncstore/*.nc')
        except:
            pass
    try:
        os.makedirs('fldmeanfiles')
    except:
        pass
    try:
        os.makedirs('remapfiles')
    except:
        pass
    try:
        os.makedirs('trendfiles')
    except:
        pass
    try:
        os.makedirs('mask')
    except:
        pass
    try:
        os.makedirs('plots')
    except:
        pass
    try:
        os.makedirs('zonalfiles')
    except:
        pass
        
def _load_masks(run):
    os.system('ln -s /raid/rc40/data/ncs/historical-' + run + '/fx/ocean/sftof/r0i0p0/*.nc ./mask/ocean')
    os.system('ln -s /raid/rc40/data/ncs/historical-' + run + '/fx/atmos/sftlf/r0i0p0/sftlf_fx_DevAM4-2_historical-edr_r0i0p0.nc ./mask/land')  
    
def _remove_files_out_of_date_range(filedict, start_dates, end_dates):
    for d in filedict:
        if len(filedict[d]) > 1:
            for infile in filedict[d][:]:
                sd, ed = getdates(infile)
                if int(sd) > int (end_dates[d[1]]) or int(ed) < int(start_dates[d[1]]):
                    filedict[d].remove(infile)
    return filedict  

                      
def _cat_file_slices(filedict):
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
    x = f.rsplit('/',1)
    x = x[1].rsplit('.',1)
    x = x[0].rsplit('_',1)
    x = x[1].split('-',1)
    return x[0][:4], x[1][:4] 
                   
def getvariable(f):
    x = f.rsplit('/',2)
    x = x[0].rsplit('/',1)
    return x[1] 

def getfrequency(f):
    x = f.rsplit('/',4)
    x = x[0].rsplit('/',1)
    return x[1]

def getrealization(f):
    x = f.rsplit('/',1)
    x = x[0].rsplit('/',1)
    x = x[1][1:2]
    return x

def getrealm(f):
    x = f.rsplit('/',3)
    x = x[0].rsplit('/',1)
    return x[1]
    
def getrealmcat(realm):
    if realm == 'aerosol' or realm == 'atmos' or realm == 'seaIce':
        realm_cat = 'atmos'
    elif realm == 'land' or realm == 'landIce':
        realm_cat = 'land'
    else:
        realm_cat = 'ocean'
    return realm_cat 
            
def getfiles(plots, run):
    _mkdir()
    files, directories = _traverse('/raid/rc40/data/ncs/historical-' + run, plots)   
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
    return plots
    
if __name__ == "__main__":    
    plots = [ 
             {    
              'variable': 'vo',
              'plot_projection': 'global_map',
              'depth_type': 'lev',
              'frequency': 'mon', 
              'realization': '1',
              'climatology': True,
              'climatology_dates': {'start_date': '1950-01', 'end_date': '1955-01'},
              'trends': False,
              'compare_trends': False,
              'compare_climatology': False,
              },
             {    
              'variable': 'vo',
              'plot_projection': 'section',
              'depth_type': 'lev',
              'frequency': 'mon', 
              'realization': '1',
              'climatology': True,
              'climatology_dates': {'start_date': '1930-01', 'end_date': '1940-01'},
              'trends': False,
              'compare_trends': False,
              'compare_climatology': False,
              },                
             {    
              'variable': 'ta',
              'plot_projection': 'section',
              'depth_type': 'lev',
              'frequency': 'mon', 
              'realization': '1',
              'climatology': True, 
              'climatology_dates': {'start_date': '1990-01', 'end_date': '2000-01'},
              'trends': False,
              'compare_trends': False,
              'compare_climatology': False,                                                
              }, 
             {    
              'variable': 'ta',
              'plot_projection': 'section',
              'depth_type': 'lev',
              'frequency': 'mon', 
              'realization': '1',
              'climatology': True, 
              'climatology_dates': {'start_date': '1990-01', 'end_date': '2000-01'},
              'trends': False,
              'compare_trends': False,
              'compare_climatology': False,  
              'trends_dates': {'start_date': '1950-01', 'end_date': '2000-01'},                                              
              }, 
            ]
    files, directories = _traverse('/raid/rc40/data/ncs/historical-edr', plots)   
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
    for key in vf:
        for f in vf[key]:
            print '\t' + f
    startdates = min_start_dates(plots)
    enddates = max_end_dates(plots)
    filedict = _remove_files_out_of_date_range(vf, startdates, enddates)
    for f in filedict:
        print f
        print filedict[f]
    filedict = _cat_file_slices(filedict)
    print filedict
