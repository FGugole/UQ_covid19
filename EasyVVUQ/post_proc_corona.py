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
***************
* SUBROUTINES *
***************
"""

def plot_runs(myruns):
    f, axes = plt.subplots(1,3,figsize=(18,6))
    ax0 = axes[0]
    ax1 = axes[1]
    ax2 = axes[2]
    for run in myruns:
        IC_inc = data.IC_inc[data.run_id == run]
        IC_prev_avg = data.IC_prev_avg[data.run_id == run]
        IC_ex = data.IC_ex[data.run_id == run]
        #
        ax0.plot(time,IC_inc,lw=2,label=run)
        ax1.plot(time,IC_prev_avg,lw=2,label=run)
        ax2.plot(time,IC_ex,lw=2,label=run)
        
    ax0.set_xlabel('time')
    ax1.set_xlabel('time')
    ax2.set_xlabel('time')
    ax0.set_title('IC_inc')
    ax1.set_title('IC_prev_avg')
    ax2.set_title('IC_ex')
    #ax1.legend(loc='best')
    #ax2.legend(loc='upper left', bbox_to_anchor=(1,1))
    f.savefig('figures/IC_runs.png')

"""
*****************
* VVUQ ANALYSES *
*****************
"""

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Reload the campaign
my_campaign = uq.Campaign(state_file = "campaign_state_CT_po2.json", work_dir = "/tmp")
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

sobols_all = sc_analysis.get_sobol_indices(qoi='IC_ex',typ='all')
sobols_all_IC_ex_max = sc_analysis.get_sobol_indices(qoi='IC_ex_max',typ='all')
#print(sobols_all_IC_ex_max)

#sc_analysis.plot_grid()
#print(results['sobols_first']['IC_ex_max'])
#print(results['sobols_first']['IC_prev_avg_max'])
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

######################################################################
# Define the difference between the mean and the std such that it is non-negative
muS_stdS = np.zeros(len(mu_S))
muE_stdE = np.zeros(len(mu_E))
muI_stdI = np.zeros(len(mu_I))
muR_stdR = np.zeros(len(mu_R))
#
muICi_stdICi = np.zeros(len(mu_IC_inc))
muICp_stdICp = np.zeros(len(mu_IC_prev_avg))
muICe_stdICe = np.zeros(len(mu_IC_ex))
#
for i in range(len(mu_S)):
    muS_stdS[i] = max(mu_S[i]-std_S[i],0)
    muE_stdE[i] = max(mu_E[i]-std_E[i],0)
    muI_stdI[i] = max(mu_I[i]-std_I[i],0)
    muR_stdR[i] = max(mu_R[i]-std_R[i],0)
    #
    muICi_stdICi[i] = max(mu_IC_inc[i]-std_IC_inc[i],0)
    muICp_stdICp[i] = max(mu_IC_prev_avg[i]-std_IC_prev_avg[i],0)
    muICe_stdICe[i] = max(mu_IC_ex[i]-std_IC_ex[i],0)

######################################################################
f, axes = plt.subplots(1,4,figsize=(24,6))
ax_S = axes[0]
ax_S.plot(mu_S,'b',linewidth=2,label='mean')
ax_S.plot(mu_S+std_S,'--r',linewidth=2,label='+/- std')
ax_S.plot(muS_stdS,'--r',linewidth=2)
ax_S.set_title('S')
ax_S.set_xlabel('time')
ax_S.legend(loc='best')
#
ax_E = axes[1]
ax_E.plot(mu_E,'b',linewidth=2,label='mean')
ax_E.plot(mu_E+std_E,'--r',linewidth=2,label='+/- std')
ax_E.plot(muE_stdE,'--r',linewidth=2)
ax_E.set_title('E')
ax_E.set_xlabel('time')
ax_E.legend(loc='best')
#
ax_I = axes[2]
ax_I.plot(mu_I,'b',linewidth=2,label='mean')
ax_I.plot(mu_I+std_I,'--r',linewidth=2,label='+/- std')
ax_I.plot(muI_stdI,'--r',linewidth=2)
ax_I.set_title('I')
ax_I.set_xlabel('time')
ax_I.legend(loc='best')
#
ax_R = axes[3]
ax_R.plot(mu_R,'b',linewidth=2,label='mean')
ax_R.plot(mu_R+std_R,'--r',linewidth=2,label='+/- std')
ax_R.plot(muR_stdR,'--r',linewidth=2)
ax_R.set_title('R')
ax_R.set_xlabel('time')
ax_R.legend(loc='best')
#
plt.tight_layout()
f.savefig('figures/SEIR.png')

######################################################################
f, axes = plt.subplots(1,3,figsize=(18,6))
ax0 = axes[0]
ax0.plot(mu_IC_inc,'b',linewidth=2,label='mean')
ax0.plot(mu_IC_inc+std_IC_inc,'--r',linewidth=2,label='+/- std')
ax0.plot(muICi_stdICi,'--r',linewidth=2)
ax0.set_title('IC_inc')
ax0.set_xlabel('time')
ax0.legend(loc='best')
#
ax1 = axes[1]
ax1.plot(mu_IC_prev_avg,'b',linewidth=2,label='mean')
ax1.plot(mu_IC_prev_avg+std_IC_prev_avg,'--r',linewidth=2,label='+/- std')
ax1.plot(muICp_stdICp,'--r',linewidth=2)
ax1.set_title('IC_prev_avg')
ax1.set_xlabel('time')
ax1.legend(loc='best')
#
ax2 = axes[2]
ax2.plot(mu_IC_ex,'b',linewidth=2,label='mean')
ax2.plot(mu_IC_ex+std_IC_ex,'--r',linewidth=2,label='+/- std')
ax2.plot(muICe_stdICe,'--r',linewidth=2)
ax2.set_title('IC_ex')
ax2.set_xlabel('time')
ax2.legend(loc='best')
#
plt.tight_layout()
f.savefig('figures/IC.png')

"""
***************************
* SOBOL 1st ORDER INDECES *
***************************
"""
#first order Sobol indices and parameter names
sobols = results['sobols_first']
params = list(my_sampler.vary.get_keys())
#print(params)

time = np.arange(0, 4*365+1, 1)
#the first part of the intervention history is common to all strategy -> not interesting
skip = 130

fig = plt.figure('Sobol_SEIR', figsize=[24, 6])
ax_S = fig.add_subplot(141, xlabel='time', title = 'S')
ax_S.set_ylim([-.1, 1.1])

ax_E = fig.add_subplot(142, xlabel='time', title = 'E')
ax_E.set_ylim([-.1, 1.1])

ax_I = fig.add_subplot(143, xlabel='time', title = 'I')
ax_I.set_ylim([-.1, 1.1])

ax_R = fig.add_subplot(144, xlabel='time', title = 'R')
ax_R.set_ylim([-.1, 1.1])

######################################################################
f = plt.figure('Sobol_IC', figsize=[18, 6])
ax_ICi = f.add_subplot(131, xlabel='time', title = 'IC_inc')
ax_ICi.set_ylim([-.1, 1.1])

ax_ICp = f.add_subplot(132, xlabel='time', title = 'IC_prev_avg')
ax_ICp.set_ylim([-.1, 1.1])

ax_ICe = f.add_subplot(133, xlabel='time', title = 'IC_ex')
ax_ICe.set_ylim([-.1, 1.1])

######################################################################
ff = plt.figure('Sobol_IC_max', figsize=[12, 6])
ax_ICp_max = ff.add_subplot(121, xlabel='time', title = 'IC_prev_avg_max')
ax_ICp_max.set_ylim([-.1, 1.1])

ax_ICe_max = ff.add_subplot(122, xlabel='time', title = 'IC_ex_max')
ax_ICe_max.set_ylim([-.1, 1.1])

for param in params: 
    ax_S.plot(time[skip:], sobols['S'][param][skip:], label=param)
    ax_E.plot(time[skip:], sobols['E'][param][skip:])
    ax_I.plot(time[skip:], sobols['I'][param][skip:])
    ax_R.plot(time[skip:], sobols['R'][param][skip:])
    #
    ax_ICi.plot(time[skip:], sobols['IC_inc'][param][skip:], label=param)
    ax_ICp.plot(time[skip:], sobols['IC_prev_avg'][param][skip:])
    ax_ICe.plot(time[skip:], sobols['IC_ex'][param][skip:])
    #
    ax_ICp_max.plot(time[skip:], sobols['IC_prev_avg_max'][param][skip:])
    ax_ICe_max.plot(time[skip:], sobols['IC_ex_max'][param][skip:], label=param)

ax_S.legend(loc='best')
ax_ICi.legend(loc='best')
ax_ICe_max.legend(loc='best')
#
plt.tight_layout()
fig.savefig('figures/Sobol_SEIR.png')
f.savefig('figures/Sobol_IC.png')
ff.savefig('figures/Sobol_IC_max.png')

"""
******************************
* SOBOL HIGHER ORDER INDECES *
******************************
"""
f = plt.figure('Sobol_higher_order',figsize=[18,6])
ax2 = f.add_subplot(131, xlabel='time', title='2nd order')
ax3 = f.add_subplot(132, xlabel='time', title='3rd order')
ax4 = f.add_subplot(133, xlabel='time', title='4th order')

ax2.plot(time[skip:],sobols_all[(0, 1)][skip:],label='1')
ax2.plot(time[skip:],sobols_all[(0, 2)][skip:],label='2')
ax2.plot(time[skip:],sobols_all[(0, 3)][skip:],label='3')
ax2.plot(time[skip:],sobols_all[(1, 2)][skip:],label='4')
ax2.plot(time[skip:],sobols_all[(1, 3)][skip:],label='5')
ax2.plot(time[skip:],sobols_all[(2, 3)][skip:],label='6')
#ax2.legend(loc='best')
#
ax3.plot(time[skip:],sobols_all[(0, 1, 2)][skip:])
ax3.plot(time[skip:],sobols_all[(0, 1, 3)][skip:])
ax3.plot(time[skip:],sobols_all[(0, 2, 3)][skip:])
ax3.plot(time[skip:],sobols_all[(1, 2, 3)][skip:])
#
ax4.plot(time[skip:],sobols_all[(0, 1, 2, 3)][skip:])

f.savefig('figures/Sobol_higher_order.png')
"""
************************
* PLOT INDIVIDUAL RUNS *
************************
"""

# Remember: if I used polynomial_order=p in the sampler, then it created p+1 runs
Runlist = ['Run_1','Run_2','Run_3','Run_4','Run_5','Run_6','Run_7','Run_8','Run_9','Run_10',\
'Run_11','Run_12','Run_13','Run_14','Run_15','Run_16']
Rundic = {'Run_1':0,'Run_2':1,'Run_3':2,'Run_4':3,'Run_5':4,'Run_6':5,'Run_7':6,'Run_8':7,\
'Run_9':8,'Run_10':9,'Run_11':10,'Run_12':11,'Run_13':12,'Run_14':13,'Run_15':14,'Run_16':15}

plot_runs(Runlist)

### END OF CODE ###