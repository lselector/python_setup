
"""
# helper functions for jupyter notebook
# by Lev Selector, 2019
"""

import sys, os
import pandas as pd
import numpy as np
import time, glob, re, pickle, gc
import datetime as dt
from IPython import get_ipython
from IPython.display import display, Image

# --------------------------------------------------------------
def is_jupyter():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

# --------------------------------------------------------------
def is_ipython():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'TerminalInteractiveShell':
            return True  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

# --------------------------------------------------------------
def sdf(df, label=""):
    """
    # for a pandas DataFrame displays Nrows, Ncols, head(3)
    """
    Nrows = len(df)
    Ncols = len(df.columns)
    if len(label) >= 1:
        print(label," : ",end="")
    print('rows = {:2,d}'.format(Nrows), ', cols = {:2,d}'.format(Ncols))
    display(df.head(3))
    print('-' * 50)

# --------------------------------------------------------------
def sdf0(df, label=""):
    """
    # for a pandas DataFrame displays Nrows, Ncols
    """
    Nrows = len(df) 
    Ncols = len(df.columns)
    if len(label) >= 1:
        print(label," : ",end="")
    print('rows = {:2,d}'.format(Nrows), ', cols = {:2,d}'.format(Ncols))
    print('-' * 50)

# --------------------------------------------------------------
def sdf1(df, label=""):
    """
    # for a pandas DataFrame displays Nrows, Ncols, columns
    """
    Nrows = len(df)
    Ncols = len(df.columns)
    if len(label) >= 1:
        print(label," : ",end="")
    print('rows = {:2,d}'.format(Nrows), ', cols = {:2,d}'.format(Ncols), list(df.columns))
    print('-' * 50)

# --------------------------------------------------------------
def sdf2(df, label=""):
    """
    # for a pandas DataFrame displays Nrows, Ncols, head(3), tail(3)
    """
    Nrows = len(df)
    Ncols = len(df.columns)
    if len(label) >= 1:
        print(label," : ",end="")
    print('rows = {:2,d}'.format(Nrows), ', cols = {:2,d}'.format(Ncols))
    print("HEAD:")
    display(df.head(3))
    print("TAIL:")
    display(df.tail(3))
    print('-' * 50)

# --------------------------------------------------------------
def sdf3(df):
    """
    # for a pandas DataFrame displays Nrows, Ncols, head(3), tail(3)
    # also summary for all columns:
    #     (count,unique,top,freq,mean,std,min,25%,50%,75%,max)
    """
    sdf2(df)
    print('SUMMARY :')
    display(df.describe(include='all'))
    print('*' * 50)

# --------------------------------------------------------------
def date_time():
    """
    # returns string YYYY-MM-DD HH:MM:SS
    """
    import datetime
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now_str

# --------------------------------------------------------------
def date_time_for_fname():
    """
    # returns string YYYYMMDD_HHMMSS
    """
    import datetime
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return now_str

# --------------------------------------------------------------
def print_date_time(label = "date_time"):
    """
    # prints current date and time
    """
    now_str = date_time()
    print (label, " : ", now_str)

# --------------------------------------------------------------
def sec_to_hms(secs):
    """
    # converts seconds into string in format "HH:MM:SS"
    """
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    h_str = "%d"   % int(h)
    m_str = "%02d" % int(m)
    s_str = "%02.2f" % round(s,2)
    s_str = re.sub(r'\.00$','',s_str)
    # return ':'.join([h_str,m_str,s_str])
    return "%sh %sm %ss" % (h_str,m_str,s_str)
# --------------------------------------------------------------
def read_df_from_extract(fname=None):
    """ reads file, returns DataFrame """
    print("reading",fname)
    df = pd.read_csv(fname, low_memory=False)
    df.index = range(len(df))
    df.columns = [x.lower() for x in list(df.columns)]
    print(" "*20 + "%d cols, %d rows" % (len(df.columns), len(df)))
    return df

# --------------------------------------------------------------
def today_yyyymmdd():
    """ returns string for today in format YYYYMMDD """
    yyyy,mm,dd = str(dt.date.today()).split('-')
    return "%s%s%s" % (yyyy,mm,dd)

# --------------------------------------------------------------
def delete_dataframes():
    """ deletes all DataFrames from memory """
    myvars = globals()
    for vv in sorted(myvars):
        if 'DataFrame' in str(type(eval(vv))):
            del globals()[vv]
    gc.collect()

# --------------------------------------------------------------
def df_memory(df):
    """ returns memory usage of pandas DataFrame "df" in MB """ 
    return df.memory_usage(deep=True).sum()/1024.0/1024.0

# --------------------------------------------------------------
def shout_error(ss, rep=10):
    for ii in range(rep):
        print("ERROR, ", ss)

    try: run_step
    except NameError: run_step = -1
    run_step -= 1

    try: ok_flag
    except NameError: ok_flag = False
    ok_flag = False

    sys.exit(1) 

# --------------------------------------------------------------
def ddd():
    """
    # returns a simple pandas DataFrame - useful for quick tests
    """
    nrows = 7
    ss = b'\xe7\x8b\x97'
    ch1 = ss.decode('utf-8')
    ss = b'\xe6\xb1\xbd\xe8\xbd\xa6'
    ch2 = ss.decode('utf-8')
    aa = pd.DataFrame({
          'ii':[0,1,2,3,4,5,np.nan],                                           # float64
          'i1':[6,5,4,3,2,1,0],
          'i2':[6,5,4,4,1,1,0],
          'ff':[0.0,1.0,2.0,np.NaN,4.0,5.0,6.0],                               # float64
          'f1':[0.0,1.01,2.002,3.0003,4.00004,5.000005,6.0000006],
          'f2':[1.11,2.22,3.33,4.44,5.55,7.77,9.99],
          'ss':['s0','s1',ch1,ch2,np.nan,'s5','s6'],                           # dtype=object, np.nan is float64
          's1':np.array(['s0','s1','s2','s2',np.nan,'s5','s6'],dtype=np.str),  # dtype=object, 'nan' is string
          's2':['1.11','2.22','3.33','4.44','5.55','7.77','9.99'],
          'bb':[True, False, True, False, np.nan, False, True],                # dtype=object, np.nan is float64
          'b1':[True, False, True, False, True, False, True],                  # dtype=bool
          'xx':range(nrows),
          'yy':[x*50 + 60 + np.random.randn() for x in range(nrows)]
    })

    return aa[['ii','i1','i2','ff','f1','f2','ss','s1','s2','bb','b1','xx','yy']]

# --------------------------------------------------------------
def cell_width(width_pct=95):
    """
    # sets width of jupyter cells (in percentage of window)
    # Usage:
    #    cell_width()      # 95% default
    #    cell_width(85)    # 85%
    """
    from IPython.core.display import display, HTML
    ss = """<style>
              .container {width:__CHANGE_ME__ !important;}
            </style>
         """
    ss = ss.replace("__CHANGE_ME__", str(width_pct)+"%")
    display(HTML(ss))
    return HTML(ss)

# --------------------------------------------------------------
def commify(n, show_cents=False):
    """
    # accepts money amount, adds commas
    # don't return cents by default
    """
    if n is None: return None
    if n < 0: return '-' + commify(-n,show_cents)
    n = round(n,2)               # only keep 2 digits for cents
    dollars = int(n)
    cents   = round((n - dollars)*100)
    dollars = '%d' % dollars
    cents   = '%02d' % cents
    groups = []
    while dollars and dollars[-1].isdigit():
        groups.append(dollars[-3:])
        dollars = dollars[:-3]
    ss = dollars + ','.join(reversed(groups))
    if show_cents :
        ss = ss + '.' + cents
    return ss

# --------------------------------------------------------------
def commify2(n):
    """
    # accepts money amount, adds commas, shows cents
    """
    return commify(n,True)

# --------------------------------------------------------------
def commify2_dollar(n):
    """
    # accepts money amount, adds commas, 
    # shows cents, prepends dollar sign
    """
    return "$" + commify2(n)
# --------------------------------------------------------------
