function Y = read_virsim_full(outputfile)
%READ_VIRSIM read entire simulation result, i.e. the  S E I R etc. values
%as a function of time
% row_start = 1;
% col_start = 0;
%  Y: [day S E I R INC]

% read CSV created by Virsim

% using csvread:
% D = csvread(outputfile,row_start,col_start);
% Using tableread:
T = readtable(outputfile);

% select a QoI:
% moving mean of I, 30 days
MM_I = movmean(T.I, 30);
% take maximum:
Y    = max(MM_I);

% alternative QoI: number of person days, where IC capacity is exceeded (in
% excess of 108 per million)

end

