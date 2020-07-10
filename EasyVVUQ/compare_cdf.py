"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
import os
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
plt.rcParams['figure.figsize'] = 8,6

"""
*****************
* VVUQ ANALYSES *
*****************
"""

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

###################
# Contact Tracing #
###################
# Reload the campaign
CT_campaign = uq.Campaign(state_file = "campaign_state_CT_MC100.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', CT_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
CT_campaign.collate()
# get full dataset of data
data_CT = CT_campaign.get_collation_result()

L = 551
n_runs = 100

IC_prev_avg_max_CT = np.zeros(n_runs,dtype='float')
IC_ex_max_CT = np.zeros(n_runs,dtype='float')

for i in range(n_runs):
    IC_prev_avg_max_CT[i] = data_CT.IC_prev_avg_max[i*L]
    IC_ex_max_CT[i] = data_CT.IC_ex_max[i*L]

IC_prev_avg_max_CT.sort()
IC_ex_max_CT.sort()

p = np.arange(start=1,stop=n_runs+1,step=1)/n_runs

#################################
# Load data from UQLab campaign #
#################################
QoI_UQLab_CT = pd.read_csv('../UQLab/runs_CT_MC100_updated_beta_gamma/CT_QoI.csv',delimiter=',',header=None)

IC_prev_avg_max_UQLab_CT = np.copy(QoI_UQLab_CT.iloc[:,0])
IC_ex_max_UQLab_CT = np.copy(QoI_UQLab_CT.iloc[:,1])
tot_IC_UQLab_CT = np.copy(QoI_UQLab_CT.iloc[:,2])

IC_prev_avg_max_UQLab_CT.sort()
IC_ex_max_UQLab_CT.sort()

f_CT = plt.figure('cdfs',figsize=[12,6])
ax_p = f_CT.add_subplot(121, xlabel='maximum of patients in IC', ylabel='cdf')
ax_p.step(IC_prev_avg_max_CT,p,lw=2,color='tab:blue')
ax_p.step(IC_prev_avg_max_UQLab_CT,p,lw=2,color='tab:orange') 
ax_p.set_xscale('log')

ax_e = f_CT.add_subplot(122, xlabel='IC patient-days in excess', ylabel='cdf')
ax_e.step(IC_ex_max_CT,p,lw=2,color='tab:blue',label='EasyVVUQ')
ax_e.step(IC_ex_max_UQLab_CT,p,lw=2,color='tab:orange',label='UQLab')
ax_e.set_xscale('log')
ax_e.legend(loc='best')

plt.tight_layout()
f_CT.savefig('figures/cdf_CT_MC100_comparison.png')

plt.show()

########################
# Flattening the curve #
########################
# Reload the campaign
FC_campaign = uq.Campaign(state_file = "campaign_state_FC_MC100.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', FC_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
FC_campaign.collate()
# get full dataset of data
data_FC = FC_campaign.get_collation_result()

IC_prev_avg_max_FC = np.zeros(n_runs,dtype='float')
IC_ex_max_FC = np.zeros(n_runs,dtype='float')

for i in range(n_runs):
    IC_prev_avg_max_FC[i] = data_FC.IC_prev_avg_max[i*L]
    IC_ex_max_FC[i] = data_FC.IC_ex_max[i*L]

IC_prev_avg_max_FC.sort()
IC_ex_max_FC.sort()

#################################
# Load data from UQLab campaign #
#################################
QoI_UQLab_FC = pd.read_csv('../UQLab/runs_FC_MC100/FC_QoI.csv',delimiter=',',header=None)

IC_prev_avg_max_UQLab_FC = np.copy(QoI_UQLab_FC.iloc[:,0])
IC_ex_max_UQLab_FC = np.copy(QoI_UQLab_FC.iloc[:,1])
tot_IC_UQLab_FC = np.copy(QoI_UQLab_FC.iloc[:,2])

IC_prev_avg_max_UQLab_FC.sort()
IC_ex_max_UQLab_FC.sort()

f_FC = plt.figure('cdfs',figsize=[12,6])
ax_1 = f_FC.add_subplot(121, xlabel='maximum of patients in IC', ylabel='cdf')
ax_1.step(IC_prev_avg_max_FC,p,lw=2,color='tab:blue')
ax_1.step(IC_prev_avg_max_UQLab_FC,p,lw=2,color='tab:orange') 
ax_1.set_xscale('log')

ax_2 = f_FC.add_subplot(122, xlabel='IC patient-days in excess', ylabel='cdf')
ax_2.step(IC_ex_max_FC,p,lw=2,color='tab:blue',label='EasyVVUQ')
ax_2.step(IC_ex_max_UQLab_FC,p,lw=2,color='tab:orange',label='UQLab')
ax_2.set_xscale('log')
ax_2.legend(loc='best')

plt.tight_layout()
f_FC.savefig('figures/cdf_FC_MC100_comparison.png')
