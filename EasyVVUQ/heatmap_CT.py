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
my_campaign = uq.Campaign(state_file = "campaign_state_CT_MC1000.json", work_dir = "/tmp")
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

trace_prob_E = np.zeros(n_runs,dtype='float')
trace_rate_I = np.zeros(n_runs,dtype='float')
trace_contact_reduction = np.zeros(n_runs,dtype='float')

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
    trace_prob_E[cnt] = run[1]['params']['trace_prob_E']
    trace_rate_I[cnt] = run[1]['params']['trace_rate_I']
    trace_contact_reduction[cnt] = run[1]['params']['trace_contact_reduction']
    cnt += 1
#     print(run[0])
#     print(run[1]['params'])

q_trace_rate_I = np.quantile(trace_rate_I,[0, 0.25, 0.5, 0.75, 1])
# print('q_uptake=',q_uptake)

# Take slabs of data corresponding to the quartiles of uptake
trace_prob_E_q = np.zeros((np.int(n_runs/4),4),dtype='float')
trace_contact_reduction_q = np.zeros((np.int(n_runs/4),4),dtype='float')
IC_prev_avg_max_q = np.zeros((np.int(n_runs/4),4),dtype='float')
IC_ex_max_q = np.zeros((np.int(n_runs/4),4),dtype='float')

cnt0 = 0; cnt1 = 0; cnt2 = 0; cnt3=0

for i in range(n_runs):
    if (trace_rate_I[i] >= q_trace_rate_I[0]) & (trace_rate_I[i] < q_trace_rate_I[1]):
        # first quartile
        trace_prob_E_q[cnt0,0] = trace_prob_E[i]
        trace_contact_reduction_q[cnt0,0] = trace_contact_reduction[i]

        IC_prev_avg_max_q[cnt0,0] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt0,0] = IC_ex_max[i]
        cnt0 += 1
    if (trace_rate_I[i] >= q_trace_rate_I[1]) & (trace_rate_I[i] < q_trace_rate_I[2]):
        # second quartile
        trace_prob_E_q[cnt1,1] = trace_prob_E[i]
        trace_contact_reduction_q[cnt1,1] = trace_contact_reduction[i]

        IC_prev_avg_max_q[cnt1,1] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt1,1] = IC_ex_max[i]
        cnt1 += 1
    if (trace_rate_I[i] >= q_trace_rate_I[2]) & (trace_rate_I[i] < q_trace_rate_I[3]):
        # third quartile
        trace_prob_E_q[cnt2,2] = trace_prob_E[i]
        trace_contact_reduction_q[cnt2,2] = trace_contact_reduction[i]

        IC_prev_avg_max_q[cnt2,2] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt2,2] = IC_ex_max[i]
        cnt2 += 1
    if (trace_rate_I[i] >= q_trace_rate_I[3]) & (trace_rate_I[i] <= q_trace_rate_I[4]):
        # fourth quartile
        trace_prob_E_q[cnt3,3] = trace_prob_E[i]
        trace_contact_reduction_q[cnt3,3] = trace_contact_reduction[i]

        IC_prev_avg_max_q[cnt3,3] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt3,3] = IC_ex_max[i]
        cnt3 += 1

"""
* Heatmap for IC_prev_avg_max
"""
f = plt.figure('heatmap_IC_prev',figsize=[12,12])
ax_0 = f.add_subplot(221, ylabel='trace_contact_reduction')
im_0 = ax_0.scatter(x=trace_prob_E_q[:,0], y=trace_contact_reduction_q[:,0], c=IC_prev_avg_max_q[:,0], cmap='plasma')
cbar_0 = f.colorbar(im_0, ax=ax_0)
cbar_0.set_ticks([100, 400, 700, 1000])
cbar_0.set_ticklabels(['100', '400', '700', '1000'])
ax_0.set_xticks([0, 0.4, 0.8])
ax_0.set_yticks([0.4, 0.7, 1])

ax_1 = f.add_subplot(222)
im_1 = ax_1.scatter(x=trace_prob_E_q[:,1], y=trace_contact_reduction_q[:,1], c=IC_prev_avg_max_q[:,1], cmap='plasma')
cbar_1 = f.colorbar(im_1, ax=ax_1)
cbar_1.set_ticks([100, 400, 700, 1000])
cbar_1.set_ticklabels(['100', '400', '700', '1000'])
ax_1.set_xticks([0, 0.4, 0.8])
ax_1.set_yticks([0.4, 0.7, 1])

ax_2 = f.add_subplot(223, xlabel='trace_prob_E', ylabel='trace_contact_reduction')
im_2 = ax_2.scatter(x=trace_prob_E_q[:,2], y=trace_contact_reduction_q[:,2], c=IC_prev_avg_max_q[:,2], cmap='plasma')
cbar_2 = f.colorbar(im_2, ax=ax_2)
cbar_2.set_ticks([100, 400, 700, 1000])
cbar_2.set_ticklabels(['100', '400', '700', '1000'])
ax_2.set_xticks([0, 0.4, 0.8])
ax_2.set_yticks([0.4, 0.7, 1])

ax_3 = f.add_subplot(224, xlabel='trace_prob_E')
im_3 = ax_3.scatter(x=trace_prob_E_q[:,3], y=trace_contact_reduction_q[:,3], c=IC_prev_avg_max_q[:,3], cmap='plasma')
cbar_3 = f.colorbar(im_3, ax=ax_3)
cbar_3.set_ticks([100, 400, 700, 1000])
cbar_3.set_ticklabels(['100', '400', '700', '1000'])
ax_3.set_xticks([0, 0.4, 0.8])
ax_3.set_yticks([0.4, 0.7, 1])

plt.tight_layout()
f.savefig('figures/heatmap_CT_IC_prev.png')

"""
* Heatmap for IC_ex_max
"""
f = plt.figure('heatmap_IC_ex',figsize=[12,12])
ax_0 = f.add_subplot(221, ylabel='trace_contact_reduction')
im_0 = ax_0.scatter(x=trace_prob_E_q[:,0], y=trace_contact_reduction_q[:,0], c=IC_ex_max_q[:,0], cmap='plasma')
cbar_0 = f.colorbar(im_0, ax=ax_0)
cbar_0.set_ticks([0, 2e4, 4e4, 6e4])
cbar_0.set_ticklabels(['0', '20000', '40000', '60000'])
ax_0.set_xticks([0, 0.4, 0.8])
ax_0.set_yticks([0.4, 0.7, 1])

ax_1 = f.add_subplot(222)
im_1 = ax_1.scatter(x=trace_prob_E_q[:,1], y=trace_contact_reduction_q[:,1], c=IC_ex_max_q[:,1], cmap='plasma')
cbar_1 = f.colorbar(im_1, ax=ax_1)
cbar_1.set_ticks([0, 2e4, 4e4, 6e4])
cbar_1.set_ticklabels(['0', '20000', '40000', '60000'])
ax_1.set_xticks([0, 0.4, 0.8])
ax_1.set_yticks([0.4, 0.7, 1])

ax_2 = f.add_subplot(223, xlabel='trace_prob_E', ylabel='trace_contact_reduction')
im_2 = ax_2.scatter(x=trace_prob_E_q[:,2], y=trace_contact_reduction_q[:,2], c=IC_ex_max_q[:,2], cmap='plasma')
cbar_2 = f.colorbar(im_2, ax=ax_2)
cbar_2.set_ticks([0, 2e4, 4e4, 6e4])
cbar_2.set_ticklabels(['0', '20000', '40000', '60000'])
ax_2.set_xticks([0, 0.4, 0.8])
ax_2.set_yticks([0.4, 0.7, 1])

ax_3 = f.add_subplot(224, xlabel='trace_prob_E')
im_3 = ax_3.scatter(x=trace_prob_E_q[:,3], y=trace_contact_reduction_q[:,3], c=IC_ex_max_q[:,3], cmap='plasma')
cbar_3 = f.colorbar(im_3, ax=ax_3)
cbar_3.set_ticks([0, 2e4, 4e4, 6e4])
cbar_3.set_ticklabels(['0', '20000', '40000', '60000'])
ax_3.set_xticks([0, 0.4, 0.8])
ax_3.set_yticks([0.4, 0.7, 1])

plt.tight_layout()
f.savefig('figures/heatmap_CT_IC_ex.png')

"""
* 3D plots *
"""

f = plt.figure('heatmap',figsize=[16,6])
ax_p = f.add_subplot(121, xlabel='trace_prob_E', ylabel='trace_cont_red', zlabel='trace_rate_I', projection='3d')
im_p = ax_p.scatter(xs=trace_prob_E, ys=trace_contact_reduction, zs=trace_rate_I, c=IC_prev_avg_max, cmap='plasma')

cbar_p = f.colorbar(im_p, ax=ax_p)
cbar_p.set_ticks([0, 100, 400, 700, 1000])
cbar_p.set_ticklabels(['0', '100', '400', '700', '1000'])

ax_p.set_xticks([0, 0.4, 0.8])
ax_p.set_yticks([0.4, 0.7, 1])
ax_p.set_zticks([0, 2, 4])

ax_p.xaxis.labelpad = 10
ax_p.yaxis.labelpad = 10
ax_p.zaxis.labelpad = 15

# ax_p.view_init(azim=60)

ax_e = f.add_subplot(122, xlabel='trace_prob_E', ylabel='trace_cont_red', zlabel='trace_rate_I', projection='3d')
im_e = ax_e.scatter(xs=trace_prob_E, ys=trace_contact_reduction, zs=trace_rate_I, c=IC_ex_max, cmap='plasma')

cbar_e = f.colorbar(im_e, ax=ax_e)
cbar_e.set_ticks([0, 2e4, 4e4, 6e4])
cbar_e.set_ticklabels(['0', '20000', '40000', '60000'])

ax_e.set_xticks([0, 0.4, 0.8])
ax_e.set_yticks([0.4, 0.7, 1])
ax_e.set_zticks([0, 2, 4])

ax_e.xaxis.labelpad = 10
ax_e.yaxis.labelpad = 10
ax_e.zaxis.labelpad = 15

# ax_e.view_init(azim=60)

plt.tight_layout()
f.savefig('figures/heatmap_CT_MC1000.png')

plt.show()

### END OF CODE ###
