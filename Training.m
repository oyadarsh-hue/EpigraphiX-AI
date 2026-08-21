clc
clear
close all

addpath('feature_extraction');
files = dir('Datalphabets');
dirFlags = [files.isdir];
subFolders = files(dirFlags);
subFolders(1:2) = [];
cnt = 1;
for fcnt = 1 : length(subFolders)
    cfilename = dir(sprintf('Datalphabets/%s/', subFolders(fcnt).name));
    tnum = length(cfilename); 
    for icnt = 3 : tnum
        filename = cfilename(icnt,1).name;
        imfiname = sprintf('Datalphabets/%s/%s', subFolders(fcnt).name, filename);
        im = imread(imfiname);

        %%
        data_features(cnt,:) = feature_extractor(im);
        %%
        Group(1,cnt) = fcnt;
        cnt = cnt + 1;
    end
end
save data_features data_features Group