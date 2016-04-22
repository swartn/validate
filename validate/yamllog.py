"""
yamllog
===============

.. moduleauthor:: David Fallis
"""

import yaml

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
    try:
        files['id_files'] = plot['idfiles_for_log']
    except KeyError:
        pass
    try:
        files['obs_files'] = plot['obsfiles_for_log']
    except KeyError:
        pass
    try:
        files['model_files'] = plot['modelfiles_for_log']
    except KeyError:
        pass
    try:    
        files['cmip5_file'] = plot['cmipmeanfile_for_log']
    except KeyError:
        pass    
    return files

def log(plot):
    yamplot = convert(plot)
    output(yamplot, 'logs/log.yml', OUTPUT_ORDER)
    
#    original_files = get_files(plot)
#    output(original_files, 'logs/files.yml')


if __name__ == "__main__":
    pass
