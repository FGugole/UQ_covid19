# Prep ----
rm(list = ls())

remotes::install_gitlab("luccoffeng/virsim")

library(virsim)
library(ggplot2)
library(data.table)
library(stats)
library(plyr)
library(extraDistr)

work_dir <- getwd()  
setwd(work_dir)

size_multiplier <- 1
param_main <- within(param_sim, {
  runtime <- 550
  
  n_agent <- 1e6 * size_multiplier
  n_cluster <- 1e3 * size_multiplier
  n_supercluster <- 20
  
  cluster_size_sd <- 0.95
  supercluster_size_sd <- 0
  
  efoi <- 0
  infection_init <- 50 * size_multiplier
  seed_supercluster <- c(rep(9, 2), rep(2, 6), rep(1, 6), rep(0, 6))
  inc_cum_cond <- 9500 * size_multiplier
  
  contact_rate <- 0.5
  contact_shape <- 3.4
  contact_assort <- 0.26
  population_mixing <- .05
  supercluster_mixing <- .05
  
  exposed_time <- list(name = "weibull",
                       shape = 20,
                       scale = exp(log(4.6) - lgamma(1 + 1 / 20)))
  infected_time <- list(name = "weibull",
                        shape = 1,
                        scale = exp(log(5) - lgamma(1 + 1 / 1)))
  
  temp_storage <- "RAM"
  aggregate <- "population"
  output_quick <- TRUE
  output_steps <- 1
  verbose <- FALSE # turn off printing of progress to console
})

########################
# Monte Carlo sampling #
########################
n_runs = 10

rnd_seed <- rdunif(n_runs,2^14,2^16)

trace_E <- rbeta(n_runs,2,4)

trace_I <- rgamma(n_runs,shape=2,scale=.4)

contact_red <- rbeta(n_runs,10,2)

param_values <- data.frame(rnd_seed, trace_E, trace_I, contact_red)

######################################
# Write parameter values to csv file #
######################################
write.csv(x=param_values, file='MC_CT_param', row.names=FALSE)

##################################################################################
# Running an individual simulation for the Contact Tracing strategy using virsim #
##################################################################################

IC_prev_avg_max = numeric(n_runs)
IC_ex_max = numeric(n_runs)

# Define the parameters
intervention_t = cumsum(c(0, 10, 7, 53, 30))
intervention_effect = c(1, .3, .15, .25, 1)
intervention_uptake = rep(1, 5)

for (i in 1:n_runs){
  
  trace_prob_E = c(rep(0, 4), trace_E[i])
  trace_rate_I = c(rep(0, 4), trace_I[i])
  trace_contact_reduction = c(rep(0, 4), contact_red[i])
  set.seed(rnd_seed[i])
  
  contact_tracing <- do.call(what = virsim,
                             args = c(param_main,
                                      list(intervention_t = intervention_t,
                                           intervention_uptake = intervention_uptake,
                                           intervention_effect = intervention_effect,
                                           trace_prob_E = trace_prob_E,
                                           trace_rate_I = trace_rate_I,
                                           trace_contact_reduction = trace_contact_reduction,
                                           efoi = 50 / 365 / param_main$n_agent)))

  contact_tracing_data = aggregate_output(contact_tracing$monitor)
  contact_tracing_data[, c("IC_inc", "IC_prev") :=
                         gen_derived_outcome(inc = inc, time = time)]
  
  ###########################################################################
  # Compute the moving average of total IC patients over a certain interval #
  ###########################################################################
  L <- length(contact_tracing_data$IC_prev)
  IC_prev_avg <- vector(mode="numeric", length=L)

  avg_window <- 30
  for (i in 1:L){
    IC_prev_avg[i] <- mean(contact_tracing_data$IC_prev[i:min(i+avg_window-1,L)])
  }
  contact_tracing_data[, "IC_prev_avg"] <- IC_prev_avg
  IC_prev_avg_max[i] <- max(IC_prev_avg)

  ###########################################################
  # Compute the number of IC patients exceeding IC capacity #
  ###########################################################
  IC_excess <- vector(mode="numeric", length=L)
  IC_capacity <- 108

  IC_excess[1] <- 0 # at the beginning of the simulation there are no IC patients in excess
  for (i in 2:L){
    IC_excess[i] <- IC_excess[i-1] + max(0, contact_tracing_data$IC_prev[i]-IC_capacity)
  }

  contact_tracing_data[, "IC_ex"] <- IC_excess
  IC_ex_max[i] <- max(IC_excess)
}

Qoi_values <- data.frame(IC_prev_avg_max, IC_ex_max)

#############################
# Write results to csv file #
#############################
write.csv(x=QoI_values, file='MC_CT_QoI', row.names=FALSE)

#######################
# Plot empirical cdfs #
#######################
IC_prev_avg_max <- sort(IC_prev_avg_max)
IC_ex_max <- sort(IC_ex_max)

p <- linspace(1, n_runs, n_runs)/n_runs

plot(step~IC_prev_avg_max,data=p,type="s")
plot.new()
plot(step~IC_ex_max,data=p,type="s")
