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
The scripts can be executed on the local machine. The codes present in the folder `<job_sub_fab>` instead submit the job to an external 
supercomputer by means of the [FabSim3](https://github.com/djgroen/FabSim3) and [QCG-PJ](https://github.com/vecma-project/QCG-PilotJob) libraries. 
These two libraries are therefore necessary for the execution of the codes in the `<job_sub_fab>` folder and we refer the reader to 
the GitHub repositories of FabSim3 and QCG-PJ for details about their installation and on how to configure the local and external machine.

## Start a campaign
`<job_submission_*.py>` starts an uncertainty quantification (UQ) campaign for a selected strategy: FC = Flattening the Curve, 
CT = Contact Tracing, IL = Intermittent Lockdown, PO = Phased Opening. Scripts with the suffix `<_bio>` in the filename, e.g. 
`<job_submission_corona_CT_bio.py>`, include uncertainties also in biology-related parameter which are otherwise not considered. 
The following holds for both the cases with or without biology-related uncertainties. I use code pieces from `<job_submission_corona_CT.py>` 
to explain the main structure of the job submission procedure.

After the necessary imports, a new campaign is initialized 
```python3
workdir = '/export/scratch2/home/federica/'
my_campaign = uq.Campaign(name='virsim_CT_nobio_', work_dir=workdir)
```
These lines will create a folder named `<virsim_CT_nobio_*>` in the working directory specified by `<workdir>` which has to 
be modified by the reader such that it points to a folder present in their local machine. EasyVVUQ adds by default 8 random symbols 
(i.e. letters or numbers) to the name such that the names of the folders are automatically unique and there is no need for manual changes. 

Afterwards a dictionary `<params>` of the parameters involved in the UQ analysis containing type, minimum, maximum and default values 
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

The `<vary>` dicitionary contains the input distributions for the parameters. Note that those parameters listed in `<params>` 
but not specified here will automatically assume the default value specified above.
```python3
vary = {
    "seed": cp.DiscreteUniform(2**14, 2**16),
    ... 
    }
```
At this point a sampler method has to be specified. The `<RandomSampler>` provided by EasyVVUQ is classic Monte Carlo sampling and 
we use it to obtain the data for the empirical cdfs and the heatmaps. The total number of simulations in the campaign is given by `<max_num>`.
```python3
my_sampler = uq.sampling.RandomSampler(vary=vary, max_num=1e2)
```
The Saltelli algorithm for the computation of the Sobol indices by means of Monte Carlo sampling is instead included in the `<MCSampler>`. 
The total number of simulations in the campaign is given by `<n_mc_samples*(len(vary)+2)>`, e.g. if `<vary>` contains 3 parameters (i.e. `<len(vary)=4>`) 
then the total number of simulations is `<n_mc_samples*(4+2)>`.
```python3
my_sampler = uq.sampling.MCSampler(vary=vary, n_mc_samples=200)
```
Finally the state of the campaign is saved in a `<.json>` file 
```python3
my_campaign.save_state('campaign_state_CT_nobio.json')
```
and the job is executed locally. The name of the campaign state has to be manually modified to ensure uniqueness and avoid overwriting.

### corona.template
The job submission procedure creates input files with the sampled values for each run in the campaign. In order for these data to be written correctly 
and in an easy to read format, a template as to be provided `<corona.template>`. Here every parameter listed in the `<params>` dictionary has to be 
included followed by a space-holder for the corresponding sampled value, e.g. 
`<{"outfile": "$out_file", "seed": "$seed",...}>`

## The R-scripts
The `<*.r>` scripts represent implementations of a particular strategy (Flattening the Curve, Contact Tracing, 
Intermittent Lockdown or Phased Opening) in the [virsim](https://gitlab.com/luccoffeng/virsim) model. 

## Post-processing
### Cdf
### Heatmap
### Sobol indices

```python3
```
`<>`
