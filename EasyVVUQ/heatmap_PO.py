"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
import os
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
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

q_phase_interval = np.quantile(phase_interval,[0, 0.25, 0.5, 0.75, 1])
# print('q_uptake=',q_uptake)

# Take slabs of data corresponding to the quartiles of uptake
pl_intervention_effect_hi_q = np.zeros((np.int(n_runs/4),4),dtype='float')
uptake_q = np.zeros((np.int(n_runs/4),4),dtype='float')
IC_prev_avg_max_q = np.zeros((np.int(n_runs/4),4),dtype='float')
IC_ex_max_q = np.zeros((np.int(n_runs/4),4),dtype='float')

cnt0 = 0; cnt1 = 0; cnt2 = 0; cnt3=0

for i in range(n_runs):
    if (phase_interval[i] >= q_phase_interval[0]) & (phase_interval[i] < q_phase_interval[1]):
        # first quartile
        pl_intervention_effect_hi_q[cnt0,0] = pl_intervention_effect_hi[i]
        uptake_q[cnt0,0] = uptake[i]

        IC_prev_avg_max_q[cnt0,0] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt0,0] = IC_ex_max[i]
        cnt0 += 1
    if (phase_interval[i] >= q_phase_interval[1]) & (phase_interval[i] < q_phase_interval[2]):
        # second quartile
        pl_intervention_effect_hi_q[cnt1,1] = pl_intervention_effect_hi[i]
        uptake_q[cnt1,1] = uptake[i]

        IC_prev_avg_max_q[cnt1,1] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt1,1] = IC_ex_max[i]
        cnt1 += 1
    if (phase_interval[i] >= q_phase_interval[2]) & (phase_interval[i] < q_phase_interval[3]):
        # third quartile
        pl_intervention_effect_hi_q[cnt2,2] = pl_intervention_effect_hi[i]
        uptake_q[cnt2,2] = uptake[i]

        IC_prev_avg_max_q[cnt2,2] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt2,2] = IC_ex_max[i]
        cnt2 += 1
    if (phase_interval[i] >= q_phase_interval[3]) & (phase_interval[i] <= q_phase_interval[4]):
        # fourth quartile
        pl_intervention_effect_hi_q[cnt3,3] = pl_intervention_effect_hi[i]
        uptake_q[cnt3,3] = uptake[i]

        IC_prev_avg_max_q[cnt3,3] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt3,3] = IC_ex_max[i]
        cnt3 += 1

"""
* Heatmap for IC_prev_avg_max
"""
f = plt.figure('heatmap_IC_prev',figsize=[12,12])
ax_0 = f.add_subplot(221, ylabel='uptake')
im_0 = ax_0.scatter(x=pl_intervention_effect_hi_q[:,0], y=uptake_q[:,0], c=IC_prev_avg_max_q[:,0], cmap='plasma', \
    vmin=min(IC_prev_avg_max_q), vmax=max(IC_prev_avg_max_q))
cbar_0 = f.colorbar(im_0, ax=ax_0)
cbar_0.set_ticks([100, 300, 500, 700])
cbar_0.set_ticklabels(['100', '300', '500', '700'])
ax_0.set_xticks([0.2, 0.4])
ax_0.set_yticks([0.5, 0.75, 1])

ax_1 = f.add_subplot(222)
im_1 = ax_1.scatter(x=pl_intervention_effect_hi_q[:,1], y=uptake_q[:,1], c=IC_prev_avg_max_q[:,1], cmap='plasma', \
    vmin=min(IC_prev_avg_max_q), vmax=max(IC_prev_avg_max_q))
cbar_1 = f.colorbar(im_1, ax=ax_1)
cbar_1.set_ticks([100, 300, 500, 700])
cbar_1.set_ticklabels(['100', '300', '500', '700'])
ax_1.set_xticks([0.2, 0.4])
ax_1.set_yticks([.5, .75, 1])

ax_2 = f.add_subplot(223, xlabel='pl_intervention_effect_hi', ylabel='uptake')
im_2 = ax_2.scatter(x=pl_intervention_effect_hi_q[:,2], y=uptake_q[:,2], c=IC_prev_avg_max_q[:,2], cmap='plasma', \
    vmin=min(IC_prev_avg_max_q), vmax=max(IC_prev_avg_max_q))
cbar_2 = f.colorbar(im_2, ax=ax_2)
cbar_2.set_ticks([100, 300, 500, 700])
cbar_2.set_ticklabels(['100', '300', '500', '700'])
ax_2.set_xticks([0.2, 0.4])
ax_2.set_yticks([.5, .75, 1])

ax_3 = f.add_subplot(224, xlabel='pl_intervention_effect_hi')
im_3 = ax_3.scatter(x=pl_intervention_effect_hi_q[:,3], y=uptake_q[:,3], c=IC_prev_avg_max_q[:,3], cmap='plasma', \
    vmin=min(IC_prev_avg_max_q), vmax=max(IC_prev_avg_max_q))
cbar_3 = f.colorbar(im_3, ax=ax_3)
cbar_3.set_ticks([100, 300, 500, 700])
cbar_3.set_ticklabels(['100', '300', '500', '700'])
ax_3.set_xticks([0.2, 0.4])
ax_3.set_yticks([.5, .75, 1])

plt.tight_layout()
f.savefig('figures/heatmap_PO_IC_prev.png')

"""
* Heatmap for IC_ex_max
"""
f = plt.figure('heatmap_IC_ex',figsize=[12,12])
ax_0 = f.add_subplot(221, ylabel='uptake')
im_0 = ax_0.scatter(x=pl_intervention_effect_hi_q[:,0], y=uptake_q[:,0], c=IC_ex_max_q[:,0], cmap='plasma', \
    vmin=min(IC_ex_max_q), vmax=max(IC_ex_max_q))
cbar_0 = f.colorbar(im_0, ax=ax_0)
cbar_0.set_ticks([0, 1e4, 2e4, 3e4, 4e4])
cbar_0.set_ticklabels(['0', '10000', '20000', '30000', '40000'])
ax_0.set_xticks([0.2, 0.4])
ax_0.set_yticks([.5, .75, 1])

ax_1 = f.add_subplot(222)
im_1 = ax_1.scatter(x=pl_intervention_effect_hi_q[:,1], y=uptake_q[:,1], c=IC_ex_max_q[:,1], cmap='plasma', \
    vmin=min(IC_ex_max_q), vmax=max(IC_ex_max_q))
cbar_1 = f.colorbar(im_1, ax=ax_1)
cbar_1.set_ticks([0, 1e4, 2e4, 3e4, 4e4])
cbar_1.set_ticklabels(['0', '10000', '20000', '30000', '40000'])
ax_1.set_xticks([0.2, 0.4])
ax_1.set_yticks([.5, .75, 1])

ax_2 = f.add_subplot(223, xlabel='pl_intervention_effect_hi', ylabel='uptake')
im_2 = ax_2.scatter(x=pl_intervention_effect_hi_q[:,2], y=uptake_q[:,2], c=IC_ex_max_q[:,2], cmap='plasma', \
    vmin=min(IC_ex_max_q), vmax=max(IC_ex_max_q))
cbar_2 = f.colorbar(im_2, ax=ax_2)
cbar_2.set_ticks([0, 1e4, 2e4, 3e4, 4e4])
cbar_2.set_ticklabels(['0', '10000', '20000', '30000', '40000'])
ax_2.set_xticks([0.2, 0.4])
ax_2.set_yticks([.5, .75, 1])

ax_3 = f.add_subplot(224, xlabel='pl_intervention_effect_hi')
im_3 = ax_3.scatter(x=pl_intervention_effect_hi_q[:,3], y=uptake_q[:,3], c=IC_ex_max_q[:,3], cmap='plasma', \
    vmin=min(IC_ex_max_q), vmax=max(IC_ex_max_q))
cbar_3 = f.colorbar(im_3, ax=ax_3)
cbar_3.set_ticks([0, 1e4, 2e4, 3e4, 4e4])
cbar_3.set_ticklabels(['0', '10000', '20000', '30000', '40000'])
ax_3.set_xticks([0.2, 0.4])
ax_3.set_yticks([.5, .75, 1])

plt.tight_layout()
f.savefig('figures/heatmap_PO_IC_ex.png')

"""
* 3D plots *
"""

f = plt.figure('heatmap',figsize=[16,6])
ax_p = f.add_subplot(121, xlabel='pl_intervention_effect_hi', ylabel='phase_interval', zlabel='uptake', projection='3d')
im_p = ax_p.scatter(xs=pl_intervention_effect_hi, ys=phase_interval, zs=uptake, c=IC_prev_avg_max, cmap='plasma')

cbar_p = f.colorbar(im_p, ax=ax_p)
cbar_p.set_ticks([0, 100, 300, 500, 700])
cbar_p.set_ticklabels(['0', '100', '300', '500', '700'])

ax_p.set_xticks([0.2, 0.4])
ax_p.set_yticks([30, 60, 90])
ax_p.set_zticks([0.5, 0.75, 1])

ax_p.xaxis.labelpad = 10
ax_p.yaxis.labelpad = 10
ax_p.zaxis.labelpad = 15

ax_p.view_init(azim=60)

ax_e = f.add_subplot(122, xlabel='pl_intervention_effect_hi', ylabel='phase_interval', zlabel='uptake', projection='3d')
im_e = ax_e.scatter(xs=pl_intervention_effect_hi, ys=phase_interval, zs=uptake, c=IC_ex_max, cmap='plasma')

cbar_e = f.colorbar(im_e, ax=ax_e)
cbar_e.set_ticks([0, 1e4, 2e4, 3e4, 4e4])
cbar_e.set_ticklabels(['0', '10000', '20000', '30000', '40000'])

ax_e.set_xticks([0.2, 0.4])
ax_e.set_yticks([30, 60, 90])
ax_e.set_zticks([0.5, 0.75, 1])

ax_e.xaxis.labelpad = 10
ax_e.yaxis.labelpad = 10
ax_e.zaxis.labelpad = 15

ax_e.view_init(azim=60)

plt.tight_layout()
f.savefig('figures/heatmap_PO_MC1000.png')

plt.show()

### END OF CODE ###
