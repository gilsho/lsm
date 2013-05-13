function model = learnWeights(M,v)
%LEARNWEIGHTS Summary of this function goes here
%   Detailed explanation goes here
    model = (v\M)';
    fprintf('training error: %f\n', norm(M*model-v)^2);
end

