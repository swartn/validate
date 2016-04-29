"""
pdf_organizer
===============
This module contains tools to produce a multipage pdf
in an organized and labelled format specific to model plots.

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
    dictionary = orderplots(plotnames)

    pstring = pdfmarks(dictionary)
    combine_str = 'gs -sDEVICE=pdfwrite -sOutputFile=plots/joined.pdf -dQUIET -dNOPAUSE -dBATCH -dAutoRotatePages=/None -f ' + pstring + ' plots/pdfmarks\n'

    os.system(combine_str)
    os.system('rm -f plots/pdfmarks')


def orderplots(plotnames):
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
    for p in plotnames:
        if 'basin' in p:
            p['plot_depth'] = p['basin']
        try:
            p['plot_depth'] = str(p['plot_depth'])
        except:
            p['plot_depth'] = 'surface'
        if p['realm'] == 'atmos':
            try:
                p['plot_depth'] = str(float(p['plot_depth'])/100)
            except:
                pass
        if p['plot_depth'] == 'None':
            p['plot_depth'] = 'surface'
        if p['plot_projection'] == 'section':
            p['plot_depth'] = '--'
        if p['plot_projection'] == 'taylor':
            if len(p['depths']) > 1:
                p['plot_depth'] = '--'
        if p['plot_depth'] == '':
            p['plot_depth'] = '--'
        
        p['season'] = ''.join(p['seasons'])
        if p['season'] == 'DJFMAMJJASON':
            p['season'] = 'annual'
    for p in plotnames:
        plotdict[p['realm']] = {}
    for p in plotnames:
        plotdict[p['realm']][p['variable']] = {}
    for p in plotnames:
        plotdict[p['realm']][p['variable']][p['plot_projection']] = {}
    for p in plotnames:
        plotdict[p['realm']][p['variable']][p['plot_projection']][p['data_type']] = {}
    for p in plotnames:
        plotdict[p['realm']][p['variable']][p['plot_projection']][p['data_type']][p['plot_depth']] = {}
    for p in plotnames:
        plotdict[p['realm']][p['variable']][p['plot_projection']][p['data_type']][p['plot_depth']][p['dates']['start_date'][:4] + '-' + p['dates']['end_date'][:4]] = {}
    for p in plotnames:
        plotdict[p['realm']][p['variable']][p['plot_projection']][p['data_type']][p['plot_depth']][p['dates']['start_date'][:4] + '-' + p['dates']['end_date'][:4]][p['season']] = {}
    for p in plotnames:
        plotdict[p['realm']][p['variable']][p['plot_projection']][p['data_type']][p['plot_depth']][p['dates']['start_date'][:4] + '-' + p['dates']['end_date'][:4]][p['season']][p['comp_model']] = {}

    for p in plotnames:
        plotdict[p['realm']][p['variable']][p['plot_projection']][p['data_type']][p['plot_depth']][p['dates']['start_date'][:4] + '-' + p['dates']['end_date'][:4]][p['season']][p['comp_model']] = p['plot_name']
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
    f = open('plots/pdfmarks', 'w')
    f.write("%% BeginProlog \n/pdfmark where \n{pop} {userdict /pdfmark /cleartomark load put} ifelse \n")
    f.write("%% EndProlog \n%% BeginSetup \n[/PageMode /UseOutlines \n")
    f.write("/Page 1 /View [/XYZ null null null] \n/DOCVIEW pdfmark \n%% EndSetup\n")

    plist = []
    page_count = 1
    for realm in plotdict:
        f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + realm + ") /Count -" + str(len(plotdict[realm].keys())) + " /OUT pdfmark\n")
        for var in plotdict[realm]:
            f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + var + ") /Count -" + str(len(plotdict[realm][var].keys())) + " /OUT pdfmark\n")
            for proj in plotdict[realm][var]:
                f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + proj + ") /Count -" + str(len(plotdict[realm][var][proj].keys())) + " /OUT pdfmark\n")
                ordered_dt_list = plotdict[realm][var][proj].keys()
                ordered_dt_list.sort()
                for dt in ordered_dt_list:
                    f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + dt + ") /Count -" + str(len(plotdict[realm][var][proj][dt].keys())) + " /OUT pdfmark\n")
                    ordered_depth_list = []
                    for depth in plotdict[realm][var][proj][dt]:
                        ordered_depth_list.append(depth)
                    try:
                        ordered_depth_list.sort(key=float)
                    except:
                        ordered_depth_list.sort()
                    for depth in ordered_depth_list:
                        f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + depth + ") /Count -" + str(len(plotdict[realm][var][proj][dt][depth].keys())) + " /OUT pdfmark\n")
                        
                        for dates in plotdict[realm][var][proj][dt][depth]:
                            f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + dates + ") /Count -" + str(len(plotdict[realm][var][proj][dt][depth][dates].keys())) + " /OUT pdfmark\n")
                            for season in plotdict[realm][var][proj][dt][depth][dates]:
                                f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + season + ") /Count -" + str(len(plotdict[realm][var][proj][dt][depth][dates][season].keys())) + " /OUT pdfmark\n")                            
                                for comp in plotdict[realm][var][proj][dt][depth][dates][season]:
                                    f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + comp + ") /OUT pdfmark\n")
                                    plist.append(str(plotdict[realm][var][proj][dt][depth][dates][season][comp]))
                                    page_count +=1

    f.close()
    pstring = " ".join(plist)
    return pstring
