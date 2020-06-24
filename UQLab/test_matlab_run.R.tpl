# Example code to run a single simulation or a batch of simulations for
# transmission and control of SARS-CoV-2 with virsim.

# Author: Luc Coffeng
# Created: 21 May 2020


# Prep ----
rm(list = ls())

remotes::install_gitlab("luccoffeng/virsim")

library(virsim)
library(ggplot2)
library(data.table)

work_dir <- "~/Dropbox/work/Programming/corona/UQ_covid19/UQLab/"  # Adjust path here
setwd(work_dir)


## Simulating a natural epidemic ----
# Running a single simulation
set.seed(12345)
natural <- virsim(runtime = 200,
                  n_supercluster = 5,
                  n_cluster = round(<X0001>),
                  n_agent = round(<X0002>),
                  output_quick = TRUE,  # recommended unless you want details
                  temp_storage = "RAM",
                  aggregate = "cluster")


# # Alternative approach: if you want to save your default preferences in an
# # intermediate placeholder 'param_default' for parameter values
# param_default <- within(param_sim, {
#   output_quick <- TRUE  # adjust default values
#   temp_storage <- "RAM"
#   verbose <- FALSE  # turn off printing of progress to console
#   aggregate <- "cluster"
# })
#
# set.seed(12345)
# natural2 <- do.call(what = virsim,
#                     args = c(param_default,
#                              list(runtime = 365,
#                                   n_supercluster = 5,
#                                   n_cluster = 100,
#                                   n_agent = 1e5)))
# all.equal(natural, natural2)
# # only 'calc_duration' should differ a little bit
# # (i.e. the time it took to run the simulation)
# rm(natural2)

# Aggregate model output to supercluster or population level, if you want
output <- natural$monitor                 # cluster level
output_sc <- aggregate_output_sc(output)  # supercluster level
output_pop <- aggregate_output(output)    # population level;  aggregate_output(output_sc) also works


# The model only predicts states S, E, I, an R (susceptible, exposed, infectious,
# and recovered/immune), along with incidence of new infectious cases ('inc').
# You can add post-hoc derived output, e.g. IC admissions. See the documentation
# to 'gen_derived_output()' for how it works.
output[, c("IC_inc", "IC_prev") :=
         gen_derived_outcome(inc = inc, time = time),
       by = cluster]
output_sc[, c("IC_inc", "IC_prev") :=
         gen_derived_outcome(inc = inc, time = time),
       by = supercluster]
output_pop[, c("IC_inc", "IC_prev") :=
         gen_derived_outcome(inc = inc, time = time)]
# Because of stochasticity, the total number of IC admission will differ (a
# little) between the three objects:
output[, sum(IC_inc)]
output_sc[, sum(IC_inc)]
output_pop[, sum(IC_inc)]
# To save computation time, aggregate before calculating derived outputs like
# IC admissions.

# qplot(data = aggregate_output(output_pop),
#       x = time,
#       y = I / (S + E + I + R) * 100,
#       geom = "line")

write.csv(x = aggregate_output(output_pop), file='virsim_results.csv', row.names=FALSE)
# Running a batch of simulations in parallel for multiple parameter sets. Here,
# we compare two hypothetical situations where the population is divided over
# either 100 or 1000 clusters (without changing the default values for mixing
# within and between clusters).
# param_default <- within(param_default, {
#   n_supercluster <- 5
#   n_cluster <- 100
#   n_agent <- 1e5
# })
# natural_batch <- run_batch(par_def = param_default,
#                            phased_lift = FALSE,
#                            seeds = 12345 + 1:4,
#                            aggregate = "population",
#                            runtime = 365,
#                            n_cluster = c(100, 1000))
#
# # Collate output and include parameter names if you want these be included in
# # the resulting output
# natural_batch_collated <- collate_batch(natural_batch,
#                                         pars = c("n_cluster"))
# natural_batch_collated[, c("IC_inc", "IC_prev") :=
#                          gen_derived_outcome(inc = inc, time = time),
#                        by = .(par_set, seed)]
#
# qplot(data = natural_batch_collated,
#       x = time,
#       y = I / (S + E + I + R) * 100,
#       geom = "line",
#       col = factor(n_cluster),
#       group = interaction(seed, n_cluster))
#
#
# ## Simulating an intervention ----
# # The following simulates a hypothetical history of interventions (loosely
# # based on the Dutch situation), where interventions are started when 950
# # cases of infection have occurred cumulatively in the population. At that
# # time point, an intervention starts that reduces transmission to 30% of its
# # original level (the population is not adhering very well yet). Then, seven
# # days later tranmission is further reduced to 15%. 53 days later transmission
# # returns to 25% of it's original potential (e.g. schools open, N.B. the 25% is
# # an assumption!). Last, either 30 or 90 days after returning to 25%, all
# # interventions are lifted.
# intervene <- run_batch(par_def = param_default,
#                        phased_lift = FALSE,
#                        seeds = 12345 + 1:4,
#                        aggregate = "population",
#                        fact_comb = TRUE,  # see documentation
#                        runtime = 365,
#                        inc_cum_cond = 950,   # see documentation
#                        # N.B. non-scalar model parameters must be entered as
#                        # a list when using run_batch
#                        intervention_t = list(cumsum(c(0, 10, 7, 53, 30)),
#                                              cumsum(c(0, 10, 7, 53, 90))),
#                        intervention_effect = list(c(1, .3, .15, .25, 1)),
#                        intervention_uptake = list(rep(1, 5)))
#
# intervene_collated <- collate_batch(intervene, pars = c("intervention_t"))
# intervene_collated[, intervention_start := sapply(intervention_t,
#                                                   function(x) x[2])]
# intervene_collated[, last_period := sapply(intervention_t,
#                                            function(x) diff(x)[4])]
# intervene_collated[, c("IC_inc", "IC_prev") :=
#                      gen_derived_outcome(inc = inc, time = time),
#                    by = .(par_set, seed)]
#
# qplot(data = intervene_collated,
#       x = time - intervention_start,
#       y = I,
#       geom = "line",
#       col = factor(last_period),
#       group = interaction(seed, par_set))
# # Can you explain why I peaks just after interventions have started?
#
# qplot(data = intervene_collated,
#       x = time - intervention_start,
#       y = IC_prev,
#       geom = "line",
#       col = factor(last_period),
#       group = interaction(seed, par_set))
# # Can you explain why IC_prev peaks after interventions have already started?


### END OF CODE ### ----
