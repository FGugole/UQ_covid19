"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
plt.rcParams['figure.figsize'] = 8,5
import fabsim3_cmd_api as fab
"""
*****************
* VVUQ ANALYSES *
*****************
"""

config = 'virsim_IL'
script = 'virsim_IL'
machine = 'eagle_vecma'
workdir = '/ufs/federica/Desktop/VirsimCampaigns'#'/tmp'

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Reload the campaign
campaign = uq.Campaign(state_file = "campaign_state_IL.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
sampler = campaign._active_sampler
# print(type(sampler._samples))
# print(sampler._samples.shape)

output_columns = campaign._active_app_decoder.output_columns

fab.verify(config, campaign.campaign_dir, 
            campaign._active_app_decoder.target_filename, 
            machine=machine, PJ=True)

# fab.fetch_results(machine=machine)

fab.get_uq_samples(config, campaign.campaign_dir, sampler.n_samples(),
                   skip=0, machine=machine)

# collate output
campaign.collate()
# get full dataset of data
data = campaign.get_collation_result()
#print(data)

# Post-processing analysis
qmc_analysis = uq.analysis.QMCAnalysis(sampler=sampler, qoi_cols=output_columns)
#campaign.apply_analysis(qmc_analysis)
#results = campaign.get_last_analysis()
results = qmc_analysis.analyse(data, output_index=-1)
#print(results)

"""
***************************
* SOBOL 1st ORDER INDICES *
***************************
"""
#first order Sobol indices and parameter names
sobols = results['sobols_first']
params = list(sampler.vary.get_keys())
#print(params)

# time = np.arange(0, 550+1, 1)

######################################################################
sobol_idx_ICp = np.zeros((len(params)), dtype='float')
yerr_ICp = np.zeros((2,len(params)), dtype='float')

sobol_idx_ICe = np.zeros((len(params)), dtype='float')
yerr_ICe = np.zeros((2,len(params)), dtype='float')

idx = 0
for param in params: 
    #
    sobol_idx = sobols['IC_prev_avg_max'][param]#[200]
    sobol_idx_ICp[idx] = sobol_idx
    low = results['conf_sobols_first']['IC_prev_avg_max'][param]['low']#[200]
    high = results['conf_sobols_first']['IC_prev_avg_max'][param]['high']#[200]
    yerr_ICp[:,idx] = [sobol_idx-low, high-sobol_idx]
    #
    sobol_idx = sobols['IC_ex_max'][param]#[200]
    sobol_idx_ICe[idx] = sobol_idx
    low = results['conf_sobols_first']['IC_ex_max'][param]['low']#[200]
    high = results['conf_sobols_first']['IC_ex_max'][param]['high']#[200]
    yerr_ICe[:,idx] = [sobol_idx-low, high-sobol_idx]
    #
    idx += 1
    # print values to terminal
    print('Param = ',param)
    print('Sobol index for IC_prev_avg_max = ', sobols['IC_prev_avg_max'][param])#[200])
    print('95% CI lower bound = ', results['conf_sobols_first']['IC_prev_avg_max'][param]['low'])#[200])
    print('95% CI upper bound = ', results['conf_sobols_first']['IC_prev_avg_max'][param]['high'])#[200])

    print('Sobol index for IC_ex_max = ', sobols['IC_ex_max'][param])#[200])
    print('95% CI lower bound = ', results['conf_sobols_first']['IC_ex_max'][param]['low'])#[200])
    print('95% CI upper bound = ', results['conf_sobols_first']['IC_ex_max'][param]['high'])#[200])

f = plt.figure('Sobol_IC_max', figsize=[12,7])
ax_ICp_max = f.add_subplot(121, title = 'IC_prev_avg_max')
ax_ICp_max.set_ylim([-.1, 1.1])

ax_ICe_max = f.add_subplot(122, title = 'IC_ex_max')
ax_ICe_max.set_ylim([-.1, 1.1])

ax_ICp_max.errorbar(np.arange(0, len(params), 1), sobol_idx_ICp, yerr=yerr_ICp, \
    fmt='o', elinewidth=2, color='forestgreen')
ax_ICe_max.errorbar(np.arange(0, len(params), 1), sobol_idx_ICe, yerr=yerr_ICe, \
    fmt='o', elinewidth=2, color='forestgreen')

ax_ICp_max.set_xticks(np.arange(0, len(params), 1))
ax_ICp_max.set_xticklabels(params, rotation=45)
ax_ICe_max.set_xticks(np.arange(0, len(params), 1))
ax_ICe_max.set_xticklabels(params, rotation=45)
#
plt.tight_layout()
f.savefig('figures/Sobol_IC_max_IL.png')

plt.show()

### END OF CODE ###
