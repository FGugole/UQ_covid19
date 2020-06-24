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
my_campaign = uq.Campaign(state_file = "campaign_state.json", work_dir = "/tmp")
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
sc_analysis = uq.analysis.SCAnalysis(sampler=my_sampler, qoi_cols=output_columns)
my_campaign.apply_analysis(sc_analysis)

results = my_campaign.get_last_analysis()

"""
****************
* PLOT MOMENTS *
****************
"""
mu_S = results['statistical_moments']['S']['mean']
std_S = results['statistical_moments']['S']['std']

mu_E = results['statistical_moments']['E']['mean']
std_E = results['statistical_moments']['E']['std']

mu_I = results['statistical_moments']['I']['mean']
std_I = results['statistical_moments']['I']['std']

mu_R = results['statistical_moments']['R']['mean']
std_R = results['statistical_moments']['R']['std']

mu_IC_inc = results['statistical_moments']['IC_inc']['mean']
std_IC_inc = results['statistical_moments']['IC_inc']['std']

mu_IC_prev_avg = results['statistical_moments']['IC_prev_avg']['mean']
std_IC_prev_avg = results['statistical_moments']['IC_prev_avg']['std']

mu_IC_ex = results['statistical_moments']['IC_ex']['mean']
std_IC_ex = results['statistical_moments']['IC_ex']['std']

f, axes = plt.subplots(1,4,figsize=(24,6))
ax_S = axes[0]
ax_S.plot(mu_S,'b',linewidth=2,label='mean')
ax_S.plot(mu_S+std_S,'--r',linewidth=2,label='+/- std')
ax_S.plot(mu_S-std_S,'--r',linewidth=2)
ax_S.set_title('S')
ax_S.set_xlabel('time')
ax_S.legend(loc='best')
#
ax_E = axes[1]
ax_E.plot(mu_E,'b',linewidth=2,label='mean')
ax_E.plot(mu_E+std_E,'--r',linewidth=2,label='+/- std')
ax_E.plot(mu_E-std_E,'--r',linewidth=2)
ax_E.set_title('E')
ax_E.set_xlabel('time')
ax_E.legend(loc='best')
#
ax_I = axes[2]
ax_I.plot(mu_I,'b',linewidth=2,label='mean')
ax_I.plot(mu_I+std_I,'--r',linewidth=2,label='+/- std')
ax_I.plot(mu_I-std_I,'--r',linewidth=2)
ax_I.set_title('I')
ax_I.set_xlabel('time')
ax_I.legend(loc='best')
#
ax_R = axes[3]
ax_R.plot(mu_R,'b',linewidth=2,label='mean')
ax_R.plot(mu_R+std_R,'--r',linewidth=2,label='+/- std')
ax_R.plot(mu_R-std_R,'--r',linewidth=2)
ax_R.set_title('R')
ax_R.set_xlabel('time')
ax_R.legend(loc='best')
#
plt.tight_layout()
f.savefig('SEIR.png')

f, axes = plt.subplots(1,3,figsize=(18,6))
ax0 = axes[0]
ax0.plot(mu_IC_inc,'b',linewidth=2,label='mean')
ax0.plot(mu_IC_inc+std_IC_inc,'--r',linewidth=2,label='+/- std')
ax0.plot(mu_IC_inc-std_IC_inc,'--r',linewidth=2)
ax0.set_title('IC_inc')
ax0.set_xlabel('time')
ax0.legend(loc='best')
#
ax1 = axes[1]
ax1.plot(mu_IC_prev_avg,'b',linewidth=2,label='mean')
ax1.plot(mu_IC_prev_avg+std_IC_prev_avg,'--r',linewidth=2,label='+/- std')
ax1.plot(mu_IC_prev_avg-std_IC_prev_avg,'--r',linewidth=2)
ax1.set_title('IC_prev_avg')
ax1.set_xlabel('time')
ax1.legend(loc='best')
#
ax2 = axes[2]
ax2.plot(mu_IC_ex,'b',linewidth=2,label='mean')
ax2.plot(mu_IC_ex+std_IC_ex,'--r',linewidth=2,label='+/- std')
ax2.plot(mu_IC_ex-std_IC_ex,'--r',linewidth=2)
ax2.set_title('IC_ex')
ax2.set_xlabel('time')
ax2.legend(loc='best')
#
plt.tight_layout()
f.savefig('IC.png')

"""
*****************
* SOBOL INDECES *
*****************
"""
#first order Sobol indices and parameter names
sobols = results['sobols_first']
params = list(my_sampler.vary.get_keys())

time = np.arange(0, 4*365+1, 1)
#the first part of the intervention history is common to all strategy -> not interesting
skip = 130

fig = plt.figure('Sobol_SEIR', figsize=[24, 6])
ax_S = fig.add_subplot(141, xlabel='time', title = 'S')
ax_S.set_ylim([0, 1])

ax_E = fig.add_subplot(142, xlabel='time', title = 'E')
ax_E.set_ylim([0, 1])

ax_I = fig.add_subplot(143, xlabel='time', title = 'I')
ax_I.set_ylim([0, 1])

ax_R = fig.add_subplot(144, xlabel='time', title = 'R')
ax_R.set_ylim([0, 1])

f = plt.figure('Sobol_IC', figsize=[18, 6])
ax_ICi = f.add_subplot(131, xlabel='time', title = 'IC_inc')
ax_ICi.set_ylim([0, 1])

ax_ICp = f.add_subplot(132, xlabel='time', title = 'IC_prev_avg')
ax_ICp.set_ylim([0, 1])

ax_ICe = f.add_subplot(133, xlabel='time', title = 'IC_ex')
ax_ICe.set_ylim([0, 1])

for param in params: 
    ax_S.plot(time[skip:], sobols['S'][param][skip:])
    ax_E.plot(time[skip:], sobols['E'][param][skip:], label=param)
    ax_I.plot(time[skip:], sobols['I'][param][skip:])
    ax_R.plot(time[skip:], sobols['R'][param][skip:])
    #
    ax_ICi.plot(time[skip:], sobols['IC_inc'][param][skip:], label=param)
    ax_ICp.plot(time[skip:], sobols['IC_prev_avg'][param][skip:])
    ax_ICe.plot(time[skip:], sobols['IC_ex'][param][skip:])

ax_E.legend(loc='best')
ax_ICi.legend(loc='best')
#
plt.tight_layout()
fig.savefig('Sobol_SEIR.png')
f.savefig('Sobol_IC.png')