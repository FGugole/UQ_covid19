"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, NullFormatter
plt.rcParams.update({'font.size': 20})
plt.rcParams['figure.figsize'] = 8,6

"""
* Load data *
"""

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Reload the campaign without biology
campaign = uq.Campaign(state_file = "campaign_state_FC_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
campaign.collate()
# get full dataset of data
data = campaign.get_collation_result()
#print(data.columns)

# Reload the campaign with biology
campaign_bio = uq.Campaign(state_file = "campaign_state_FC_bio_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', campaign_bio.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
campaign_bio.collate()
# get full dataset of data
data_bio = campaign_bio.get_collation_result()
#print(data.columns)

"""
* Collect data in matrices, compute the mean and rank them
"""

n_runs = 1000
L = 551 
IC_capacity = 109
t = np.arange(start=0, stop=L, step=1)

alpha = 0.05
n_burn = np.int(n_runs*alpha/2)

IC_prev_avg = np.zeros((L,n_runs), dtype='float')
IC_ex = np.zeros((L,n_runs), dtype='float')
IC_prev_avg_bio = np.zeros((L,n_runs), dtype='float')
IC_ex_bio = np.zeros((L,n_runs), dtype='float')

for i in range(n_runs):
    # without biology
    IC_prev_avg[:,i] = data.IC_prev_avg[i*L:(i+1)*L]
    IC_ex[:,i] = data.IC_ex[i*L:(i+1)*L]
    # with biology
    IC_prev_avg_bio[:,i] = data_bio.IC_prev_avg[i*L:(i+1)*L]
    IC_ex_bio[:,i] = data_bio.IC_ex[i*L:(i+1)*L]

# without biology
mean_IC_prev_avg = np.mean(IC_prev_avg, axis=1)

mean_IC_ex = np.mean(IC_ex, axis=1)
# with biology
mean_IC_prev_avg_bio = np.mean(IC_prev_avg_bio, axis=1)

mean_IC_ex_bio = np.mean(IC_ex_bio, axis=1)

# rank the simulation results from the smallest to the largest for each time step 
for i in range(L):
    # without biology
    IC_prev_avg[i,:].sort()
    IC_ex[i,:].sort()
    # with biology
    IC_prev_avg_bio[i,:].sort()
    IC_ex_bio[i,:].sort()

"""
* Plot *
"""
f = plt.figure('QoI',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='time', ylabel='IC_prev_avg')
# without biology
ax_p.plot(t[15:-15], mean_IC_prev_avg[15:-15], lw=2, color='blue', label='without biology')
ax_p.plot(t[15:-15], IC_prev_avg[15:-15,n_burn+1], linestyle='--', lw=2, color='cornflowerblue')
ax_p.plot(t[15:-15], IC_prev_avg[15:-15,-n_burn-1], linestyle='--', lw=2, color='cornflowerblue')
# with biology
ax_p.plot(t[15:-15], mean_IC_prev_avg_bio[15:-15], lw=2, color='darkred', label='with biology')
ax_p.plot(t[15:-15], IC_prev_avg_bio[15:-15,n_burn+1], linestyle='--', lw=2, color='indianred')
ax_p.plot(t[15:-15], IC_prev_avg_bio[15:-15,-n_burn-1], linestyle='--', lw=2, color='indianred')
# general settings
ax_p.hlines(y=IC_capacity, xmin=15, xmax=L-15, linestyle=':', lw=2, color='darkorange', label='IC capacity')
ax_p.set_xticks([0, 150, 300, 450])
ax_p.set_yticks([0, 200, 400, 600])
ax_p.set_ylim([0, 650])
ax_p.legend(loc='best')

ax_e = f.add_subplot(122, xlabel='time', ylabel='IC_ex')
# without biology
ax_e.plot(t[15:-15], mean_IC_ex[15:-15], lw=2, color='blue')
ax_e.plot(t[15:-15], IC_ex[15:-15,n_burn+1], linestyle='--', lw=2, color='cornflowerblue')
ax_e.plot(t[15:-15], IC_ex[15:-15,-n_burn-1], linestyle='--', lw=2, color='cornflowerblue')
# with biology
ax_e.plot(t[15:-15], mean_IC_ex_bio[15:-15], lw=2, color='darkred', label='with biology')
ax_e.plot(t[15:-15], IC_ex_bio[15:-15,n_burn+1], linestyle='--', lw=2, color='indianred')
ax_e.plot(t[15:-15], IC_ex_bio[15:-15,-n_burn-1], linestyle='--', lw=2, color='indianred')
# general settings
ax_e.set_xticks([0, 150, 300, 450])
ax_e.set_yticks([0, 1e4, 2e4, 3e4])

plt.tight_layout()
f.savefig('figures/QoIs_FC_MC1000_ranking.pdf')
f.savefig('figures/QoIs_FC_MC1000_ranking.png')

plt.show()

### END OF CODE ###
