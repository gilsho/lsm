

function [outDatRawCoord, outDatRawTS] = readNG(filename)


% tic

% should determine file size and use that to determine how many timestamps
% will be read - should be  able to do it perfectly
s = dir(filename);
numEntries = round(s.bytes/14);

if numEntries~=s.bytes/14
    disp('warning: file size not evenly divisible by the correct number of bytes; may have an error');
    numEntries = numEntries-1;
end

% outDatRawCoord = zeros(3,numEntries,'uint16');
% outDatRawTS = zeros(1,numEntries, 'double');
% 
% 
% % open the file and read the data straight out of it; there is no header
% fid = fopen(filename, 'r');
% 
% try
%     readInd = 1;
%     while ~feof(fid) && readInd<numEntries
%         
%         outDatRawCoord(1, readInd) = fread(fid, 1, 'uint16');
%         outDatRawCoord(2, readInd) = fread(fid, 1, 'uint16');
%         outDatRawCoord(3, readInd) = fread(fid, 1, 'uint16');
%         outDatRawTS(readInd) = fread(fid, 1, 'double');
%         readInd = readInd+1;
%     end
%     
%     fclose(fid);
% catch e
%     keyboard;
% end
% toc


% algorithm two
tic

try
    outDatRawCoord2 = zeros(3,numEntries,'uint16');
    outDatRawTS2 = zeros(1,numEntries, 'double');
    
    fid = fopen(filename, 'r');
    outDatRawCoord2(1,:) = fread(fid,Inf,'uint16=>uint16', 12);
    fclose(fid);
    
    fid = fopen(filename, 'r');
    fread(fid,1,'uint16');
    outDatRawCoord2(2,:) = fread(fid,Inf,'uint16=>uint16', 12);
    fclose(fid);
    
    fid = fopen(filename, 'r');
    fread(fid,2,'uint16');
    outDatRawCoord2(3,:) = fread(fid,Inf,'uint16=>uint16', 12);
    fclose(fid);
    
    fid = fopen(filename, 'r');
    fread(fid,3,'uint16');
    outDatRawTS2(1,:) = fread(fid,Inf,'double=>double', 6);
    fclose(fid);
catch e
    disp(e.message);
    disp('Crash while reading .spk file; common causes are empty file or file that is still being written (experiment wasn''t stopped)');
    keyboard;
end

toc;
% size(outDatRawCoord)
% sum(outDatRawCoord(1,:)==outDatRawCoord2(1,:))
% sum(outDatRawCoord(2,:)==outDatRawCoord2(2,:))
% sum(outDatRawCoord(3,:)==outDatRawCoord2(3,:))
% sum(outDatRawTS==outDatRawTS2)


% algoritm 3

% tic
% 
% 
% try
%     outDatRawCoord3 = zeros(3,numEntries,'uint16');
%     outDatRawTS3 = zeros(1,numEntries, 'double');
%     
%     fid = fopen(filename, 'r');
%     buffer = fread(fid,Inf,'uint16=>uint16');
%     fclose(fid);
%     
% %     inds1 = sort([1:14:length(buffer) 2:14:length(buffer)]);indsTS
% %     inds2 = sort([3:14:length(buffer) 4:14:length(buffer)]);
% %     inds3 = sort([5:14:length(buffer) 6:14:length(buffer)]);
% %     indsTS = sort([7:14:length(buffer) 8:14:length(buffer) 9:14:length(buffer) 10:14:length(buffer) 11:14:length(buffer) 12:14:length(buffer) 13:14:length(buffer) 14:14:length(buffer)]);
% %     outDatRawCoord3(1,:) = typecast(buffer(inds1), 'uint16');
% %     outDatRawCoord3(2,:) = typecast(buffer(inds2), 'uint16');
% %     outDatRawCoord3(3,:) = typecast(buffer(inds3), 'uint16');
% %     outDatRawTS3(1,:) = typecast(buffer(indsTS), 'double');
% 
%     outDatRawCoord3(1,:) = buffer(1:7:end);
%     outDatRawCoord3(2,:) = buffer(2:7:end);
%     outDatRawCoord3(3,:) = buffer(3:7:end);
%     outDatRawTS3(1,:) = typecast(buffer(sort([4:7:length(buffer) 5:7:length(buffer) 6:7:length(buffer) 7:7:length(buffer)])), 'double');
% 
% catch e
%     disp(e.message);
%     keyboard;
% end
% 
% toc;
% size(outDatRawCoord3)
% sum(outDatRawCoord2(1,:)==outDatRawCoord3(1,:))
% sum(outDatRawCoord2(2,:)==outDatRawCoord3(2,:))
% sum(outDatRawCoord2(3,:)==outDatRawCoord3(3,:))
% sum(outDatRawTS2==outDatRawTS3)


outDatRawCoord = outDatRawCoord2;
outDatRawTS = outDatRawTS2;

