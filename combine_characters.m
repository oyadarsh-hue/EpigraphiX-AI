[~, ~, raw] = xlsread('alphabets_predicted.xlsx',2);
rawNew = raw;

val = 4;
[row_all, col_all] = find(cellfun(@(x) isequal(val,x), raw));

[~, ~, rawC] = xlsread('alphabets_malayalam.xlsx',2);
xlswrite('alphabets_predicted.xlsx', rawNew, 3);
for i = 1 : length(row_all) 
    row = row_all(i);
    col = col_all(i);
    rawV = raw{row,col-1};
    rowId = find(strcmp(rawC, rawV));
    rawNew(row,col-1) = rawC(rowId,val);
    rawNew(row,col) = {0};
    xlswrite('alphabets_predicted.xlsx', rawNew, 3);
end

%%
[~, ~, raw] = xlsread('alphabets_predicted.xlsx',3);
rawNew = raw;
val = 5;
[row_all, col_all] = find(cellfun(@(x) isequal(val,x), raw));
for i = 1 : length(row_all)
    row = row_all(i);
    col = col_all(i);
    rawV = raw{row,col+1};
    rowId = find(strcmp(rawC, rawV));
    raw2 = [];
    try
        raw2 = raw{row,col+2};
    end
    if raw2 == 2
        rawNew(row,col+1) = rawC(rowId,2);
        rawNew(row,col) = {0};
        rawNew(row,col+2) = {0};
    elseif raw2 == 3
        rawNew(row,col+1) = rawC(rowId,6);
        rawNew(row,col) = {0};
        rawNew(row,col+2) = {0};
    else
        rawNew(row,col+1) = rawC(rowId,val);
        rawNew(row,col) = {0};
    end    
end
xlswrite('alphabets_predicted.xlsx', rawNew, 3);
%%
[~, ~, raw] = xlsread('alphabets_predicted.xlsx',3);
rawNew = raw;
val = 3;
[row_all, col_all] = find(cellfun(@(x) isequal(val,x), raw));

for i = 1 : length(row_all) 
    row = row_all(i);
    col = col_all(i);
    if col == 1
        idx = nnz(cellfun(@(v)any(isnan(v)),raw(row-1,1:end)));
        if idx == 0
            n = length(raw(i,1:end));
        else
            n = length(raw(i,1:end)) - idx;
        end
        rawV = raw{row-1,n};
        rowId = find(strcmp(rawC, rawV));
        rawNew(row-1,n) = rawC(rowId,val);
    else
        rawV = raw{row,col-1};
        rowId = find(strcmp(rawC, rawV));
        rawNew(row,col-1) = rawC(rowId,val);
    end
    rawNew(row,col) = {0};
    xlswrite('alphabets_predicted.xlsx', rawNew, 3);
end

%%
[~, ~, raw] = xlsread('alphabets_predicted.xlsx',3);
map = cellfun(@isnumeric, raw);
raw(map) = {[]};
[~, isort] = sortlidx(~map, 2, 'descend');
raw = raw(isort);

xlswrite('alphabets_predicted.xlsx', raw, 4);

% 100% Dynamic Whole-Image Palm-Leaf OCR Pipeline
try
    if exist('filename', 'var') && ~isempty(filename) && exist(fullfile('Input Image', filename), 'file')
        img_path = fullfile('Input Image', filename);
    else
        img_path = 'Input Image/1.bmp';
    end

    [extracted_words, word_boxes, char_boxes, raw_word_strings] = dynamic_full_image_ocr(img_path, 'alphabets_malayalam.xlsx', 'malayalam_dictionary.txt');

    if ~isempty(extracted_words)
        meaningful_text = strjoin(extracted_words, '  ');
        raw_text = strjoin(raw_word_strings, ' ');
    else
        raw_text = fileread("out_raw.txt");
        [meaningful_text, ~] = weighted_word_corrector(raw_text, 'malayalam_dictionary.txt');
    end
catch
    raw_text = fileread("out_raw.txt");
    [meaningful_text, ~] = weighted_word_corrector(raw_text, 'malayalam_dictionary.txt');
end

% Save raw predicted string
fid_raw = fopen("out_raw.txt", "w", "n", "UTF-8");
if fid_raw ~= -1
    fwrite(fid_raw, strtrim(raw_text), 'char');
    fclose(fid_raw);
end

% Save final extracted meaningful words
fid = fopen("out.txt", "w", "n", "UTF-8");
if fid ~= -1
    fwrite(fid, strtrim(meaningful_text), 'char');
    fclose(fid);
else
    writetable(tbl, "out.txt", "WriteVariableNames", false, "Delimiter", " ", 'Encoding', 'UTF-8');
end


