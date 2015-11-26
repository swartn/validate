"""
yamllog
===============

.. moduleauthor:: David Fallis
"""


import yaml
from collections import OrderedDict

OUTPUT_ORDER = ['plot_name',
                'variable',
                'depth',
                'plot_projection',
                'plot_type',
                'dates',
                ]
                
def convert(plot):
    yamplot = {}
    print
    yamplot['plot_name'] = plot['plot_name']
    yamplot['variable'] = plot['variable']
    yamplot['depth'] = str(plot['plot_depth'])    
    yamplot['plot_projection'] = plot['plot_projection']
    yamplot['plot_type'] = plot['plot_type']
    if plot['plot_type'] == 'climatology' or plot['plot_type'] == 'compare_climatology':
        yamplot['dates'] = plot['climatology_dates']
    else:
        yamplot['dates'] = plot['trends_dates']
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
#        with open('log.yml', 'a') as outfile:
#            outfile.write(yaml.dump(yamplot, width=20, default_flow_style=False, explicit_start=True, explicit_end=False))

if __name__ == "__main__":
    pass
