"""
@author: Federica Gugole

__license__ = "LGPL"
"""

import chaospy as cp
import easyvvuq as uq
import os, subprocess

#home dir of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Set up a fresh campaign called "corona"
my_campaign = uq.Campaign(name='corona', work_dir='/tmp')

# Define parameter space
params = {
    "seed": {
        "type": "float",
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
output_columns = ["S","E","I","R","IC_inc","IC_prev","IC_prev_avg","IC_prev_avg_max","IC_ex","IC_ex_max"]

encoder = uq.encoders.GenericEncoder(
    template_fname= HOME + '/corona.template',
    delimiter='$',
    target_filename='corona_in.json')
decoder = uq.decoders.SimpleCSV(target_filename=output_filename,
                                output_columns=output_columns,
                                header=0)
collater = uq.collate.AggregateSamples(average=False)

# Add the SC app (automatically set as current app)
my_campaign.add_app(name="sc",
                    params=params,
                    encoder=encoder,
                    decoder=decoder,
                    collater=collater) 

# Create the sampler
vary = {
    "seed": cp.DiscreteUniform(2**14, 2**16),
    # "trace_prob_E": cp.Beta(alpha=2, beta=4),
    # "trace_rate_I": cp.Gamma(shape=2, scale=.4),
    # "trace_contact_reduction": cp.Beta(alpha=10, beta=2),
    # "intervention_effect": cp.Beta(alpha=38, beta=70),
    "lockdown_effect": cp.Beta(alpha=14, beta=42),
    "lockdown_length": cp.Gamma(shape=20, scale=2),
    "lift_length": cp.Gamma(shape=15, scale=1),
    # "phase_interval": cp.Gamma(shape=25, scale=2),
    "uptake": cp.Beta(alpha=16, beta=2),
    # "Rzero": cp.Gamma(shape=100,scale=.025),
    # "duration_infectiousness": cp.Gamma(shape=25,scale=.2), 
    # "shape_exposed_time": cp.Gamma(shape=17.5,scale=1),
    # "intervention_effect_var_inv": cp.Gamma(shape=2,scale=.05)
}

#my_sampler = uq.sampling.SCSampler(vary=vary, polynomial_order=3, 
#                                   quadrature_rule='G', sparse=False)
my_sampler = uq.sampling.RandomSampler(vary=vary, max_num=1e3)

# Associate the sampler with the campaign
my_campaign.set_sampler(my_sampler)

# Will draw all (of the finite set of samples)
my_campaign.draw_samples()

my_campaign.populate_runs_dir()

#Run execution sequentially 
#my_campaign.apply_for_each_run_dir(uq.actions.ExecuteLocal('flattening_the_curve_UQ.r corona_in.json', interpret='Rscript'))

# Run execution in parallel without Fabsim (using gnu parallel)
cwd = os.getcwd()
pcmd = f"ls -d {my_campaign.campaign_dir}/runs/Run_* | parallel -j 8 'cd {{}} ; Rscript {cwd}/intermittent_lockdown_UQ.r corona_in.json > output.txt ; cd .. '"
print('Parallel run command: ',pcmd)
subprocess.call(pcmd,shell=True)

#Save the Campaign
my_campaign.save_state("campaign_state.json")

print('Job submission complete')

### END OF CODE ###
