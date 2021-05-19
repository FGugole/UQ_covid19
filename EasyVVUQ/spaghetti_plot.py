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

n_runs = 16
fig = plt.figure()
ax = fig.add_subplot(111, ylabel='Prevalent cases in IC', xlabel='Time (days)')
ax.set_xticks([0, 100, 200, 300, 400, 500])
ax.set_yticks([0, 40, 80, 120, 160, 200])
for i in range(n_runs):
    ax.plot(time,data.IC_prev.iloc[i*L:(i+1)*L].to_numpy(), lw=2, c='black')

ax.hlines(y=IC_capacity, xmin=0, xmax=L, lw=2, ls=':', color='red')

plt.tight_layout()
fig.savefig('figures/S5Fig_spaghetti_plot.eps')

plt.show()