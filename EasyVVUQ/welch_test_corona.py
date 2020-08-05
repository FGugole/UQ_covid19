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
campaign = uq.Campaign(state_file = "campaign_state_PO_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
#IL_sampler = IL_campaign._active_sampler
#output_columns = my_campaign._active_app_decoder.output_columns

# collate output
campaign.collate()
# get full dataset of data
data = campaign.get_collation_result()
#print(IL_data.columns)

# Reload the campaign with bio
bio_campaign = uq.Campaign(state_file = "campaign_state_PO_bio_MC1000.json", work_dir = "/tmp")
print('========================================================')
print('Reloaded campaign', bio_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
#bio_sampler = bio_campaign._active_sampler
#output_columns = my_campaign._active_app_decoder.output_columns

# collate output
bio_campaign.collate()
# get full dataset of data
bio_data = bio_campaign.get_collation_result()
#print(IL_bio_data.columns)

# Extract maximum values within the ensemble
L = 551 
IC_capacity = 109

n_runs = 1000

IC_prev_avg_max = np.zeros(n_runs,dtype='float')
bio_IC_prev_avg_max = np.zeros(n_runs,dtype='float')

for i in range(n_runs):
    IC_prev_avg_max[i] = data.IC_prev_avg_max[i*L]
    bio_IC_prev_avg_max[i] = bio_data.IC_prev_avg_max[i*L]

# Perform Welch's t-test to see if the difference between the two is significant
[t_stat, p_val] = stats.ttest_ind(a=IC_prev_avg_max, b=bio_IC_prev_avg_max, equal_var=False)

print('Minimum value without bio = ',min(IC_prev_avg_max))
print('Minimum value with bio = ',min(bio_IC_prev_avg_max))

print('t-statistic = ',t_stat)
print('p-value = ',p_val)

### END OF CODE
