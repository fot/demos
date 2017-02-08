# Initial Instructions:
#
# 1) Open terminal
# 2) type "skatest" (without double quotes) at the command prompt, hit enter
# 3) type "ipython --pylab" at the command prompt, hit enter
# 4) type "execfile('ska_demo.py')" at the ipython command prompt, hit enter

# ------------------------------------------------------------------------------------------------
# Import Libraries
# 
# All libraries are available under https://github.com/sot/, but will not run correctly without
# access to the telemetry data which is not publicly available.
#
# matplotlib is a general purpose open source plotting package (i.e. library)
#
# Ska.matplotlib is a Chandra-specific plotting library that is built upon matplotlib
#
# plot_cxctime is a custom function built on top of available matplotlib functions and from other
# packages
#
from Ska.Matplotlib import plot_cxctime

# Ska.engarchive is a Chandra specific package built to facilitate fast access to spacecraft
# telemetry
#
# fetch_eng is the fetch function built into the Ska.engarchive package
from Ska.engarchive import fetch_eng as fetch

# ------------------------------------------------------------------------------------------------
# Query Telemetry and Generate Plot

# Define variables for sensor name (msid) and start time
msid = 'aacccdpt'
starttime = '2001:001'

# Query Telemetry
data = fetch.Msid(msid, starttime)

# Generate Interactive Plot
plot_cxctime(data.times, data.vals)

# See http://matplotlib.org/gallery.html for examples of plot customization