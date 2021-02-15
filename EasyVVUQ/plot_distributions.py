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
plt.rcParams['figure.figsize'] = 16, 20

# Contact tracing
beta_tpE = cp.Beta(alpha=2, beta=6)
beta_tcr = cp.Beta(alpha=10, beta=2)
gamma_trI = cp.Gamma(shape=2, scale=.2)

x_CT = np.linspace(0, 1.5, 151)

# Flattening the curve
beta_int1 = cp.Beta(alpha=38, beta=70)
beta_up = cp.Beta(alpha=16, beta=2)

x_FT = np.linspace(0, 1, 101)

# Intermittent lockdown & Phased Opening
beta_lockeffect = cp.Beta(alpha=14,beta=42)
gamma_locklength = cp.Gamma(shape=20,scale=2)
gamma_liftlength = cp.Gamma(shape=15,scale=1)
gamma_phase_interval = cp.Gamma(shape=25,scale=2)

x_IL = np.linspace(0, 1, 101)
x_IL_length = np.linspace(0, 90, 901)

# Other parameters
gamma_Rzero = cp.Gamma(shape=100,scale=.025)
gamma_duration_infectiousness = cp.Gamma(shape=25,scale=.2)
gamma_intervention_effect_var = cp.Gamma(shape=2,scale=.05)
gamma_exposed_time = cp.Gamma(shape=17.5,scale=1)

x_bio = np.linspace(0, 8, 801)
x_exposed_time = np.linspace(0, 40, 4001)

"""
* Plot *
"""

f = plt.figure('distributions')

# Flattening the Curve
ax_FC = f.add_subplot(321, ylabel='P(x)')
ax_FC.plot(x_FT,beta_int1.pdf(x_FT),lw=2,label='Intervention effect')
ax_FC.plot(x_FT,beta_up.pdf(x_FT),lw=2,label='Uptake')
ax_FC.set_xticks([0.0, .5, 1.0])
ax_FC.set_ylim([0, 9])
ax_FC.set_yticks([0, 4, 8])

ax_FC.legend(loc='upper right')

# Contact Tracing
ax_CT = f.add_subplot(322)
ax_CT.plot(x_CT,beta_tpE.pdf(x_CT),lw=2,label='Trace probability')
ax_CT.plot(x_CT,gamma_trI.pdf(x_CT),lw=2,label='Rate of tracing')
ax_CT.plot(x_CT,beta_tcr.pdf(x_CT),lw=2,label='Contact reduction')
ax_CT.set_xticks([0.0, .5, 1.0, 1.5])
ax_CT.set_ylim([0, 5])
ax_CT.set_yticks([0, 1.5, 3, 4.5])

ax_CT.legend(loc='upper left')

# Intermittent Lockdown
ax_IL = f.add_subplot(323, ylabel='P(x)')
ax_IL.plot(x_IL,beta_lockeffect.pdf(x_IL),lw=2,label='Lockdown effect')
ax_IL.plot(x_IL,beta_up.pdf(x_IL),lw=2,label='Uptake')
ax_IL.set_xticks([0.0, .5, 1.0])
ax_IL.set_ylim([0.0, 9.0])
ax_IL.set_yticks([0, 4, 8])

ax_IL.legend(loc='upper right')

ax_ILPO = f.add_subplot(324)
ax_ILPO.plot(x_IL_length,gamma_locklength.pdf(x_IL_length),lw=2,label='Lockdown period')
ax_ILPO.plot(x_IL_length,gamma_liftlength.pdf(x_IL_length),lw=2,label='Lift period')
ax_ILPO.plot(x_IL_length,gamma_phase_interval.pdf(x_IL_length),lw=2,label='Intervention interval')
ax_ILPO.set_xticks([0, 30, 60, 90])
ax_ILPO.set_ylim([0, 0.11])
ax_ILPO.set_yticks([0.0, .05, .1])

ax_ILPO.legend(loc='upper right')

# Other parameters
ax_OT = f.add_subplot(325, xlabel='x', ylabel='P(x)')
ax_OT.plot(x_bio,gamma_Rzero.pdf(x_bio),lw=2,label='$R_{0}$')
ax_OT.plot(x_bio,gamma_duration_infectiousness.pdf(x_bio),lw=2,label='Duration of infectiousness')
ax_OT.plot(x_bio,gamma_intervention_effect_var.pdf(x_bio),lw=2,label='intervention_effect_var$^{-1}$')
ax_OT.set_xticks([0, 4, 8])
ax_OT.set_ylim([0, 8])
ax_OT.set_yticks([0, 4, 8])

ax_OT.legend(loc='upper right')

ax_sh = f.add_subplot(326, xlabel='x')
ax_sh.plot(x_exposed_time,gamma_exposed_time.pdf(x_exposed_time),lw=2,label='Shape param. of exposed time distr.')
ax_sh.set_xticks([0, 20, 40])
ax_sh.set_ylim([0.0, 0.12])
ax_sh.set_yticks([0.0, .05, .1])

ax_sh.legend(loc='upper center')

plt.tight_layout()

f.savefig('figures/distributions.pdf')

plt.show()

### END OF CODE ###
