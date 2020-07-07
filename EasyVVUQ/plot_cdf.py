import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
plt.rcParams['figure.figsize'] = 8,6

QoI = pd.read_csv('MC_CT_QoI.csv',delimiter=',')

n_runs = len(QoI["IC_prev_avg_max"])

IC_prev_avg_max = sort(QoI["IC_prev_avg_max"])
IC_ex_max = sort(QoI["IC_ex_max"])

p = np.arange(start=1,stop=n_runs+1,step=1)/n_runs

f = plt.figure('cdfs',figsize=[12,6])
ax_p = f.add_subplot(121, xlabel='IC_prev_avg_max', ylabel='cdf')
ax_p.step(IC_prev_avg_max,p,lw=2)

ax_e = f.add_subplot(122, xlabel='IC_ex_max', ylabel='cdf')
ax_e.step(IC_ex_max,p,lw=2)

plt.tight_layout()
f.savefig('figures/empirical_cdfs.png')

plt.show()