"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
import os
#import matplotlib as mpl
#mpl.use('Agg')
#from matplotlib import ticker
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
my_campaign = uq.Campaign(state_file = "campaign_state_FC_po3_moreuptake.json", work_dir = "/tmp")
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
print(data)

# Post-processing analysis
sc_analysis = uq.analysis.SCAnalysis(sampler=my_sampler, qoi_cols=output_columns)
my_campaign.apply_analysis(sc_analysis)

results = my_campaign.get_last_analysis()

"""
*************************
* Empirical CDF of QoIs *
*************************
"""
mu_IC_prev_avg = results['statistical_moments']['IC_prev_avg']['mean']
L = len(mu_IC_prev_avg)

N_runs = 4**3

IC_prev_avg_max = np.zeros(N_runs,dtype='float')
IC_ex_max = np.zeros(N_runs,dtype='float')

for i in range(N_runs):
	IC_prev_avg_max[i] = data.IC_prev_avg_max[i*L]
	IC_ex_max[i] = data.IC_ex_max[i*L]

IC_prev_avg_max.sort()
IC_ex_max.sort()

print(IC_prev_avg_max)
print(IC_ex_max)