import os
import cdo; cdo = cdo.Cdo()
       

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
        os.system('rm ncstore/*.nc')
    try:
        os.makedirs('fldmeanfiles')
    except:
        pass
    try:
        os.makedirs('remapfiles)
    except:
        pass
    try:
        os.makedirs('trendfiles')
    except:
        pass
    try:
        os.makedirs('areacella')
    except:
        pass
    try:
        os.makedirs('plots')
    except:
        pass
               
def _cat_file_slices(filedict):
    count = 0
    for d in filedict:
        if len(filedict[d]) > 1:
            count += 1
            outfile = 'ncstore/merged' + str(count) + '.nc'
            infiles = ' '.join(filedict[d])
            print infiles
            os.system('cdo mergetime ' + infiles + ' ' + outfile)
            print 'done merge' 
            filedict[d] = outfile
        else:
            filedict[d] = filedict[d][0]
    return filedict


               
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
    print 'here'
    if realm == 'aerosol' or realm == 'atmos':
        realm_cat = 'atmos'
    elif realm == 'land' or realm == 'landIce':
        realm_cat = 'land'
    else:
        realm_cat = 'ocean'
    return realm_cat 
            
def getfiles(plots, run):
    #returns the plots with the locations of the correct files
    _mkdir()
    files, directories = _traverse('/raid/rc40/data/ncs/historical-' + run, plots)
    #vardict = _make_variable_dictionary(filedict)
    #_fill_frequency(plots)
    #withoutvardict = _remove_variables(vardict, plots)
    #filedict = _cat_file_slices(withoutvardict)    
    os.system('ln -s /raid/rc40/data/ncs/historical-edr/fx/ocean/sftof/r0i0p0/*.nc ./areacella/ocean') 
    vf = {}
    fvr = []
    for f in files:
        vf[(getfrequency(f), getvariable(f), getrealization(f))] = []
    for f in files:
        vf[(getfrequency(f), getvariable(f), getrealization(f))].append(f)        
    for p in plots:
        fvr.append((p['frequency'], p['variable'], str(p['realization']))) 
    for key in vf:
        print key
    for key in vf.keys():
        if key not in fvr:
            del vf[key]
    for key in vf:
        for f in vf[key]:
            print '\t' + f
    filedict = _cat_file_slices(vf)
    
    for p in plots:
        if 'ifile' not in p:
            p['ifile'] = filedict[(p['frequency'], p['variable'], str(p['realization']))] 
        p['realm'] = getrealm(f)
        p['realm_cat'] = getrealmcat(p['realm'])
        print 
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
              },
             {    
              'variable': 'vo',
              'plot_projection': 'section',
              'depth_type': 'lev',
              'frequency': 'mon', 
              'realization': '1',                       
              },                
             {    
              'variable': 'ta',
              'plot_projection': 'section',
              'depth_type': 'lev',
              'frequency': 'mon', 
              'realization': '1',                                      
              }, 
            ]
    plots = getfiles(plots, 'cvu')
    for p in plots:
        print p['variable'] + ' ' + p['ifile']
    print 
   

