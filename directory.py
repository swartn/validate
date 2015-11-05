import os

def _traverse(root, plots):
    files = []
    directories = []
    filedict = {}
    for dirname, subdirlist, filelist in os.walk(root):
        if len(filelist) > 0:
            if checvariable(dirname, plots
            filedict[dirname] = [dirname + '/' + f for f in filelist]
        for f in filelist:
            files.append(dirname + '/' + f)
            directories.append(dirname + '/')
    return filedict, files, directories

def _cat_file_slices(filedict):
    count = 0
    for d in filedict:
        if len(filedict[d]) > 1:
            count += 1
            outfile = 'merged' + str(count) + '.nc'
            infiles = ' '.join(filedict[d])
            cdo.mergetime(input=infiles, output=outfile)
            filedict[d] = outfile
        else:
            filedict[d] = filedict[d][0]
    return filedict

def _make_variable_dictionary(fdict):
    f_v_r = {'day': {},
             'mon': {},
             'yr': {},
             'fx': {},}
    for key in fdict:
        f_v_r[getfrequency(key)][getvariable(key)] = {}
        f_v_r[getfrequency(key)][getvariable(key)][getrealization(key)] = fdict[key]
    return f_v_r

def _remove_variables(vardict, plots):
    variables = []
    for p in plots:
        variables.append([variable['frequency'], p['variable']])
    for f in vardict:
        for v in vardict[key]:
            if [f,v] not in variables:
                del vardict[f][v]
    return vardict
        
def _fill_frequency(plots):
    for p in plots:
        if 'frequency' not in p:
            p['frequency'] = 'mon'         
               
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
    return x[1]

def getrealm(f):
    x = f.rsplit('/',3)
    x = x[0].rsplit('/',1)
    return x[1]
    
def getrealmcat(realm):
    print 'here'
    print realm
    if realm == 'aerosol' or realm == 'atmos':
        realm_cat = 'atmos'
    elif realm == 'land' or realm == 'landIce':
        realm_cat = 'land'
    else:
        realm_cat = 'ocean'
    print realm_cat
    return realm_cat 
            
def getfiles(plots, run):
    #returns the plots with the locations of the correct files
    filedict, files, directories = _traverse('/raid/rc40/data/ncs/historical-' + run)
    vardict = _make_variable_dictionary(filedict)
    _fill_frequency(plots)
    withoutvardict = _remove_variables(vardict, plots)
    filedict = _cat_file_slices(withoutvardict)    
    os.system('ln -s /raid/rc40/data/ncs/historical-edr/fx/ocean/sftof/r0i0p0/*.nc ./areacella/ocean')
    vf = {'day': {},
          'mon': {},
          'yr': {},
          'fx': {},}
    vrf = {'day': {},
          'mon': {},
          'yr': {},
          'fx': {},} 

    for f in files:
        vf[getfrequency(f)][getvariable(f)] = f
    for f in files:
        vrf[getfrequency(f)][getrealm(f)] = {}
        vrf[getfrequency(f)][getrealm(f)][getvariable(f)] = f
    for p in plots:
        if 'ifile' not in p:
            if 'frequency' not in p:
                p['frequency'] = 'mon'
            p['ifile'] = vf[p['frequency']][p['variable']] 
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
              'variable': 'phyc',
              'plot_projection': 'global_map',
              'depth_type': 'lev',                        
              }, 
             {    
              'variable': 'phyc',
              'plot_projection': 'section',
              'depth_type': 'lev',                        
              }, 
            ]
    plots, vrf = getfiles(plots, 'aaa')
    print vrf['fx']
   

