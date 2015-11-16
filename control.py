from directory_tools import getfiles, remfiles
from plotter import loop
from pdforganize import arrange
from defaults import fill

def execute(plots, run, obs, defaults, delete):
    filled_plots = fill(plots, obs, defaults)
    plots_with_files = getfiles(filled_plots, run)    
    plotnames = loop(plots_with_files)
    remfiles(**delete)
    arrange(plotnames)
    
        
