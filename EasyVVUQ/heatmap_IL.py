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

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Reload the FC campaign without biology
workdir = '/export/scratch2/home/federica/'
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
IC_capacity = 109

lockdown_effect = data['lockdown_effect',0] 
lockdown_effect = lockdown_effect.to_numpy()

uptake = data['uptake',0] 
uptake = uptake.to_numpy()

IC_prev_avg_max = data['IC_prev_avg_max',0] 
IC_prev_avg_max = IC_prev_avg_max.to_numpy()

IC_ex_max = data['IC_ex_max',0] 
IC_ex_max = IC_ex_max.to_numpy()

# Plot
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

ax_e = f.add_subplot(122, xlabel='Effect of lockdown')
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