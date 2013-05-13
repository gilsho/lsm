function out = smoothSpikes(spikes,maxtime,tstep)
%SMOOTHSPIKES takes a vector whose entries correspond to times in which
%spikes occurred and computes a continuous waveform using an exponential
%filter
% tstep is the resolution to plot the file in ms. 1 == 1ms
    tau = 5*tstep;        % as specified in Mass, Natschlanger, Markam
    maxval = 20;
    t = 0:tstep:maxtime;                
    kernel = exp(-(t/tau).^2);
    spikeind = int64(spikes/(1000*tstep));     
    spikebin = zeros(length(t),1);
    spikebin(spikeind)=1;
    spikecont = conv(spikebin,kernel);
    spikecont = spikecont(1:length(t));   % truncate output
    %out(out > maxval) = maxval; % floor anything above maxval
    out = 1./(1+exp(-spikecont));   % saturating non-linearity
end

