import os

def traverse(root):
    files = []
    for dirname, subdirlist, filelist in os.walk(root):
        for f in filelist:
            files.append(dirname + '/' + f)
    return files

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

            
def getfiles(plots, run):
    #returns the plots with the locations of the correct files
    files = traverse('/raid/rc40/data/ncs/historical-edr')
    vf = {'day': {},
          'mon': {},
          'yr': {},
          'fx': {},}
    for f in files:
        vf[getfrequency(f)][getvariable(f)]= f
    for p in plots:
        if 'ifile' not in p:
            if 'frequency' not in p:
                p['frequency'] = 'mon'
            p['ifile'] = vf[p['frequency']][p['variable']] 
     
    return plots
    
if __name__ == "__main__":    
    pass

