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
            plist.append(pl[0])
            page_count += 1
    f.close()
    pstring = " ".join(plist)
    return pstring

