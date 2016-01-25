"""
yamllog
===============

.. moduleauthor:: David Fallis
"""

import yaml

OUTPUT_ORDER = ['plot_name',
                'variable',
                'depth',
                'plot_projection',
                'plot_type',
                'comp_file',
                'dates',
                'frequency',
                'units',
                'stats'
                ]


def convert(plot):
    yamplot = {}
    yamplot['plot_name'] = plot['plot_name']
    yamplot['variable'] = plot['variable']
    yamplot['depth'] = str(plot['plot_depth'])
    yamplot['plot_projection'] = plot['plot_projection']
    yamplot['plot_type'] = plot['plot_type']
    try:
        yamplot['comp_file'] = plot['comp_file']
    except:
        yamplot['comp_file'] = 'N/A'
    if plot['plot_type'] == 'climatology' or plot['plot_type'] == 'compare_climatology':
        yamplot['dates'] = plot['climatology_dates']
    else:
        yamplot['dates'] = plot['trends_dates']
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


def output(yamplot):
    with open('logs/log.yml', 'a') as outfile:
        outfile.write('\n-----\n\n')
    for name in OUTPUT_ORDER:
        printer = {name: yamplot[name]}
        with open('logs/log.yml', 'a') as outfile:
            outfile.write(yaml.dump(printer, default_flow_style=False))


def log(plot):
    yamplot = convert(plot)
    output(yamplot)


if __name__ == "__main__":
    pass
