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
workdir = '/export/scratch2/home/federica/'
my_campaign = uq.Campaign(state_file = "campaign_state_FC_bio_1e2.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', my_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler from my_campaign object
my_sampler = my_campaign._active_sampler

# collate output
my_campaign.collate()

# get full dataset of data
data = my_campaign.get_collation_result()
#print(data.columns)

L = 551 
IC_capacity = 109

n_runs = 1000

intervention_effect = data['intervention_effect',0] 
intervention_effect = intervention_effect.to_numpy()

uptake = data['uptake',0] 
uptake = uptake.to_numpy()

IC_prev_avg_max = data['IC_prev_avg_max',0] 
IC_prev_avg_max = IC_prev_avg_max.to_numpy()

IC_ex_max = data['IC_ex_max',0] 
IC_ex_max = IC_ex_max.to_numpy()

# Plot

f = plt.figure('heatmap',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='Effect of intervention', ylabel='Uptake by the population')
im_p = ax_p.scatter(x=intervention_effect[np.where(IC_prev_avg_max <= IC_capacity)], y=uptake[np.where(IC_prev_avg_max <= IC_capacity)], \
	c='black')
im_p = ax_p.scatter(x=intervention_effect[np.where(IC_prev_avg_max > IC_capacity)], y=uptake[np.where(IC_prev_avg_max > IC_capacity)], \
	c=IC_prev_avg_max[np.where(IC_prev_avg_max > IC_capacity)], cmap='plasma')
cbar_p = f.colorbar(im_p, ax=ax_p)
cbar_p.set_ticks([150, 250, 350, 450])
cbar_p.set_ticklabels(['150', '250', '350', '450'])

ax_p.set_xticks([0.25, 0.35, 0.45])
ax_p.set_yticks([0.6, 0.8, 1.0])

ax_e = f.add_subplot(122, xlabel='Effect of intervention')
im_e = ax_e.scatter(x=intervention_effect[np.where(IC_ex_max == 0)], y=uptake[np.where(IC_ex_max == 0)], \
	c='black')
im_e = ax_e.scatter(x=intervention_effect[np.where(IC_ex_max > 0)], y=uptake[np.where(IC_ex_max > 0)], \
	c=IC_ex_max[np.where(IC_ex_max > 0)], cmap='plasma')
cbar_e = f.colorbar(im_e, ax=ax_e)
cbar_e.set_ticks([1e4, 2e4, 3e4])
cbar_e.set_ticklabels(['10000', '20000', '30000'])

ax_e.set_xticks([0.25, 0.35, 0.45])
ax_e.set_yticks([0.6, 0.8, 1.0])

plt.tight_layout()
f.savefig('figures/heatmap_FC_MC100.png')

plt.show()

### END OF CODE ###
