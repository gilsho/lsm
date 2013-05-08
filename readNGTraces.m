

function [timeStamps, ADCValues] = readNGTraces(filename)

% each of timeStamps and ADCValues are Z-by-T cell arrays where Z is the chip
% number and T is the "tap" number. Within each cell, timeStamps has a
% double array and ADCValues has a uint16 array. 


% should determine file size and use that to determine how many timestamps
% will be read - should be  able to do it perfectly
s = dir(filename);
numEntries = round(s.bytes/12);

if numEntries~=s.bytes/12
    disp('warning: file size not evenly divisible by the correct number of bytes; may have an error');
    numEntries = numEntries-1;
end


try
    
    Zvals = zeros(1,numEntries,'uint8');
    TapVals = zeros(1,numEntries, 'uint8');
    ts = zeros(1,numEntries, 'double');
    adcv = zeros(1,numEntries, 'uint16');
%     outDatRawCoord2 = zeros(3,numEntries,'uint16');
%     outDatRawTS2 = zeros(1,numEntries, 'double');
    
    fid = fopen(filename, 'r');
    Zvals = fread(fid,Inf,'uint8=>uint8', 11);
    fclose(fid);
    
    fid = fopen(filename, 'r');
    fread(fid,1,'uint8');
    TapVals = fread(fid,Inf,'uint8=>uint8', 11);
    fclose(fid);
    
    fid = fopen(filename, 'r');
    fread(fid,2,'uint8');
    adcv = fread(fid,Inf,'uint16=>uint16', 10);
    fclose(fid);
    
    fid = fopen(filename, 'r');
    fread(fid,4,'uint8');
    ts = fread(fid,Inf,'double=>double', 4);
    fclose(fid);
catch e
    disp(e.message);
    keyboard;
end


adcv(adcv>2047) = 2047;
% ADCValues = adcv;
% timeStamps = ts;



% now reformat the data into these cell arrays for usefulness

uniqueZ = sort(unique(Zvals));
uniqueTap = sort(unique(TapVals));

numZ = length(uniqueZ);
numTap = length(uniqueTap);
timeStamps = cell(numZ, numTap);
ADCValues = cell(numZ, numTap);

for z = 1:numZ
    for t = 1:numTap
        thisZ = uniqueZ(z);
        thisTap = uniqueTap(t);
        timeStamps{z,t} = ts(Zvals==thisZ & TapVals==thisTap);
        ADCValues{z,t} = adcv(Zvals==thisZ & TapVals==thisTap);
    end
end


