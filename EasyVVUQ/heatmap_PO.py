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
pl_intervention_effect_hi_q = np.zeros((np.int(n_runs/4),4),dtype='float')
phase_interval_q = np.zeros((np.int(n_runs/4),4),dtype='float')
IC_prev_avg_max_q = np.zeros((np.int(n_runs/4),4),dtype='float')
IC_ex_max_q = np.zeros((np.int(n_runs/4),4),dtype='float')

cnt0 = 0; cnt1 = 0; cnt2 = 0; cnt3=0

for i in range(n_runs):
    if (uptake[i] >= q_uptake[0]) & (uptake[i] < q_uptake[1]):
        # first quartile
        pl_intervention_effect_hi_q[cnt0,0] = pl_intervention_effect_hi[i]
        phase_interval_q[cnt0,0] = phase_interval[i]

        IC_prev_avg_max_q[cnt0,0] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt0,0] = IC_ex_max[i]
        cnt0 += 1
    if (uptake[i] >= q_uptake[1]) & (uptake[i] < q_uptake[2]):
        # second quartile
        pl_intervention_effect_hi_q[cnt1,1] = pl_intervention_effect_hi[i]
        phase_interval_q[cnt1,1] = phase_interval[i]

        IC_prev_avg_max_q[cnt1,1] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt1,1] = IC_ex_max[i]
        cnt1 += 1
    if (uptake[i] >= q_uptake[2]) & (uptake[i] < q_uptake[3]):
        # third quartile
        pl_intervention_effect_hi_q[cnt2,2] = pl_intervention_effect_hi[i]
        phase_interval_q[cnt2,2] = phase_interval[i]

        IC_prev_avg_max_q[cnt2,2] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt2,2] = IC_ex_max[i]
        cnt2 += 1
    if (uptake[i] >= q_uptake[3]) & (uptake[i] <= q_uptake[4]):
        # fourth quartile
        pl_intervention_effect_hi_q[cnt3,3] = pl_intervention_effect_hi[i]
        phase_interval_q[cnt3,3] = phase_interval[i]

        IC_prev_avg_max_q[cnt3,3] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt3,3] = IC_ex_max[i]
        cnt3 += 1

"""
* Heatmap for IC_prev_avg_max
"""
f = plt.figure('heatmap_IC_prev',figsize=[12,12])
ax_0 = f.add_subplot(221, xlabel='pl_intervention_effect_hi', ylabel='phase_interval')
im_0 = ax_0.scatter(x=pl_intervention_effect_hi_q[:,0], y=phase_interval_q[:,0], c=IC_prev_avg_max_q[:,0], cmap='plasma')
cbar_0 = f.colorbar(im_0, ax=ax_0)
cbar_0.set_ticks([100, 300, 500, 700])
cbar_0.set_ticklabels(['100', '300', '500', '700'])
ax_0.set_xticks([0.2, 0.4])
ax_0.set_yticks([30, 60, 90])

ax_1 = f.add_subplot(222, xlabel='pl_intervention_effect_hi', ylabel='phase_interval')
im_1 = ax_1.scatter(x=pl_intervention_effect_hi_q[:,1], y=phase_interval_q[:,1], c=IC_prev_avg_max_q[:,1], cmap='plasma')
cbar_1 = f.colorbar(im_1, ax=ax_1)
cbar_1.set_ticks([100, 300, 500, 700])
cbar_1.set_ticklabels(['100', '300', '500', '700'])
ax_1.set_xticks([0.2, 0.4])
ax_1.set_yticks([30, 60, 90])

ax_2 = f.add_subplot(223, xlabel='pl_intervention_effect_hi', ylabel='phase_interval')
im_2 = ax_2.scatter(x=pl_intervention_effect_hi_q[:,2], y=phase_interval_q[:,2], c=IC_prev_avg_max_q[:,2], cmap='plasma')
cbar_2 = f.colorbar(im_2, ax=ax_2)
cbar_2.set_ticks([100, 300, 500, 700])
cbar_2.set_ticklabels(['100', '300', '500', '700'])
ax_2.set_xticks([0.2, 0.4])
ax_2.set_yticks([30, 60, 90])

ax_3 = f.add_subplot(224, xlabel='pl_intervention_effect_hi', ylabel='phase_interval')
im_3 = ax_3.scatter(x=pl_intervention_effect_hi_q[:,3], y=phase_interval_q[:,3], c=IC_prev_avg_max_q[:,3], cmap='plasma')
cbar_3 = f.colorbar(im_3, ax=ax_3)
cbar_3.set_ticks([100, 300, 500, 700])
cbar_3.set_ticklabels(['100', '300', '500', '700'])
ax_3.set_xticks([0.2, 0.4])
ax_3.set_yticks([30, 60, 90])

plt.tight_layout()
f.savefig('figures/heatmap_PO_IC_prev.png')

# f = plt.figure('heatmap_IC_ex',figsize=[12,6])
# ax_e = f.add_subplot(122, xlabel='pl_intervention_effect_hi')
# im_e = ax_e.scatter(x=pl_intervention_effect_hi, y=phase_interval, c=IC_ex_max, cmap='plasma')
# cbar_e = f.colorbar(im_e, ax=ax_e)
# cbar_e.set_ticks([0, 1e4, 2e4, 3e4, 4e4])
# cbar_e.set_ticklabels(['0', '10000', '20000', '30000', '40000'])

# ax_e.set_xticks([0.2, 0.4])
# ax_e.set_yticks([30, 60, 90])

# plt.tight_layout()
# f.savefig('figures/heatmap_PO_MC1000.png')

plt.show()

### END OF CODE ###
