The `job_submission_*_fab.py` scripts in this subfolder make use of the [FabSim3](https://github.com/djgroen/FabSim3) v2.6 and [QCG-PilotJob](https://github.com/vecma-project/QCG-PilotJob) v0.10.0 packages. 
These libraries allow to execute the job on an external computer (e.g. a supercomputer) and retrieve the data on the local machine such that post-processing analysis can be done locally. 
These scripts cannot be run per-se in the current folder as they have to be located in the FabSim3 root to make use of the FabSim3 functionalities. 
We report them here for sake of completeness.

We invite the interested user to check the respective GitHub repositories for more info about installation and configuration of the [FabSim3](https://github.com/djgroen/FabSim3) and [QCG-PilotJob](https://github.com/vecma-project/QCG-PilotJob) packages.
Examples on how to integrate EasyVVUQ and FabSim3 (including the application to our case) can be found in [FabUQCampaign](https://github.com/wedeling/FabUQCampaign).
