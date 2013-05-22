function  generateWav(vector,res,filepath)
%GENERATEWAV Summary of this function goes here
%   Detailed explanation goes here

    f = fopen(filepath,'w');
    for i=1:res:length(vector)
        fprintf(f,[num2str(res),' ',num2str(vector(i)),'\n']);
    end
    fclose(f);

end

