"""
pdforganize
===============

.. moduleauthor:: David Fallis
"""

import subprocess
import os
def arrange(plotnames):
    """ Outputs a pdf named plots/joined.pdf with all of the plots
        organized and bookmarked
    
    Parameters
    ----------
    plotnames : list of tuples
                (name of plot, plot dictionary, plot type)
    
    """
    dictionary = _orderplots(plotnames)
    
    pstring = pdfmarks(dictionary)   
    combine_str ='gs -sDEVICE=pdfwrite -sOutputFile=plots/joined.pdf -dQUIET -dNOPAUSE -dBATCH -dAutoRotatePages=/None -f '+pstring+' plots/pdfmarks\n'

    os.system(combine_str)
    os.system('rm -f plots/pdfmarks')
    
def _orderplots(plotnames):
    """ Organizes the names into a dictionary that can be used to cycle through the plots
    
    Parameters
    ----------
    plotnames : list of tuples
                (name of plot, plot dictionary, plot type) 
    Returns
    -------
    dictionary
    """   
    plotdict = {}
    for name, p, t in plotnames:
        plotdict[p['variable']] = {}
    for name, p, t in plotnames:
        plotdict[p['variable']][t] = {}


    for name, p, t in plotnames:
        plotdict[p['variable']][t][p['plot_projection']] = {'sorteddepthlist': [],
                                                           'depthfile': {},}
    for name, p, t in plotnames:
        plotdict[p['variable']][t][p['plot_projection']]['sorteddepthlist'].append(p['plot_depth']) 
        plotdict[p['variable']][t][p['plot_projection']]['sorteddepthlist'].sort()
        plotdict[p['variable']][t][p['plot_projection']]['depthfile'][p['plot_depth']] = name[0]        
    return plotdict

def pdfmarks(plotdict):
    """ Writes to pdfmarks file to organize the plots under bookmarks
    
    Parameters
    ----------
    plotdict : dictionary
               organized into the bookmark levels
    Returns
    -------
    string with all of the plot names in the order they will be in joined.pdf
    """ 
    f = open('plots/pdfmarks','w')
    f.write("%% BeginProlog \n/pdfmark where \n{pop} {userdict /pdfmark /cleartomark load put} ifelse \n")
    f.write("%% EndProlog \n%% BeginSetup \n[/PageMode /UseOutlines \n")
    f.write("/Page 1 /View [/XYZ null null null] \n/DOCVIEW pdfmark \n%% EndSetup\n")
    
    plist = []
    page_count = 1
    for var in plotdict:    
        f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + var + ") /Count -"+str(len(plotdict[var].keys())) + " /OUT pdfmark\n")
        for ptype in plotdict[var]:
            f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + ptype + ") /Count -" + str(len(plotdict[var][ptype].keys())) + " /OUT pdfmark\n")
            for pp in plotdict[var][ptype]:
                f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + pp + ") /Count -" + str(len(plotdict[var][ptype][pp]['sorteddepthlist'])) + " /OUT pdfmark\n")
                for depth in plotdict[var][ptype][pp]['sorteddepthlist']:
                    plotdict[var][ptype][pp]['sorteddepthlist'] = list(set(plotdict[var][ptype][pp]['sorteddepthlist']))
                    f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + str(depth) + ") /OUT pdfmark\n")
                    print plotdict[var][ptype][pp]['depthfile'][depth]
                    plist.append(str(plotdict[var][ptype][pp]['depthfile'][depth]))
                    page_count += 1

    f.close()
    pstring = " ".join(plist)
    return pstring

