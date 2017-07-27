import sys
import matplotlib.pyplot as plt
from tools.tools import *

if __name__ == '__main__':
    # Specify log filename in the first argument.
    # Example:
    # >> python log_viewer.py log_sample.csv

    # parameters
    log_filename = sys.argv[1]
    log_format_filename = "./tools/log_format.json"
    settings_filename = "./tools/settings.json"

    # load log file
    print("Loading \""+log_filename)
    dfs = load_log_file(log_filename, log_format_filename)
    print("File load successful")

    plot_dataframes(dfs, log_format_filename, settings_filename)
