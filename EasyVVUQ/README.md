# Requirements
* Python 3.6+
 * chaospy
 * [easyvvuq](https://github.com/UCL-CCS/EasyVVUQ)
 * numpy
 * os
 * pandas
 * matplotlib
 * mpl_toolkits.mplot3d
 * subprocess

* R 3.6.0+
 * data.table
 * devtools
 * forecast
 * ggplot2
 * Rcpp
 * remotes
 * rjson
 * usethis
 

# Files
The scripts can be executed on the local machine; the variable `<workdir>` will have to be modified by the reader 
such that it points to a folder present in the local machine. 

## Start a campaign

## The R-scripts
The `<*.r>` scripts represent implementations of a particular strategy (Flattening the Curve, Contact Tracing, 
Intermittent Lockdown or Phased Opening) in the [virsim](https://gitlab.com/luccoffeng/virsim) model. 

## Post-processing
