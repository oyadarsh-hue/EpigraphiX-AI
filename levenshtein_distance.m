function [dist, ops] = levenshtein_distance(str1, str2)
% LEVENSHTEIN_DISTANCE Compute Levenshtein Edit Distance between two strings
% Inputs:
%   str1 - Source string (or cell array of chars)
%   str2 - Target string (or cell array of chars)
% Outputs:
%   dist - Minimum edit distance (integer)
%   ops  - Struct detailing substitutions, insertions, deletions

    if ischar(str1)
        u1 = unicode2native(str1, 'UTF-8');
        c1 = cellstr(split(char(str1), ''));
        c1 = c1(~cellfun('isempty', c1));
    else
        c1 = str1;
    end

    if ischar(str2)
        c2 = cellstr(split(char(str2), ''));
        c2 = c2(~cellfun('isempty', c2));
    else
        c2 = str2;
    end

    m = length(c1);
    n = length(c2);

    if m == 0
        dist = n;
        ops.insertions = n;
        ops.deletions = 0;
        ops.substitutions = 0;
        return;
    end

    if n == 0
        dist = m;
        ops.insertions = 0;
        ops.deletions = m;
        ops.substitutions = 0;
        return;
    end

    D = zeros(m+1, n+1);
    D(:,1) = 0:m;
    D(1,:) = 0:n;

    for i = 1:m
        for j = 1:n
            if strcmp(c1{i}, c2{j})
                cost = 0;
            else
                cost = 1;
            end
            D(i+1, j+1) = min([D(i, j+1) + 1, ...      % Deletion
                              D(i+1, j) + 1, ...      % Insertion
                              D(i, j) + cost]);       % Substitution
        end
    end

    dist = D(m+1, n+1);
    
    % Trace back operations
    i = m + 1;
    j = n + 1;
    subs = 0; ins = 0; dels = 0;
    while i > 1 || j > 1
        if i > 1 && j > 1 && strcmp(c1{i-1}, c2{j-1})
            i = i - 1;
            j = j - 1;
        elseif i > 1 && j > 1 && D(i,j) == D(i-1,j-1) + 1
            subs = subs + 1;
            i = i - 1;
            j = j - 1;
        elseif j > 1 && D(i,j) == D(i,j-1) + 1
            ins = ins + 1;
            j = j - 1;
        else
            dels = dels + 1;
            i = i - 1;
        end
    end
    
    ops.substitutions = subs;
    ops.insertions = ins;
    ops.deletions = dels;
end
