# Prep ----
rm(list = ls())

remotes::install_gitlab("luccoffeng/virsim")

library(virsim)
library(ggplot2)
library(data.table)
library(rjson)

work_dir <- getwd()  
setwd(work_dir)

param_default <- within(param_sim, {
  output_quick <- TRUE  # adjust default values
  temp_storage <- "RAM"
  verbose <- FALSE  # turn off printing of progress to console
  aggregate <- "population"
  n_supercluster <- 20
  n_cluster <- 1e3
  n_agent <- 1e6
  runtime <- 4*365
  inc_cum_cond <- 9500
})

###############################################################
# the json input file containing the values of the parameters #
###############################################################
json_data <- fromJSON(file="corona_in.json")

int_1 <- unname(sapply(json_data$intervention_1, as.numeric))

int_2 <- unname(sapply(json_data$intervention_2, as.numeric))

uptake <- unname(sapply(json_data$uptake, as.numeric))

external_forcing <- unname(sapply(json_data$efoi, as.numeric))

output_filename <- json_data$outfile

#######################################################################################
# Running an individual simulation for the Flattening the Curve strategy using virsim #
#######################################################################################
intervention_t = cumsum(c(0, 10, 7, 53, 60, 365, 365, 120))
intervention_effect = c(1, .3, .15, .25, int_1, int_2, .9, 1)
intervention_uptake = rep(uptake, length(intervention_t))

# Select a random seed per each realization (using the system time)
initial_seed <- as.integer(Sys.time())
# take the last 5 digits of the initial seed
the_seed <- initial_seed %% 1e5
# set the seed
set.seed(the_seed)

flat_curve <- do.call(what = virsim,
                      args = c(param_default,
                               list(intervention_t = intervention_t,
                                    intervention_uptake = intervention_uptake,
                                    intervention_effect = intervention_effect,
                                    efoi = external_forcing/param_default$n_agent)))

flat_curve_data = aggregate_output(flat_curve$monitor)
flat_curve_data[, c("IC_inc", "IC_prev") :=
                  gen_derived_outcome(inc = inc, time = time)]

###########################################################################
# Compute the moving average of total IC patients over a certain interval #
###########################################################################
L <- length(flat_curve_data$IC_prev)
IC_prev_avg <- vector(mode="numeric", length=L)

interval = 30
for (i in 1:L){
  IC_prev_avg[i] <- mean(flat_curve_data$IC_prev[i:min(i+interval-1,L)])
}
flat_curve_data[, "IC_prev_avg"] <- IC_prev_avg

###########################################################
# Compute the number of IC patients exceeding IC capacity #
###########################################################
IC_excess <- vector(mode="numeric", length=L)
IC_capacity <- 108

IC_excess[1] <- 0 # at the beginning of the simulation there are no IC patients in excess
for (i in 2:L){
  IC_excess[i] <- IC_excess[i-1] + max(0, flat_curve_data$IC_prev[i]-IC_capacity)
}

flat_curve_data[, "IC_ex"] <- IC_excess

#############################
# Write results to csv file #
#############################
write.csv(x=flat_curve_data, file=output_filename, row.names=FALSE)
