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
plt.rcParams['figure.figsize'] = 12,9

"""
*************
* Load data *
*************
"""
workdir = '/export/scratch2/home/federica/'

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Reload the FC campaign without biology
FC_campaign = uq.Campaign(state_file = "campaign_state_FC_nobio_1e2.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', FC_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
FC_campaign.collate()
# get full dataset of data
FC_data = FC_campaign.get_collation_result()
#print(FC_data.columns)


# Reload the CT campaign without biology
CT_campaign = uq.Campaign(state_file = "campaign_state_CT_nobio_1e2.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', CT_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
CT_campaign.collate()
# get full dataset of data
CT_data = CT_campaign.get_collation_result()
#print(CT_data.columns)


# Reload the IL campaign without biology
IL_campaign = uq.Campaign(state_file = "campaign_state_IL_nobio_1e2.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', IL_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
IL_campaign.collate()
# get full dataset of data
IL_data = IL_campaign.get_collation_result()
#print(IL_data.columns)


# Reload the PO campaign without biology
PO_campaign = uq.Campaign(state_file = "campaign_state_PO_nobio_1e2.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', PO_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
PO_campaign.collate()
# get full dataset of data
PO_data = PO_campaign.get_collation_result()
#print(PO_data.columns)

###############################################################################################

# Reload the FC campaign with biology
FC_bio_campaign = uq.Campaign(state_file = "campaign_state_FC_bio_1e2.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', FC_bio_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
FC_bio_campaign.collate()
# get full dataset of data
FC_bio_data = FC_bio_campaign.get_collation_result()
#print(FC_bio_data.columns)


# Reload the CT campaign with biology
CT_bio_campaign = uq.Campaign(state_file = "campaign_state_CT_bio_1e2.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', CT_bio_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
CT_bio_campaign.collate()
# get full dataset of data
CT_bio_data = CT_bio_campaign.get_collation_result()
#print(CT_bio_data.columns)


# Reload the IL campaign with biology
IL_bio_campaign = uq.Campaign(state_file = "campaign_state_IL_bio_1e2.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', IL_bio_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
IL_bio_campaign.collate()
# get full dataset of data
IL_bio_data = IL_bio_campaign.get_collation_result()
#print(IL_bio_data.columns)


# Reload the PO campaign with biology
PO_bio_campaign = uq.Campaign(state_file = "campaign_state_PO_bio_1e2.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', PO_bio_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
PO_bio_campaign.collate()
# get full dataset of data
PO_bio_data = PO_bio_campaign.get_collation_result()
#print(PO_bio_data.columns)

#####################################################################################################

"""
*************************
* Empirical CDF of QoIs *
*************************
"""

# without bio
FC_IC_prev_avg_max = FC_data['IC_prev_avg_max', 0] 
FC_IC_prev_avg_max = FC_IC_prev_avg_max.to_numpy()
FC_IC_ex_max = FC_data['IC_ex_max', 0] 
FC_IC_ex_max = FC_IC_ex_max.to_numpy()

CT_IC_prev_avg_max = CT_data['IC_prev_avg_max', 0] 
CT_IC_prev_avg_max = CT_IC_prev_avg_max.to_numpy()
CT_IC_ex_max = CT_data['IC_ex_max', 0] 
CT_IC_ex_max = CT_IC_ex_max.to_numpy()

IL_IC_prev_avg_max = IL_data['IC_prev_avg_max', 0] 
IL_IC_prev_avg_max = IL_IC_prev_avg_max.to_numpy()
IL_IC_ex_max = IL_data['IC_ex_max', 0] 
IL_IC_ex_max = IL_IC_ex_max.to_numpy()

PO_IC_prev_avg_max = PO_data['IC_prev_avg_max', 0] 
PO_IC_prev_avg_max = PO_IC_prev_avg_max.to_numpy()
PO_IC_ex_max = PO_data['IC_ex_max', 0] 
PO_IC_ex_max = PO_IC_ex_max.to_numpy()

# with bio
FC_IC_prev_avg_max_bio = FC_bio_data['IC_prev_avg_max', 0] 
FC_IC_prev_avg_max_bio = FC_IC_prev_avg_max_bio.to_numpy()
FC_IC_ex_max_bio = FC_bio_data['IC_ex_max', 0] 
FC_IC_ex_max_bio = FC_IC_ex_max_bio.to_numpy()

CT_IC_prev_avg_max_bio = CT_bio_data['IC_prev_avg_max', 0] 
CT_IC_prev_avg_max_bio = CT_IC_prev_avg_max_bio.to_numpy()
CT_IC_ex_max_bio = CT_bio_data['IC_ex_max', 0] 
CT_IC_ex_max_bio = CT_IC_ex_max_bio.to_numpy()

IL_IC_prev_avg_max_bio = IL_bio_data['IC_prev_avg_max', 0] 
IL_IC_prev_avg_max_bio = IL_IC_prev_avg_max_bio.to_numpy()
IL_IC_ex_max_bio = IL_bio_data['IC_ex_max', 0] 
IL_IC_ex_max_bio = IL_IC_ex_max_bio.to_numpy()

PO_IC_prev_avg_max_bio = PO_bio_data['IC_prev_avg_max', 0] 
PO_IC_prev_avg_max_bio = PO_IC_prev_avg_max_bio.to_numpy()
PO_IC_ex_max_bio = PO_bio_data['IC_ex_max', 0] 
PO_IC_ex_max_bio = PO_IC_ex_max_bio.to_numpy()

# parameters for DKW confidence interval
IC_capacity = 109

n_runs = len(FC_IC_prev_avg_max)
#print('n_runs = ', n_runs)

alpha_DKW = 0.05
eps_DKW = np.sqrt( np.log(2/alpha_DKW) / (2*n_runs) )

# Sort values in increasing order
FC_IC_prev_avg_max.sort()
FC_IC_ex_max.sort()

CT_IC_prev_avg_max.sort()
CT_IC_ex_max.sort()

IL_IC_prev_avg_max.sort()
IL_IC_ex_max.sort()

PO_IC_prev_avg_max.sort()
PO_IC_ex_max.sort()

FC_IC_prev_avg_max_bio.sort()
FC_IC_ex_max_bio.sort()

CT_IC_prev_avg_max_bio.sort()
CT_IC_ex_max_bio.sort()

IL_IC_prev_avg_max_bio.sort()
IL_IC_ex_max_bio.sort()

PO_IC_prev_avg_max_bio.sort()
PO_IC_ex_max_bio.sort()

p = np.arange(start=1,stop=n_runs+1,step=1)/n_runs

"""
********
* Plot *
********
"""

f = plt.figure('cdfs',figsize=[12,7])
ax_p_bio = f.add_subplot(221, ylabel='With biological \n uncertainties \n \n Probability')
# with biology
ax_p_bio.step(FC_IC_prev_avg_max_bio,p,lw=2,color='orchid',label='FC')
ax_p_bio.step(FC_IC_prev_avg_max_bio,p+eps_DKW,lw=1,color='plum',ls='--')
ax_p_bio.step(FC_IC_prev_avg_max_bio,p-eps_DKW,lw=1,color='plum',ls='--')
#
ax_p_bio.step(CT_IC_prev_avg_max_bio,p,lw=2,color='cornflowerblue',label='CT')
ax_p_bio.step(CT_IC_prev_avg_max_bio,p+eps_DKW,lw=1,color='lightskyblue',ls='--')
ax_p_bio.step(CT_IC_prev_avg_max_bio,p-eps_DKW,lw=1,color='lightskyblue',ls='--')
#
ax_p_bio.step(IL_IC_prev_avg_max_bio,p,lw=2,color='salmon',label='IL')
ax_p_bio.step(IL_IC_prev_avg_max_bio,p+eps_DKW,lw=1,color='lightsalmon',ls='--')
ax_p_bio.step(IL_IC_prev_avg_max_bio,p-eps_DKW,lw=1,color='lightsalmon',ls='--')
#
ax_p_bio.step(PO_IC_prev_avg_max_bio,p,lw=2,color='lightseagreen',label='PO')
ax_p_bio.step(PO_IC_prev_avg_max_bio,p+eps_DKW,lw=1,color='mediumaquamarine',ls='--')
ax_p_bio.step(PO_IC_prev_avg_max_bio,p-eps_DKW,lw=1,color='mediumaquamarine',ls='--')
#
ax_p_bio.axvline(x=IC_capacity,lw=2,linestyle=':',color='black')
# general settings
ax_p_bio.set_xscale('log')
# ax_p.set_xticks([3e2, 1e3])
ax_p_bio.get_xaxis().get_major_formatter().labelOnlyBase = False
ax_p_bio.get_xaxis().set_minor_formatter(NullFormatter())
# ax_p_bio.set_xlim([1e1, 1e3])
ax_p_bio.set_xticks([1e1, 1e2, 1e3])
ax_p_bio.set_yticks([0, 0.5, 1])

ax_e_bio = f.add_subplot(222)
# with biology
ax_e_bio.step(FC_IC_ex_max_bio,p,lw=2,color='orchid')
ax_e_bio.step(FC_IC_ex_max_bio,p+eps_DKW,lw=1,color='plum',ls='--')
ax_e_bio.step(FC_IC_ex_max_bio,p-eps_DKW,lw=1,color='plum',ls='--')
#
ax_e_bio.step(CT_IC_ex_max_bio,p,lw=2,color='cornflowerblue')
ax_e_bio.step(CT_IC_ex_max_bio,p+eps_DKW,lw=1,color='lightskyblue',ls='--')
ax_e_bio.step(CT_IC_ex_max_bio,p-eps_DKW,lw=1,color='lightskyblue',ls='--')
#
ax_e_bio.step(IL_IC_ex_max_bio,p,lw=2,color='salmon')
ax_e_bio.step(IL_IC_ex_max_bio,p+eps_DKW,lw=1,color='lightsalmon',ls='--')
ax_e_bio.step(IL_IC_ex_max_bio,p-eps_DKW,lw=1,color='lightsalmon',ls='--')
#
ax_e_bio.step(PO_IC_ex_max_bio,p,lw=2,color='lightseagreen')
ax_e_bio.step(PO_IC_ex_max_bio,p+eps_DKW,lw=1,color='mediumaquamarine',ls='--')
ax_e_bio.step(PO_IC_ex_max_bio,p-eps_DKW,lw=1,color='mediumaquamarine',ls='--')
#
# general settings
ax_e_bio.set_xscale('log')
ax_e_bio.get_xaxis().get_major_formatter().labelOnlyBase = False
ax_e_bio.get_xaxis().set_minor_formatter(NullFormatter())
ax_e_bio.set_xlim([1e1, 1e5])
ax_e_bio.set_xticks([1e1, 1e3, 1e5])
ax_e_bio.set_yticks([0, 0.5, 1])

leg = ax_p_bio.legend(loc='upper left')
leg.get_frame().set_linewidth(0.0)
leg.get_frame().set_facecolor('none')
plt.tight_layout()

ax_p = f.add_subplot(223, xlabel='Maximum of patients in IC \n per million capita', \
	ylabel='Without biological \n uncertainties \n \n Probability')
# without biology
ax_p.step(FC_IC_prev_avg_max,p,lw=2,color='orchid',label='FC')
ax_p.step(FC_IC_prev_avg_max,p+eps_DKW,lw=1,color='plum',ls='--')
ax_p.step(FC_IC_prev_avg_max,p-eps_DKW,lw=1,color='plum',ls='--')
#
ax_p.step(CT_IC_prev_avg_max,p,lw=2,color='cornflowerblue',label='CT')
ax_p.step(CT_IC_prev_avg_max,p+eps_DKW,lw=1,color='lightskyblue',ls='--')
ax_p.step(CT_IC_prev_avg_max,p-eps_DKW,lw=1,color='lightskyblue',ls='--')
#
ax_p.step(IL_IC_prev_avg_max,p,lw=2,color='salmon',label='SL')
ax_p.step(IL_IC_prev_avg_max,p+eps_DKW,lw=1,color='lightsalmon',ls='--')
ax_p.step(IL_IC_prev_avg_max,p-eps_DKW,lw=1,color='lightsalmon',ls='--')
#
ax_p.step(PO_IC_prev_avg_max,p,lw=2,color='lightseagreen',label='PO')
ax_p.step(PO_IC_prev_avg_max,p+eps_DKW,lw=1,color='mediumaquamarine',ls='--')
ax_p.step(PO_IC_prev_avg_max,p-eps_DKW,lw=1,color='mediumaquamarine',ls='--')
#
ax_p.axvline(x=IC_capacity,lw=2,linestyle=':',color='black')
# general settings
ax_p.set_xscale('log')
# ax_p.set_xticks([3e2, 1e3])
ax_p.get_xaxis().get_major_formatter().labelOnlyBase = False
ax_p.get_xaxis().set_minor_formatter(NullFormatter())
# ax_p.set_xlim([1e1, 1e3])
ax_p.set_xticks([1e1, 1e2, 1e3])
ax_p.set_yticks([0, 0.5, 1])

ax_e = f.add_subplot(224, xlabel='IC patient-days in excess \n per million capita')
# without biology
ax_e.step(FC_IC_ex_max,p,lw=2,color='orchid')
ax_e.step(FC_IC_ex_max,p+eps_DKW,lw=1,color='plum',ls='--')
ax_e.step(FC_IC_ex_max,p-eps_DKW,lw=1,color='plum',ls='--')
#
ax_e.step(CT_IC_ex_max,p,lw=2,color='cornflowerblue')
ax_e.step(CT_IC_ex_max,p+eps_DKW,lw=1,color='lightskyblue',ls='--')
ax_e.step(CT_IC_ex_max,p-eps_DKW,lw=1,color='lightskyblue',ls='--')
#
ax_e.step(IL_IC_ex_max,p,lw=2,color='salmon')
ax_e.step(IL_IC_ex_max,p+eps_DKW,lw=1,color='lightsalmon',ls='--')
ax_e.step(IL_IC_ex_max,p-eps_DKW,lw=1,color='lightsalmon',ls='--')
#
ax_e.step(PO_IC_ex_max,p,lw=2,color='lightseagreen')
ax_e.step(PO_IC_ex_max,p+eps_DKW,lw=1,color='mediumaquamarine',ls='--')
ax_e.step(PO_IC_ex_max,p-eps_DKW,lw=1,color='mediumaquamarine',ls='--')
#
# general settings
ax_e.set_xscale('log')
# ax_e.set_xticks([1e4, 6e4])
ax_e.get_xaxis().get_major_formatter().labelOnlyBase = False
ax_e.get_xaxis().set_minor_formatter(NullFormatter())
ax_e.set_xlim([1e1, 1e5])
ax_e.set_xticks([1e1, 1e3, 1e5])
ax_e.set_yticks([0, 0.5, 1])

plt.tight_layout()

f.savefig('figures/cdfs.pdf')

plt.show()

### END OF CODE ###
