"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
import os
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import ScalarFormatter, NullFormatter
plt.rcParams.update({'font.size': 18, 'legend.fontsize': 15})
plt.rcParams['figure.figsize'] = 12,7

"""
*************
* Load data *
*************
"""
workdir = '/export/scratch1/federica/VirsimCampaigns'

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Reload the FC campaign without biology
FC_campaign = uq.Campaign(state_file = "campaign_state_FC_MC2k.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', FC_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
FC_campaign.collate()
# get full dataset of data
FC_data = FC_campaign.get_collation_result()
#print(FC_data.columns)

# get sampler and output columns from my_campaign object
FC_sampler = FC_campaign._active_sampler
FC_output_columns = FC_campaign._active_app_decoder.output_columns

# Post-processing analysis
FC_qmc_analysis = uq.analysis.QMCAnalysis(sampler=FC_sampler, qoi_cols=FC_output_columns)
FC_campaign.apply_analysis(FC_qmc_analysis)

FC_results = FC_campaign.get_last_analysis()

# Reload the CT campaign without biology
CT_campaign = uq.Campaign(state_file = "campaign_state_CT_MC2k_newdistr.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', CT_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
CT_campaign.collate()
# get full dataset of data
CT_data = CT_campaign.get_collation_result()
#print(CT_data.columns)

# get sampler and output columns from my_campaign object
CT_sampler = CT_campaign._active_sampler
CT_output_columns = CT_campaign._active_app_decoder.output_columns

# Post-processing analysis
CT_qmc_analysis = uq.analysis.QMCAnalysis(sampler=CT_sampler, qoi_cols=CT_output_columns)
CT_campaign.apply_analysis(CT_qmc_analysis)

CT_results = CT_campaign.get_last_analysis()

# Reload the IL campaign without biology
IL_campaign = uq.Campaign(state_file = "campaign_state_IL_nobio_MC2k.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', IL_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
IL_campaign.collate()
# get full dataset of data
IL_data = IL_campaign.get_collation_result()
#print(IL_data.columns)

# get sampler and output columns from my_campaign object
IL_sampler = IL_campaign._active_sampler
IL_output_columns = IL_campaign._active_app_decoder.output_columns

# Post-processing analysis
IL_qmc_analysis = uq.analysis.QMCAnalysis(sampler=IL_sampler, qoi_cols=IL_output_columns)
IL_campaign.apply_analysis(IL_qmc_analysis)

IL_results = IL_campaign.get_last_analysis()

# Reload the PO campaign without biology
PO_campaign = uq.Campaign(state_file = "campaign_state_PO_MC2k.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', PO_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
PO_campaign.collate()
# get full dataset of data
PO_data = PO_campaign.get_collation_result()
#print(PO_data.columns)

# get sampler and output columns from my_campaign object
PO_sampler = PO_campaign._active_sampler
PO_output_columns = PO_campaign._active_app_decoder.output_columns

# Post-processing analysis
PO_qmc_analysis = uq.analysis.QMCAnalysis(sampler=PO_sampler, qoi_cols=PO_output_columns)
PO_campaign.apply_analysis(PO_qmc_analysis)

PO_results = PO_campaign.get_last_analysis()

"""
***************************
* SOBOL 1st ORDER INDICES *
***************************
"""
#first order Sobol indices and parameter names
FC_params = list(FC_sampler.vary.get_keys())
CT_params = list(CT_sampler.vary.get_keys())
IL_params = list(IL_sampler.vary.get_keys())
PO_params = list(PO_sampler.vary.get_keys())

FC_sobol_idx_ICp = np.zeros((len(FC_params)), dtype='float')
FC_err_ICp = np.zeros((2,len(FC_params)), dtype='float')

CT_sobol_idx_ICp = np.zeros((len(CT_params)), dtype='float')
CT_err_ICp = np.zeros((2,len(CT_params)), dtype='float')

IL_sobol_idx_ICp = np.zeros((len(IL_params)), dtype='float')
IL_err_ICp = np.zeros((2,len(IL_params)), dtype='float')

PO_sobol_idx_ICp = np.zeros((len(PO_params)), dtype='float')
PO_err_ICp = np.zeros((2,len(PO_params)), dtype='float')

idx = 0
for param in FC_params: 
    #
    sobol_idx = FC_results.sobols_first('IC_prev_avg_max',param) 
    FC_sobol_idx_ICp[idx] = sobol_idx
    low = FC_results._get_sobols_first_conf('IC_prev_avg_max',param)[0] 
    high = FC_results._get_sobols_first_conf('IC_prev_avg_max',param)[1] 
    FC_err_ICp[:,idx] = [sobol_idx-low, high-sobol_idx]
    #
    idx += 1

idx = 0
for param in CT_params: 
    #
    sobol_idx = CT_results.sobols_first('IC_prev_avg_max',param) 
    CT_sobol_idx_ICp[idx] = sobol_idx
    low = CT_results._get_sobols_first_conf('IC_prev_avg_max',param)[0] 
    high = CT_results._get_sobols_first_conf('IC_prev_avg_max',param)[1] 
    CT_err_ICp[:,idx] = [sobol_idx-low, high-sobol_idx]
    #
    idx += 1

idx = 0
for param in IL_params: 
    #
    sobol_idx = IL_results.sobols_first('IC_prev_avg_max',param) 
    IL_sobol_idx_ICp[idx] = sobol_idx
    low = IL_results._get_sobols_first_conf('IC_prev_avg_max',param)[0] 
    high = IL_results._get_sobols_first_conf('IC_prev_avg_max',param)[1] 
    IL_err_ICp[:,idx] = [sobol_idx-low, high-sobol_idx]
    #
    idx += 1

idx = 0
for param in PO_params: 
    #
    sobol_idx = PO_results.sobols_first('IC_prev_avg_max',param) 
    PO_sobol_idx_ICp[idx] = sobol_idx
    low = PO_results._get_sobols_first_conf('IC_prev_avg_max',param)[0] 
    high = PO_results._get_sobols_first_conf('IC_prev_avg_max',param)[1] 
    PO_err_ICp[:,idx] = [sobol_idx-low, high-sobol_idx]
    #
    idx += 1

"""
* Plot * 
"""
f = plt.figure('Sobols')

ax_FC = f.add_subplot(221, title = 'FC')
ax_FC.invert_yaxis()
ax_FC.set_xlim([-.1, 1.1])

ax_FC.barh(np.arange(0, len(FC_params), 1), FC_sobol_idx_ICp, xerr=FC_err_ICp, linewidth=2, \
    color=['mediumaquamarine','lightsalmon','lightskyblue'], \
    ecolor=['teal','indianred','royalblue'], \
    height=0.6)

ax_FC.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax_FC.set_yticks(np.arange(0, len(FC_params), 1))
ax_FC.set_yticklabels(FC_params)

ax_CT = f.add_subplot(222, title = 'CT')
ax_CT.invert_yaxis()
ax_CT.set_xlim([-.1, 1.1])

ax_CT.barh(np.arange(0, len(CT_params), 1), CT_sobol_idx_ICp, xerr=CT_err_ICp, linewidth=2, \
    color=['mediumaquamarine','lightskyblue','lightsalmon','lightskyblue'], \
    ecolor=['teal','royalblue','indianred', 'royalblue'], \
    height=0.6)

ax_CT.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax_CT.set_yticks(np.arange(0, len(CT_params), 1))
ax_CT.set_yticklabels(CT_params)

ax_IL = f.add_subplot(223, title = 'IL')
ax_IL.invert_yaxis()
ax_IL.set_xlim([-.1, 1.1])

ax_IL.barh(np.arange(0, len(IL_params), 1), IL_sobol_idx_ICp, xerr=IL_err_ICp, linewidth=2, \
    color=['mediumaquamarine','lightskyblue','mediumaquamarine','mediumaquamarine', 'lightsalmon'], \
    ecolor=['teal','royalblue','teal','teal','indianred'], \
    height=0.6)

IL_labels = ['seed', 'lock_effect', 'lock_length', 'lift_length', 'uptake']

ax_IL.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax_IL.set_yticks(np.arange(0, len(IL_labels), 1))
ax_IL.set_yticklabels(IL_labels)

ax_PO = f.add_subplot(224, title = 'PO')
ax_PO.invert_yaxis()
ax_PO.set_xlim([-.1, 1.1])

ax_PO.barh(np.arange(0, len(PO_params), 1), PO_sobol_idx_ICp, xerr=PO_err_ICp, linewidth=2, \
    color=['mediumaquamarine','lightsalmon','lightskyblue','lightsalmon'], \
    ecolor=['teal','indianred','royalblue','indianred'], \
    height=0.6)

PO_labels = ['seed', 'pl_intervention_effect_hi', 'intervention_lift_interval', 'uptake']

ax_PO.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax_PO.set_yticks(np.arange(0, len(PO_labels), 1))
ax_PO.set_yticklabels(PO_labels)

plt.tight_layout()
f.savefig('figures/Sobols.pdf')

plt.show()
