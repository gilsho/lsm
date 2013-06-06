close all
clear
N = 64;

experiment_inputs = [50,5; 100,200; 200,200; 200,500; 500,400; 100,20; 100,200];

NUM_MODELS = 3;
TRAIN_FRAC = 0.6;
CV_FRAC = 0.2;
TEST_FRAC = 1-(TRAIN_FRAC+CV_FRAC); 
exp_rates = cell(NUM_MODELS);

exp_rates{1} = [ 50    5
                 100   200
                 200   200
                 200   500 
                 500   400];
             
exp_rates{2} = [ 100   20
                 100   200];
    
    
feed_forward_input = 1:5;
chips = 1;

total_samples = 31000;
neurons = 4096;

train_set = zeros(int64(total_samples*TRAIN_FRAC),neurons);
cv_set = zeros(int64(total_samples*CV_FRAC),neurons);
test_set = zeros(int64(total_samples*TEST_FRAC),neurons);

train_labels = zeros(int64(total_samples*TRAIN_FRAC,1));
cv_labels = zeros(int64(total_samples*CV_FRAC));
test_labels = zeros(int64(total_samples*TEST_FRAC));

train_index = 0;
cv_index = 0;
test_index = 0;

for expNum = 1:5
   
    exp_dir = ['data/exp',num2str(expNum),'/'];
    exp_file = [exp_dir,'out.spk'];
    sparse_spikes = readNGBinSparse_reorder(exp_file,N,N,chips);
    data = full(cell2mat(sparse_spikes));
    data = expsmooth(data', 1000, 5);
    [samples, neurons] = size(data);

    exp_train_length = int64(TRAIN_FRAC*samples);
    exp_cv_length = int64(CV_FRAC*samples);
    exp_test_length = samples-(exp_train_length+exp_cv_length);

    exp_train = data(1:exp_train_length,:);
    exp_cv = data(exp_train_length+1:exp_train_length+exp_cv_length,:);
    exp_test = data(exp_train_length+exp_cv_length+1:end,:);
    
    exp_labels = ones(samples,1)* ...
                 (exp_rates{1}(expNum,1) - exp_rates{1}(expNum,2));
    exp_train_labels = exp_labels(1:exp_train_length);
    exp_cv_labels = exp_labels(exp_train_length+1:exp_train_length+exp_cv_length);
    exp_test_labels = exp_labels(exp_train_length+exp_cv_length+1:end);
    
    train_set(1+train_index:train_index+exp_train_length,:)= exp_train;
    cv_set(1+cv_index:cv_index+exp_cv_length,:)   = exp_cv;
    test_set(1+test_index:test_index+exp_test_length,:) = exp_test;
    
    train_labels(1+train_index:train_index+exp_train_length)= exp_train_labels;
    cv_labels(1+cv_index:cv_index+exp_cv_length) = exp_cv_labels;
    test_labels(1+test_index:test_index+exp_test_length) = exp_test_labels; 
    
    train_index = train_index + exp_train_length;
    cv_index = cv_index + exp_cv_length;
    test_index = test_index + exp_test_length;
    
end

model = (train_set\train_labels);

fprintf('training error: %f\n', norm(train_set*model-train_labels)^2);
fprintf('test error: %f\n', norm(cv_set*model-cv_labels)^2);


% save('current_model', 'model')
% figure
% subplot(211)
% hold on
% grid on
% for i = 1:N*N  
%     plot(model(i,1:5), experiment_inputs(feed_forward_input,1))
% end
% title('Feed Forward Experiment Weights')
% xlabel('Current 1')
% ylabel('Weight')
% subplot(212)
% hold on
% grid on
% for i = 1:N*N  
%     plot(model(i,1:5), experiment_inputs(feed_forward_input,2))
% end
% title('Feed Forward Experiment Weights')
% xlabel('Current 2')
% ylabel('Weight')
% 
