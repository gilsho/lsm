close all
clear
N = 64;

for expNum = 1:7
    chips = 1;
    exp_dir = ['data/exp',num2str(expNum),'/'];
    exp_file = [exp_dir,'out.spk'];

    [sparse_spikes, coord, ts] = readNGBinSparse_reorder(exp_file,N,N,chips);
    full_spikes = full(cell2mat(sparse_spikes));

    %Use 90% of the data for training, 10% for testing
    train_length = int64(0.9*size(full_spikes,2));
    test_length = size(full_spikes,2)-train_length;

    train_spikes = full_spikes(:,1:train_length);
    test_spikes = full_spikes(:,train_length+1:end);

    %out1 = smoothSpikes(full_spikes(2,:), 1.0002, 0.0001)
    %out2 = expsmooth(full_spikes(2,:)', 10000, 200);
    
    % Find average firing rate over training period
    for i = 1:(N*N)
        train_rate(i) = sum(train_spikes(i,:))/(double(train_length)/10000.0);
    end

    % Find average firing rate over testing period
    for i = 1:(N*N)
        test_rate(i) = sum(test_spikes(i,:))/(double(test_length)/10000.0);
    end

    %Experiment 0 inputs [0 200] crashed when reading it
    experiment_inputs = [50,5; 100,200; 200,200; 200,500; 500,400; 100,20; 100,200];

    % How is the input layed out????
    input = double(diag([ones(1,N*N/2)*experiment_inputs(expNum,1), ones(1,N*N/2)*experiment_inputs(expNum,2)]));

    model(:,expNum) = (input\train_rate');
    fprintf('training error: %f\n', norm(input*model(:,expNum)-train_rate')^2);
    fprintf('test error: %f\n', norm(input*model(:,expNum)-test_rate')^2);
end

save('current_model', 'model')
figure
hold on
grid on
for i = 1:N*N  
    plot(model(i,1:5))
end
title('Feed Forward Experiment Weights')
xlabel('Experiment #')
ylabel('Weight')

figure
hold on
grid on
for i = 1:N*N  
    plot(model(i,6:7))
end
title('Tanya Experiment Weights')
xlabel('Experiment #')
ylabel('Weight')
 