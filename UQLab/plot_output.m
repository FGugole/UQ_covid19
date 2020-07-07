% load multiple csv's and plot results

%% settings
folder_name = 'runs/UQLinkOutput/';
file_name   = 'output_contact_tracing';%'virsim_results';
file_ext    = '.csv';
n_start  = 1;
n_end    = 10;
n_digits = 6;

avg_window = 30;
IC_capacity = 108;


%% start
j = 0;
n_tot = n_end - n_start + 1;
IC_avg_max = zeros(n_tot,1);
ind_max    = zeros(n_tot,1);
Y = zeros(n_tot,2); % QoIs

for i=n_start:n_end
    
    j      = j+1;
    
    % read file
    n_zero = n_digits - length(num2str(i));
    zeros  = num2str(10^n_zero);
    T      = readtable([folder_name file_name zeros(2:end) num2str(i) file_ext]);
    
    % process data to get QoIs
    IC_avg = movmean(T.IC_prev,avg_window);
    [IC_avg_max(j), ind_max(j)] = max(IC_avg);
    IC_excess = cumsum(max(0,T.IC_prev - IC_capacity));
    
    Y(j,1) = IC_avg_max(j);
    Y(j,2) = IC_excess;
    
    figure(101)
    %     plot(T.time,T.IC_prev_avg)
    %     hold on
    plot(T.time,IC_avg,'-')
    hold on
    plot(T.time(ind_max(j)),IC_avg_max(j),'o');
    
    figure(102)
    plot(T.time,IC_excess);
    
end

figure(101)
grid on
ylabel('Moving average of total IC patients');

figure(102)
grid on
ylabel('cumulative excess in IC person-days');