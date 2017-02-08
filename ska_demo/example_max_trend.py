
# -------------------------------------------------------------------------------------------------
# Package Imports

from os.path import expanduser
import sys
from matplotlib import rcParams, rc, font_manager, ticker

home = expanduser("~")

addthispath = home + '/AXAFLIB/fot_trend'
sys.path.append(addthispath)
from fot_trend import MSIDTrend

addthispath = home + '/AXAFLIB/fot_bad_intervals/'
sys.path.append(addthispath)
import fot_bad_intervals


# -------------------------------------------------------------------------------------------------
# General Plot Settings

rcParams['xtick.major.pad'] = 5
rcParams['ytick.major.pad'] = 10
rc('font', family='sans-serif') 
rc('font', weight='light')
lightfont = font_manager.FontProperties(weight='light')
minorLocator   = ticker.AutoMinorLocator(2)


# -------------------------------------------------------------------------------------------------
# Function Definitions

def filter_out_more_bad_data(datatimes):
    ''' Filter out additional data
    '''
    def filterout(datatimes, keep, t1, t2):
        bad1 = datatimes > DateTime(t1).secs
        bad2 = datatimes < DateTime(t2).secs
        bad = bad1 & bad2
        allbad = ~keep | bad
        keep = ~allbad
        return keep

    t1 = '2015:336:00:00:00'
    t2 = '2015:341:00:00:00'
    keep = np.array([True]*len(datatimes))
    return filterout(datatimes, keep, t1, t2)


# -------------------------------------------------------------------------------------------------
# Fetch and Clean Data

starttime = '2000:001:00:00:00'
stoptime = '2017:001:23:59:59.999'
msid = '3FLCABPT'
data = fetch_eng.Msid(msid, starttime, stoptime)    

keep = fot_bad_intervals.get_keep_ind(data.times, None, '1dpamyt', 'daily')
keep2 = filter_out_more_bad_data(data.times)
mask = keep & keep2


# -------------------------------------------------------------------------------------------------
# Generate Trends

s0 = MSIDTrend(msid, tstart=starttime, tstop=stoptime, numstddev=0, 
                         removeoutliers=True, maxoutlierstddev=5, trendmonths=36)
s2 = MSIDTrend(msid, tstart=starttime, tstop=stoptime, numstddev=2, 
                         removeoutliers=True, maxoutlierstddev=5, trendmonths=36)
s3 = MSIDTrend(msid, tstart=starttime, tstop=stoptime, numstddev=3, 
                         removeoutliers=True, maxoutlierstddev=5, trendmonths=36)
p0, std0 = s0.get_polyfit_line(s0.telem.monthlymaxes)
p2, std2 = s2.get_polyfit_line(s2.telem.monthlymaxes)

xfit = np.linspace(s0.telem.monthlytimes[-36], 
                   s0.telem.monthlytimes[-1] + 12*365.25*24*3600, 10)
yfit = np.polyval(p0, xfit)


# -------------------------------------------------------------------------------------------------
# Create Plot

xdate = ['%d:001:00:00:00'%n for n in range(2000,2030,1)]
xtik = DateTime(xdate).secs
xlab = np.array([t[:4] for t in xdate])
xlab[1:-1:2] = ''
if np.mod(int(xlab[-1][-1]), 2) == 1:
    xlab[-1] = ''

fig = plt.figure(figsize=(16,8),facecolor=[1,1,1])
ax = fig.add_axes([0.1, 0.15, 0.8, 0.75])
ax.plot(data.times[mask], data.vals[mask], color=[0.4, 0.6, 1]) #, marker='.')    
ax.plot(s0.telem.monthlytimes[-36:], s0.telem.monthlymaxes[-36:], 
           color = [0.3, 0.3, 0.8], marker='o')
ax.plot(xfit, yfit, 'b-')
ax.plot(xfit, yfit + std0*2, 'b--')

ax.grid(visible=True)
ax.set_ylabel('Temperature in C', fontsize=18, fontproperties=lightfont)
ax.set_xticklabels('')
ax.set_xticks(xtik)
ax.set_xticklabels(xlab, fontsize=16, ha='right', rotation=30, rotation_mode='anchor')
ax.set_xlim(xtik[0],xtik[-1]+3600*24*10)
ax.set_ylim(-5,45)
ax.set_yticks(range(-5,50,5))
ax.set_yticklabels(ax.get_yticks(), fontsize=18)
ax.set_title('Example Trend Analysis (3FLCABPT)', fontsize=22)


# -------------------------------------------------------------------------------------------------
# Plot Annotations

yellowlimitline = ax.plot([xtik[0],xtik[-1]], [33, 33],'orange',linewidth=1.5)
redlimitline = ax.plot([xtik[0],xtik[-1]], [37.5, 37.5], 'red', linewidth=1.5)

whtext = ax.text(xtik[0]+5e6, 38,
                 'Current Warning High (Red) = 37.5C', ha="left",
                 va="bottom", size=18)
chtext = ax.text(xtik[0]+5e6, 33.0,
                 'Current Caution High (Yellow) = 33.0C', ha="left",
                 va="bottom", size=18)

s0text = ax.annotate('Trendline + 0$\sigma$',
                    xy=(xtik[24] - 220*24*3600, 30),  xycoords='data',
                    xytext=(xtik[22], 25),
                    textcoords='data',arrowprops=dict(arrowstyle="->"),
                    horizontalalignment='left', verticalalignment='center',
                    fontsize=18)

s2text = ax.annotate('Trendline + 2$\sigma$',
                    xy=(xtik[20], 30),  xycoords='data',
                    xytext=(xtik[14], 30),
                    textcoords='data',arrowprops=dict(arrowstyle="->"),
                    horizontalalignment='left', verticalalignment='center',
                    fontsize=18)

crosstext = ax.annotate('May Exceed Warning High Limit in 2027',
                    xy=(xtik[26] + 300*24*3600, 38),  xycoords='data',
                    xytext=(xtik[16], 42),
                    textcoords='data',arrowprops=dict(arrowstyle="->"),
                    horizontalalignment='left', verticalalignment='center',
                    fontsize=14)

telemtext = ax.annotate('Telemetry \n(Light Blue)',
                    xy=(xtik[15], 8),  xycoords='data',
                    xytext=(xtik[19], 7),
                    textcoords='data',arrowprops=dict(arrowstyle="->"),
                    horizontalalignment='left', verticalalignment='center',
                    fontsize=18)

mothlytext = ax.annotate('Monthly Maximum Data \n(Dark Blue Circles)',
                    xy=(xtik[16], 20),  xycoords='data',
                    xytext=(xtik[18], 16),
                    textcoords='data',arrowprops=dict(arrowstyle="->"),
                    horizontalalignment='left', verticalalignment='center',
                    fontsize=18)

plt.draw()
