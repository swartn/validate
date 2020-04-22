"""
yamllog
===============

.. moduleauthor:: David Fallis
"""

import yaml
import hashlib

OUTPUT_ORDER = ['plot_name',
                'variable',
                'ifile',
                'depth',
                'plot_projection',
                'plot_type',
                'comp_file',
                'dates',
                'comp_dates',
                'frequency',
                'units',
                'stats'
                ]


def convert(plot):
    yamplot = {}
    yamplot['plot_name'] = plot['plot_name']
    yamplot['variable'] = plot['variable']
    yamplot['ifile'] = plot['ifile']
    yamplot['depth'] = str(plot['plot_depth'])
    yamplot['plot_projection'] = plot['plot_projection']
    yamplot['plot_type'] = plot['plot_type']
    try:
        yamplot['comp_file'] = plot['comp_file']
    except:
        yamplot['comp_file'] = 'N/A'
    yamplot['dates'] = plot['dates']
    yamplot['comp_dates'] = plot['comp_dates']
    yamplot['frequency'] = plot['frequency']
    yamplot['units'] = str(plot['units'])
    try:
        yamplot['stats'] = plot['stats']
    except:
        yamplot['stats'] = 'N/A'
#    for key in plot['stats']:
#        if type(plot['stats'][key]) is dict:
#            yamplot['stats'][key] = plot['stats'][key]
#        else:
#            yamplot['stats'][plot['obs']] = plot['stats']

    return yamplot


def output(yamplot, filename, output_order):
    with open(filename, 'a') as outfile:
        outfile.write('\n-----\n\n')
    for name in output_order:
        printer = {name: yamplot[name]}
        with open(filename, 'a') as outfile:
            outfile.write(yaml.dump(printer, default_flow_style=False))

def get_sha(filename):
    """ returns a dictionary linking the name of all
        the file in the ensemble and the SHA1# of
        those files
    Parameters
    ----------
    ens : Datanode
    
    Return
    ------
    dictionary of strings
    """      
    def hashfile(array):
        sha1 = hashlib.sha1(array)
        return sha1.hexdigest()
    data = {}
    for f in ens.objects('ncfile'):
         data[f.name] = hashfile(cdo.readMaArray(f.name, varname=f.parent.name))
    return data

def get_files(plot):
    files = {}
    files['ifiles'] = plot['ifiles_for_log']
    file_list = list(files['ifiles'])
    try:
        files['id_files'] = dict(plot['idfiles_for_log'])
        for key in files['id_files']:
            file_list.extend(files['id_files'][key])
    except KeyError:
        pass
    try:
        files['obs_file'] = dict(plot['obs_file'])
        for key in files['obs_file']:
            file_list.append(files['obs_file'][key])
    except KeyError:
        pass
    try:
        files['model_files'] = plot['modelfiles_for_log']
        for key in files['model_files']:
            file_list.extend(files['model_files'][key])
    except KeyError:
        pass
    try:    
        files['cmip5_file'] = plot['cmipmeanfile_for_log']
        file_list.extend(files['cmip5_files'])
    except KeyError:
        pass
    return files, file_list

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    
def sha_log(plotname, files):
    with open('logs/sha_log.txt', 'a') as ofile:
        ofile.write('\n------------------------\n')
        ofile.write(plotname + '\n')
        for f in files:
            ofile.write(f + '\t' + md5(f) + '\n')
  
def log(plot):
    yamplot = convert(plot)
    output(yamplot, 'logs/log.yml', OUTPUT_ORDER)
    
    original_files, file_list = get_files(plot)   
    sha_log(plot['plot_name'], file_list)

def reproduce_log(plots):
    dump_plots = []
    for plot in plots:
        plot = dict(plot)
        original_files, _ = get_files(plot)
        for key in original_files:
            plot[key] = original_files[key]
    dump_plots.append(plot)
    yaml.Dumper.ignore_aliases = lambda *args: True
    printer = {'plots': dump_plots}
    with open('logs/reproduce.yml', 'a') as outfile:
        outfile.write('\n')        
        outfile.write(yaml.dump(printer, default_flow_style=False))     


if __name__ == "__main__":
    pass
