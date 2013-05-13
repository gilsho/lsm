function y = vectorizeWav(wav,tstep)
%VECTORIZE converts a waveform data file into a 
% timeseries matlab vector.
    tstep = tstep * 1000;   % convert to miliseconds
    y = [];
    lasty = 0;
    lastx = 0;
    for i=1:size(wav,1) 
       thisx = wav(i,1);
       y = [y; ones((thisx-lastx)/tstep,1)*lasty];
       lastx = thisx;
       lasty = wav(i,2);
    end
    y = [y; y(end)];
end

