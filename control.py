import directory_tools as dt
import plotter as pltr
import pdforganize as org
import defaults as dft

def execute(plots, run, obs, defaults, delete):
    filled_plots = dft.fill(plots, obs, defaults)
    plots_with_files = dt.getfiles(filled_plots, run)    
    plotnames = pltr.loop(plots_with_files)
    dt.remfiles(**delete)
    org.arrange(plotnames)
    
        
