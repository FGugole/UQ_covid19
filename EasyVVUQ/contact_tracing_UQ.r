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

trace_E <- unname(sapply(json_data$trace_prob_E, as.numeric))

trace_I <- unname(sapply(json_data$trace_rate_I, as.numeric))

contact_red <- unname(sapply(json_data$trace_contact_reduction, as.numeric))

uptake <- unname(sapply(json_data$uptake, as.numeric))

external_forcing <- unname(sapply(json_data$efoi, as.numeric))

output_filename <- json_data$outfile

##################################################################################
# Running an individual simulation for the Contact Tracing strategy using virsim #
##################################################################################

# Define the parameters
intervention_t = cumsum(c(0, 10, 7, 53, 60))
intervention_effect = c(1, .3, .15, .25, 1)
intervention_uptake = rep(uptake, 5)

trace_prob_E = c(rep(0, 4), trace_E)
trace_rate_I = c(rep(0, 4), trace_I)
trace_contact_reduction = c(rep(0, 4), contact_red)

# Select a random seed per each realization (using the system time)
initial_seed <- as.integer(Sys.time())
# take the last 5 digits of the initial seed
the_seed <- initial_seed %% 1e5
# set the seed
set.seed(the_seed)

contact_tracing <- do.call(what = virsim,
                           args = c(param_default,
                                    list(intervention_t = intervention_t,
                                         intervention_uptake = intervention_uptake,
                                         intervention_effect = intervention_effect,
                                         trace_prob_E = trace_prob_E,
                                         trace_rate_I = trace_rate_I,
                                         trace_contact_reduction = trace_contact_reduction,
                                         efoi = external_forcing/param_default$n_agent)))

contact_tracing_data = aggregate_output(contact_tracing$monitor)
contact_tracing_data[, c("IC_inc", "IC_prev") :=
                       gen_derived_outcome(inc = inc, time = time)]

###########################################################################
# Compute the moving average of total IC patients over a certain interval #
###########################################################################
L <- length(contact_tracing_data$IC_prev)
IC_prev_avg <- vector(mode="numeric", length=L)

interval = 30
for (i in 1:L){
  IC_prev_avg[i] <- mean(contact_tracing_data$IC_prev[i:min(i+interval-1,L)])
}
contact_tracing_data[, "IC_prev_avg"] <- IC_prev_avg

#############################
# Write results to csv file #
#############################
write.csv(x=contact_tracing_data, file=output_filename, row.names=FALSE)
