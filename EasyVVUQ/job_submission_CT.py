"""
@author: Federica Gugole

__license__ = "LGPL"
"""

import chaospy as cp
import easyvvuq as uq
import os, subprocess

#home dir of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Set up a fresh campaign 
workdir = '/export/scratch2/home/federica/'
campaign = uq.Campaign(name='virsim_CT_nobio_', work_dir=workdir)

# Define parameter space
params = {
    "seed": {
        "type": "integer", # set to "float" when using MCSampler
        "min": 0,
        "max": 2**31,
        "default": 12345},
    "trace_prob_E": {
        "type": "float",
        "min": 0.0,
        "max": 1.0,
        "default": .6},
    "trace_rate_I": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
        "default": .5},
    "trace_contact_reduction": {
        "type": "float",
        "min": 0.0,
        "max": 1.0,
        "default": .6},
    "intervention_effect": {
        "type": "float",
        "min": 0.0,
        "max": 1.0,
        "default": .35},
    "lockdown_effect": {
        "type": "float",
        "min": 0.0,
        "max": 1.0,
        "default": .25},
    "lockdown_length": {
        "type": "float",
        "min": 0.0,
        "max": 300.0,
        "default": 40.0},
    "lift_length": {
        "type": "float",
        "min": 0.0,
        "max": 200.0,
        "default": 20.0},
    "phase_interval": {
        "type": "float",
        "min": 0.0,
        "max": 300.0,
        "default": 45.0},
    "uptake": {
        "type": "float",
        "min": 0.0,
        "max": 1.0,
        "default": 1.0},
    "Rzero": {
        "type": "float",
        "min": 0.0,
        "max": 5.0,
        "default": 2.5},
    "duration_infectiousness": {
        "type": "float",
        "min": 0.0,
        "max": 10.0,
        "default": 5.0},
    "shape_exposed_time": {
        "type": "float",
        "min": 0.0,
        "max": 50.0,
        "default": 20.0},
    "intervention_effect_var_inv": {
        "type": "float",
        "min": 0.0,
        "max": 10.0,
        "default": 0.1},
    "out_file": {
        "type": "string",
        "default": "output.csv"}}
    
output_filename = params["out_file"]["default"]
output_columns = ["IC_prev_avg_max","IC_ex_max"]

encoder = uq.encoders.GenericEncoder(
    template_fname= HOME + '/corona.template',
    delimiter='$',
    target_filename='corona_in.json')
decoder = uq.decoders.SimpleCSV(target_filename=output_filename,
                                output_columns=output_columns)

campaign.add_app(name='mc',
                    params=params,
                    encoder=encoder,
                    decoder=decoder) 

# Create the sampler
vary = {
    "seed": cp.DiscreteUniform(2**14, 2**16),
    "trace_prob_E": cp.Beta(alpha=2, beta=6),
    "trace_rate_I": cp.Gamma(shape=2, scale=.2),
    "trace_contact_reduction": cp.Beta(alpha=10, beta=2)
}

# For estimation of the cdf and heatmap
sampler = uq.sampling.RandomSampler(vary=vary, max_num=1e3)

# For the computation of the Sobol indices
# sampler = uq.sampling.MCSampler(vary=vary, n_mc_samples=100)

# Associate the sampler with the campaign
campaign.set_sampler(sampler)

# Will draw all (of the finite set of samples)
campaign.draw_samples()

campaign.populate_runs_dir()

# Save the campaign
campaign.save_state('campaign_state_CT_nobio_1k.json')

# Run execution sequentially 
#campaign.apply_for_each_run_dir(uq.actions.ExecuteLocal('contact_tracing_UQ.r corona_in.json', interpret='Rscript'))

# Run execution in parallel without Fabsim (using gnu parallel)
cwd = os.getcwd()
pcmd = f"ls -d {campaign.campaign_dir}/runs/Run_* | parallel -j 4 'cd {{}} ; Rscript {cwd}/contact_tracing_UQ.r corona_in.json > output.txt ; cd .. '"
print('Parallel run command: ',pcmd)
subprocess.call(pcmd,shell=True)

print('Job submission complete')

### END OF CODE ###
