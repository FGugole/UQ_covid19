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

# Reload the campaign
my_campaign = uq.Campaign(state_file = "campaign_state_CT_MC1000.json", work_dir = "/tmp")
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
#sc_analysis = uq.analysis.SCAnalysis(sampler=my_sampler, qoi_cols=output_columns)
#my_campaign.apply_analysis(sc_analysis)

#results = my_campaign.get_last_analysis()

"""
*************************
* Empirical CDF of QoIs *
*************************
"""
#mu_IC_prev_avg = results['statistical_moments']['IC_prev_avg']['mean']
L = 551 #len(mu_IC_prev_avg)
IC_capacity = 109
IC_ex_threshold = 0.05

n_runs = 1000

IC_prev_avg_max = np.zeros(n_runs,dtype='float')
IC_ex_max = np.zeros(n_runs,dtype='float')
tot_IC = np.zeros(n_runs,dtype='float')
IC_ex_percentage = np.zeros(n_runs,dtype='float')

for i in range(n_runs):
    IC_prev_avg_max[i] = data.IC_prev_avg_max[i*L]
    IC_ex_max[i] = data.IC_ex_max[i*L]

    tot_IC[i] = sum(data.IC_prev[i*L:(i+1)*L])
    #print(IC_ex_max[i], tot_IC[i])
    IC_ex_percentage[i] = IC_ex_max[i]/tot_IC[i]

IC_prev_avg_max.sort()
IC_ex_max.sort()
IC_ex_percentage.sort()

#print(IC_prev_avg_max)
#print(IC_ex_max)

p = np.arange(start=1,stop=n_runs+1,step=1)/n_runs

alpha_DKW = 0.05
eps_DKW = np.sqrt( np.log(2/alpha) / (2*n_runs) )

for i in range(n_runs-1):
    if (IC_prev_avg_max[i]<IC_capacity) & (IC_prev_avg_max[i+1]>IC_capacity):
        print('Probability that the maximum number of IC patient is below IC capacity:',p[i])
    if (IC_ex_percentage[i]<IC_ex_threshold) & (IC_ex_percentage[i+1]>IC_ex_threshold):
        print('Probability that the percentage of IC patient days is below 5%:',p[i])

f = plt.figure('cdfs',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='maximum of patients in IC', ylabel='cdf')
ax_p.step(IC_prev_avg_max,p,lw=2)
ax_p.step(IC_prev_avg_max,p+eps_DKW,'--',lw=2,color='tab:red')
ax_p.step(IC_prev_avg_max,p-eps_DKW,'--',lw=2,color='tab:red')
#ax_p.axvline(x=IC_capacity,color='tab:orange')

ax_e = f.add_subplot(122, xlabel='IC patient-days in excess', ylabel='cdf')
ax_e.step(IC_ex_max,p,lw=2)
ax_p.step(IC_ex_max,p+eps_DKW,'--',lw=2,color='tab:red')
ax_p.step(IC_ex_max,p-eps_DKW,'--',lw=2,color='tab:red')

plt.tight_layout()
f.savefig('figures/cdf_CT_MC1000.png')

f = plt.figure('IC_ex_percentage_cdf')
ax = f.add_subplot(111, xlabel='% of IC patient days in excess', ylabel='cdf')
ax.step(IC_ex_percentage*100,p,lw=2)
ax.axvline(x=IC_ex_threshold*100,color='tab:orange')

plt.tight_layout()
f.savefig('figures/cdf_CT_IC_ex_percentage')

#################################
# Load data from UQLab campaign #
#################################
# QoI_UQLab = pd.read_csv('../UQLab/runs_FC_MC100/FC_QoI.csv',delimiter=',',header=None)

# IC_prev_avg_max_UQLab = np.copy(QoI_UQLab.iloc[:,0])
# IC_ex_max_UQLab = np.copy(QoI_UQLab.iloc[:,1])
# tot_IC_UQLab = np.copy(QoI_UQLab.iloc[:,2])

# IC_prev_avg_max_UQLab.sort()
# IC_ex_max_UQLab.sort()

# f = plt.figure('cdfs',figsize=[12,6])
# ax_p = f.add_subplot(121, xlabel='maximum of patients in IC', ylabel='cdf')
# ax_p.step(IC_prev_avg_max,p,lw=2,color='tab:blue')
# ax_p.step(IC_prev_avg_max_UQLab,p,lw=2,color='tab:orange') 

# ax_e = f.add_subplot(122, xlabel='IC patient-days in excess', ylabel='cdf')
# ax_e.step(IC_ex_max,p,lw=2,color='tab:blue',label='EasyVVUQ')
# ax_e.step(IC_ex_max_UQLab,p,lw=2,color='tab:orange',label='UQLab')
# ax_e.legend(loc='best')

# plt.tight_layout()
# f.savefig('figures/cdf_FC_MC100_comparison.png')

plt.show()
