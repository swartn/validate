import subprocess
import os
def arrange(plotnames):
    #outputs a pdf with all of the plots organized and bookmarked
    dictionary = _orderplots(plotnames)
    pstring = pdfmarks(dictionary)
    #subprocess.Popen(('pdfunite ' + ' '.join(plotnames) +
    #                  ' plots/joined.pdf'), shell=True).wait()    
    combine_str ='gs -sDEVICE=pdfwrite -sOutputFile=plots/joined.pdf -dQUIET -dNOPAUSE -dBATCH -dAutoRotatePages=/None -f '+pstring+' plots/pdfmarks\n'

    os.system(combine_str)
    os.system('rm -f plots/pdfmarks')
    
def _orderplots(plotnames):
    plotdict = {}
    for name, p, t in plotnames:
        plotdict[p['variable']] = []
    for name, p, t in plotnames:
        plotdict[p['variable']].append((name,t))  
    #print 'here'      
    #print plotdict
    return plotdict

def pdfmarks(plotnames):

    f = open('plots/pdfmarks','w')
    f.write("%% BeginProlog \n/pdfmark where \n{pop} {userdict /pdfmark /cleartomark load put} ifelse \n")
    f.write("%% EndProlog \n%% BeginSetup \n[/PageMode /UseOutlines \n")
    f.write("/Page 1 /View [/XYZ null null null] \n/DOCVIEW pdfmark \n%% EndSetup\n")
    
    plist = []
    page_count = 1
    for var in plotnames:
        #v = open('plots/' + var + 'title', 'a')
        #v.write(var)
        #v.close()    
        f.write("[ /Page "+str(page_count)+" /View [/XYZ null null null] /Title ("+var+") /Count -"+str(len(plotnames[var]))+" /OUT pdfmark\n")
        #page_count += 1
        #plist.append(var + 'title.pdf')
        for pl, ty in plotnames[var]:   
            f.write("[ /Page "+str(page_count)+" /View [/XYZ null null null] /Title (" + ty + ") /OUT pdfmark\n")
            plist.append(pl)
            page_count += 1
    f.close()
    pstring = " ".join(plist)
    return pstring
"""        
        # use the bookmark dictionary to finish pdfmarks
        page_count=1
        for var in bookmark:cd 
            # each variable set should be a bookmark
            f.write("[ /Page "+str(page_count)+" /View [/XYZ null null null] /Title ("+var+") /Count -"+str(len(bookmark[var]))+" /OUT pdfmark\n")
            # each plot_type for a certain variable set should be a sub-bookmark
            for pt in bookmark[var]:
                f.write("[ /Page "+str(page_count)+" /View [/XYZ null null null] /Title ("+pt+") /Count -"+str(len(bookmark[var][pt]))+" /OUT pdfmark\n")
                # each site for each plot_type and variable set should be a sub-sub-bookmark
                for site in bookmark[var][pt]:
                    f.write("[ /Page "+str(page_count)+" /View [/XYZ null null null] /Title ("+site+") /OUT pdfmark\n")
                    pdf_str = pdf_str + " " + re.search('^(.*)\\n$',file_list[bookmark[var][pt][site]['tag']]).group(1)
                    page_count = page_count + 1
        f.close()
"""
#pdfmarks()
