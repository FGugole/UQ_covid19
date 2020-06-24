# Prep ----
rm(list = ls())

remotes::install_gitlab("luccoffeng/virsim")

library(virsim)
library(ggplot2)
library(data.table)

work_dir <- getwd()  
setwd(work_dir)

param_default <- within(param_sim, {
  output_quick <- TRUE  # adjust default values
  temp_storage <- "RAM"
  verbose <- FALSE  # turn off printing of progress to console
  #  aggregate <- "cluster"
  n_supercluster <- 10
  n_cluster <- 1000
  n_agent <- 1e6
})

###############################################################################
# Running a batch of simulations in parallel for multiple parameter sets 
###############################################################################
intervene <- run_batch(par_def = param_default,
                       phased_lift = TRUE,
                       seeds = 12345 + 1:4,
                       aggregate = "population",
                       fact_comb = TRUE,  # see documentation
                       runtime = 2*365,
                       inc_cum_cond = list(950, 1500),   # see documentation
                       n_phases = list(5, 10))

# Collate output 
intervene_collated <- collate_batch(intervene, pars = c("inc_cum_cond","n_phases"))
intervene_collated[, c("IC_inc", "IC_prev") :=
                     gen_derived_outcome(inc = inc, time = time),
                   by = .(par_set, seed)]

qplot(data = intervene_collated,
      x = time,
      #y = IC_inc,
      y = R / (S + E + I + R) * 100,
      geom = "line",
      col = factor(n_phases),
      group = interaction(seed, par_set))

#################################################################################
# Running an individual simulation for the Phased Opening strategy using virsim #
# (and not run_batch)                                                           #
#################################################################################

# First define manually intervention_t, ...
n_phases <- param_default$n_supercluster
intervention_start <- 30
init_lockdown_dur <- 60
interventions_lift_interval <- 45
extra_duration_first_interval <- 15
start_times <-intervention_start + init_lockdown_dur +
  c(0, extra_duration_first_interval +
      interventions_lift_interval * (1:(n_phases - 1)))
intervention_t <- c(0, intervention_start, start_times)

# ... intervention_uptake, ...
uptake <- 0.9
intervention_uptake <- matrix(0,
                              nrow = n_phases,
                              ncol = length(intervention_t),
                              dimnames = list(NULL,
                                              intervention_t))
intervention_uptake[, -c(1, length(intervention_t))] <- uptake

# ... intervention_effect ...
lockdown_effect <- 0.20
pl_intervention_effect_hi <- 0.25
pl_intervention_effect_lo <- 1
intervention_effect <- matrix(0,
                              nrow = n_phases,
                              ncol = length(intervention_t),
                              dimnames = list(NULL,
                                              intervention_t))
intervention_effect[, -1] <- pl_intervention_effect_hi
intervention_effect[, 2] <- lockdown_effect
for (t in 1:n_phases) {
  start_index <- which(intervention_t == start_times[t])
  intervention_effect[t, start_index:length(intervention_t)] <- pl_intervention_effect_lo
}

# ... and sc_isolation_effect
sc_isolation <- 0.5
sc_isolation_effect <- matrix(1,
                              nrow = n_phases,
                              ncol = length(intervention_t),
                              dimnames = list(NULL,
                                              intervention_t))
diag(sc_isolation_effect[,-(1:2)]) <- sc_isolation

# Finish setup
setup <- rep(ceiling(param_default$n_supercluster / n_phases), n_phases)
if (sum(setup) > param_default$n_supercluster) {
  setup[length(setup)] <- setup[length(setup)] - (sum(setup) - param_default$n_supercluster)
}
setup <- rep(1:length(setup), setup)
intervention_uptake <- intervention_uptake[setup, ]
intervention_effect <- intervention_effect[setup, ]
sc_isolation_effect <- sc_isolation_effect[setup, ]

# Running a single simulation
set.seed(12345)
phased_opening <- do.call(what = virsim,
                          args = c(param_default,
                                   list(runtime = 3*365,
                                        intervention_t = intervention_t,
                                        intervention_uptake = intervention_uptake,
                                        intervention_effect = intervention_effect,
                                        sc_isolation_effect = sc_isolation_effect)))

# Plot
qplot(data = aggregate_output(phased_opening$monitor),
      x = time,
      y = I / (S + E + I + R) * 100,
      geom = "line")
