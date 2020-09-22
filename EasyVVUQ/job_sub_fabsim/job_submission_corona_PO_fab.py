"""
@author: Federica Gugole

__license__ = "LGPL"
"""

import chaospy as cp
import easyvvuq as uq
import os, subprocess
import fabsim3_cmd_api as fab

config = 'virsim'
script = 'virsim_PO'
machine = 'eagle_vecma'
workdir = '/home/federica/Desktop/VirsimCampaigns'#'/tmp'

#home dir of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

# Set up a fresh campaign called "virsim_PO"
campaign = uq.Campaign(name='virsim_PO', work_dir=workdir)

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
campaign.add_app(name="sc",
                    params=params,
                    encoder=encoder,
                    decoder=decoder,
                    collater=collater) 

# Create the sampler
vary = {
    "seed": cp.DiscreteUniform(2**14, 2**16),
    "lockdown_effect": cp.Beta(alpha=14, beta=42),
    "phase_interval": cp.Gamma(shape=25, scale=2),
    "uptake": cp.Beta(alpha=16, beta=2),
    # "Rzero": cp.Gamma(shape=100,scale=.025),
    # "duration_infectiousness": cp.Gamma(shape=25,scale=.2), 
    # "shape_exposed_time": cp.Gamma(shape=17.5,scale=1),
    # "intervention_effect_var_inv": cp.Gamma(shape=2,scale=.05)
}

#sampler = uq.sampling.SCSampler(vary=vary, polynomial_order=3, 
#                                   quadrature_rule='G', sparse=False)
sampler = uq.sampling.QMCSampler(vary=vary, n_mc_samples=2)

# Associate the sampler with the campaign
campaign.set_sampler(sampler)

# Will draw all (of the finite set of samples)
campaign.draw_samples()
campaign.populate_runs_dir()

# run the UQ ensemble
fab.run_uq_ensemble(config, campaign.campaign_dir, script=script,
                    machine=machine, PilotJob = True)

#wait for job to complete
# fab.wait(machine=machine)

#wait for jobs to complete and check if all output files are retrieved 
#from the remote machine
fab.verify(config, campaign.campaign_dir, 
            campaign._active_app_decoder.target_filename, 
            machine=machine, PilotJob=True)

#run the UQ ensemble
fab.get_uq_samples(config, campaign.campaign_dir, sampler._n_samples,
                   skip=0, machine='eagle_vecma')
campaign.collate()

#Save the Campaign
campaign.save_state("campaign_state_PO.json")

# # collate output
# # get full dataset of data
# data = campaign.get_collation_result()
# # print(data)

# # Post-processing analysis
# qmc_analysis = uq.analysis.QMCAnalysis(sampler=sampler, qoi_cols=output_columns)
# campaign.apply_analysis(qmc_analysis)

# results = campaign.get_last_analysis()
# print(results)

print('Job submission complete')

### END OF CODE ###
