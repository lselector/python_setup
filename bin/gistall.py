#! /bin/env python

"""
# gistall.py
# checks status of all repos under ~/mydir
# It effectively runs "gist" command in all repos directories.
# To use it, create a symbolic link like this:
#    cd ~/bin
#    ln -s py_lib/bin/gistall.py ./gistall
"""

import os
import sys
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"

import re
import argparse

import ipython_debug
# reload(ipython_debug)
from ipython_debug import *

import mybag
# reload(mybag)
from mybag import *

import myutil
# reload(myutil)
from myutil import *

# ---------------------------------------------------------------
def make_cmd_template(bag):
    """
    # returns template string with shell commands
    """
    ss = """cd __REPO_DIR__; echo "__SEP__" `pwd`;""" 
    if bag.update_from_remote:
        ss += """ git stash clear;
                  git stash -q;
                  git pull;
                  stashes=`git stash list | wc -l`;
                  if [ $stashes -ne 0 ]; then git stash apply; fi;"""
        ss = ss.replace("__SEP__", bag.sep)
        ss = re.sub(r'\s+', ' ', ss)
        return ss
    # ----------------------------------
    # if we are here - we will do gist
    if not bag.verbose:
        ss += """ git fetch -q; 
                  git diff --name-status origin/master . ;
                  git status -s . ;"""
    else:
        ss += """
        echo "__SEP__ files which diff from remote repo";
        git fetch;
        git diff --name-status origin/master . ;
        echo "__SEP__ files changed locally";
        git status . ;
        echo "__SEP__" ; """
    
    ss = ss.replace("__SEP__", bag.sep)
    ss = re.sub(r'\s+', ' ', ss)

    return ss


# ---------------------------------------------------------------
def process_cmd_args(bag):
    """
    # process cmd line arguments
    """
    descr_str = """Script to check status of all repos under ~/mydir
        by running git fetch, diff, and status in subdirectories"""
    parser = argparse.ArgumentParser(description=descr_str)
    parser.add_argument('--verbose', '-verbose', '-v', 
        action='store_true',  dest='arg_verbose', default=False,
        help="flag to get more verbose output")
    parser.add_argument('--update', '-update', '-u', 
        action='store_true',  dest='arg_update', default=False,
        help="update from remote server")
    bag.arg_raw = parser.parse_args()
    bag.verbose = False
    bag.update_from_remote = False
    if bag.arg_raw.arg_verbose:
        bag.verbose = True
    if bag.arg_raw.arg_update:
        bag.update_from_remote = True

# ---------------------------------------------------------------
def set_bag_repo_dirs(bag):
    """
    # populate bag.repo_dirs - a list of repositories to go through
    # reades the list from file ~/.gitsall  
    """
    mylist = ["common_config", "py_lib"] # min list
    bag.dot_gistall = bag.home + "/.gistall"
    if os.path.isfile(bag.dot_gistall):
        lines = slurp(bag.dot_gistall).split("\n") 
        for line in lines:
            myword = line.strip()
            mydir  = bag.root_dir + "/" + myword
            if len(myword) and (myword[0] != '#') and os.path.isdir(mydir):
                mylist.append(myword)
    
    bag.repo_dirs = sorted(set(mylist)) # remove duplicates and order

# ---------------------------------------------------------------
def myexit(bag):
    """
    # returns to initial directory 
    # and exists with proper return code
    """
    os.chdir(bag.init_dir)
    sys.exit(bag.error_flag)

# ---------------------------------------------------------------
def chdir_mydir(bag):
    """
    # cd into mydir directory
    """    
    if not os.path.isdir(bag.root_dir):
        print("ERROR, directory '%s' doesn't exist, Exiting ..." % bag.root_dir)
        bag.error_flag = 1
        myexit(bag)
    
    os.chdir(bag.root_dir)
    
    # check that we are in correct directory
    if os.getcwd() != bag.root_dir:
        print("ERROR, script only runs from '%s' directory. Exiting ..." % bag.root_dir)
        bag.error_flag = 1
        myexit(bag)

# ---------------------------------------------------------------
def main(bag):
    """
    # main execution
    """
    bag.error_flag = 0
    bag.sep = "-"*36
    process_cmd_args(bag)
    bag.init_dir = os.getcwd() # initial directory
    bag.home = os.path.expanduser("~")
    bag.root_dir = bag.home + "/" + "mydir"
    set_bag_repo_dirs(bag)
    chdir_mydir(bag)
    bag.cmd_template = make_cmd_template(bag)
    for repo_dir in bag.repo_dirs:
        if not os.path.isdir(repo_dir):
            if bag.verbose:
                print("\n", bag.sep, "directory '%s' doesn't exist, skipping ...\n" % repo_dir)
            continue
        mycmd = bag.cmd_template.replace("__REPO_DIR__",repo_dir)
        if bag.verbose:
            print(mycmd,"\n")
        run_cmd(bag, mycmd, verbose=False)

    myexit(bag)

# ---------------------------------------------------------------
# main execution
# ---------------------------------------------------------------
if __name__ == "__main__":
    bag = MyBunch()
    main(bag)
