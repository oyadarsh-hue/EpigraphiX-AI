function bw = sauvola_binarize(img, window_size, k, R)
% SAUVOLA_BINARIZE Local adaptive thresholding for textured historical media (palm leaf, manuscripts)
% Inputs:
%   img         - Input image (grayscale or RGB)
%   window_size - Local window size (odd integer, default 25)
%   k           - Sauvola parameter (default 0.25)
%   R           - Dynamic range of standard deviation (default 128)
% Output:
%   bw          - Binary logical image (true for ink foreground, false for background)

    if nargin < 2 || isempty(window_size)
        window_size = 25;
    end
    if nargin < 3 || isempty(k)
        k = 0.25;
    end
    if nargin < 4 || isempty(R)
        R = 128;
    end

    if size(img, 3) == 3
        img_gray = rgb2gray(img);
    else
        img_gray = img;
    end

    img_double = double(img_gray);

    % Mean filter using integral image or convolution
    h = fspecial('average', [window_size window_size]);
    local_mean = filter2(h, img_double, 'same');

    % Local standard deviation
    local_sq_mean = filter2(h, img_double.^2, 'same');
    local_std = sqrt(max(0, local_sq_mean - local_mean.^2));

    % Sauvola threshold matrix
    threshold = local_mean .* (1 + k * (local_std ./ R - 1));

    % Binarization (ink strokes are darker than textured wood background)
    bw = img_double < threshold;

    % Morphological cleaning: area open to remove single-pixel wood grain noise
    bw = bwareaopen(bw, 15);
end
