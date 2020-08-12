
% start uqlab
uqlab;

InputOpts.Marginals(1).Name = 'test';
InputOpts.Marginals(1).Type = 'Gamma';
InputOpts.Marginals(1).Parameters = [1/0.4 2];

% create input object with UQLab
myInput = uq_createInput(InputOpts);

% display input properties
uq_print(myInput);
uq_display(myInput);

% compare with Matlab Gamma function
figure
x = linspace(0,3,100);
plot(x,gampdf(x,2,0.4))