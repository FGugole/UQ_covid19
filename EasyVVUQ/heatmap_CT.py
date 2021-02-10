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
workdir = '/export/scratch2/home/federica/'
campaign = uq.Campaign(state_file = "campaign_state_CT_nobio_1k.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler from my_campaign object
sampler = campaign._active_sampler

# collate output
campaign.collate()
# get full dataset of data
data = campaign.get_collation_result()
#print(data.columns)
 
IC_capacity = 109

trace_prob_E = data['trace_prob_E',0] 
trace_prob_E = trace_prob_E.to_numpy()

trace_rate_I = data['trace_rate_I',0] 
trace_rate_I = trace_rate_I.to_numpy()

trace_contact_reduction = data['trace_contact_reduction',0] 
trace_contact_reduction = trace_contact_reduction.to_numpy()

IC_prev_avg_max = data['IC_prev_avg_max',0] 
IC_prev_avg_max = IC_prev_avg_max.to_numpy()

IC_ex_max = data['IC_ex_max',0] 
IC_ex_max = IC_ex_max.to_numpy()

n_runs = len(IC_ex_max)
#print('n_runs = ', n_runs)

q_trace_prob_E = np.quantile(trace_prob_E,[0, 0.25, 0.5, 0.75, 1])

# Take slabs of data corresponding to the quartiles of trace_prob_E
trace_rate_I_q = np.zeros((np.int(n_runs/4),4),dtype='float')
trace_contact_reduction_q = np.zeros((np.int(n_runs/4),4),dtype='float')
IC_prev_avg_max_q = np.zeros((np.int(n_runs/4),4),dtype='float')
IC_ex_max_q = np.zeros((np.int(n_runs/4),4),dtype='float')

cnt0 = 0; cnt1 = 0; cnt2 = 0; cnt3=0

for i in range(n_runs):
    if (trace_prob_E[i] >= q_trace_prob_E[0]) & (trace_prob_E[i] < q_trace_prob_E[1]):
        # first quartile
        trace_rate_I_q[cnt0,0] = trace_rate_I[i]
        trace_contact_reduction_q[cnt0,0] = trace_contact_reduction[i]

        IC_prev_avg_max_q[cnt0,0] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt0,0] = IC_ex_max[i]
        cnt0 += 1
    if (trace_prob_E[i] >= q_trace_prob_E[1]) & (trace_prob_E[i] < q_trace_prob_E[2]):
        # second quartile
        trace_rate_I_q[cnt1,1] = trace_rate_I[i]
        trace_contact_reduction_q[cnt1,1] = trace_contact_reduction[i]

        IC_prev_avg_max_q[cnt1,1] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt1,1] = IC_ex_max[i]
        cnt1 += 1
    if (trace_prob_E[i] >= q_trace_prob_E[2]) & (trace_prob_E[i] < q_trace_prob_E[3]):
        # third quartile
        trace_rate_I_q[cnt2,2] = trace_rate_I[i]
        trace_contact_reduction_q[cnt2,2] = trace_contact_reduction[i]

        IC_prev_avg_max_q[cnt2,2] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt2,2] = IC_ex_max[i]
        cnt2 += 1
    if (trace_prob_E[i] >= q_trace_prob_E[3]) & (trace_prob_E[i] <= q_trace_prob_E[4]):
        # fourth quartile
        trace_rate_I_q[cnt3,3] = trace_rate_I[i]
        trace_contact_reduction_q[cnt3,3] = trace_contact_reduction[i]

        IC_prev_avg_max_q[cnt3,3] = IC_prev_avg_max[i]
        IC_ex_max_q[cnt3,3] = IC_ex_max[i]
        cnt3 += 1

"""
* Heatmap for IC_prev_avg_max
"""
f = plt.figure('heatmap_IC_prev',figsize=[12,12])
ax_0 = f.add_subplot(221, ylabel='Contact reduction \n of traced individuals')
im_0 = ax_0.scatter(x=trace_rate_I_q[np.where(IC_prev_avg_max_q[:,0] <= IC_capacity),0], \
    y=trace_contact_reduction_q[np.where(IC_prev_avg_max_q[:,0] <= IC_capacity),0], c='black')
im_0 = ax_0.scatter(x=trace_rate_I_q[np.where(IC_prev_avg_max_q[:,0] > IC_capacity),0], \
    y=trace_contact_reduction_q[np.where(IC_prev_avg_max_q[:,0] > IC_capacity),0], \
    c=IC_prev_avg_max_q[np.where(IC_prev_avg_max_q[:,0] > IC_capacity),0], cmap='plasma', \
    vmin=np.min(IC_prev_avg_max[np.where(IC_prev_avg_max > IC_capacity)]), vmax=np.max(IC_prev_avg_max))
cbar_0 = f.colorbar(im_0, ax=ax_0)
cbar_0.set_ticks([200, 600, 1000])
cbar_0.set_ticklabels(['200', '600', '1000'])
ax_0.set_xticks([0, 1, 2, 3])
ax_0.set_yticks([0.4, 0.6, 0.8, 1])

ax_1 = f.add_subplot(222)
im_1 = ax_1.scatter(x=trace_rate_I_q[np.where(IC_prev_avg_max_q[:,1] <= IC_capacity),1], \
    y=trace_contact_reduction_q[np.where(IC_prev_avg_max_q[:,1] <= IC_capacity),1], c='black')
im_1 = ax_1.scatter(x=trace_rate_I_q[np.where(IC_prev_avg_max_q[:,1] > IC_capacity),1], \
    y=trace_contact_reduction_q[np.where(IC_prev_avg_max_q[:,1] > IC_capacity),1], \
    c=IC_prev_avg_max_q[np.where(IC_prev_avg_max_q[:,1] > IC_capacity),1], cmap='plasma', \
    vmin=np.min(IC_prev_avg_max[np.where(IC_prev_avg_max > IC_capacity)]), vmax=np.max(IC_prev_avg_max))
cbar_1 = f.colorbar(im_1, ax=ax_1)
cbar_1.set_ticks([200, 600, 1000])
cbar_1.set_ticklabels(['200', '600', '1000'])
ax_1.set_xticks([0, 1, 2, 3])
ax_1.set_yticks([0.4, 0.6, 0.8, 1])

ax_2 = f.add_subplot(223, xlabel='Rate per day of \n identified infected individuals', ylabel='Contact reduction \n of traced individuals')
im_2 = ax_2.scatter(x=trace_rate_I_q[np.where(IC_prev_avg_max_q[:,2] <= IC_capacity),2], \
    y=trace_contact_reduction_q[np.where(IC_prev_avg_max_q[:,2] <= IC_capacity),2], c='black')
im_2 = ax_2.scatter(x=trace_rate_I_q[np.where(IC_prev_avg_max_q[:,2] > IC_capacity),2], \
    y=trace_contact_reduction_q[np.where(IC_prev_avg_max_q[:,2] > IC_capacity),2], \
    c=IC_prev_avg_max_q[np.where(IC_prev_avg_max_q[:,2] > IC_capacity),2], cmap='plasma', \
    vmin=np.min(IC_prev_avg_max[np.where(IC_prev_avg_max > IC_capacity)]), vmax=np.max(IC_prev_avg_max))
cbar_2 = f.colorbar(im_2, ax=ax_2)
cbar_2.set_ticks([200, 600, 1000])
cbar_2.set_ticklabels(['200', '600', '1000'])
ax_2.set_xticks([0, 1, 2, 3])
ax_2.set_yticks([0.4, 0.6, 0.8, 1])

ax_3 = f.add_subplot(224, xlabel='Rate per day of \n identified infected individuals')
im_3 = ax_3.scatter(x=trace_rate_I_q[np.where(IC_prev_avg_max_q[:,3] <= IC_capacity),3], \
    y=trace_contact_reduction_q[np.where(IC_prev_avg_max_q[:,3] <= IC_capacity),3], c='black')
im_3 = ax_3.scatter(x=trace_rate_I_q[np.where(IC_prev_avg_max_q[:,3] > IC_capacity),3], \
    y=trace_contact_reduction_q[np.where(IC_prev_avg_max_q[:,3] > IC_capacity),3], \
    c=IC_prev_avg_max_q[np.where(IC_prev_avg_max_q[:,3] > IC_capacity),3], cmap='plasma', \
    vmin=np.min(IC_prev_avg_max[np.where(IC_prev_avg_max > IC_capacity)]), vmax=np.max(IC_prev_avg_max))
cbar_3 = f.colorbar(im_3, ax=ax_3)
cbar_3.set_ticks([200, 600, 1000])
cbar_3.set_ticklabels(['200', '600', '1000'])
ax_3.set_xticks([0, 1, 2, 3])
ax_3.set_yticks([0.4, 0.6, 0.8, 1])

plt.tight_layout()
f.savefig('figures/heatmap_CT_IC_prev.pdf')

"""
* Heatmap for IC_ex_max
"""
f = plt.figure('heatmap_IC_ex',figsize=[12,12])
ax_0 = f.add_subplot(221, ylabel='Contact reduction \n of traced individuals')
im_0 = ax_0.scatter(x=trace_rate_I_q[np.where(IC_ex_max_q[:,0] == 0),0], \
    y=trace_contact_reduction_q[np.where(IC_ex_max_q[:,0] == 0),0], c='black')
im_0 = ax_0.scatter(x=trace_rate_I_q[np.where(IC_ex_max_q[:,0] > 0),0], \
    y=trace_contact_reduction_q[np.where(IC_ex_max_q[:,0] > 0),0], \
    c=IC_ex_max_q[np.where(IC_ex_max_q[:,0] > 0),0], cmap='plasma', \
    vmin=np.min(IC_ex_max[np.where(IC_ex_max > 0)]), vmax=np.max(IC_ex_max))
cbar_0 = f.colorbar(im_0, ax=ax_0)
cbar_0.set_ticks([2e4, 4e4, 6e4])
cbar_0.set_ticklabels(['20000', '40000', '60000'])
ax_0.set_xticks([0, 2, 4])
ax_0.set_yticks([0.4, 0.6, 0.8, 1])

ax_1 = f.add_subplot(222)
im_1 = ax_1.scatter(x=trace_rate_I_q[np.where(IC_ex_max_q[:,1] == 0),1], \
    y=trace_contact_reduction_q[np.where(IC_ex_max_q[:,1] == 0),1], c='black')
im_1 = ax_1.scatter(x=trace_rate_I_q[np.where(IC_ex_max_q[:,1] > 0),1], \
    y=trace_contact_reduction_q[np.where(IC_ex_max_q[:,1] > 0),1], \
    c=IC_ex_max_q[np.where(IC_ex_max_q[:,1] > 0),1], cmap='plasma', \
    vmin=np.min(IC_ex_max[np.where(IC_ex_max > 0)]), vmax=np.max(IC_ex_max))
cbar_1 = f.colorbar(im_1, ax=ax_1)
cbar_1.set_ticks([2e4, 4e4, 6e4])
cbar_1.set_ticklabels(['20000', '40000', '60000'])
ax_1.set_xticks([0, 2, 4])
ax_1.set_yticks([0.4, 0.6, 0.8, 1])

ax_2 = f.add_subplot(223, xlabel='Rate per day of \n identified infected individuals', ylabel='Contact reduction \n of traced individuals')
im_2 = ax_2.scatter(x=trace_rate_I_q[np.where(IC_ex_max_q[:,2] == 0),2], \
    y=trace_contact_reduction_q[np.where(IC_ex_max_q[:,2] == 0),2], c='black')
im_2 = ax_2.scatter(x=trace_rate_I_q[np.where(IC_ex_max_q[:,2] > 0),2], \
    y=trace_contact_reduction_q[np.where(IC_ex_max_q[:,2] > 0),2], \
    c=IC_ex_max_q[np.where(IC_ex_max_q[:,2] > 0),2], cmap='plasma', \
    vmin=np.min(IC_ex_max[np.where(IC_ex_max > 0)]), vmax=np.max(IC_ex_max))
cbar_2 = f.colorbar(im_2, ax=ax_2)
cbar_2.set_ticks([2e4, 4e4, 6e4])
cbar_2.set_ticklabels(['20000', '40000', '60000'])
ax_2.set_xticks([0, 2, 4])
ax_2.set_yticks([0.4, 0.6, 0.8, 1])

ax_3 = f.add_subplot(224, xlabel='Rate per day of \n identified infected individuals')
im_3 = ax_3.scatter(x=trace_rate_I_q[np.where(IC_ex_max_q[:,3] == 0),3], \
    y=trace_contact_reduction_q[np.where(IC_ex_max_q[:,3] == 0),3], c='black')
im_3 = ax_3.scatter(x=trace_rate_I_q[np.where(IC_ex_max_q[:,3] > 0),3], \
    y=trace_contact_reduction_q[np.where(IC_ex_max_q[:,3] > 0),3], \
    c=IC_ex_max_q[np.where(IC_ex_max_q[:,3] > 0),3], cmap='plasma', \
    vmin=np.min(IC_ex_max[np.where(IC_ex_max > 0)]), vmax=np.max(IC_ex_max))
cbar_3 = f.colorbar(im_3, ax=ax_3)
cbar_3.set_ticks([2e4, 4e4, 6e4])
cbar_3.set_ticklabels(['20000', '40000', '60000'])
ax_3.set_xticks([0, 2, 4])
ax_3.set_yticks([0.4, 0.6, 0.8, 1])

plt.tight_layout()
f.savefig('figures/heatmap_CT_IC_ex.pdf')

"""
* 3D plots *
"""

f = plt.figure('heatmap',figsize=[16,6])
ax_p = f.add_subplot(121, xlabel='trace_prob_E', ylabel='trace_cont_red', zlabel='trace_rate_I', projection='3d')
im_p = ax_p.scatter(xs=trace_prob_E[np.where(IC_prev_avg_max <= IC_capacity)], \
    ys=trace_contact_reduction[np.where(IC_prev_avg_max <= IC_capacity)], \
    zs=trace_rate_I[np.where(IC_prev_avg_max <= IC_capacity)], c='black')
im_p = ax_p.scatter(xs=trace_prob_E[np.where(IC_prev_avg_max > IC_capacity)], \
    ys=trace_contact_reduction[np.where(IC_prev_avg_max > IC_capacity)], \
    zs=trace_rate_I[np.where(IC_prev_avg_max > IC_capacity)], \
    c=IC_prev_avg_max[np.where(IC_prev_avg_max > IC_capacity)], cmap='plasma')

cbar_p = f.colorbar(im_p, ax=ax_p)
cbar_p.set_ticks([200, 600, 1000])
cbar_p.set_ticklabels(['200', '600', '1000'])

ax_p.set_xticks([0, 0.4, 0.8])
ax_p.set_yticks([0.4, 0.7, 1])
ax_p.set_zticks([0, 2, 4])

ax_p.xaxis.labelpad = 10
ax_p.yaxis.labelpad = 10
ax_p.zaxis.labelpad = 5

ax_p.view_init(azim=-30)

ax_e = f.add_subplot(122, xlabel='trace_prob_E', ylabel='trace_cont_red', zlabel='trace_rate_I', projection='3d')
im_e = ax_e.scatter(xs=trace_prob_E[np.where(IC_ex_max == 0)], \
    ys=trace_contact_reduction[np.where(IC_ex_max == 0)], \
    zs=trace_rate_I[np.where(IC_ex_max == 0)], c='black')
im_e = ax_e.scatter(xs=trace_prob_E[np.where(IC_ex_max > 0)], \
    ys=trace_contact_reduction[np.where(IC_ex_max > 0)], \
    zs=trace_rate_I[np.where(IC_ex_max > 0)], \
    c=IC_ex_max[np.where(IC_ex_max > 0)], cmap='plasma')

cbar_e = f.colorbar(im_e, ax=ax_e)
cbar_e.set_ticks([2e4, 4e4, 6e4])
cbar_e.set_ticklabels(['20000', '40000', '60000'])

ax_e.set_xticks([0, 0.4, 0.8])
ax_e.set_yticks([0.4, 0.7, 1])
ax_e.set_zticks([0, 2, 4])

ax_e.xaxis.labelpad = 10
ax_e.yaxis.labelpad = 10
ax_e.zaxis.labelpad = 5

ax_e.view_init(azim=-30)

plt.tight_layout()
f.savefig('figures/heatmap_CT.pdf')

plt.show()

### END OF CODE ###
