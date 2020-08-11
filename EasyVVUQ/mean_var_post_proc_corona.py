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
campaign = uq.Campaign(state_file = "campaign_state_PO_MC1000.json", work_dir = "/tmp")
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

IC_prev_avg = np.zeros((L,n_runs), dtype='float')

for i in range(n_runs):
    IC_prev_avg[:,i] = data.IC_prev_avg[i*L:(i+1)*L]

mean_IC_prev_avg = np.mean(IC_prev_avg, axis=1)
std_IC_prev_avg = np.std(IC_prev_avg, axis=1)

CI_low = np.zeros(L, dtype='float')
CI_up = np.zeros(L, dtype='float')

for i in range(L):
    CI_low[i] = max(0, mean_IC_prev_avg[i]-1.96*std_IC_prev_avg[i])
    CI_up[i] = max(0, mean_IC_prev_avg[i]+1.96*std_IC_prev_avg[i])

t = np.arange(start=0, stop=L, step=1)

f = plt.figure('IC_prev_avg')
ax = f.add_subplot(111, xlabel='time', ylabel='IC_prev_avg')
ax.plot(t,mean_IC_prev_avg,lw=2,label='ensemble mean')
ax.plot(t,CI_low,linestyle='--',lw=2,color='tab:green',label='95% CI')
ax.plot(t,CI_up,linestyle='--',lw=2,color='tab:green')

ax.set_xticks([0, 150, 300, 450])
ax.set_yticks([0, 100, 200, 300])

ax.legend(loc='best')
plt.tight_layout()
f.savefig('figures/IC_prev_avg_PO_MC1000.png')
