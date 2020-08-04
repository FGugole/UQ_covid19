"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
from scipy import stats
import os

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Reload the campaign without bio
IL_campaign = uq.Campaign(state_file = "campaign_state_IL_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', IL_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
#IL_sampler = IL_campaign._active_sampler
#output_columns = my_campaign._active_app_decoder.output_columns

# collate output
IL_campaign.collate()
# get full dataset of data
IL_data = IL_campaign.get_collation_result()
#print(IL_data.columns)

# Reload the campaign with bio
IL_bio_campaign = uq.Campaign(state_file = "campaign_state_IL_bio_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', IL_bio_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
#IL_bio_sampler = IL_bio_campaign._active_sampler
#output_columns = my_campaign._active_app_decoder.output_columns

# collate output
IL_bio_campaign.collate()
# get full dataset of data
IL_bio_data = IL_bio_campaign.get_collation_result()
#print(IL_bio_data.columns)

# Extract maximum values within the ensemble
L = 551 
IC_capacity = 109

n_runs = 1000

IL_IC_prev_avg_max = np.zeros(n_runs,dtype='float')
IL_bio_IC_prev_avg_max = np.zeros(n_runs,dtype='float')

for i in range(n_runs):
    IL_IC_prev_avg_max[i] = IL_data.IC_prev_avg_max[i*L]
    IL_bio_IC_prev_avg_max[i] = IL_bio_data.IC_prev_avg_max[i*L]

# Perform Welch's t-test to see if the difference between the two is significant
[t_stat, p_val] = stats.ttest_ind(a=IL_IC_prev_avg_max, b=IL_bio_IC_prev_avg_max, equal_var=False)

print('t-statistic = ',t_stat)
print('p-value = ',p_val)

### END OF CODE