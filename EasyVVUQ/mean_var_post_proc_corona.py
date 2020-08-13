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

# Reload the campaign
campaign = uq.Campaign(state_file = "campaign_state_CT_bio_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
campaign.collate()
# get full dataset of data
data = campaign.get_collation_result()
#print(data.columns)

# get sampler and output columns from campaign object
# sampler = campaign._active_sampler
# output_columns = campaign._active_app_decoder.output_columns

# Post-processing analysis
# mc_analysis = uq.analysis.BasicStats(qoi_cols=output_columns)
# campaign.apply_analysis(mc_analysis)

# results = campaign.get_last_analysis()
# print(results) # returns the averall mean and not the mean-time series

n_runs = 1000
L = 551 
IC_capacity = 109

IC_prev_avg = np.zeros((L,n_runs), dtype='float')
IC_ex = np.zeros((L,n_runs), dtype='float')

for i in range(n_runs):
    IC_prev_avg[:,i] = data.IC_prev_avg[i*L:(i+1)*L]
    IC_ex[:,i] = data.IC_ex[i*L:(i+1)*L]

mean_IC_prev_avg = np.mean(IC_prev_avg, axis=1)
std_IC_prev_avg = np.std(IC_prev_avg, axis=1)

mean_IC_ex = np.mean(IC_ex, axis=1)
std_IC_ex = np.std(IC_ex, axis=1)

CI_low_IC_prev_avg = np.zeros(L, dtype='float')
CI_up_IC_prev_avg = np.zeros(L, dtype='float')

CI_low_IC_ex = np.zeros(L, dtype='float')
CI_up_IC_ex = np.zeros(L, dtype='float')

for i in range(L):
    CI_low_IC_prev_avg[i] = max(0, mean_IC_prev_avg[i]-1.96*std_IC_prev_avg[i])
    CI_up_IC_prev_avg[i] = max(0, mean_IC_prev_avg[i]+1.96*std_IC_prev_avg[i])

    CI_low_IC_ex[i] = max(0, mean_IC_ex[i]-1.96*std_IC_ex[i])
    CI_up_IC_ex[i] = max(0, mean_IC_ex[i]+1.96*std_IC_ex[i])

t = np.arange(start=0, stop=L, step=1)

f = plt.figure('QoI',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='time', ylabel='IC_prev_avg')
ax_p.plot(t[15:-15], mean_IC_prev_avg[15:-15], lw=2, label='mean')
ax_p.plot(t[15:-15], CI_low_IC_prev_avg[15:-15], linestyle='--', lw=2, color='tab:green', label='95% CI')
ax_p.plot(t[15:-15], CI_up_IC_prev_avg[15:-15], linestyle='--', lw=2, color='tab:green')
ax_p.hlines(y=IC_capacity, xmin=15, xmax=L-15, linestyle=':', lw=2, color='tab:red', label='IC capacity')

ax_p.set_xticks([0, 150, 300, 450])
ax_p.set_yticks([0, 200, 400])

ax_p.legend(loc='best')

ax_e = f.add_subplot(122, xlabel='time', ylabel='IC_ex')
ax_e.plot(t[15:-15], mean_IC_ex[15:-15], lw=2, label='mean')
ax_e.plot(t[15:-15], CI_low_IC_ex[15:-15], linestyle='--', lw=2, color='tab:green', label='95% CI')
ax_e.plot(t[15:-15], CI_up_IC_ex[15:-15], linestyle='--', lw=2, color='tab:green')

ax_e.set_xticks([0, 150, 300, 450])
ax_e.set_yticks([0, 1e4, 2e4, 3e4])

plt.tight_layout()
f.savefig('figures/QoIs_CT_bio_MC1000.png')

plt.show()

### END OF CODE ###
