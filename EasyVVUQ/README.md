# Requirements
* Python 3.6+ 
  * chaospy
  * [easyvvuq](https://github.com/UCL-CCS/EasyVVUQ) v0.8 (use `pip3 install easyvvuq==0.8` to install the specified version)
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
The scripts can be executed on the local machine. The codes present in the folder `job_sub_fab` instead submit the job to an external 
supercomputer by means of the [FabSim3](https://github.com/djgroen/FabSim3) and [QCG-PJ](https://github.com/vecma-project/QCG-PilotJob) libraries. 
These two libraries are therefore necessary for the execution of the codes in the `job_sub_fab` folder and we refer the reader to 
the GitHub repositories of FabSim3 and QCG-PJ for details about their installation and on how to configure the local and remote machine.

## Start a campaign
`job_submission_*.py` starts an uncertainty quantification (UQ) campaign for a selected strategy: FC = Flattening the Curve, 
CT = Contact Tracing, IL = Intermittent Lockdown, PO = Phased Opening. Scripts with the suffix `_bio` in the filename, e.g. 
`job_submission_CT_bio.py`, include uncertainties also in biology-related parameter which are otherwise not considered. 
The following holds for both the cases with or without biology-related uncertainties. I use code pieces from `job_submission_CT.py` 
to explain the main structure of the job submission procedure.

After the necessary imports, a new campaign is initialized 
```python3
campaign = uq.Campaign(name='virsim_CT_nobio_', work_dir=workdir)
```
These lines will create a folder named `virsim_CT_nobio_*` in the working directory specified by `workdir` which has to 
be modified by the reader such that it points to a folder present in their local machine. EasyVVUQ adds by default 8 random symbols 
(i.e. letters or numbers) to the name such that the names of the folders are automatically unique and there is no need for manual changes. 

Afterwards a dictionary `params` of the parameters involved in the UQ analysis containing type, minimum, maximum and default values 
per each parameter is defined.
```python3
params = {
    "seed": {
        "type": "integer",
        "min": 0,
        "max": 2**31,
        "default": 12345},
    ...
        "out_file": {
        "type": "string",
        "default": "output.csv"}}
    
```

The selected quantities of interest (QoI) are specified in 
```python3
output_columns = ["IC_prev_avg_max","IC_ex_max"]
```
Then an encoder and a decoder are specified as required by EasyVVUQ and added to the campaign's app.

The `vary` dicitionary contains the input distributions for the parameters. Note that those parameters listed in `params` 
but not specified here will automatically assume the default value specified above.
```python3
vary = {
    "seed": cp.DiscreteUniform(2**14, 2**16),
    ... 
    }
```
At this point a sampler method has to be specified. The `RandomSampler` provided by EasyVVUQ is classic Monte Carlo sampling and 
we use it to obtain the data for the empirical cdfs and the heatmaps. The total number of simulations in the campaign is given by `max_num`.
```python3
sampler = uq.sampling.RandomSampler(vary=vary, max_num=1e2)
```
The Saltelli algorithm for the computation of the Sobol indices by means of Monte Carlo sampling is instead included in the `MCSampler`. 
The total number of simulations in the campaign is given by `n_mc_samples*(len(vary)+2)`, e.g. if `vary` contains 4 parameters (i.e. `len(vary)=4`) 
then the total number of simulations is `n_mc_samples*(4+2)`. When using this sampler, all variables that would assume integer values 
have to be defined as float because of the joint ditribution constructed via the `chaospy` library.
```python3
sampler = uq.sampling.MCSampler(vary=vary, n_mc_samples=100)
```
Finally the state of the campaign is saved in a `*.json` file 
```python3
campaign.save_state('campaign_state_CT_nobio.json')
```
and the job is executed locally. The name of the campaign state has to be manually modified to ensure uniqueness and avoid overwriting.
To start the job submission process for e.g. Contact Tracing without biology-related uncertainties, type on terminal `> python3 job_submission_corona_CT.py`.

### corona.template
The job submission procedure creates input files with the sampled values for each run in the campaign. In order for these data to be written correctly 
and in an easy to read format, a template as to be provided `corona.template`. Here every parameter listed in the `params` dictionary has to be 
included followed by a space-holder (indicated by the symbol `$`) for the corresponding sampled value, e.g. 
`{"outfile": "$out_file", "seed": "$seed",...}`

## R-scripts
The `*.r` scripts represent implementations of a particular strategy (Flattening the Curve, Contact Tracing, 
Intermittent Lockdown or Phased Opening) in the [virsim](https://gitlab.com/luccoffeng/virsim) model. 
If biology-related parameters are also considered, the suffix `_bio` is present in the filename, 
e.g. `phased_opening_UQ_bio.r`.
Each job submission file links to one of them: `job_submission_FC.py` links to `flattening_the_curve_UQ.r` 
and similarly for the other strategies and for the cases with biology-related parameters included 
(i.e. `job_submission_IL_bio.py` links to `intermittent_lockdown_UQ_bio.r`).

The `*.r` scripts read the input files generated by EasyVVUQ in the job submission procedure, run the model and write an output file with the QoIs. 
They do not need to be manually executed by the user as their execution is part of the job submission procedure.

## Post-processing analyses
Via the campaign state files, EasyVVUQ collects the data and allow the user to perform post-processing analysis. Therefore the user has to be careful 
not to overwrite them and to give them unique filenames such that data of multiple campaigns can be retrieved at once. The variable `workdir` in the 
post-processing scripts must contain the path to the same folder indicated in the job submission file. 
```python3
# Reload the campaign
campaign = uq.Campaign(state_file = "campaign_state_CT.json", work_dir = workdir)
# collate output
campaign.collate()
# get full dataset of data
data = campaign.get_collation_result()
```

### Cdf
The code `cdfs_plot.py` creates the plot of the cdfs for all strategies with and without non-policy-related uncertainties (i.e. 8 empirical cdfs). 
Execute this script by typing on terminal `> python3 cdfs_plot.py`.

The campaigns meant to provide the data for this analysis have to be excuted using the `RandomSampler` of the EasyVVUQ library.

### Sobol indices
The first order Sobol indices are computed with the script `sobols_first.py`. By selecting the campaign states of the four strategies, the respective 
Sobol indices can be computed. Execute this script by typing on terminal, `> python3 sobols_first.py`.

To compute the Sobol indices via the Saltelli algorithm, it is necessary to apply the `QMCAnalysis` object of the EasyVVUQ library. 
Note that `QMCAnalysis` will work only if the campaign used the `MCSampler` (or the `QMCSampler` although the latter is not of interest here) 
and it will not work if the `RandomSampler` has been used instead.
```python3
# Post-processing analysis
qmc_analysis = uq.analysis.QMCAnalysis(sampler=sampler, qoi_cols=output_columns)
campaign.apply_analysis(qmc_analysis)

results = campaign.get_last_analysis()
```
The first order Sobol indices can be retrieved with `results.sobols_first()` and their respective confidence intervals with `results._get_sobols_first_conf(name_QoI, name_param)`. Similar functions are available also for the total Sobol indices. 
The script `sobols_total.py` computes the total Sobol indices and creates the corresponding plot.

### Heatmap
For each strategy considered there is the corresponding Python3 script generating the heatmap: `heatmap_FC.py` corresponds to Flattening the Curve, 
`heatmap_CT.py` to Contact Tracing, `heatmap_IL.py` to Intermittent Lockdown and `heatmap_PO.py` to Phased Opening. Since in Contact Tracing and 
Phased Opening we are considering three parameters, we divide the data per quartiles of one of them and make 2D heatmaps of the resulting subsets. 
In case of Intermittent Lockdown instead we show the data as a function of the two parameters with the highest Sobol indices.
Execute these scripts by typing on terminal, e.g., `> python3 heatmap_FC.py`.

The campaigns meant to provide the data for this analysis have to be excuted using the `RandomSampler` of the EasyVVUQ library.
