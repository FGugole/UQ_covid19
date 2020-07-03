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

################################################################################
# Running an individual simulation for the Contact Tracing strategy using virsim 
################################################################################

# Define the parameters
intervention_t = cumsum(c(0, 10, 7, 53, 60))
intervention_effect = c(1, .3, .15, .25, 1)
intervention_uptake = rep(1, 5)

trace_prob_E = c(0, .1, .3, .5, .6)
trace_rate_I = c(0, .1, .3, .5, .5)
trace_contact_reduction = c(0, .1, .3, .5, .6)

# Running a single simulation
set.seed(12345+4)
contact_tracing <- do.call(what = virsim,
                           args = c(param_default,
                                    list(runtime = 3*365,
                                         inc_cum_cond = 950,
                                         intervention_t = intervention_t,
                                         intervention_uptake = intervention_uptake,
                                         intervention_effect = intervention_effect,
                                         trace_prob_E = trace_prob_E,
                                         trace_rate_I = trace_rate_I,
                                         trace_contact_reduction = trace_contact_reduction)))

contact_tracing_data = aggregate_output(contact_tracing$monitor)
contact_tracing_data[, c("IC_inc", "IC_prev") :=
                       gen_derived_outcome(inc = inc, time = time)]

# Plot
qplot(data = contact_tracing_data,
      x = time,
      y = IC_prev,
      #y = R / (S + E + I + R) * 100,
      geom = "line")

#################################################################################
# Running a batch of simulations for the Contact Tracing strategy using run_batch 
#################################################################################
contact_batch <- run_batch(par_def = param_default,
                           phased_lift = FALSE,
                           seeds = 12345 + 1:4,
                           aggregate = "population",
                           fact_comb = TRUE,  # see documentation
                           runtime = 3*365,
                           inc_cum_cond = 950,   # see documentation
                           # N.B. non-scalar model parameters must be entered as
                           # a list when using run_batch
                           intervention_t = list(cumsum(c(0, 10, 7, 53, 60))),
                           intervention_effect = list(c(1, .3, .15, .25, 1)),
                           intervention_uptake = list(rep(1, 5)),
                           trace_prob_E = list(c(rep(0, 4), .6)),
                           trace_rate_I = list(c(rep(0, 4), .5)),
                           trace_contact_reduction = list(c(rep(0, 4), .6),
                                                          c(rep(0, 4), .7)))

contact_collated <- collate_batch(contact_batch, pars = c("trace_contact_reduction"))
contact_collated[, c("IC_inc", "IC_prev") :=
                   gen_derived_outcome(inc = inc, time = time),
                 by = .(par_set, seed)]

contact_collated[, last_reduction := sapply(trace_contact_reduction,
                                            function(x) x[5])]

n_runs <- 12
L <- length(contact_collated$IC_prev)/n_runs
IC_prev_avg <- vector(mode="numeric", length=L*n_runs)

interval = 21
for (n in 0:(n_runs-1)){
  for (i in 1:L){
    IC_prev_avg[n*L+i] <- mean(contact_collated$IC_prev[n*L+i:min(i+interval-1,L)])
  }
}
contact_collated[,"IC_prev_avg"] <- IC_prev_avg

# Plot
qplot(data = contact_collated,
      x = time,
      #y = R / (S + E + I + R) * 100,
      y = IC_prev_avg,
      geom = "line",
      col = factor(last_reduction),
      group = interaction(seed, par_set))
