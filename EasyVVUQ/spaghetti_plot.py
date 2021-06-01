"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18, 'legend.fontsize': 15})
plt.rcParams['figure.figsize'] = 12,9

"""
*************
* Load data *
*************
"""

data = pd.read_csv('FC_spaghetti_plot.csv', header = 0)
L = 551
time = np.arange(start=0, stop=L, step=1)
IC_capacity = 109

n_runs = 100

# store in a matrix the moving average of IC_prev (each column is a different simulation)
IC_prev_avg = np.zeros((L,n_runs), dtype='float')
for i in range(n_runs):
    #IC_prev_avg[:,i] = np.copy(data.IC_prev.iloc[i*L:(i+1)*L].to_numpy())
    IC_prev_avg[:,i] = data.IC_prev.iloc[i*L:(i+1)*L].rolling(window=30, center=True).mean()

# store few individual realizations to plot
runs2plot = [18, 7, 45, 27, 69]
IC_prev_avg_2plot = np.zeros((L,len(runs2plot)), dtype='float')
for i in range(len(runs2plot)):
    IC_prev_avg_2plot[:,i] = np.copy(IC_prev_avg[:,runs2plot[i]])
    
# sort values to detect 5th-95th percentile interval
IC_prev_avg.sort(axis=1)

fig = plt.figure()
ax = fig.add_subplot(111, ylabel='Moving average of the prevalent cases in IC per million capita', xlabel='Time (days)')
ax.set_xticks([0, 100, 200, 300, 400, 500])
ax.set_yticks([0, 40, 80, 120, 160, 200])

ax.fill_between(time, IC_prev_avg[:,5], IC_prev_avg[:,94], color = 'lightgray')

for i in range(len(runs2plot)):
    ax.plot(time, IC_prev_avg_2plot[:,i], linewidth=2)

ax.hlines(y=IC_capacity, xmin=0, xmax=L, lw=2, ls=':', color='black')

plt.tight_layout()

fig.savefig('figures/S5Fig_spaghetti_plot.eps')

plt.show()