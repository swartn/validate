import subprocess
import os
def arrange(plotnames):
    print '\n\n\n\n\n'
    #outputs a pdf with all of the plots organized and bookmarked
    dictionary = _orderplots(plotnames)
    
    pstring = pdfmarks(dictionary)
    #subprocess.Popen(('pdfunite ' + ' '.join(plotnames) +
    #                  ' plots/joined.pdf'), shell=True).wait()    
    combine_str ='gs -sDEVICE=pdfwrite -sOutputFile=plots/joined.pdf -dQUIET -dNOPAUSE -dBATCH -dAutoRotatePages=/None -f '+pstring+' plots/pdfmarks\n'

    os.system(combine_str)
    #os.system('rm -f plots/pdfmarks')
    
def _orderplots(plotnames):
    plotdict = {}
    for name, p, t in plotnames:
        plotdict[p['variable']] = {}
        if p['climatology']:
            plotdict[p['variable']]['climatology'] = {}
        if p['trends']:
            plotdict[p['variable']]['trends'] = {}                                  
        if p['compare_climatology']:
            plotdict[p['variable']]['compare_climatology'] = {}                                  
        if p['compare_trends']:
            plotdict[p['variable']]['compare_trends'] = {}
        for ptype in plotdict[p['variable']]:
            plotdict[p['variable']][ptype] = {'sorteddepthlist': [],
                                              'depthfile': {},}        
    for name, p, t in plotnames:
        plotdict[p['variable']][t]['sorteddepthlist'].append(p['plot_depth'])
        plotdict[p['variable']][t]['sorteddepthlist'].sort()
        
        plotdict[p['variable']][t]['depthfile'][p['plot_depth']] = name[0]  
    #print 'here'      
    #print plotdict
    return plotdict

def pdfmarks(plotdict):
    f = open('plots/pdfmarks','w')
    f.write("%% BeginProlog \n/pdfmark where \n{pop} {userdict /pdfmark /cleartomark load put} ifelse \n")
    f.write("%% EndProlog \n%% BeginSetup \n[/PageMode /UseOutlines \n")
    f.write("/Page 1 /View [/XYZ null null null] \n/DOCVIEW pdfmark \n%% EndSetup\n")
    
    plist = []
    page_count = 1
    for var in plotdict:    
        f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + var + ") /Count -"+str(len(plotdict[var].keys())) + " /OUT pdfmark\n")
        for ptype in plotdict[var]:
            if len(plotdict[var][ptype]['sorteddepthlist']) > 0:          
                f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + ptype + ") /Count -" + str(len(plotdict[var][ptype]['sorteddepthlist'])) + " /OUT pdfmark\n")
                for depth in plotdict[var][ptype]['sorteddepthlist']:
                    f.write("[ /Page " + str(page_count) + " /View [/XYZ null null null] /Title (" + str(depth) + ") /OUT pdfmark\n")
                    plist.append(plotdict[var][ptype]['depthfile'][depth])
                    page_count += 1

    f.close()
    pstring = " ".join(plist)
    return pstring

