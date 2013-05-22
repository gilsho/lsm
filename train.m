
N = 64
expNum = 1;
chips = 1;
exp_dir = ['data/exp',num2str(expNum),'/'];
exp_file = [exp_dir,'out.spk'];

spikes = readNGBinSparse_reorder(exp_file,N,N,chips);
