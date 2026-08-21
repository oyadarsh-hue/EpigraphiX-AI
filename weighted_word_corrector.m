function [corrected_text, word_details] = weighted_word_corrector(raw_text, dict_file)
% WEIGHTED_WORD_CORRECTOR Post-processes raw OCR output strings using Malayalam Lexicon
% Inputs:
%   raw_text  - String or char array of OCR output words
%   dict_file - (Optional) Path to malayalam_dictionary.txt
% Outputs:
%   corrected_text - Corrected text string
%   word_details   - Cell array of structs containing match metrics for each word

    if nargin < 2 || isempty(dict_file)
        dict_file = 'malayalam_dictionary.txt';
    end

    % Load dictionary
    if ~exist(dict_file, 'file')
        warning('Dictionary file %s not found. Returning raw text.', dict_file);
        corrected_text = raw_text;
        word_details = {};
        return;
    end

    fid = fopen(dict_file, 'r', 'n', 'UTF-8');
    dict_words = {};
    while ~feof(fid)
        line = fgetl(fid);
        if ischar(line)
            line = strtrim(line);
            if ~isempty(line)
                dict_words{end+1} = line;
            end
        end
    end
    fclose(fid);

    % Tokenize raw text
    if iscell(raw_text)
        words = raw_text;
    else
        words = strsplit(strtrim(char(raw_text)));
    end

    corrected_words = cell(size(words));
    word_details = cell(size(words));

    for w_idx = 1:length(words)
        target_word = strtrim(words{w_idx});
        if isempty(target_word)
            corrected_words{w_idx} = '';
            continue;
        end

        best_match = target_word;
        min_dist = inf;
        best_ops = struct('substitutions', 0, 'insertions', 0, 'deletions', 0);

        target_len = max(length(char(target_word)), 1);

        for d_idx = 1:length(dict_words)
            dict_word = dict_words{d_idx};
            
            % Skip length disparities > 4
            if abs(length(char(target_word)) - length(char(dict_word))) > 4
                continue;
            end

            [d, ops] = levenshtein_distance(target_word, dict_word);
            
            if d < min_dist
                min_dist = d;
                best_match = dict_word;
                best_ops = ops;
                if min_dist == 0
                    break; % Exact match found
                end
            end
        end

        % Calculate confidence score (%)
        confidence = max(0, (1 - min_dist / target_len) * 100);

        % If edit distance is too large (> 50% of word length), keep original raw word
        if min_dist > ceil(target_len * 0.6)
            final_word = target_word;
            is_corrected = false;
        else
            final_word = best_match;
            is_corrected = ~strcmp(target_word, best_match);
        end

        corrected_words{w_idx} = final_word;

        details.raw = target_word;
        details.corrected = final_word;
        details.dictionary_match = best_match;
        details.distance = min_dist;
        details.confidence = confidence;
        details.is_corrected = is_corrected;
        details.ops = best_ops;

        word_details{w_idx} = details;
    end

    corrected_text = strjoin(corrected_words, ' ');
end
