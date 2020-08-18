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
my_campaign = uq.Campaign(state_file = "campaign_state_PO_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', my_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
my_sampler = my_campaign._active_sampler
#output_columns = my_campaign._active_app_decoder.output_columns

# collate output
my_campaign.collate()
# get full dataset of data
data = my_campaign.get_collation_result()
#print(data.columns)

L = 551 
IC_capacity = 109

n_runs = 1000

pl_intervention_effect_hi = np.zeros(n_runs,dtype='float')
phase_interval = np.zeros(n_runs,dtype='float')
IC_prev_avg_max = np.zeros(n_runs,dtype='float')
IC_ex_max = np.zeros(n_runs,dtype='float')

for i in range(n_runs):
    IC_prev_avg_max[i] = data.IC_prev_avg_max[i*L]
    IC_ex_max[i] = data.IC_ex_max[i*L]

params = list(my_sampler.vary.get_keys())
# Save parameters values used in the simulations
cnt = 0
info = my_campaign.list_runs()
for run in info:
	pl_intervention_effect_hi[cnt] = run[1]['params']['lockdown_effect']
	phase_interval[cnt] = run[1]['params']['phase_interval']
	cnt += 1
#     print(run[0])
#     print(run[1]['params'])

f = plt.figure('heatmap',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='pl_intervention_effect_hi', ylabel='phase_interval')
im_p = ax_p.scatter(x=pl_intervention_effect_hi, y=phase_interval, c=IC_prev_avg_max, cmap='plasma')
f.colorbar(im_p, ax=ax_p)

#ax_p.set_xticks([0.2, 0.35, 0.5])
#ax_p.set_yticks([30, 50, 70])

ax_e = f.add_subplot(122, xlabel='pl_intervention_effect_hi')
im_e = ax_e.scatter(x=pl_intervention_effect_hi, y=phase_interval, c=IC_ex_max, cmap='plasma')
cbar_e = f.colorbar(im_e, ax=ax_e)
cbar_e.set_ticks([0, 1e4, 2e4, 3e4])
cbar_e.set_ticklabels(['0', '10000', '20000', '30000'])

#ax_e.set_xticks([0.2, 0.35, 0.5])
#ax_e.set_yticks([30, 50, 70])

plt.tight_layout()
f.savefig('figures/heatmap_PO_MC1000.png')

plt.show()

### END OF CODE ###
