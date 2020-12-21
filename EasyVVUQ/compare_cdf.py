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

workdir = '/export/scratch2/home/federica/'
###################
# Contact Tracing #
###################
# Reload the campaign
CT_campaign = uq.Campaign(state_file = "campaign_state_CT_nobio.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', CT_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
CT_campaign.collate()
# get full dataset of data
data_CT = CT_campaign.get_collation_result()

IC_prev_avg_max_CT = data_CT['IC_prev_avg_max',0] 
IC_prev_avg_max_CT = IC_prev_avg_max_CT.to_numpy()

IC_ex_max_CT = data_CT['IC_ex_max',0] 
IC_ex_max_CT = IC_ex_max_CT.to_numpy()

n_runs = len(IC_prev_avg_max_CT)

IC_prev_avg_max_CT.sort()
IC_ex_max_CT.sort()

p = np.arange(start=1,stop=n_runs+1,step=1)/n_runs

#################################
# Load data from UQLab campaign #
#################################
QoI_UQLab_CT = pd.read_csv('../UQLab/runs_Cartesius/CT_MC3840/CT_QoI.csv',delimiter=',',header=None)

n_runs_UQLab = 3840
p_UQLab = np.arange(start=1,stop=n_runs_UQLab+1,step=1)/n_runs_UQLab

IC_prev_avg_max_UQLab_CT = np.copy(QoI_UQLab_CT.iloc[:,0])
IC_ex_max_UQLab_CT = np.copy(QoI_UQLab_CT.iloc[:,1])
tot_IC_UQLab_CT = np.copy(QoI_UQLab_CT.iloc[:,2])

IC_prev_avg_max_UQLab_CT.sort()
IC_ex_max_UQLab_CT.sort()

f_CT = plt.figure('cdfs_CT',figsize=[12,6])
ax_p = f_CT.add_subplot(121, xlabel='maximum of patients in IC', ylabel='cdf')
ax_p.step(IC_prev_avg_max_CT,p,lw=2,color='tab:blue')
ax_p.step(IC_prev_avg_max_UQLab_CT,p_UQLab,lw=2,color='tab:orange')
ax_p.set_xscale('log')
#ax_p.set_xticks([1e2, 1e3])

ax_e = f_CT.add_subplot(122, xlabel='IC patient-days in excess', ylabel='cdf')
ax_e.step(IC_ex_max_CT,p,lw=2,color='tab:blue',label='EasyVVUQ')
ax_e.step(IC_ex_max_UQLab_CT,p_UQLab,lw=2,color='tab:orange',label='UQLab')
ax_e.set_xscale('log')
ax_e.legend(loc='best')

plt.tight_layout()
f_CT.savefig('figures/cdf_CT_comparison.png')

########################
# Flattening the curve #
########################
# Reload the campaign
# FC_campaign = uq.Campaign(state_file = "campaign_state_FC_nobio.json", work_dir = workdir)
# print('========================================================')
# print('Reloaded campaign', FC_campaign.campaign_dir.split('/')[-1])
# print('========================================================')

# # collate output
# FC_campaign.collate()
# # get full dataset of data
# data_FC = FC_campaign.get_collation_result()

# IC_prev_avg_max_FC = data_FC['IC_prev_avg_max',0] 
# IC_prev_avg_max_FC = IC_prev_avg_max_FC.to_numpy()

# IC_ex_max_FC = data['IC_ex_max',0] 
# IC_ex_max_FC = IC_ex_max_FC.to_numpy()

# IC_prev_avg_max_FC.sort()
# IC_ex_max_FC.sort()

# #################################
# # Load data from UQLab campaign #
# #################################
# QoI_UQLab_FC = pd.read_csv('../UQLab/runs_FC_MC100/FC_QoI.csv',delimiter=',',header=None)

# IC_prev_avg_max_UQLab_FC = np.copy(QoI_UQLab_FC.iloc[:,0])
# IC_ex_max_UQLab_FC = np.copy(QoI_UQLab_FC.iloc[:,1])
# tot_IC_UQLab_FC = np.copy(QoI_UQLab_FC.iloc[:,2])

# IC_prev_avg_max_UQLab_FC.sort()
# IC_ex_max_UQLab_FC.sort()

# f_FC = plt.figure('cdfs_FC',figsize=[12,6])
# ax_p = f_FC.add_subplot(121, xlabel='maximum of patients in IC', ylabel='cdf')
# ax_p.step(IC_prev_avg_max_FC,p,lw=2,color='tab:blue')
# ax_p.step(IC_prev_avg_max_UQLab_FC,p,lw=2,color='tab:orange') 
# ax_p.set_xscale('log')
# ax_p.set_xticks([1e2, 1e3])

# ax_e = f_FC.add_subplot(122, xlabel='IC patient-days in excess', ylabel='cdf')
# ax_e.step(IC_ex_max_FC,p,lw=2,color='tab:blue',label='EasyVVUQ')
# ax_e.step(IC_ex_max_UQLab_FC,p,lw=2,color='tab:orange',label='UQLab')
# ax_e.set_xscale('log')
# ax_e.legend(loc='best')

# plt.tight_layout()
# f_FC.savefig('figures/cdf_FC_MC100_comparison.png')

##################
# Phased Opening #
##################
# Reload the campaign
PO_campaign = uq.Campaign(state_file = "campaign_state_PO_nobio.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', PO_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
PO_campaign.collate()
# get full dataset of data
data_PO = PO_campaign.get_collation_result()

IC_prev_avg_max_PO = data_PO['IC_prev_avg_max',0] 
IC_prev_avg_max_PO = IC_prev_avg_max_PO.to_numpy()

IC_ex_max_PO = data_PO['IC_ex_max',0] 
IC_ex_max_PO = IC_ex_max_PO.to_numpy()

IC_prev_avg_max_PO.sort()
IC_ex_max_PO.sort()

#################################
# Load data from UQLab campaign #
#################################
QoI_UQLab_PO = pd.read_csv('../UQLab/runs_Cartesius/PO_MC3840/PO3840_QoI.csv',delimiter=',',header=None)

#n_runs_UQLab = 960
p_UQLab = np.arange(start=1,stop=n_runs_UQLab+1,step=1)/n_runs_UQLab

IC_prev_avg_max_UQLab_PO = np.copy(QoI_UQLab_PO.iloc[:,0])
IC_ex_max_UQLab_PO = np.copy(QoI_UQLab_PO.iloc[:,1])
tot_IC_UQLab_PO = np.copy(QoI_UQLab_PO.iloc[:,2])

IC_prev_avg_max_UQLab_PO.sort()
IC_ex_max_UQLab_PO.sort()

f_PO = plt.figure('cdfs_PO',figsize=[12,6])
ax_p = f_PO.add_subplot(121, xlabel='maximum of patients in IC', ylabel='cdf')
ax_p.step(IC_prev_avg_max_PO,p,lw=2,color='tab:blue')
ax_p.step(IC_prev_avg_max_UQLab_PO,p_UQLab,lw=2,color='tab:orange')
ax_p.set_xscale('log')
#ax_p.set_xticks([1e2, 1e3])

ax_e = f_PO.add_subplot(122, xlabel='IC patient-days in excess', ylabel='cdf')
ax_e.step(IC_ex_max_PO,p,lw=2,color='tab:blue',label='EasyVVUQ')
ax_e.step(IC_ex_max_UQLab_PO,p_UQLab,lw=2,color='tab:orange',label='UQLab')
ax_e.set_xscale('log')
ax_e.legend(loc='best')

plt.tight_layout()
f_PO.savefig('figures/cdf_PO_comparison.png')

plt.show()

### END OF CODE ###
