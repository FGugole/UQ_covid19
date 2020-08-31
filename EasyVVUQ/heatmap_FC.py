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
my_campaign = uq.Campaign(state_file = "campaign_state_FC_MC1000.json", work_dir = "/tmp")
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

intervention_effect = np.zeros(n_runs,dtype='float')
uptake = np.zeros(n_runs,dtype='float')
IC_prev_avg_max = np.zeros(n_runs,dtype='float')
IC_ex_max = np.zeros(n_runs,dtype='float')

markers = []

for i in range(n_runs):
    IC_prev_avg_max[i] = data.IC_prev_avg_max[i*L]
    IC_ex_max[i] = data.IC_ex_max[i*L]

params = list(my_sampler.vary.get_keys())
# Save parameters values used in the simulations
cnt = 0
info = my_campaign.list_runs()
for run in info:
	intervention_effect[cnt] = run[1]['params']['intervention_effect']
	uptake[cnt] = run[1]['params']['uptake']
	cnt += 1
#     print(run[0])
#     print(run[1]['params'])

f = plt.figure('heatmap',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='intervention_effect', ylabel='uptake')
im_p = ax_p.scatter(x=intervention_effect[np.where(IC_prev_avg_max <= IC_capacity)], y=uptake[np.where(IC_prev_avg_max <= IC_capacity)], \
	c='black')
im_p = ax_p.scatter(x=intervention_effect[np.where(IC_prev_avg_max > IC_capacity)], y=uptake[np.where(IC_prev_avg_max > IC_capacity)], \
	c=IC_prev_avg_max[np.where(IC_prev_avg_max > IC_capacity)], cmap='plasma')
cbar_p = f.colorbar(im_p, ax=ax_p)
cbar_p.set_ticks([150, 250, 350, 450])
cbar_p.set_ticklabels(['150', '250', '350', '450'])

ax_p.set_xticks([0.2, 0.35, 0.5])
ax_p.set_yticks([0.6, 0.8, 1.0])

ax_e = f.add_subplot(122, xlabel='intervention_effect')
im_e = ax_e.scatter(x=intervention_effect, y=uptake, c=IC_ex_max, cmap='plasma')
cbar_e = f.colorbar(im_e, ax=ax_e)
cbar_e.set_ticks([0, 1e4, 2e4, 3e4])
cbar_e.set_ticklabels(['0', '10000', '20000', '30000'])

ax_e.set_xticks([0.2, 0.35, 0.5])
ax_e.set_yticks([0.6, 0.8, 1.0])

plt.tight_layout()
f.savefig('figures/heatmap_FC_MC1000.png')

plt.show()

### END OF CODE ###
