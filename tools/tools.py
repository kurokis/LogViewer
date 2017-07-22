import json
import csv
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

### BEGIN PARAMETERS ###
my_xlim = (838,842)
use_my_xlim = False
### END PARAMETERS ###

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

def plot_flightctrl(fig, df, log_format_filename):
    # get y-axis labels
    log_format = json.load(open(log_format_filename))
    for id in log_format["id"].keys():
        if log_format["id"][id]["logtype"] == 'flightctrl':
            labels = log_format["id"][id]["labels"]
            units = log_format["id"][id]["units"]
            ylabels = {}
            for label,unit in zip(labels,units):
                ylabels[label] = unit
            break

    t = np.array(df["timestamp"])/1000000.
    nmr = np.array(df["nav mode request"])
    fcs = np.array(df["flightctrl state"])
    ax = np.array(df["accelerometer x"])
    ay = np.array(df["accelerometer y"])
    az = np.array(df["accelerometer z"])
    wx = np.array(df["gyro x"])
    wy = np.array(df["gyro y"])
    wz = np.array(df["gyro z"])
    q0 = np.array(df["quaternion 0"])
    qx = np.array(df["quaternion x"])
    qy = np.array(df["quaternion y"])
    qz = np.array(df["quaternion z"])
    pa = np.array(df["pressure altitude"])

    # Nav mode request
    ax1 = fig.add_subplot(231)
    ax1.plot(t,nmr)
    ax1.grid()
    ax1.set_xlabel("time (s)")
    ax1.set_title("Nav Mode Request")

    # Flightctrl request
    ax2 = fig.add_subplot(232)
    ax2.plot(t,fcs)
    ax2.grid()
    ax2.set_xlabel("time (s)")
    ax2.set_title("FlightCtrl State")

    # Accelerometer
    ax3 = fig.add_subplot(233)
    ax3.plot(t,ax)
    ax3.plot(t,ay)
    ax3.plot(t,az)
    ax3.grid()
    ax3.set_xlabel("time (s)")
    ax3.set_ylabel(ylabels["accelerometer x"])
    ax3.set_title("Accelerometer")

    # Gyro
    ax4 = fig.add_subplot(234)
    ax4.plot(t,wx)
    ax4.plot(t,wy)
    ax4.plot(t,wz)
    ax4.grid()
    ax4.set_xlabel("time (s)")
    ax4.set_ylabel(ylabels["gyro x"])
    ax4.set_title("Gyro")

    # Quaternion
    ax5 = fig.add_subplot(235)
    ax5.plot(t,q0)
    ax5.plot(t,qx)
    ax5.plot(t,qy)
    ax5.plot(t,qz)
    ax5.grid()
    ax5.set_xlabel("time (s)")
    ax5.set_title("Quaternion")

    # Pressure altitude
    ax6 = fig.add_subplot(236)
    ax6.plot(t,pa)
    ax6.grid()
    ax6.set_xlabel("time (s)")
    ax6.set_ylabel(ylabels["pressure altitude"])
    ax6.set_title("Pressure Altitude")

    # Change xlim
    if use_my_xlim:
        ax1.set_xlim(my_xlim)
        ax2.set_xlim(my_xlim)
        ax3.set_xlim(my_xlim)
        ax4.set_xlim(my_xlim)
        ax5.set_xlim(my_xlim)
        ax6.set_xlim(my_xlim)

def plot_vision(fig, df, log_format_filename):
    # get y-axis labels
    log_format = json.load(open(log_format_filename))
    for id in log_format["id"].keys():
        if log_format["id"][id]["logtype"] == 'vision':
            labels = log_format["id"][id]["labels"]
            units = log_format["id"][id]["units"]
            ylabels = {}
            for label,unit in zip(labels,units):
                ylabels[label] = unit
            break

    t = np.array(df["timestamp"])/1000000.
    rx = np.array(df["position x"])
    ry = np.array(df["position y"])
    rz = np.array(df["position z"])
    qx = np.array(df["quaternion x"])
    qy = np.array(df["quaternion y"])
    qz = np.array(df["quaternion z"])
    rvarx = np.array(df["r var x"])
    rvary = np.array(df["r var y"])
    rvarz = np.array(df["r var z"])
    st = np.array(df["status"])

    # Position
    ax1 = fig.add_subplot(221)
    ax1.plot(t,rx)
    ax1.plot(t,ry)
    ax1.plot(t,rz)
    ax1.grid()
    ax1.set_xlabel("time (s)")
    ax1.set_ylabel(ylabels["position x"])
    ax1.set_title("Position")

    # Quaternion
    ax2 = fig.add_subplot(222)
    ax2.plot(t,qx)
    ax2.plot(t,qy)
    ax2.plot(t,qz)
    ax2.grid()
    ax2.set_xlabel("time (s)")
    ax2.set_title("Quaternion")

    # Position variance
    ax3 = fig.add_subplot(223)
    ax3.plot(t,rvarx)
    ax3.plot(t,rvary)
    ax3.plot(t,rvarz)
    ax3.grid()
    ax3.set_xlabel("time (s)")
    ax3.set_ylabel(ylabels["r var x"])
    ax3.set_title("Position Variance")

    # Status
    ax4 = fig.add_subplot(224)
    ax4.plot(t,st)
    ax4.grid()
    ax4.set_xlabel("time (s)")
    ax4.set_title("Status")

    # Change xlim
    if use_my_xlim:
        ax1.set_xlim(my_xlim)
        ax2.set_xlim(my_xlim)
        ax3.set_xlim(my_xlim)
        ax4.set_xlim(my_xlim)

def plot_debug(fig, df, log_format_filename):
    # get y-axis labels
    log_format = json.load(open(log_format_filename))
    for id in log_format["id"].keys():
        if log_format["id"][id]["logtype"] == 'debug':
            labels = log_format["id"][id]["labels"]
            units = log_format["id"][id]["units"]
            ylabels = {}
            for label,unit in zip(labels,units):
                ylabels[label] = unit
            break

    t = np.array(df["timestamp"])/1000000.
    nmr = np.array(df["nav mode request"])
    fcs = np.array(df["flightctrl state"])
    rx = np.array(df["position x"])
    ry = np.array(df["position y"])
    rz = np.array(df["position z"])
    gbx = np.array(df["g_b_cmd x"])
    gby = np.array(df["g_b_cmd y"])
    q0 = np.array(df["quaternion 0"])
    qx = np.array(df["quaternion x"])
    qy = np.array(df["quaternion y"])
    qz = np.array(df["quaternion z"])
    tc = np.array(df["thrust cmd"])

    # Nav mode request
    ax1 = fig.add_subplot(231)
    ax1.plot(t,nmr)
    ax1.grid()
    ax1.set_xlabel("time (s)")
    ax1.set_title("Nav Mode Request")

    # Flightctrl request
    ax2 = fig.add_subplot(232)
    ax2.plot(t,fcs)
    ax2.grid()
    ax2.set_xlabel("time (s)")
    ax2.set_title("FlightCtrl State")

    # Position
    ax3 = fig.add_subplot(233)
    ax3.plot(t,rx)
    ax3.plot(t,ry)
    ax3.plot(t,rz)
    ax3.grid()
    ax3.set_xlabel("time (s)")
    ax3.set_ylabel(ylabels["position x"])
    ax3.set_title("Position")

    # Gravity command in b-frame
    ax4 = fig.add_subplot(234)
    ax4.plot(t,gbx)
    ax4.plot(t,gby)
    ax4.grid()
    ax4.set_xlabel("time (s)")
    ax4.set_ylabel(ylabels["g_b_cmd x"])
    ax4.set_title("Gravity command in b-frame")

    # Quaternion
    ax5 = fig.add_subplot(235)
    ax5.plot(t,q0)
    ax5.plot(t,qx)
    ax5.plot(t,qy)
    ax5.plot(t,qz)
    ax5.grid()
    ax5.set_xlabel("time (s)")
    ax5.set_title("Quaternion")

    # Thrust command
    ax6 = fig.add_subplot(236)
    ax6.plot(t,tc)
    ax6.grid()
    ax6.set_xlabel("time (s)")
    ax6.set_ylabel(ylabels["thrust cmd"])
    ax6.set_title("Thrust command")

    # Change xlim
    if use_my_xlim:
        ax1.set_xlim(my_xlim)
        ax2.set_xlim(my_xlim)
        ax3.set_xlim(my_xlim)
        ax4.set_xlim(my_xlim)
        ax5.set_xlim(my_xlim)
        ax6.set_xlim(my_xlim)
