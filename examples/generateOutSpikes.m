function generateOutSpikes(wav,numfiles,outdir)
%GENERATEOUTSPIKES generates outspikes based on a waveform vector
    
    v = vectorizeWav(wav,0.001);
    muscale = 0.1;
    baserate = 0.002;

    mkdir(outdir);
    delete(strcat(outdir,'*.spk'));
    
    spikebins = zeros(length(v),numfiles);
    for i=1:numfiles
        f = fopen(strcat(outdir,num2str(i),'.spk'),'w');
        for j=1:length(v)
           r = rand;
           didspike = (v(j)*muscale > r) || (baserate > r);
           spikebins(j,i) = didspike;
           if (didspike) 
              fprintf(f,strcat(num2str((j+rand)),'\n'));
           end
        end
        fclose(f);
    end
    
    figure; plot(spikebins(:,1));
     figure; plot(spikebins(:,2));
      figure; plot(spikebins(:,3));
       figure; plot(spikebins(:,4));
        figure; plot(spikebins(:,5));
    
end

