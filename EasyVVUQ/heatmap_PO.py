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
uptake = np.zeros(n_runs,dtype='float')

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
    uptake[cnt] = run[1]['params']['uptake']
    cnt += 1
#     print(run[0])
#     print(run[1]['params'])

q_uptake = np.quantile(uptake,[0, 0.25, 0.5, 0.75, 1])
# print('q_uptake=',q_uptake)

# Take slabs of data corresponding to the quartiles of uptake
pl_intervention_effect_hi_0 = []
phase_interval_0 = []
IC_prev_avg_max_0 = []
IC_ex_max_0 = []

pl_intervention_effect_hi_1 = []
phase_interval_1 = []
IC_prev_avg_max_1 = []
IC_ex_max_1 = []

pl_intervention_effect_hi_2 = []
phase_interval_2 = []
IC_prev_avg_max_2 = []
IC_ex_max_2 = []

pl_intervention_effect_hi_3 = []
phase_interval_3 = []
IC_prev_avg_max_3 = []
IC_ex_max_3 = []

for i in range(n_runs):
    if (uptake[i] > q_uptake[0]) & (uptake[i] < q_uptake[1]):
        # first quartile
        pl_intervention_effect_hi_0.append(pl_intervention_effect_hi[i])
        phase_interval_0.append(phase_interval[i])

        IC_prev_avg_max_0.append(IC_prev_avg_max[i])
        IC_ex_max_0.append(IC_ex_max[i])
    if (uptake[i] > q_uptake[1]) & (uptake[i] < q_uptake[2]):
        # second quartile
        pl_intervention_effect_hi_1.append(pl_intervention_effect_hi[i])
        phase_interval_1.append(phase_interval[i])

        IC_prev_avg_max_1.append(IC_prev_avg_max[i])
        IC_ex_max_1.append(IC_ex_max[i])
    if (uptake[i] > q_uptake[2]) & (uptake[i] < q_uptake[3]):
        # third quartile
        pl_intervention_effect_hi_2.append(pl_intervention_effect_hi[i])
        phase_interval_2.append(phase_interval[i])

        IC_prev_avg_max_2.append(IC_prev_avg_max[i])
        IC_ex_max_2.append(IC_ex_max[i])
    if (uptake[i] > q_uptake[3]) & (uptake[i] < q_uptake[4]):
        # first quartile
        pl_intervention_effect_hi_3.append(pl_intervention_effect_hi[i])
        phase_interval_3.append(phase_interval[i])

        IC_prev_avg_max_3.append(IC_prev_avg_max[i])
        IC_ex_max_3.append(IC_ex_max[i])

print(len(phase_interval_0))
print(len(phase_interval_1))
print(len(phase_interval_2))
print(len(phase_interval_3))

f = plt.figure('heatmap',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='pl_intervention_effect_hi', ylabel='phase_interval')
im_p = ax_p.scatter(x=pl_intervention_effect_hi, y=phase_interval, c=IC_prev_avg_max, cmap='plasma')
cbar_p = f.colorbar(im_p, ax=ax_p)
cbar_p.set_ticks([100, 300, 500, 700])
cbar_p.set_ticklabels(['100', '300', '500', '700'])

ax_p.set_xticks([0.2, 0.4])
ax_p.set_yticks([30, 60, 90])

ax_e = f.add_subplot(122, xlabel='pl_intervention_effect_hi')
im_e = ax_e.scatter(x=pl_intervention_effect_hi, y=phase_interval, c=IC_ex_max, cmap='plasma')
cbar_e = f.colorbar(im_e, ax=ax_e)
cbar_e.set_ticks([0, 1e4, 2e4, 3e4, 4e4])
cbar_e.set_ticklabels(['0', '10000', '20000', '30000', '40000'])

ax_e.set_xticks([0.2, 0.4])
ax_e.set_yticks([30, 60, 90])

plt.tight_layout()
f.savefig('figures/heatmap_PO_MC1000.png')

plt.show()

### END OF CODE ###
