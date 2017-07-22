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
    df_flightctrl = None
    try:
        df_flightctrl = dfs[[df.index.name for df in dfs].index('flightctrl')]
    except ValueError:
        print("\'flightctrl\' not in log file")
    if df_flightctrl is not None:
        fig = plt.figure()
        plot_flightctrl(fig, df_flightctrl, log_format_filename)

    # plot vision data
    df_vision = None
    try:
        df_vision = dfs[[df.index.name for df in dfs].index('vision')]
    except ValueError:
        print("\'vision\' not in log file")
    if df_vision is not None:
        fig2 = plt.figure()
        plot_vision(fig2, df_vision, log_format_filename)

    # plot debug data
    df_debug = None
    try:
        df_debug = dfs[[df.index.name for df in dfs].index('debug')]
    except ValueError:
        print("\'debug\' not in log file")
    if df_debug is not None:
        fig3 = plt.figure()
        plot_debug(fig3, df_debug, log_format_filename)

    # show plot
    plt.show()
