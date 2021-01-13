
Utility to monitor internet speed on a Mac.
Every 10 min refreshes image ~/Desktop/sptest.png

To make it work:
  create directory $HOME/internet_speed_test/
  and copy there the following files:
     speedtest.py
     log_speedtest.py
     speedtest.log
     speedtest.ipynb

The jupyter notebook helps to debug code
(in case some libraries are missing).
     

Then add the following entry to the crontab:

# run internet speed test every 10 min
*/10 * * * * bash -c 'cd ~/; source .bashrc; cd ~/internet_speed_test; python speedtest_log.py >> speedtest.err 2>&1'

# create a link to show image on Desktop
cd ~/Desktop
ln -s $HOME/internet_speed_test/sptest.png sptest.png

Note - the original code:
    https://www.accelebrate.com/blog/pandas-bandwidth-python-tutorial-plotting-results-internet-speed-tests/
    https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py

See there how to parse the log file and show graphics
