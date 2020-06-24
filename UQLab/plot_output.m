% load multiple csv's and plot results

folder_name = 'runs/UQLinkOutput/';
file_name   = 'virsim_results';
file_ext    = '.csv';
n_start  = 1;
n_end    = 20;
n_digits = 6;

figure(101)
for i=n_start:n_end
    
    n_zero = n_digits - length(num2str(i));
    zeros  = num2str(10^n_zero);
    T      = readtable([folder_name file_name zeros(2:end) num2str(i) file_ext]);
    
    plot(T.time,T.I)
    hold on
end
grid
