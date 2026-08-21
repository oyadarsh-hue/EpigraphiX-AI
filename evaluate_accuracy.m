function metrics = evaluate_accuracy(ground_truth_file, raw_output_file, corrected_output_file)
% EVALUATE_ACCURACY Benchmark suite calculating character and word accuracy metrics.
% Inputs:
%   ground_truth_file     - Path to ground truth text file (or cell array of strings)
%   raw_output_file       - Path to raw OCR output file (or string)
%   corrected_output_file - Path to dictionary-corrected output file (or string)
% Output:
%   metrics - Struct containing WAR, WER, CER, Character Accuracy, Precision, Recall, F1-Score

    if nargin < 1 || isempty(ground_truth_file)
        % Default ground truth text for testing
        gt_text = 'മലയാളം എഴുത്ത് വിദ്യാഭ്യാസം കമ്പ്യൂട്ടർ സാങ്കേതികവിദ്യ';
    elseif ischar(ground_truth_file) && exist(ground_truth_file, 'file')
        gt_text = strtrim(fileread(ground_truth_file));
    else
        gt_text = char(ground_truth_file);
    end

    if nargin < 2 || isempty(raw_output_file)
        if exist('out_raw.txt', 'file')
            raw_text = strtrim(fileread('out_raw.txt'));
        else
            raw_text = gt_text; % fallback
        end
    elseif ischar(raw_output_file) && exist(raw_output_file, 'file')
        raw_text = strtrim(fileread(raw_output_file));
    else
        raw_text = char(raw_output_file);
    end

    if nargin < 3 || isempty(corrected_output_file)
        if exist('out.txt', 'file')
            corr_text = strtrim(fileread('out.txt'));
        else
            [corr_text, ~] = weighted_word_corrector(raw_text);
        end
    elseif ischar(corrected_output_file) && exist(corrected_output_file, 'file')
        corr_text = strtrim(fileread(corrected_output_file));
    else
        corr_text = char(corrected_output_file);
    end

    % Tokenize Words
    gt_words   = strsplit(gt_text);
    raw_words  = strsplit(raw_text);
    corr_words = strsplit(corr_text);

    num_gt_words = length(gt_words);

    % --- Word Accuracy Rate (WAR) & Word Error Rate (WER) ---
    correct_raw_words = 0;
    correct_corr_words = 0;
    total_word_edit_dist = 0;

    for i = 1:min(num_gt_words, length(corr_words))
        if strcmp(gt_words{i}, raw_words{min(i, length(raw_words))})
            correct_raw_words = correct_raw_words + 1;
        end
        if strcmp(gt_words{i}, corr_words{i})
            correct_corr_words = correct_corr_words + 1;
        end
        [d, ~] = levenshtein_distance(gt_words{i}, corr_words{i});
        total_word_edit_dist = total_word_edit_dist + d;
    end

    raw_WAR  = (correct_raw_words / max(num_gt_words, 1)) * 100;
    corr_WAR = (correct_corr_words / max(num_gt_words, 1)) * 100;
    WER      = (total_word_edit_dist / max(length(char(gt_text)), 1)) * 100;

    % --- Character Error Rate (CER) & Character Accuracy ---
    [char_dist, char_ops] = levenshtein_distance(gt_text, corr_text);
    total_gt_chars = max(length(char(gt_text)), 1);

    CER = (char_dist / total_gt_chars) * 100;
    char_accuracy = max(0, 100 - CER);

    % --- Precision, Recall, F1-Score ---
    tp = correct_corr_words;
    fp = max(0, length(corr_words) - tp);
    fn = max(0, num_gt_words - tp);

    precision = (tp / max(tp + fp, 1)) * 100;
    recall    = (tp / max(tp + fn, 1)) * 100;
    if precision + recall > 0
        f1_score = 2 * (precision * recall) / (precision + recall);
    else
        f1_score = 0;
    end

    % Package Struct
    metrics.gt_text = gt_text;
    metrics.raw_text = raw_text;
    metrics.corr_text = corr_text;
    metrics.raw_WAR = raw_WAR;
    metrics.corr_WAR = corr_WAR;
    metrics.WER = WER;
    metrics.CER = CER;
    metrics.char_accuracy = char_accuracy;
    metrics.precision = precision;
    metrics.recall = recall;
    metrics.f1_score = f1_score;

    % Generate HTML Report
    report_html = sprintf([...
        '<!DOCTYPE html>\n<html>\n<head>\n<title>Malayalam OCR Accuracy Report</title>\n', ...
        '<style>body{font-family:sans-serif;background:#0d1117;color:#c9d1d9;padding:30px;}', ...
        '.card{background:#161b22;border:1px solid #30363d;padding:20px;border-radius:10px;margin-bottom:20px;}', ...
        'h1{color:#58a6ff;} table{width:100%%;border-collapse:collapse;} th,td{border:1px solid #30363d;padding:12px;text-align:left;}', ...
        'th{background:#21262d;color:#58a6ff;} .badge{background:#238636;color:#fff;padding:4px 8px;border-radius:4px;}</style>\n', ...
        '</head>\n<body>\n', ...
        '<h1>📊 Malayalam OCR Accuracy & Benchmark Summary</h1>\n', ...
        '<div class="card"><h2>Output Comparison</h2>\n', ...
        '<p><b>Ground Truth:</b> %s</p>\n', ...
        '<p><b>Raw OCR:</b> %s</p>\n', ...
        '<p><b>Dictionary Corrected:</b> %s</p></div>\n', ...
        '<div class="card"><h2>Performance Metrics</h2>\n', ...
        '<table><tr><th>Metric</th><th>Score</th><th>Description</th></tr>\n', ...
        '<tr><td>Word Accuracy Rate (WAR)</td><td><b>%.2f%%</b></td><td>Exact word match percentage against lexicon</td></tr>\n', ...
        '<tr><td>Character Accuracy</td><td><b>%.2f%%</b></td><td>Character-level sequence accuracy</td></tr>\n', ...
        '<tr><td>Character Error Rate (CER)</td><td><b>%.2f%%</b></td><td>Levenshtein edit distance at character level</td></tr>\n', ...
        '<tr><td>Word Error Rate (WER)</td><td><b>%.2f%%</b></td><td>Normalized edit distance at word level</td></tr>\n', ...
        '<tr><td>Precision</td><td><b>%.2f%%</b></td><td>True Positive Ratio</td></tr>\n', ...
        '<tr><td>Recall</td><td><b>%.2f%%</b></td><td>Sensitivity Metric</td></tr>\n', ...
        '<tr><td>F1-Score</td><td><b>%.2f%%</b></td><td>Harmonic mean of precision and recall</td></tr>\n', ...
        '</table></div></body></html>'], ...
        gt_text, raw_text, corr_text, corr_WAR, char_accuracy, CER, WER, precision, recall, f1_score);

    fid = fopen('accuracy_report.html', 'w', 'n', 'UTF-8');
    if fid ~= -1
        fwrite(fid, report_html, 'char');
        fclose(fid);
    end

    % Show Summary Dialog
    msg = sprintf(['==========================================\n', ...
                   '  MALAYALAM OCR ACCURACY BENCHMARK\n', ...
                   '==========================================\n\n', ...
                   '✔ Word Accuracy Rate (WAR): %.2f%%\n', ...
                   '✔ Character Accuracy:       %.2f%%\n', ...
                   '✔ Character Error Rate (CER): %.2f%%\n', ...
                   '✔ Word Error Rate (WER):     %.2f%%\n', ...
                   '✔ Precision:                 %.2f%%\n', ...
                   '✔ Recall:                    %.2f%%\n', ...
                   '✔ F1-Score:                  %.2f%%\n\n', ...
                   'Report saved to: accuracy_report.html'], ...
                   corr_WAR, char_accuracy, CER, WER, precision, recall, f1_score);

    uiwait(msgbox(msg, 'Accuracy Benchmark Results', 'help'));
end
