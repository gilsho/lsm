function [outDat, coord, ts] = readNGBinSparse_reorder(filename, xSize, ySize, varargin)
% NOTE: This is the same as readNGSparse by Nick Steinmetz, but re-orders
% the neuron list to agree with Steve Sloan's python code.
% Author: emt, 10/20/11
% % filename is a .spk file. 
%
% xSize and ySize are the size of the array of neurons you're using; e.g.
% using the whole chip would be xSize = 256 and ySize = 256. 
%
% the one optional argument is an array containing the numbers of the chips
% that you want to get spiking data from, just so the rest can be discarded
% and save RAM space. 
%
% example call: 
%   outDat = readNGBinSparse('test.spk', 128, 128, [1 3]);

[coord, ts] = readNG(filename);

numChips = double(max(coord(1,:))+1);
if ~isempty(varargin)
    chipsToUse = varargin{1};
else
    chipsToUse = 1:numChips;
end

ts = ts(coord(2,:)<xSize & coord(3,:)<ySize & ismember(coord(1,:), chipsToUse-1));
coord = coord(:,coord(2,:)<xSize & coord(3,:)<ySize & ismember(coord(1,:), chipsToUse-1));

%numChips = double(max(coord(1,:))+1);
numChips = length(chipsToUse);
timeInMs = round(max(ts)+1);

outDat = cell(1,numChips);

for chip = 1:length(outDat)
    chipNum = chipsToUse(chip);
    thisChip = (coord(1,:)==chipNum-1);
    outDat{chip} = sparse(double(coord(2,thisChip)+coord(3,thisChip)*ySize+1), round(ts(thisChip)+1), ones(1,length(ts(thisChip))), xSize*ySize, timeInMs);    
end

