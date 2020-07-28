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
beta_tpE = cp.Beta(alpha=2, beta=4)
beta_tcr = cp.Beta(alpha=10, beta=2)
gamma_trI = cp.Gamma(shape=2, scale=.4)

x_CT = np.linspace(0, 1.5, 151)

f = plt.figure('distributions_CT')
ax = f.add_subplot(111, xlabel='x', ylabel='pdf')
ax.plot(x_CT,beta_tpE.pdf(x_CT),lw=2,label='trace_prob_E')
ax.plot(x_CT,gamma_trI.pdf(x_CT),lw=2,label='trace_rate_I')
ax.plot(x_CT,beta_tcr.pdf(x_CT),lw=2,label='trace_cont_red')
ax.set_xticks([0.0, .5, 1.0, 1.5])

leg = plt.legend()
leg.set_draggable(True)
plt.tight_layout()

# Flattening the curve
beta_int1 = cp.Beta(alpha=38, beta=70)
beta_up = cp.Beta(alpha=16, beta=2)

x_FT = np.linspace(0, 1, 101)

f = plt.figure('distributions_FC')
ax = f.add_subplot(111, xlabel='x', ylabel='pdf')
ax.plot(x_FT,beta_int1.pdf(x_FT),lw=2,label='intervention_effect')
ax.plot(x_FT,beta_up.pdf(x_FT),lw=2,label='uptake')
ax.set_xticks([0.0, .5, 1.0])

leg = plt.legend()
leg.set_draggable(True)
plt.tight_layout()

# Intermittent lockdown
beta_lockeffect = cp.Beta(alpha=14,beta=42)
gamma_locklength = cp.Gamma(shape=20,scale=2)
gamma_liftlength = cp.Gamma(shape=17.5,scale=1)

x_IL = np.linspace(0, 1, 101)
x_IL_length = np.linspace(0, 60, 601)

f = plt.figure('distributions_IL')
ax = f.add_subplot(111, xlabel='x', ylabel='pdf')
ax.plot(x_IL,beta_lockeffect.pdf(x_IL),lw=2,label='effect of lockdowns')
ax.plot(x_IL,beta_up.pdf(x_IL),lw=2,label='uptake')
ax.set_xticks([0.0, .5, 1.0])

leg = plt.legend()
leg.set_draggable(True)
plt.tight_layout()

f = plt.figure('distributions_IL_lengths')
ax = f.add_subplot(111, xlabel='x', ylabel='pdf')
ax.plot(x_IL_length,gamma_locklength.pdf(x_IL_length),lw=2,label='length of lockdowns')
ax.plot(x_IL_length,gamma_liftlength.pdf(x_IL_length),lw=2,label='length of lifts')
ax.set_xticks([0, 20, 40, 60])

leg = plt.legend()
leg.set_draggable(True)
plt.tight_layout()

# Phased opening
gamma_phase_interval = cp.Gamma(shape=25,scale=2)

x_PO = np.linspace(0, 1, 101)
x_PO_length = np.linspace(0, 90, 901)

f = plt.figure('distributions_PO')
ax = f.add_subplot(111, xlabel='x', ylabel='pdf')
ax.plot(x_PO,beta_lockeffect.pdf(x_PO),lw=2,label='pl_intervention_effect_hi')
ax.plot(x_PO,beta_up.pdf(x_PO),lw=2,label='uptake')
ax.set_xticks([0.0, .5, 1.0])

leg = plt.legend()
leg.set_draggable(True)
plt.tight_layout()

f = plt.figure('distributions_PO_lengths')
ax = f.add_subplot(111, xlabel='x', ylabel='pdf')
ax.plot(x_PO_length,gamma_phase_interval.pdf(x_PO_length),lw=2,label='intervention_lift_interval')
ax.set_xticks([0, 30, 60, 90])

leg = plt.legend()
leg.set_draggable(True)
plt.tight_layout()

# Biology related parameters
gamma_Rzero = cp.Gamma(shape=100,scale=.025)
gamma_duration_infectiousness = cp.Gamma(shape=25,scale=.2)
gamma_intervention_effect_var = cp.Gamma(shape=2,scale=.05)
gamma_exposed_time = cp.Gamma(shape=17.5,scale=1)

x_bio = np.linspace(0, 8, 801)
x_exposed_time = np.linspace(0, 40, 4001)

f = plt.figure('distributions_bio')
ax = f.add_subplot(111, xlabel='x', ylabel='pdf')
ax.plot(x_bio,gamma_Rzero.pdf(x_bio),lw=2,label='$R_{0}$')
ax.plot(x_bio,gamma_duration_infectiousness.pdf(x_bio),lw=2,label='duration_infectiousness')
ax.plot(x_bio,gamma_intervention_effect_var.pdf(x_bio),lw=2,label='intervention_effect_var$^{-1}$')
ax.set_xticks([0, 4, 8])

leg = plt.legend()
leg.set_draggable(True)
plt.tight_layout()

f = plt.figure('distribution_exposed_time')
ax = f.add_subplot(111, xlabel='x', ylabel='pdf')
ax.plot(x_exposed_time,gamma_exposed_time.pdf(x_exposed_time),lw=2,label='shape param. of exposed time distr.')
ax.set_xticks([0, 20, 40])

leg = plt.legend()
leg.set_draggable(True)
plt.tight_layout()

plt.show()