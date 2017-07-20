import sys
import matplotlib.pyplot as plt
from tools.tools import *

if __name__ == '__main__':
    # Specify log filename in the first argument.
    # Example:
    # >> python log_viewer.py log_sample.csv

    # parameters
    log_filename = sys.argv[1]
    log_format_filename = 'tools/log_format.json'

    # load log file
    print("Loading \""+log_filename+"\" using log format defined in \""+log_format_filename+"\"")
    dfs = load_log_file(log_filename, log_format_filename)
    print("File load successful")

    print(dfs)
    # plot flightctrl data
    fig = plt.figure()
    df_flightctrl = dfs[[df.index.name for df in dfs].index('flightctrl')]
    plot_flightctrl(fig, df_flightctrl, log_format_filename)

    # plot vision data
    fig2 = plt.figure()
    df_vision = dfs[[df.index.name for df in dfs].index('vision')]
    plot_vision(fig2, df_vision, log_format_filename)

    # show plot
    plt.show()
    print("Plot successful")
