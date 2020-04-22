import os
import subprocess
import validate.constants as constants
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

def external(ifile, *args, **kwargs):
    function = kwargs.pop('function', None)
    if not function:
        return ifile
    function = os.path.join(constants.external_root, function)
    language = kwargs.pop('language', None)

    if not language:
        sub_list = [function, ifile] + args
    else:
        sub_list = [language, function, ifile] + list(args)
    subprocess.call(sub_list)
    ofile = kwargs.pop('ofile', None)
    new_ofile = ('netcdf/{}_{}').format(kwargs.pop('prefix', 'external'), split(ifile))

    os.rename(ofile, new_ofile)
    return new_ofile
