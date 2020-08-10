# Prep ----
rm(list = ls())

remotes::install_gitlab("luccoffeng/virsim")

library(virsim)
library(ggplot2)
library(data.table)
library(rjson)
library(forecast)

work_dir <- getwd()  
setwd(work_dir)

###############################################################
# the json input file containing the values of the parameters #
###############################################################
json_data <- fromJSON(file="corona_in.json")

rnd_seed <- unname(sapply(json_data$seed, as.integer))

output_filename <- json_data$outfile

# biology
Rzero <- unname(sapply(json_data$Rzero, as.numeric))

avg_duration_infectiousness <- unname(sapply(json_data$duration_infectiousness, as.numeric))

avg_contact_rate <- Rzero / avg_duration_infectiousness

shape_exposed_time <- unname(sapply(json_data$shape_exposed_time, as.numeric))

intervention_effect_var_inv <- unname(sapply(json_data$intervention_effect_var_inv, as.numeric))

# strategy
lock_effect <- unname(sapply(json_data$lockdown_effect, as.numeric))

lock_length <- unname(sapply(json_data$lockdown_length, as.integer))

lift_length <- unname(sapply(json_data$lift_length, as.integer))

uptake <- unname(sapply(json_data$uptake, as.numeric))

#################################
# define main set of parameters #
#################################
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
  
  contact_rate <- avg_contact_rate
  contact_shape <- 3.4
  contact_assort <- 0.26
  population_mixing <- .05
  supercluster_mixing <- .05
  
  exposed_time <- list(name = "weibull",
                       shape = shape_exposed_time,
                       scale = exp(log(4.6) - lgamma(1 + 1 / shape_exposed_time)))
  infected_time <- list(name = "weibull",
                        shape = 1,
                        scale = exp(log(avg_duration_infectiousness) - lgamma(1 + 1 / 1)))
  
  # intervention_effect_var <- 1 / intervention_effect_var_inv

  trace_prob_E <- c(rep(0, 34))
  trace_rate_I <- c(rep(0, 34))
  trace_contact_reduction <- c(rep(0, 34))

  temp_storage <- "RAM"
  aggregate <- "population"
  output_quick <- TRUE
  output_steps <- 1
  verbose <- FALSE # turn off printing of progress to console
})

#######################################################################################
# Running an individual simulation for the Flattening the Curve strategy using virsim #
#######################################################################################
intervention_t = cumsum(c(0, 10, 7, 53, rep(c(lock_length, lift_length),15) ))
intervention_effect = c(1, .3, .15, .25, rep(c(lock_effect, 1),15) )
intervention_uptake = rep(uptake, length(intervention_t))

# Select a random seed per each realization (using the system time)
#initial_seed <- as.integer(Sys.time())
# take the last 5 digits of the initial seed
#the_seed <- initial_seed %% 1e5
# set the seed
set.seed(rnd_seed)

intermittent_lock <- do.call(what = virsim,
                      args = c(param_main,
                               list(intervention_t = intervention_t,
                                    intervention_uptake = intervention_uptake,
                                    intervention_effect = intervention_effect)))

intermittent_lock_data = aggregate_output(intermittent_lock$monitor)
intermittent_lock_data[, c("IC_inc", "IC_prev") :=
                  gen_derived_outcome(inc = inc, time = time)]

###########################################################################
# Compute the moving average of total IC patients over a certain interval #
###########################################################################
L <- length(intermittent_lock_data$IC_prev)
IC_prev_avg <- vector(mode="numeric", length=L)

avg_window <- 30
#for (i in 1:L){
#  IC_prev_avg[i] <- mean(intermittent_lock_data$IC_prev[i:min(i+avg_window-1,L)])
#}
IC_prev_avg <- ma(x=intermittent_lock_data$IC_prev,order=avg_window)
#IC_prev_avg <- na.omit(IC_prev_avg)
intermittent_lock_data[, "IC_prev_avg"] <- IC_prev_avg
intermittent_lock_data[, "IC_prev_avg_max"] <- max(na.omit(IC_prev_avg))

###########################################################
# Compute the number of IC patients exceeding IC capacity #
###########################################################
IC_excess <- vector(mode="numeric", length=L)
IC_capacity <- 109

IC_excess[1] <- 0 # at the beginning of the simulation there are no IC patients in excess
for (i in 2:L){
  IC_excess[i] <- IC_excess[i-1] + max(0, intermittent_lock_data$IC_prev[i]-IC_capacity)
}

intermittent_lock_data[, "IC_ex"] <- IC_excess
intermittent_lock_data[, "IC_ex_max"] <- max(IC_excess)

#############################
# Write results to csv file #
#############################
write.csv(x=intermittent_lock_data, file=output_filename, row.names=FALSE)
