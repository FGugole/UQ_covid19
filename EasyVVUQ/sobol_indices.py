"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
import os
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

# Reload the campaign
workdir = '/export/scratch2/home/federica/'
my_campaign = uq.Campaign(state_file = "campaign_state_PO_MC20.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', my_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
my_sampler = my_campaign._active_sampler

output_columns = my_campaign._active_app_decoder.output_columns

# collate output
my_campaign.collate()
# get full dataset of data
data = my_campaign.get_collation_result()
#print(data)

# Post-processing analysis
qmc_analysis = uq.analysis.QMCAnalysis(sampler=my_sampler, qoi_cols=output_columns)
my_campaign.apply_analysis(qmc_analysis)

results = my_campaign.get_last_analysis()
#print(dir(results))

"""
***************************
* SOBOL 1st ORDER INDICES *
***************************
"""
# Get parameter names
params = list(my_sampler.vary.get_keys())
#print(params)

sobol_idx_ICp = np.zeros((len(params)), dtype='float')
yerr_ICp = np.zeros((2,len(params)), dtype='float')

sobol_idx_ICe = np.zeros((len(params)), dtype='float')
yerr_ICe = np.zeros((2,len(params)), dtype='float')

idx = 0
for param in params: 
    #
    sobol_idx = results.sobols_first('IC_prev_avg_max', param)
    sobol_idx_ICp[idx] = sobol_idx
    low = results._get_sobols_first_conf('IC_prev_avg_max', param)[0]
    high = results._get_sobols_first_conf('IC_prev_avg_max', param)[1]
    yerr_ICp[:,idx] = [sobol_idx-low, high-sobol_idx]
    #
    sobol_idx = results.sobols_first('IC_ex_max', param)
    sobol_idx_ICe[idx] = sobol_idx
    low = results._get_sobols_first_conf('IC_ex_max', param)[0]
    high = results._get_sobols_first_conf('IC_ex_max', param)[1]
    yerr_ICe[:,idx] = [sobol_idx-low, high-sobol_idx]
    #
    idx += 1

    # print values to terminal
    print('Param = ', param)
    print('Sobol index for IC_prev_avg_max = ', results.sobols_first('IC_prev_avg_max', param))
    print('Sobol index for IC_ex_max = ', results.sobols_first('IC_ex_max', param))

'''
********
* Plot *
********
'''

f = plt.figure('Sobol_IC_max', figsize=[12, 6])
ax_ICp_max = f.add_subplot(121, title = 'IC_prev_avg_max')
ax_ICp_max.set_ylim([-.1, 1.1])

ax_ICe_max = f.add_subplot(122, title = 'IC_ex_max')
ax_ICe_max.set_ylim([-.1, 1.1])

ax_ICp_max.errorbar(np.arange(0, len(params), 1), sobol_idx_ICp, yerr=yerr_ICp, \
    fmt='o', elinewidth=2, color='teal')
ax_ICe_max.errorbar(np.arange(0, len(params), 1), sobol_idx_ICe, yerr=yerr_ICe, \
    fmt='o', elinewidth=2, color='teal')

ax_ICp_max.set_xticks(np.arange(0, len(params), 1))
ax_ICp_max.set_xticklabels(params, rotation=45)
ax_ICe_max.set_xticks(np.arange(0, len(params), 1))
ax_ICe_max.set_xticklabels(params, rotation=45)
#
plt.tight_layout()
f.savefig('figures/Sobols_PO.png')

plt.show()

### END OF CODE ###
