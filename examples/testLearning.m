% run this file from the main lsm directory

clear;
clc;


tstep = 0.001;
maxtime = 1;
datadir = 'data/';
outdir = strcat(datadir,'out/ml/');
wavfile = 'wav/heavyside.dat';
numfiles = 5;

generateOutSpikes(load(wavfile),numfiles,outdir);

fnames = dir(strcat(outdir,'*.spk'));
numfids = length(fnames);
spiketimes = zeros(maxtime/tstep+1,numfids);
for i = 1:numfids
    spiketimes(:,i) = ...
    smoothSpikes(load(strcat(outdir,fnames(i).name)),maxtime,tstep);
end

%figure; plot(spiketimes(:,1));
v = vectorizeWav(load(strcat(datadir,wavfile)),tstep);
w = learnWeights(spiketimes,v);
figure; 
subplot(211);
plot(v);
subplot(212);
plot(spiketimes*w);
