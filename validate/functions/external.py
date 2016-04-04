import os
import cdo
cdo = cdo.Cdo()

def split(name):
    """ Returns the name of a file without the directory path
    """
    path, filename = os.path.split(name)
    return filename

def sample(ifile, **kwargs):    
    print 'called external function'
    return ifile
    
def field_integral(ifile, **kwargs):
    out = 'netcdf/field-integral_' + split(ifile)
    fout = 'netcdf/gridarea_' + split(ifile)
    mout = 'netcdf/mul_' + split(ifile)
    ymean = 'netcdf/yrmean' + split(out)
    cdo.gridarea(input=ifile, output=fout)
    cdo.mul(input=ifile + ' ' + fout, output=mout)
    cdo.fldsum(input=mout, output=out)
    cdo.yearmean(input=out, output=ymean)
    return ymean
