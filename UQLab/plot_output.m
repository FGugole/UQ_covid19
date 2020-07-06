% load multiple csv's and plot results

folder_name = 'runs/UQLinkOutput/';
file_name   = 'output_contact_tracing';%'virsim_results';
file_ext    = '.csv';
n_start  = 1;
n_end    = 10;
n_digits = 6;

figure(101)
for i=n_start:n_end
    
    n_zero = n_digits - length(num2str(i));
    zeros  = num2str(10^n_zero);
    T      = readtable([folder_name file_name zeros(2:end) num2str(i) file_ext]);
    
    figure(101)
%     plot(T.time,T.IC_prev_avg)
%     hold on
%     
%     figure (102)
    plot(T.time,movmean(T.IC_prev,30),'-')
    hold on
%     MM_I = movmean(T.IC_prev, 30);
end
grid
