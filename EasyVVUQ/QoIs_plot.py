"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
import chaospy as cp
import os
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, NullFormatter
plt.rcParams.update({'font.size': 18, 'legend.fontsize': 15})
plt.rcParams['figure.figsize'] = 12,9

"""
*************
* Load data *
*************
"""
workdir = '/home/federica/Desktop/VirsimCampaigns'#'/tmp'

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Reload the PO campaign without biology
PO_campaign = uq.Campaign(state_file = "campaign_state_PO_nobio.json", work_dir = workdir)
print('========================================================')
print('Reloaded campaign', PO_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# collate output
PO_campaign.collate()
# get full dataset of data
PO_data = PO_campaign.get_collation_result()
#print(PO_data.columns)

"""
*****************
* VVUQ ANALYSES *
*****************
"""

L = 551 
time = np.arange(start=0, stop=L, step=1)

IC_capacity = 109

n_runs2plot = 4
#runs2plot = cp.DiscreteUniform(0, 999).sample(n_runs2plot)
#print(runs2plot)
runs2plot = [178, 757, 945, 827]

IC_prev_PO = np.zeros((L,n_runs2plot), dtype='float')
IC_prev_avg_PO = np.zeros((L,n_runs2plot), dtype='float')
IC_ex_PO = np.zeros((L,n_runs2plot), dtype='float')

for i in range(n_runs2plot):
	IC_prev_PO[:,i] = PO_data.IC_prev[(PO_data.index >= runs2plot[i]*L) & 
										(PO_data.index < (1+runs2plot[i])*L)]
	IC_prev_avg_PO[:,i] = PO_data.IC_prev_avg[(PO_data.index >= runs2plot[i]*L) & 
												(PO_data.index < (1+runs2plot[i])*L)]
	IC_ex_PO[:,i] = PO_data.IC_ex[(PO_data.index >= runs2plot[i]*L) & 
										(PO_data.index < (1+runs2plot[i])*L)]

# Plot
fig = plt.figure('QoIs',figsize=[14,5])

ax0 = fig.add_subplot(131, ylabel='Prevalent cases in IC', xlabel='Time (days)')
ax1 = fig.add_subplot(132, ylabel='Prevalent cases in IC \n Moving average', xlabel='Time (days)')
ax2 = fig.add_subplot(133, ylabel='IC patient-days in excess', xlabel='Time (days)')

for i in range(n_runs2plot):
	ax0.plot(time, IC_prev_PO[:,i], lw=2)
	ax1.plot(time, IC_prev_avg_PO[:,i], lw=2)
	ax2.plot(time, IC_ex_PO[:,i], lw=2)
	add circles to indicate QoIs
	# first (and last) 14 components of the array are nan
	circle_qoi1 = plt.Circle((14+np.argmax(IC_prev_avg_PO[~np.isnan(IC_prev_avg_PO[:,i]),i]), \
		np.max(IC_prev_avg_PO[~np.isnan(IC_prev_avg_PO[:,i]),i])), \
		radius=10, color='black', lw=2, fill=False)
	ax1.add_artist(circle_qoi1)
	circle_qoi2 = Ellipse((L, np.max(IC_ex_PO[:,i])), \
		width=20, height=1000, color='black', lw=2, fill=False)
	ax2.add_artist(circle_qoi2)

	# # indicate the QoIs with an arrow
	# ax1.arrow(x=14+np.argmax(IC_prev_avg_PO[~np.isnan(IC_prev_avg_PO[:,i]),i])+30, \
	# 	y=np.max(IC_prev_avg_PO[~np.isnan(IC_prev_avg_PO[:,i]),i])+30, dx=-20, dy=-20, lw=2, \
	# 	head_width=6, shape='full')
	# if i<=1:
	# 	ax2.arrow(x=L-30, y=np.max(IC_ex_PO[:,i])+900, dx=20, dy=-600, lw=2, \
	# 		head_width=6, shape='full')		
	# else:
	# 	ax2.arrow(x=L-30, y=np.max(IC_ex_PO[:,i])-900, dx=20, dy=600, lw=2, \
	# 		head_width=6, shape='full')

ax0.hlines(y=IC_capacity, xmin=0, xmax=L, lw=2, ls=':', color='black')
ax1.hlines(y=IC_capacity, xmin=0, xmax=L, lw=2, ls=':', color='black')

ax0.set_ylim([0, 500])
ax0.set_yticks([0, 200, 400])
ax1.set_ylim([0, 500])
ax1.set_yticks([0, 200, 400])

ax2.set_yticks([0, 10000, 20000])

plt.tight_layout()
fig.savefig('figures/QoIs.pdf')

plt.show()