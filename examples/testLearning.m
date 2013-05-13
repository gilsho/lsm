% run this file from the main lsm directory

clear;
clc;


tstep = 0.001;
maxtime = 1;
datadir = 'data/';
outdir = strcat(datadir,'out/ml/');

generateOutSpikes(load('wav2.dat'),20,outdir);

fnames = dir(strcat(outdir,'*.spk'));
numfids = length(fnames);
spiketimes = zeros(maxtime/tstep+1,numfids);
for i = 1:numfids
    spiketimes(:,i) = ...
    smoothSpikes(load(strcat(outdir,fnames(i).name)),maxtime,tstep);
end

%figure; plot(spiketimes(:,1));
v = vectorizeWav(load(strcat(datadir,'wav/wav2.dat')),tstep);
w = learnWeights(spiketimes,v);
figure; 
subplot(211);
plot(v);
subplot(212);
plot(spiketimes*w);
