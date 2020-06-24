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

######################################################################################
# Running a batch of simulations for the Flattening the Curve strategy using run_batch
######################################################################################
flat_batch <- run_batch(par_def = param_default,
                        phased_lift = FALSE,
                        seeds = 12345 + 1:4,
                        aggregate = "population",
                        fact_comb = TRUE,  # see documentation
                        runtime = 4*365,
                        inc_cum_cond = 950,   # see documentation
                        # N.B. non-scalar model parameters must be entered as
                        # a list when using run_batch
                        intervention_t = list(cumsum(c(0, 10, 7, 53, 90, 365, 365, 120))),
                        intervention_effect = list(c(1, .3, .15, .25, .3, .55, .9, 1),
                                                   c(1, .3, .15, .25, .35, .55, .9, 1),
                                                   c(1, .3, .15, .25, .4, .55, .9, 1)),
                        intervention_uptake = list(rep(1, 8)))

flat_collated <- collate_batch(flat_batch, pars = c("intervention_effect"))
flat_collated[, c("IC_inc", "IC_prev") :=
                gen_derived_outcome(inc = inc, time = time),
              by = .(par_set, seed)]

flat_collated[, first_reduction := sapply(intervention_effect,
                                          function(x) x[5])]

n_runs <- 12
L <- length(flat_collated$IC_prev)/n_runs
IC_prev_avg <- vector(mode="numeric", length=L*n_runs)

interval = 10
for (n in 0:(n_runs-1)){
  for (i in 1:L){
    IC_prev_avg[n*L+i] <- mean(flat_collated$IC_prev[n*L+i:min(i+interval-1,L)])
  }
}
flat_collated[, "IC_prev_avg"] <- IC_prev_avg

# Plot
png(file="~/Desktop/virsim/figures/IC_prev.png",width=12,height=6,units="cm",res=300)
qplot(data = flat_collated,
      x = time,
      #y = R / (S + E + I + R) * 100,
      y = IC_prev_avg,
      geom = "line",
      col = factor(first_reduction),
      group = interaction(seed, par_set))
dev.off()