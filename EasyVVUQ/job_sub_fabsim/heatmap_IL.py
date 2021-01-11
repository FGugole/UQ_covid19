"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, NullFormatter
plt.rcParams.update({'font.size': 18, 'legend.fontsize': 15})
plt.rcParams['figure.figsize'] = 12,7

"""
*************
* Load data *
*************
"""
workdir = '/home/federica/Desktop/VirsimCampaigns'#'/tmp'

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Reload the FC campaign without biology
campaign = uq.Campaign(state_file = "campaign_state_IL_nobio.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from campaign object
sampler = campaign._active_sampler
#output_columns = campaign._active_app_decoder.output_columns

# collate output
campaign.collate()
# get full dataset of data
data = campaign.get_collation_result()
#print(data.columns)

"""
*****************
* VVUQ ANALYSES *
*****************
"""
L = 551 
IC_capacity = 109

n_runs = 1000

lockdown_effect = np.zeros(n_runs,dtype='float')
uptake = np.zeros(n_runs,dtype='float')
IC_prev_avg_max = np.zeros(n_runs,dtype='float')
IC_ex_max = np.zeros(n_runs,dtype='float')

markers = []

for i in range(n_runs):
    IC_prev_avg_max[i] = data.IC_prev_avg_max[i*L]
    IC_ex_max[i] = data.IC_ex_max[i*L]

params = list(sampler.vary.get_keys())
# Save parameters values used in the simulations
cnt = 0
info = campaign.list_runs()
for run in info:
	lockdown_effect[cnt] = run[1]['params']['lockdown_effect']
	uptake[cnt] = run[1]['params']['uptake']
	cnt += 1
#     print(run[0])
#     print(run[1]['params'])

f = plt.figure('heatmap',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='Effect of lockdown', ylabel='Uptake by the population')
im_p = ax_p.scatter(x=lockdown_effect[np.where(IC_prev_avg_max <= IC_capacity)], y=uptake[np.where(IC_prev_avg_max <= IC_capacity)], \
	c='black')
im_p = ax_p.scatter(x=lockdown_effect[np.where(IC_prev_avg_max > IC_capacity)], y=uptake[np.where(IC_prev_avg_max > IC_capacity)], \
	c=IC_prev_avg_max[np.where(IC_prev_avg_max > IC_capacity)], cmap='plasma')
cbar_p = f.colorbar(im_p, ax=ax_p)
cbar_p.set_ticks([200, 400, 600, 800])
cbar_p.set_ticklabels(['200', '400', '600', '800'])

ax_p.set_xticks([0.1, 0.2, 0.3, 0.4])
ax_p.set_yticks([0.6, 0.8, 1.0])

ax_e = f.add_subplot(122, xlabel='Effect of intervention')
im_e = ax_e.scatter(x=lockdown_effect[np.where(IC_ex_max == 0)], y=uptake[np.where(IC_ex_max == 0)], \
	c='black')
im_e = ax_e.scatter(x=lockdown_effect[np.where(IC_ex_max > 0)], y=uptake[np.where(IC_ex_max > 0)], \
	c=IC_ex_max[np.where(IC_ex_max > 0)], cmap='plasma')
cbar_e = f.colorbar(im_e, ax=ax_e)
cbar_e.set_ticks([1e4, 2e4, 3e4, 4e4])
cbar_e.set_ticklabels(['10000', '20000', '30000', '40000'])

ax_e.set_xticks([0.1, 0.2, 0.3, 0.4])
ax_e.set_yticks([0.6, 0.8, 1.0])

plt.tight_layout()
f.savefig('figures/heatmap_IL_MC1000.png')

plt.show()

### END OF CODE ###