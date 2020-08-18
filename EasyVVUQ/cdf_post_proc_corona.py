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

# Reload the campaign without biology
campaign = uq.Campaign(state_file = "campaign_state_CT_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
sampler = campaign._active_sampler
#output_columns = my_campaign._active_app_decoder.output_columns

# collate output
campaign.collate()
# get full dataset of data
data = campaign.get_collation_result()
#print(data.columns)

# Reload the campaign with biology
campaign_bio = uq.Campaign(state_file = "campaign_state_CT_bio_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', campaign_bio.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
sampler_bio = campaign_bio._active_sampler
#output_columns = my_campaign._active_app_decoder.output_columns

# collate output
campaign_bio.collate()
# get full dataset of data
data_bio = campaign_bio.get_collation_result()
#print(data_bio.columns)

"""
*************************
* Empirical CDF of QoIs *
*************************
"""
L = 551 
IC_capacity = 109
IC_ex_threshold = 0.05

n_runs = 1000

IC_prev_avg_max = np.zeros(n_runs,dtype='float')
IC_ex_max = np.zeros(n_runs,dtype='float')
IC_prev_avg_max_bio = np.zeros(n_runs,dtype='float')
IC_ex_max_bio = np.zeros(n_runs,dtype='float')

for i in range(n_runs):
	# without biology
    IC_prev_avg_max[i] = data.IC_prev_avg_max[i*L]
    IC_ex_max[i] = data.IC_ex_max[i*L]
    # with biology
    IC_prev_avg_max_bio[i] = data_bio.IC_prev_avg_max[i*L]
    IC_ex_max_bio[i] = data_bio.IC_ex_max[i*L]

IC_prev_avg_max.sort()
IC_ex_max.sort()
IC_prev_avg_max_bio.sort()
IC_ex_max_bio.sort()

print('Minimum value in the peak of IC patients without biology = ',min(IC_prev_avg_max))
print('Minimum value in the peak of IC patients with biology = ',min(IC_prev_avg_max_bio))

p = np.arange(start=1,stop=n_runs+1,step=1)/n_runs

alpha_DKW = 0.05
eps_DKW = np.sqrt( np.log(2/alpha_DKW) / (2*n_runs) )

for i in range(n_runs-1):
	# wihout biology
    if (IC_prev_avg_max[i]<IC_capacity) & (IC_prev_avg_max[i+1]>IC_capacity):
        print('Probability that the maximum number of IC patient is below IC capacity (without biology):',p[i])
    # with biology
    if (IC_prev_avg_max_bio[i]<IC_capacity) & (IC_prev_avg_max_bio[i+1]>IC_capacity):
        print('Probability that the maximum number of IC patient is below IC capacity (with biology):',p[i])

params = list(sampler.vary.get_keys())
bio_params = list(sampler_bio.vary.get_keys())
# Print parameters values used in the simulations
info = campaign.list_runs()
# for run in info:
#     print(run[0])
#     print(run[1]['params'])

f = plt.figure('cdfs',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='maximum of patients in IC', ylabel='P(x)')
# without biology
ax_p.step(IC_prev_avg_max,p,lw=2,color='blue', label='without biology')
ax_p.step(IC_prev_avg_max,p+eps_DKW,linestyle='--',lw=2,color='cornflowerblue')
ax_p.step(IC_prev_avg_max,p-eps_DKW,linestyle='--',lw=2,color='cornflowerblue')
# with biology
ax_p.step(IC_prev_avg_max_bio,p,lw=2,color='darkred',label='with biology')
ax_p.step(IC_prev_avg_max_bio,p+eps_DKW,linestyle='--',lw=2,color='indianred')
ax_p.step(IC_prev_avg_max_bio,p-eps_DKW,linestyle='--',lw=2,color='indianred')
# general settings
ax_p.set_xscale('log')
# ax_p.set_xticks([3e2, 1e3])
ax_p.get_xaxis().get_major_formatter().labelOnlyBase = False
ax_p.get_xaxis().set_minor_formatter(NullFormatter())

ax_e = f.add_subplot(122, xlabel='IC patient-days in excess')
# without biology
ax_e.step(IC_ex_max,p,lw=2,color='blue')
ax_e.step(IC_ex_max,p+eps_DKW,linestyle='--',lw=2,color='cornflowerblue')
ax_e.step(IC_ex_max,p-eps_DKW,linestyle='--',lw=2,color='cornflowerblue')
# with biology
ax_e.step(IC_ex_max_bio,p,lw=2,color='darkred')
ax_e.step(IC_ex_max_bio,p+eps_DKW,linestyle='--',lw=2,color='indianred')
ax_e.step(IC_ex_max_bio,p-eps_DKW,linestyle='--',lw=2,color='indianred')
# general settings
ax_e.set_xscale('log')
# ax_e.set_xticks([1e4, 6e4])
#ax_e.get_xaxis().set_major_formatter(ScalarFormatter())
ax_e.get_xaxis().get_major_formatter().labelOnlyBase = False
ax_e.get_xaxis().set_minor_formatter(NullFormatter())

ax_p.legend(loc='best')
plt.tight_layout()
f.savefig('figures/cdf_CT_MC1000.png')

plt.show()

### END OF CODE ###
