function Y = read_virsim(outputfile)
%READ_VIRSIM Summary of this function goes here
%   Detailed explanation goes here
% row_start = 1;
% col_start = 0;
%  Y: [day S E I R INC]

% read CSV created by Virsim

% using csvread:
% D = csvread(outputfile,row_start,col_start);
% Using tableread:
T = readtable(outputfile);

% select a QoI:
% moving mean of I, 20 days
MM_I = movmean(T.I, 20);
% take maximum:
Y    = max(MM_I);

% alternative QoI: number of person days, where IC capacity is exceeded (in
% excess of 108 per million)

end

