#! /usr/bin/env python

# --------------------------------------------------------------
# Utility to monitor internet speed on a Mac.
# Every 10 min refreshes image ~/Desktop/sptest.png
# 
# To make it work:
#   create directory $HOME/internet_speed_test/
#   and copy there the following files:
#      speedtest.py
#      log_speedtest.py
#      speedtest.log
#      speedtest.ipynb
# 
# The jupyter notebook helps to debug code
# (in case some libraries are missing).
#      
# 
# Then add the following entry to the crontab:
# 
# # run internet speed test every 10 min
# */10 * * * * bash -c 'cd ~/; source .bashrc; cd ~/internet_speed_test; python speedtest_log.py >> speedtest.err 2>&1'
# 
# 
# Note - the original code:
#     https://www.accelebrate.com/blog/pandas-bandwidth-python-tutorial-plotting-results-internet-speed-tests/
#     https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py
# 
# See there how to parse the log file and show graphics
# --------------------------------------------------------------
import sys, os
import logging, datetime
import matplotlib.pyplot as plt
from matplotlib import dates, rcParams
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

SPEEDTEST_CMD = 'speedtest.py'
LOG_FILE      = 'speedtest.log'
IMG_FILE      = '/Users/levselector/Desktop/sptest.png'

# --------------------------------------------------------------
def setup_logging():
    logging.basicConfig (
        filename = LOG_FILE,
        level    = logging.INFO,
        format   = "%(asctime)s %(message)s",
        datefmt  = "%Y-%m-%d %H:%M" )

# --------------------------------------------------------------
def get_speedtest_results():
    """
    # Run test and parse results.
    # Returns tuple of ping speed, download speed, and upload speed,
    # or raises ValueError if unable to parse data.
    """
    ping = download = upload = None

    with os.popen(SPEEDTEST_CMD + ' --simple') as speedtest_output:
        for line in speedtest_output:
            label, value, unit = line.split()
            if 'Ping' in label:
              ping = float(value)
            elif 'Download' in label:
              download = float(value)
            elif 'Upload' in label:
              upload = float(value)

        if all((ping, download, upload)): # if all 3 values were parsed
          return ping, download, upload
        else:
          raise ValueError('TEST FAILED')

# --------------------------------------------------------------
def make_plot(plt, df, row_index=1, nhours=2):
    # ---------------------------------
    # select last "nhours" of data
    index_max = df.index[-1]
    dtmax = df.loc[index_max,'timestamp']
    dtmin = dtmax - datetime.timedelta(hours=nhours)

    mask = df['timestamp'] > dtmin
    df = df.loc[mask,:].copy()
    df.index = range(len(df))
    # ---------------------------------
    # subplot(nrows, ncols, index, **kwargs)
    plt.subplot(3, 1, row_index)
    plt.plot(df['timestamp'],df['download'], 'b-')
    plt.title('Internet Speed (Download in Mbps)')
    plt.ylabel('Bandwidth in MBps')
    y_range = 1.2*df.download.max()
    plt.ylim(0.0,y_range)
    plt.xlabel('Date/Time')
    plt.xticks(rotation='45', ha='right')
    # ---------------------------------
    ax = plt.gca()
    fg = plt.gcf()

    start = df.loc[0,'timestamp']
    end   = df.loc[df.index[-1],'timestamp']
    delta = (end-start)/11.0
    arr = [start]
    for ii in range(12):
        val = arr[-1]
        arr += [val+delta]

    ax.xaxis.set_ticks(arr)
    h_fmt = dates.DateFormatter('%m/%d %H:%M')
    ax.xaxis.set_major_formatter(h_fmt)
    # ---------------------------------
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)

    fg.subplots_adjust(bottom=.25)
    plt.grid();

# --------------------------------------------------------------
def read_data():
    df = pd.io.parsers.read_csv(
        'speedtest.log',
        names='date time ping download upload'.split(),
        header=None,
        sep=r'\s+',
        parse_dates={'timestamp':[0,1]},
        na_values=['TEST','FAILED'])

    for col in 'ping download upload'.split():
        df[col] = df[col].fillna(0.0)

    # We run script every 10 min, or 6/hr, or 6*24=144/day
    Nrows = 5*144
    return df[-Nrows:]   # return dots for last Nrows only

# --------------------------------------------------------------
def main():
    setup_logging()
    try:
        ping, download, upload = get_speedtest_results()
    except ValueError as err:
        logging.info(err)
    else:
        logging.info("%5.1f %5.1f %5.1f", ping, download, upload)
    df = read_data()
    
    # ------------------------------------------
    w = 10
    h = 5
    rcParams['figure.figsize'] = w, h
    plt.gcf().clear()
    make_plot(plt, df.copy(), row_index=1, nhours=5*24)
    make_plot(plt, df.copy(), row_index=3, nhours=2   )
    fg = plt.gcf()
    fg.savefig(IMG_FILE)

# --------------------------------------------------------------
if __name__ == '__main__':
  main()

