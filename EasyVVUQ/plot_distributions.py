#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 09:41:32 2020

@author: federica
"""

import numpy as np
import chaospy as cp 
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
plt.rcParams['figure.figsize'] = 8,6

beta_1 = cp.Beta(alpha=3, beta=2, lower=.4)

beta_2 = cp.Beta(alpha=6, beta=2, lower=.4)

gamma_1 = cp.Gamma(shape=2, scale=.4)

x = np.linspace(0, 1.5, 151)

f = plt.figure('distributions')
ax = f.add_subplot(111, xlabel='x')
ax.plot(x,beta_1.pdf(x),lw=2,label='trace_prob_E')
ax.plot(x,gamma_1.pdf(x),lw=2,label='trace_rate_I')
ax.plot(x,beta_2.pdf(x),lw=2,label='trace_cont_red')
ax.set_xticks([0.0, .5, 1.0, 1.5])

leg = plt.legend()
leg.set_draggable(True)
plt.tight_layout()

plt.show()