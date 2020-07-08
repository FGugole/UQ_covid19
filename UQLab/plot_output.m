% load multiple csv's and plot results
clearvars
close all

%% settings
folder_name = 'runs_FC_MC100/UQLinkOutput/';
file_name   = 'output_flattening_the_curve';
file_ext    = '.csv';
n_start  = 1;
n_end    = 100;
n_digits = 6;

avg_window  = 30;
IC_capacity = 108;

% UQLab results synthesis in MAT file
matfile_name = 'runs_FC_MC100/Virsim_FC_MC100.mat';


%% get colormap
figure(101)
cmap = get(gca,'ColorOrder');
nc   = size(cmap,1);

%% start loading data
j = 0;
n_tot = n_end - n_start + 1;
IC_avg_max     = zeros(n_tot,1);
ind_avg_max    = zeros(n_tot,1);
IC_excess_max  = zeros(n_tot,1);
ind_excess_max = zeros(n_tot,1);

Y = zeros(n_tot,2); % QoIs

for i=n_start:n_end
    
    j      = j+1;
    
    % read file
    n_zero = n_digits - length(num2str(i));
    zeros  = num2str(10^n_zero);
    T      = readtable([folder_name file_name zeros(2:end) num2str(i) file_ext]);
    
    % process data to get QoIs
    % moving average of IC cases
    IC_avg = movmean(T.IC_prev,avg_window);
    [IC_avg_max(j), ind_avg_max(j)] = max(IC_avg);
    % cumulative excess capacity
    IC_excess = cumsum(max(0,T.IC_prev - IC_capacity));
    [IC_excess_max(j), ind_excess_max(j)] = max(IC_excess);
    
    
    Y(j,1) = IC_avg_max(j);
    Y(j,2) = IC_excess_max(j);
    
    figure(101)
    
    %     plot(T.time,T.IC_prev_avg)
    %     hold on
    j_mod = mod(j-1,nc)+1;
    plot(T.time,IC_avg,'-','Color',cmap(j_mod,:))
    hold on
    plot(T.time(ind_avg_max(j)),IC_avg_max(j),'o','Color',cmap(j_mod,:));
    
    figure(102)
    plot(T.time,IC_excess);
    hold on
%     plot(T.time(ind_excess_max(j)),IC_excess_max(j),'o');
    

end

%%
figure(101)
set(gcf,'Color','w')
set(gca,'LineWidth',1)
set(gca,'FontSize',14)
grid on
xlabel('time (days)')
ylabel('Moving average of total IC patients');

figure(102)
set(gcf,'Color','w')
set(gca,'LineWidth',1)
set(gca,'FontSize',14)
grid on
xlabel('time (days)')
ylabel('Cumulative excess in IC person-days');

%%
UQdata = load(matfile_name);
if ( max(abs(UQdata.uq_ProcessedY - Y(:,1)))>eps)
    error('stored QoI different from postprocessed QoI');
end
figure(103)
% histogram(Y(:,1),n_tot,'Normalization','cdf','DisplayStyle','stairs')
ecdf(Y(:,1));
ylim([0 1])
grid on
set(gcf,'Color','w')
set(gca,'LineWidth',1)
set(gca,'FontSize',14)
xlabel('max. of moving average')
ylabel('empirical cdf');

figure(104)
% histogram(Y(:,2),n_tot,'Normalization','cdf','DisplayStyle','stairs')
ecdf(Y(:,2));
ylim([0 1])
grid on
set(gcf,'Color','w')
set(gca,'LineWidth',1)
set(gca,'FontSize',14)

xlabel('cumulative IC excess')
ylabel('empirical cdf');