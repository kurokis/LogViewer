import sys
import matplotlib.pyplot as plt
from tools.tools import *

if __name__ == '__main__':
    # Specify log filename in the first argument.
    # Example:
    # >> python log_viewer.py log_sample.csv

    # load log file
    log_filename = sys.argv[1]
    log_format_filename = 'tools/log_format.json'
    print("Loading \""+log_filename+"\" using log format defined in \""+log_format_filename+"\"")
    dfs = load_log_file(log_filename, log_format_filename)
    print("File load successful")

    # plot flightctrl data
    fig = plt.figure()
    df_flightctrl = dfs[[df.index.name for df in dfs].index('flightctrl')]
    plot_flightctrl(fig, df_flightctrl)
    plt.show()
    print("Plot successful")
