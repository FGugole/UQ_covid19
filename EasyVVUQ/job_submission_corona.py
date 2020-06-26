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
    "intervention_effect_1": {
        "type": "float",
        "min": .25,
        "max": .45,
        "default": .35},
    "intervention_effect_2": {
        "type": "float",
        "min": .45,
        "max": .65,
        "default": .55},
    "intervention_interval": {
        "type": "float",
        "min": 20,
        "max": 400,
        "default": 365},
    "trace_prob_E": {
        "type": "float",
        "min": 0.0,
        "max": 1.0,
        "default": .6},
    "trace_rate_I": {
        "type": "float",
        "min": 0.0,
        "max": 1.0,
        "default": .5},
    "trace_contact_reduction": {
        "type": "float",
        "min": 0.0,
        "max": 1.0,
        "default": .6},
    "uptake": {
        "type": "float",
        "min": 0.0,
        "max": 1.0,
        "default": 1.0},
    "efoi": {
        "type": "float",
        "min": 0.0,
        "max": .1,
        "default": .05},
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
#my_campaign.add_app(name="pce",
#                    params=params,
#                    encoder=encoder,
#                    decoder=decoder,
#                    collater=collater) 

# Create the sampler
vary = {
#    "intervention_effect_1": cp.Uniform(.3, .4),
#    "intervention_effect_2": cp.Uniform(.5, .6),
    "intervention_interval": cp.DiscreteUniform(30, 90),
    "trace_prob_E": cp.Uniform(.4, .8),
    "trace_rate_I": cp.Uniform(.3, .6),
    "trace_contact_reduction": cp.Uniform(.6, .8),
#    "efoi": cp.Uniform(0.0, .1)
    "uptake": cp.Uniform(0.8, 1)
}

my_sampler = uq.sampling.SCSampler(vary=vary, polynomial_order=4, 
                                   quadrature_rule='G', sparse=False)
#my_sampler = uq.sampling.PCESampler(vary=vary, polynomial_order=2)

# Associate the sampler with the campaign
my_campaign.set_sampler(my_sampler)

# Will draw all (of the finite set of samples)
my_campaign.draw_samples()

my_campaign.populate_runs_dir()

#Run execution sequentially 
#my_campaign.apply_for_each_run_dir(uq.actions.ExecuteLocal('flattening_the_curve_UQ.r corona_in.json', interpret='Rscript'))
#my_campaign.apply_for_each_run_dir(uq.actions.ExecuteLocal('contact_tracing_UQ.r corona_in.json', interpret='Rscript'))

# Run execution in parallel without Fabsim (using gnu parallel)
cwd = os.getcwd()
pcmd = f"ls -d {my_campaign.campaign_dir}/runs/Run_* | parallel -j 4 'cd {{}} ; Rscript {cwd}/contact_tracing_UQ.r corona_in.json > output.txt ; cd .. '"
print('Parallel run command: ',pcmd)
subprocess.call(pcmd,shell=True)

#Save the Campaign
my_campaign.save_state("campaign_state.json")

print('Job submission complete')

### END OF CODE ###