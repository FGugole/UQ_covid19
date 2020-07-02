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

# Contact tracing
beta_tpE = cp.Beta(alpha=3, beta=2, lower=.4)
beta_tcr = cp.Beta(alpha=6, beta=2, lower=.4)
gamma_trI = cp.Gamma(shape=2, scale=.4)

x_CT = np.linspace(0, 1.5, 151)

f = plt.figure('distributions_CT')
ax = f.add_subplot(111, xlabel='x')
ax.plot(x_CT,beta_tpE.pdf(x_CT),lw=2,label='trace_prob_E')
ax.plot(x_CT,gamma_trI.pdf(x_CT),lw=2,label='trace_rate_I')
ax.plot(x_CT,beta_tcr.pdf(x_CT),lw=2,label='trace_cont_red')
ax.set_xticks([0.0, .5, 1.0, 1.5])

leg = plt.legend()
leg.set_draggable(True)
plt.tight_layout()

# Flattening the curve
beta_int1 = cp.Beta(alpha=3, beta=2, lower=.3, upper=.4)
beta_up = cp.Beta(alpha=3, beta=2, lower=.5)

x_FT = np.linspace(0, 1, 101)

f = plt.figure('distributions_FT')
ax = f.add_subplot(111, xlabel='x')
ax.plot(x_FT,beta_int1.pdf(x_FT),lw=2,label='intervention_effect')
ax.plot(x_FT,beta_up.pdf(x_FT),lw=2,label='uptake')
ax.set_xticks([0.0, .5, 1.0])

leg = plt.legend()
leg.set_draggable(True)
plt.tight_layout()

plt.show()