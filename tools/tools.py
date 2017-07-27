import json
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def load_log_file(log_filename, log_format_filename):
    log_format = json.load(open(log_format_filename))

    # create empty list for storing data
    data = {}
    for id in log_format["id"].keys():
        logtype = log_format["id"][id]["logtype"]
        labels = log_format["id"][id]["labels"]
        data[logtype] = {"labels": labels, "data": []}

    # read log file and append each row to corresponding list
    with open(log_filename, 'r') as f:
        reader = csv.reader(f, lineterminator='\n')
        row_number = 0
        for row in reader:
            print("row "+str(row_number)+":",row)
            id = row[0]
            logtype = log_format["id"][id]["logtype"]
            ndata = len(log_format["id"][id]["labels"])
            try:
                if ndata + 1 > len(row):
                    raise IndexError("Insufficient number of columns for id = "+ id +" at row "+str(row_number))
                    break
                row_trimmed = [float(x) for x in row[1:ndata+1]]
                data[logtype]["data"].append(row_trimmed)
            except ValueError:
                pass
            row_number += 1

    # generate separate log files for easier processing
    dfs = []
    for logtype in data.keys():
        labels = data[logtype]["labels"]
        arr = data[logtype]["data"]
        if len(arr) != 0:
            df = pd.DataFrame(data = arr)
            df.columns = labels
            df.index.name = logtype
            #print(df)
            df.to_csv("./output/"+log_filename.replace('.csv','_'+logtype+'.csv'))
            dfs.append(df)
        else:
            pass
    return dfs

def plot_dataframes(dfs, log_format_filename, settings_filename):
    # dfs: list of pandas dataframes
    settings = json.load(open(settings_filename))
    logtypes = list(settings["log_viewer"]["plot"].keys())

    # logtype is inserted in logtypes_present if
    # 1. plot is enabled in settings, and
    # 2. data for this logtype is present in the given dfs
    logtypes_present = [logtype for logtype in logtypes if (settings["log_viewer"]["plot"][logtype]==1 and (logtype in [df.index.name for df in dfs]))]

    print("Plotting:", logtypes_present)
    figs = [plt.figure() for i in range(len(logtypes_present))]
    for i,logtype in enumerate(logtypes_present):
        df = dfs[[df.index.name for df in dfs].index(logtype)]
        autogen_plot(figs[i], df, log_format_filename, settings_filename)

    plt.show()

def autogen_plot(fig, df, log_format_filename, settings_filename):
    # find corrensponding log id
    logtype = df.index.name
    id = get_corresponding_id(logtype, log_format_filename)

    # extract x-axis data
    log_format = json.load(open(log_format_filename))
    axes = log_format["id"][id]["axes"]
    idx_xaxis = axes.index(0)
    xaxis_label = log_format["id"][id]["labels"][idx_xaxis]
    xunit = log_format["id"][id]["units"][idx_xaxis]
    x_axis_data = np.array(df[xaxis_label])
    if xunit == "microseconds":
        x_axis_data /= 1000000.0
        xunit = "Time (s)"
    else:
        xunit = xaxis_label

    # plot
    labels = log_format["id"][id]["labels"]
    units = log_format["id"][id]["units"]
    axes = log_format["id"][id]["axes"]
    axes_layout = log_format["id"][id]["axes_layout"]
    for i in range(1,max(axes)+1):
        ax = fig.add_subplot(axes_layout[0], axes_layout[1], i)

        # find label for y-axis
        for ax_num, label, unit in zip(axes, labels, units):
            if ax_num == i: # plot in this ax
                y_axis_data = np.array(df[label])
                ax.plot(x_axis_data, y_axis_data)
                ax.grid(True)
                ax.set_xlabel(xunit)
                ax.set_ylabel(unit)
                ax.set_title(label)

        # Change xlim
        settings = json.load(open(settings_filename))
        use_xlim = int(settings["log_viewer"]["use_xlim"])
        xlim = settings["log_viewer"]["xlim"]
        if use_xlim:
            ax.set_xlim(xlim)

def get_corresponding_id(logtype, log_format_filename):
    log_format = json.load(open(log_format_filename))
    ids = list(log_format["id"].keys())
    id = [id for id in ids if log_format["id"][id]["logtype"] == logtype][0]
    return id
