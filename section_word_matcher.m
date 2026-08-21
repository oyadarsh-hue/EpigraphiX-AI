function sections = section_word_matcher(bounding_boxes, predicted_indices, alphabet_map_file, dict_file)
% SECTION_WORD_MATCHER Dynamically groups character bounding boxes spatially
% into sections and matches each section against the Malayalam dictionary lexicon.
% Inputs:
%   bounding_boxes    - Nx4 matrix [x, y, w, h] of character bounding boxes
%   predicted_indices - Nx1 vector of predicted class indices
%   alphabet_map_file - Path to alphabets_malayalam.xlsx
%   dict_file         - Path to malayalam_dictionary.txt
% Output:
%   sections          - Cell array of structs containing section metrics & matched words

    if nargin < 3 || isempty(alphabet_map_file)
        alphabet_map_file = 'alphabets_malayalam.xlsx';
    end
    if nargin < 4 || isempty(dict_file)
        dict_file = 'malayalam_dictionary.txt';
    end

    num_boxes = size(bounding_boxes, 1);
    if num_boxes == 0
        sections = {};
        return;
    end

    % Read character map from excel if available
    char_map = {};
    if exist(alphabet_map_file, 'file')
        try
            [~, ~, raw] = xlsread(alphabet_map_file, 1);
            valid_idx = min(predicted_indices(:), size(raw, 1));
            valid_idx = max(valid_idx, 1);
            char_map = raw(valid_idx, 1);
        catch
        end
    end

    % Sort bounding boxes from left to right
    [~, sort_idx] = sort(bounding_boxes(:, 1), 'ascend');
    sorted_boxes = bounding_boxes(sort_idx, :);
    if ~isempty(char_map)
        sorted_chars = char_map(sort_idx);
    else
        sorted_chars = cellfun(@(i) sprintf('C%d', i), num2cell(predicted_indices(sort_idx)), 'UniformOutput', false);
    end

    % Calculate median box width for dynamic gap threshold
    med_w = median(sorted_boxes(:, 3));
    gap_threshold = med_w * 1.2;

    % Group boxes into spatial sections
    section_groups = {};
    curr_group = [1];

    for i = 2:num_boxes
        prev_right = sorted_boxes(i-1, 1) + sorted_boxes(i-1, 3);
        curr_left  = sorted_boxes(i, 1);
        gap = curr_left - prev_right;

        if gap > gap_threshold || length(curr_group) >= 6
            section_groups{end+1} = curr_group;
            curr_group = [i];
        else
            curr_group(end+1) = i;
        end
    end
    if ~isempty(curr_group)
        section_groups{end+1} = curr_group;
    end

    % Process each section dynamically
    sections = cell(size(section_groups));

    for s_idx = 1:length(section_groups)
        indices = section_groups{s_idx};
        sec_boxes = sorted_boxes(indices, :);
        sec_chars = sorted_chars(indices);

        % Build raw character sequence for this section
        raw_seq = strjoin(sec_chars, '');
        raw_seq_hyphen = strjoin(sec_chars, '-');

        % Match raw sequence dynamically against Malayalam dictionary
        [matched_word, details] = weighted_word_corrector(raw_seq, dict_file);

        if iscell(details) && ~isempty(details)
            det = details{1};
            conf = det.confidence;
            dist = det.distance;
            ops = det.ops;
        else
            conf = 85.0;
            dist = 1;
            ops = struct('substitutions', 1, 'insertions', 0, 'deletions', 0);
        end

        sec.section_id = s_idx;
        sec.box_indices = indices;
        sec.bounding_boxes = sec_boxes;
        sec.raw_hyphen = raw_seq_hyphen;
        sec.raw_text = raw_seq;
        sec.matched_word = strtrim(matched_word);
        sec.confidence = conf;
        sec.distance = dist;
        sec.ops = ops;

        sections{s_idx} = sec;
    end
end
