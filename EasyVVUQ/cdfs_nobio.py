"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, NullFormatter
plt.rcParams.update({'font.size': 20})
plt.rcParams['figure.figsize'] = 8,6

"""
*************
* Load data *
*************
"""

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Reload the CT campaign without biology
CT_campaign = uq.Campaign(state_file = "campaign_state_CT_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', CT_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
CT_sampler = CT_campaign._active_sampler
#output_columns = my_campaign._active_app_decoder.output_columns

# collate output
CT_campaign.collate()
# get full dataset of data
CT_data = CT_campaign.get_collation_result()
#print(CT_data.columns)

# Reload the FC campaign without biology
FC_campaign = uq.Campaign(state_file = "campaign_state_FC_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', FC_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
FC_sampler = FC_campaign._active_sampler
#output_columns = my_campaign._active_app_decoder.output_columns

# collate output
FC_campaign.collate()
# get full dataset of data
FC_data = FC_campaign.get_collation_result()
#print(FC_data.columns)

# Reload the PO campaign without biology
PO_campaign = uq.Campaign(state_file = "campaign_state_PO_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', PO_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
PO_sampler = PO_campaign._active_sampler
#output_columns = my_campaign._active_app_decoder.output_columns

# collate output
PO_campaign.collate()
# get full dataset of data
PO_data = PO_campaign.get_collation_result()
#print(PO_data.columns)

"""
*************************
* Empirical CDF of QoIs *
*************************
"""
L = 551 
IC_capacity = 109
IC_ex_threshold = 0.05

n_runs = 1000

CT_IC_prev_avg_max = np.zeros(n_runs,dtype='float')
CT_IC_ex_max = np.zeros(n_runs,dtype='float')

FC_IC_prev_avg_max = np.zeros(n_runs,dtype='float')
FC_IC_ex_max = np.zeros(n_runs,dtype='float')

PO_IC_prev_avg_max = np.zeros(n_runs,dtype='float')
PO_IC_ex_max = np.zeros(n_runs,dtype='float')

for i in range(n_runs):
	# CT
    CT_IC_prev_avg_max[i] = CT_data.IC_prev_avg_max[i*L]
    CT_IC_ex_max[i] = CT_data.IC_ex_max[i*L]
    # FC
    FC_IC_prev_avg_max[i] = FC_data.IC_prev_avg_max[i*L]
    FC_IC_ex_max[i] = FC_data.IC_ex_max[i*L]
    # PO
    PO_IC_prev_avg_max[i] = PO_data.IC_prev_avg_max[i*L]
    PO_IC_ex_max[i] = PO_data.IC_ex_max[i*L]

CT_IC_prev_avg_max.sort()
CT_IC_ex_max.sort()

FC_IC_prev_avg_max.sort()
FC_IC_ex_max.sort()

PO_IC_prev_avg_max.sort()
PO_IC_ex_max.sort()

p = np.arange(start=1,stop=n_runs+1,step=1)/n_runs

"""
********
* Plot *
********
"""

f = plt.figure('cdfs',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='maximum of patients in IC', ylabel='P(x)')
# without biology
ax_p.step(CT_IC_prev_avg_max,p,lw=2,label='CT')
ax_p.step(FC_IC_prev_avg_max,p,lw=2,label='FC')
ax_p.step(PO_IC_prev_avg_max,p,lw=2,label='PO')
ax_p.axvline(x=IC_capacity,linestyle=':',color='black',label='IC capacity')
# general settings
ax_p.set_xscale('log')
# ax_p.set_xticks([3e2, 1e3])
ax_p.get_xaxis().get_major_formatter().labelOnlyBase = False
ax_p.get_xaxis().set_minor_formatter(NullFormatter())

ax_e = f.add_subplot(122, xlabel='IC patient-days in excess')
# without biology
ax_e.step(CT_IC_ex_max,p,lw=2)
ax_e.step(FC_IC_ex_max,p,lw=2)
ax_e.step(PO_IC_ex_max,p,lw=2)
# general settings
ax_e.set_xscale('log')
# ax_e.set_xticks([1e4, 6e4])
#ax_e.get_xaxis().set_major_formatter(ScalarFormatter())
ax_e.get_xaxis().get_major_formatter().labelOnlyBase = False
ax_e.get_xaxis().set_minor_formatter(NullFormatter())

ax_p.legend(loc='best')
plt.tight_layout()
f.savefig('figures/cdf_nobio_MC1000.png')

plt.show()

### END OF CODE ###
