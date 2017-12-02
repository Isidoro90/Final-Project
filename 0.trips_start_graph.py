#!/usr/bin/env python

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

#%matplotlib inline

trips = pd.read_csv("Divvy_Trips.csv",
                index_col = "TRIP ID", usecols = ["TRIP ID", "START TIME"], parse_dates = ["START TIME"])

trips["Weekday"] = trips["START TIME"].dt.dayofweek.astype(int)
trips["Hour"] = trips["START TIME"].dt.hour.astype(int)
trips["time"] = trips["Weekday"]*24 + trips["Hour"]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(trips['time'],168)
ax.set_xticks(range(0,168,24))
ax.set_xticklabels(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
ax.xaxis.set_minor_locator(ticker.MultipleLocator(12))
ax.xaxis.grid(True, which='major')
ax.xaxis.grid(False, which='minor')
ax.set(xlabel='Hours in a week', ylabel='Number of trips',title='Days of a Week')
plt.savefig("start_time_graph.png")
plt.show()
