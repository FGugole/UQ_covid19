%% Parametric uncertainty quantification on ODE model for COVID-19 outbreak
% this code is using the Virsim model from Luc Coffeng,
% see GitLab, luccoffeng/virsim,
% in order to investigate parametric uncertainty using the UQLab toolbox,
% https://www.uqlab.com/

% this code uses:
% -UQLab (Matlab package)
% -Virsim (R package)
% -this script

% you need to provide:
% * R-file that calls Virsim, e.g. contact_tracing_UQ.R
% * same R-file but then with uncertain parameters replaced by <X0001> etc,
%   e.g. test_matlab_run.R.tpl
% * file to read the virsim output, e.g. read_virsim_qoi.m
% * make sure that a CSV file is created by Virsim and that the name
%   corresponds to the name provided below

% outputs are stored in runs/

clearvars
close all
clc

%% general settings

% UQLab installation path
UQLab_path     = '/Users/sanderse/Dropbox/work/Programming/UQ/UQLabCore_Rel1.3.0/';

% R filename
filename_R     = 'contact_tracing_UQ.r'; % pointing to R file in current directory

% Matlab filename that processes Virsim output
process_output = 'read_virsim_qoi';

% CSV filename that is created by Virsim when executing filename_R
virsim_output  = 'output_contact_tracing.csv';

%% input uncertainties

% load case-specific parameters
% run(input_file);
InputOpts.Marginals(1).Name = 'Trace-prob-E';
InputOpts.Marginals(1).Type = 'Beta';
InputOpts.Marginals(1).Parameters = [6 4];

InputOpts.Marginals(2).Name = 'Trace-rate-I';
InputOpts.Marginals(2).Type = 'Gamma';
InputOpts.Marginals(2).Parameters = [2 0.4];

InputOpts.Marginals(3).Name = 'Trace-contact-red';
InputOpts.Marginals(3).Type = 'Beta';
InputOpts.Marginals(3).Parameters = [10 2];

InputOpts.Marginals(4).Name = 'Seed';
InputOpts.Marginals(4).Type = 'Uniform';
InputOpts.Marginals(4).Parameters = [2^14 2^16];


% dimension of parameter space:
ndim = length(InputOpts.Marginals);



%% method options

% specify which methods should be run
% pick from: 'MC','PCE_OLS','PCE_LARS','PCE_Quad'
% methods = {'MC','PCE_OLS','PCE_LARS'};
methods = {'MC'};
% methods = {'MC','PCE_OLS'};

% % for Monte Carlo, specify number of times to repeat MC-based methods to obtain 'nice' convergence
% % graphs
MC_repeat = 1;
% % number of samples with MC
NsamplesMC = [100]; % 10 20 40 80]; % 160 320]; %[1e1 1e2 1e3 1e4];
%
% % for PCE-Quad, specify the polynomial degrees to be tested
% DegreesQuad = 1:3; %[1 2 3 4 5 6];
%
% % for PCE-OLS:
NsamplesOLS = [5 10]; % 40 80 160 320]; % if not specified, the number of samples from Quad is taken
OLS_repeat = 1; % like MC_repeat
%
% % for PCE-LARS:
% NsamplesLARS = 320; %[5 10 20 40 80 160 320]; % if not specified, the number of samples from Quad is taken
% LARS_repeat = 1; % like MC_repeat
%

% Sobol options
Sobol_analysis = false;
% SobolOpts.Type        = 'Sensitivity';
% SobolOpts.Method      = 'Sobol';
% SobolOpts.Sobol.Order = 1;
%
% % if available, give exact mean and std
% % mean_exact =
% % std_exact

%% set model options
% example of system call: [status,result]=system('/usr/local/bin/Rscript test_system_run.R')

% create UQLink model which is useful to interface with external software
% by using input templates
ModelOpts.Type = 'UQLink';
ModelOpts.Name = 'Virsim';
% command to execute the R script
ModelOpts.Command = ['/usr/local/bin/Rscript ' filename_R];
% template file
ModelOpts.Template = [filename_R '.tpl'];
% name of m-file that processes the R output
ModelOpts.Output.Parser   = process_output;
% filename that contains the R output
ModelOpts.Output.FileName = virsim_output;

% other options
ModelOpts.Counter.Digits = 6; % (default value 6)
ModelOpts.Format = {'%.8f','%.8f','%.8f','%.0f'}; % notation for variables, can also be an array, e.g. {'%1.8e','%2.6f'}
ModelOpts.Archiving.Action = 'save';
ModelOpts.Archiving.FolderName = 'runs';
ModelOpts.Archiving.Zip = false ;
ModelOpts.Display = 'quiet'; % Set the display to quiet



%% now let's do some UQ
addpath(genpath(UQLab_path));

% start uqlab
uqlab;

% create and add the model to UQLab
myModel = uq_createModel(ModelOpts);
% create input object with UQLab
myInput = uq_createInput(InputOpts);

% display input properties
uq_print(myInput);
uq_display(myInput);


%%

if (exist('mean_exact','var'))
    compare_mean = 1;
else
    compare_mean = 0;
end
if (exist('std_exact','var'))
    compare_std = 1;
else
    compare_std = 0;
end


%% run UQLab with different UQ methods: MC and PCE

if (find(strcmp(methods,'MC')))
    
    disp('=========MC==========');
    N_MC     = length(NsamplesMC);
    mean_MC  = zeros(MC_repeat,N_MC);
    std_MC   = zeros(MC_repeat,N_MC);
    if (Sobol_analysis)
        Sobol_MC_FirstOrder = zeros(MC_repeat,N_MC,ndim);
        Sobol_MC_Total      = zeros(MC_repeat,N_MC,ndim);
        Sobol_MC_Nsamples   = zeros(N_MC,1);
    end
    
    
    % perform multiple runs to decrease effect of random sampling
    for k = 1:MC_repeat
        for i=1:N_MC
            
            disp(NsamplesMC(i));
            % get random samples ('experimental design')
            X_ED = uq_getSample(NsamplesMC(i),'MC');
            
            % evaluate model at sample
            Y_ED = uq_evalModel(myModel,X_ED);
            
            % moments of solution
            mean_MC(k,i) = mean(Y_ED);
            std_MC(k,i)  = std(Y_ED);
            
            if (Sobol_analysis)
                
                % Sobol analysis;
                SobolOpts.Sobol.SampleSize = NsamplesMC(i);
                SobolAnalysis_MC           = uq_createAnalysis(SobolOpts);
                SobolResults_MC            = SobolAnalysis_MC.Results;
                Sobol_MC_FirstOrder(k,i,1:ndim) = SobolResults_MC.FirstOrder;
                Sobol_MC_Total(k,i,1:ndim)      = SobolResults_MC.Total;
                Sobol_MC_Nsamples(i)          = SobolResults_MC.Cost;
            end
        end
    end
    
    if (Sobol_analysis)
        % take average over first dimension (multiple MC runs)
        AVG_Sobol_MC_FirstOrder = squeeze(mean(Sobol_MC_FirstOrder,1));
        AVG_Sobol_MC_Total      = squeeze(mean(Sobol_MC_Total,1));
    end
    %
    if (compare_mean == 1)
        err_mean_MC = abs((mean(mean_MC,1)-mean_exact)/mean_ref);
    end
    if (compare_std == 1)
        err_std_MC = abs((mean(std_MC,1)-std_exact)/std_ref);
    end
    
end
%% Polynomial Chaos with quadrature

if (find(strcmp(methods,'PCE_Quad')))
    
    disp('=========PCE==========');
    
    N_Quad      = length(DegreesQuad);
    NsamplesQuad = zeros(N_Quad,1);
    mean_Quad    = zeros(N_Quad,1);
    std_Quad     = zeros(N_Quad,1);
    Sobol_Quad_FirstOrder = zeros(N_Quad,ndim);
    Sobol_Quad_Total = zeros(N_Quad,ndim);
    
    % set up PCE metamodel
    metamodelQuad.FullModel = myModel;
    metamodelQuad.Input     = myInput;
    metamodelQuad.Type      = 'Metamodel';
    metamodelQuad.MetaType  = 'PCE';
    
    metamodelQuad.Method          = 'Quadrature' ;
    metamodelQuad.Quadrature.Type = 'Full';
    
    for i = 1:N_Quad
        
        metamodelQuad.Degree = DegreesQuad(i);
        myPCE_Quad           = uq_createModel(metamodelQuad);
        
        % moments of solution
        NsamplesQuad(i) = myPCE_Quad.ExpDesign.NSamples;
        mean_Quad(i)    = myPCE_Quad.PCE.Moments.Mean;
        std_Quad(i)     = sqrt(myPCE_Quad.PCE.Moments.Var);
        
        if (Sobol_analysis)
            % Sobol analysis
            % note the same options structure SobolOpts can be re-used to create a new analysis on the PCE model
            SobolAnalysis_Quad    = uq_createAnalysis(SobolOpts);
            SobolResults_Quad     = SobolAnalysis_Quad.Results;
            Sobol_Quad_FirstOrder(i,1:ndim) = SobolResults_Quad.FirstOrder;
            Sobol_Quad_Total(i,1:ndim)      = SobolResults_Quad.Total;
        end
    end
    
    if (compare_mean == 1)
        err_mean_Quad =  abs((mean_Quad - mean_exact)/mean_ref);
    end
    if (compare_std == 1)
        err_std_Quad  =  abs((std_Quad - std_exact)/std_ref);
    end
    
end
%% Polynomial Chaos with ordinary least squares (OLS)

if (find(strcmp(methods,'PCE_OLS')))
    
    disp('=========OLS==========');
    
    if (~exist('NsamplesOLS','var'))
        if (find(strcmp(methods,'PCE_Quad')))
            % we specify number of OLS samples based on samples used with
            % quadrature
            NsamplesOLS = NsamplesQuad;
            warning('number of OLS samples taken based on number of Quadrature samples');
        else
            error('please specify NsamplesOLS');
        end
    end
    
    N_OLS       = length(NsamplesOLS);
    mean_OLS    = zeros(OLS_repeat, N_OLS);
    std_OLS     = zeros(OLS_repeat, N_OLS);
    Sobol_OLS_FirstOrder = zeros(OLS_repeat, N_OLS, ndim);
    Sobol_OLS_Total      = zeros(OLS_repeat, N_OLS, ndim);
    
    metamodelOLS.FullModel = myModel;
    metamodelOLS.Input     = myInput;
    metamodelOLS.Type      = 'Metamodel';
    metamodelOLS.MetaType  = 'PCE';
    metamodelOLS.Method    = 'OLS';
    % specify array of possible degrees;
    % the degree with the lowest Leave-One-Out cross-validation error (LOO error)
    % is automatically selected:
    metamodelOLS.Degree    = 1:4;
    
    % if there are issues with LOO, try the following: metamodelOLS.OLS.ModifiedLOO = 0;
    % note that default sampling is LHS, this can be changed (see below)
    
    % as there is randomness in the experimental design, we can
    % average over several runs
    for k = 1:OLS_repeat
        for i = 1:N_OLS
            
            metamodelOLS.ExpDesign.NSamples = NsamplesOLS(i);
            metamodelOLS.ExpDesign.Sampling = 'LHS'; % LHS is default
            myPCE_OLS = uq_createModel(metamodelOLS);
            
            % moments of solution
            mean_OLS(k,i) = myPCE_OLS.PCE.Moments.Mean;
            std_OLS(k,i)  = sqrt(myPCE_OLS.PCE.Moments.Var);
            
            if (Sobol_analysis)
                % Sobol analysis
                % note the same options structure SobolOpts can be re-used to create a new analysis on the PCE model
                SobolAnalysis_OLS    = uq_createAnalysis(SobolOpts);
                SobolResults_OLS     = SobolAnalysis_OLS.Results;
                Sobol_OLS_FirstOrder(k,i,1:ndim) = SobolResults_OLS.FirstOrder;
                Sobol_OLS_Total(k,i,1:ndim)      = SobolResults_OLS.Total;
            end
        end
        
    end
    
    if (Sobol_analysis)
        % take average over first dimension (multiple OLS runs)
        AVG_Sobol_OLS_FirstOrder = squeeze(mean(Sobol_OLS_FirstOrder,1));
        AVG_Sobol_OLS_Total      = squeeze(mean(Sobol_OLS_Total,1));
    end
    
    % take mean over first dimension (k)
    if (compare_mean == 1)
        err_mean_OLS =  abs((mean(mean_OLS,1)-mean_exact)/mean_ref);
    end
    if (compare_std == 1)
        err_std_OLS =  abs((mean(std_OLS,1)-std_exact)/std_ref);
    end
    
end

%% Polynomial Chaos with LARS
if (find(strcmp(methods,'PCE_LARS')))
    
    disp('=========LARS==========');
    
    if (~exist('NsamplesLARS','var'))
        if (find(strcmp(methods,'PCE_Quad')))
            % we specify number of OLS samples based on samples used with
            % quadrature
            NsamplesLARS = NsamplesQuad;
            warning('number of LARS samples taken based on number of Quadrature samples');
        else
            error('please specify NsamplesLARS');
        end
    end
    
    N_LARS       = length(NsamplesLARS);
    mean_LARS    = zeros(LARS_repeat, N_LARS);
    std_LARS     = zeros(LARS_repeat, N_LARS);
    
    if (Sobol_analysis)
        Sobol_LARS_FirstOrder = zeros(LARS_repeat, N_LARS, ndim);
        Sobol_LARS_Total      = zeros(LARS_repeat, N_LARS, ndim);
    end
    
    metamodelLARS.FullModel = myModel;
    metamodelLARS.Input     = myInput;
    metamodelLARS.Type      = 'Metamodel';
    metamodelLARS.MetaType  = 'PCE';
    metamodelLARS.Method    = 'LARS';
    metamodelLARS.Degree    = 1:4; % this automatically switches on degree adaptive PCE
    metamodelLARS.TruncOptions.qNorm = 0.75;
    
    % as there is randomness in the experimental design, we can
    % average over several runs
    for k = 1:LARS_repeat
        for i = 1:N_LARS
            
            % use manual experimental design:
            %         X_ED = uq_getSample(NsamplesLARS(i),'MC') ;
            %         Y_ED = uq_evalModel(myModel,X_ED);
            %         metamodelLARS.ExpDesign.X = X_ED;
            %         metamodelLARS.ExpDesign.Y = Y_ED;
            
            
            % use sampling strategy, note that default is MC!
            metamodelLARS.ExpDesign.Sampling = 'LHS'; % or 'LHS' or 'Sobol' or 'Halton'
            metamodelLARS.ExpDesign.NSamples = NsamplesLARS(i);
            myPCE_LARS     = uq_createModel(metamodelLARS);
            
            % moments of solution
            mean_LARS(k,i) = myPCE_LARS.PCE.Moments.Mean;
            std_LARS(k,i)  = sqrt(myPCE_LARS.PCE.Moments.Var);
            
            if (Sobol_analysis)
                % Sobol analysis
                %             note the same options structure SobolOpts can be re-used to create a new analysis on the PCE model
                SobolAnalysis_LARS    = uq_createAnalysis(SobolOpts);
                SobolResults_LARS     = SobolAnalysis_LARS.Results;
                Sobol_LARS_FirstOrder(k, i, 1:ndim) = SobolResults_LARS.FirstOrder;
                Sobol_LARS_Total(k, i, 1:ndim)      = SobolResults_LARS.Total;
            end
        end
    end
    
    if (Sobol_analysis)
        % take average over first dimension (multiple LARS runs)
        AVG_Sobol_LARS_FirstOrder = squeeze(mean(Sobol_LARS_FirstOrder,1));
        AVG_Sobol_LARS_Total      = squeeze(mean(Sobol_LARS_Total,1));
    end
    
    if (compare_mean == 1)
        err_mean_LARS =  abs((mean(mean_LARS,1)-mean_exact)/mean_ref);
    end
    if (compare_std == 1)
        err_std_LARS =  abs((mean(std_LARS,1)-std_exact)/std_ref);
    end
    
end



%%
post_processing;