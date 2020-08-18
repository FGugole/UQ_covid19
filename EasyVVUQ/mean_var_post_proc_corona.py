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
*****************
* VVUQ ANALYSES *
*****************
"""

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Reload the campaign without biology
campaign = uq.Campaign(state_file = "campaign_state_CT_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
campaign.collate()
# get full dataset of data
data = campaign.get_collation_result()
#print(data.columns)

# Reload the campaign with biology
campaign_bio = uq.Campaign(state_file = "campaign_state_CT_bio_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', campaign_bio.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
campaign_bio.collate()
# get full dataset of data
data_bio = campaign_bio.get_collation_result()
#print(data.columns)

n_runs = 1000
L = 551 
IC_capacity = 109

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
std_IC_prev_avg = np.std(IC_prev_avg, axis=1)

mean_IC_ex = np.mean(IC_ex, axis=1)
std_IC_ex = np.std(IC_ex, axis=1)
# with biology
mean_IC_prev_avg_bio = np.mean(IC_prev_avg_bio, axis=1)
std_IC_prev_avg_bio = np.std(IC_prev_avg_bio, axis=1)

mean_IC_ex_bio = np.mean(IC_ex_bio, axis=1)
std_IC_ex_bio = np.std(IC_ex_bio, axis=1)

###################
CI_low_IC_prev_avg = np.zeros(L, dtype='float')
CI_up_IC_prev_avg = np.zeros(L, dtype='float')

CI_low_IC_ex = np.zeros(L, dtype='float')
CI_up_IC_ex = np.zeros(L, dtype='float')

CI_low_IC_prev_avg_bio = np.zeros(L, dtype='float')
CI_up_IC_prev_avg_bio = np.zeros(L, dtype='float')

CI_low_IC_ex_bio = np.zeros(L, dtype='float')
CI_up_IC_ex_bio = np.zeros(L, dtype='float')

for i in range(L):
    # without biology
    CI_low_IC_prev_avg[i] = max(0, mean_IC_prev_avg[i]-1.96*std_IC_prev_avg[i])
    CI_up_IC_prev_avg[i] = max(0, mean_IC_prev_avg[i]+1.96*std_IC_prev_avg[i])

    CI_low_IC_ex[i] = max(0, mean_IC_ex[i]-1.96*std_IC_ex[i])
    CI_up_IC_ex[i] = max(0, mean_IC_ex[i]+1.96*std_IC_ex[i])
    # with biology
    CI_low_IC_prev_avg_bio[i] = max(0, mean_IC_prev_avg_bio[i]-1.96*std_IC_prev_avg_bio[i])
    CI_up_IC_prev_avg_bio[i] = max(0, mean_IC_prev_avg_bio[i]+1.96*std_IC_prev_avg_bio[i])

    CI_low_IC_ex_bio[i] = max(0, mean_IC_ex_bio[i]-1.96*std_IC_ex_bio[i])
    CI_up_IC_ex_bio[i] = max(0, mean_IC_ex_bio[i]+1.96*std_IC_ex_bio[i])

t = np.arange(start=0, stop=L, step=1)

f = plt.figure('QoI',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='time', ylabel='IC_prev_avg')
# without biology
ax_p.plot(t[15:-15], mean_IC_prev_avg[15:-15], lw=2, color='blue', label='without biology')
ax_p.plot(t[15:-15], CI_low_IC_prev_avg[15:-15], linestyle='--', lw=2, color='cornflowerblue', label='95% CI')
ax_p.plot(t[15:-15], CI_up_IC_prev_avg[15:-15], linestyle='--', lw=2, color='cornflowerblue')
# with biology
ax_p.plot(t[15:-15], mean_IC_prev_avg_bio[15:-15], lw=2, color='darkred', label='with biology')
ax_p.plot(t[15:-15], CI_low_IC_prev_avg_bio[15:-15], linestyle='--', lw=2, color='indianred', label='95% CI')
ax_p.plot(t[15:-15], CI_up_IC_prev_avg_bio[15:-15], linestyle='--', lw=2, color='indianred')
# general settings
ax_p.hlines(y=IC_capacity, xmin=15, xmax=L-15, linestyle=':', lw=2, color='tab:red', label='IC capacity')
ax_p.set_xticks([0, 150, 300, 450])
ax_p.set_yticks([0, 200, 400])
ax_p.legend(loc='best')

ax_e = f.add_subplot(122, xlabel='time', ylabel='IC_ex')
# without biology
ax_e.plot(t[15:-15], mean_IC_ex[15:-15], lw=2, color='blue')
ax_e.plot(t[15:-15], CI_low_IC_ex[15:-15], linestyle='--', lw=2, color='cornflowerblue')
ax_e.plot(t[15:-15], CI_up_IC_ex[15:-15], linestyle='--', lw=2, color='cornflowerblue')
# with biology
ax_e.plot(t[15:-15], mean_IC_ex_bio[15:-15], lw=2, color='darkred')
ax_e.plot(t[15:-15], CI_low_IC_ex_bio[15:-15], linestyle='--', lw=2, color='indianred')
ax_e.plot(t[15:-15], CI_up_IC_ex_bio[15:-15], linestyle='--', lw=2, color='indianred')
# general settings
ax_e.set_xticks([0, 150, 300, 450])
ax_e.set_yticks([0, 1e4, 2e4, 3e4])

plt.tight_layout()
f.savefig('figures/QoIs_CT_MC1000.png')

plt.show()

### END OF CODE ###
