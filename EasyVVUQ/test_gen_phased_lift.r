# Prep ----
rm(list = ls())

remotes::install_gitlab("luccoffeng/virsim")

library(virsim)
library(ggplot2)
library(data.table)

work_dir <- getwd()  
setwd(work_dir)

param_temp <- gen_phased_lift(intervention_start = 15,
                              init_lockdown_dur = 60,
                              lockdown_effect = 0.2,
                              n_phases = 20,
                              interventions_lift_interval = 60,
                              extra_duration_first_interval = -15,
                              start_reduce_interval = 3,
                              repeat_reduction = 1,
                              reduce_interval = c(15, rep(c(5, rep(0, 4)), 4)),
                              pl_intervention_effect_hi = 0.25,
                              pl_intervention_effect_lo = 1 ,
                              sc_isolation_effect = 0.5,
                              lockdown_isol = FALSE)

set.seed(12345)
phased_opening <- do.call(what = virsim,
                          args = param_temp)

# Plot
qplot(data = aggregate_output(phased_opening$monitor),
      x = time,
      y = I / (S + E + I + R) * 100,
      geom = "line")

print(param_temp$intervention_t)