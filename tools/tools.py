import json
import csv
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def load_log_file(log_filename, data_format_filename):
    data_format = json.load(open(data_format_filename))

    # create empty list for storing data
    data = {}
    for id in data_format["id"].keys():
        logtype = data_format["id"][id]["logtype"]
        labels = data_format["id"][id]["labels"]
        data[logtype] = {"labels": labels, "data": []}

    # read log file and append each row to corresponding list
    with open(log_filename, 'r') as f:
        reader = csv.reader(f, lineterminator='\n')
        row_number = 0
        for row in reader:
            id = row[0]
            logtype = data_format["id"][id]["logtype"]
            ndata = len(data_format["id"][id]["labels"])
            if ndata + 1 > len(row):
                raise IndexError("Insufficient number of columns for id = "+ id +" at row "+str(row_number))
                break
            row_trimmed = [float(x) for x in row[1:ndata+1]]
            data[logtype]["data"].append(row_trimmed)
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
            df.to_csv(log_filename.replace('.csv','_'+logtype+'.csv'))
            dfs.append(df)
        else:
            pass
    return dfs

def plot_flightctrl(fig, df):
    t = np.array(df["timestamp"])
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
    ax1.set_title("Nav Mode Request")

    # Flightctrl request
    ax2 = fig.add_subplot(232)
    ax2.plot(t,fcs)
    ax2.grid()
    ax2.set_title("FlightCtrl State")

    # Accelerometer
    ax3 = fig.add_subplot(233)
    ax3.plot(t,ax)
    ax3.plot(t,ay)
    ax3.plot(t,az)
    ax3.grid()
    ax3.set_title("Accelerometer")

    # Gyro
    ax4 = fig.add_subplot(234)
    ax4.plot(t,wx)
    ax4.plot(t,wy)
    ax4.plot(t,wz)
    ax4.grid()
    ax4.set_title("Gyro")

    # Quaternion
    ax5 = fig.add_subplot(235)
    ax5.plot(t,q0)
    ax5.plot(t,qx)
    ax5.plot(t,qy)
    ax5.plot(t,qz)
    ax5.grid()
    ax5.set_title("Quaternion")

    # Pressure altitude
    ax6 = fig.add_subplot(236)
    ax6.plot(t,pa)
    ax6.grid()
    ax6.set_title("Pressure Altitude")
