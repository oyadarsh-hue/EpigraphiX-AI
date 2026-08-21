function [prepared] = prep_image(image)

[labeled,N_obj] = bwlabel(image);
for i = 1:N_obj
    N_currentobj = numel(find(labeled == i));
    if N_currentobj == 1
        labeled(labeled == i) = 0;
    end
end
non_zero = labeled ~= 0;
labeled(non_zero) = 1;
prepared = labeled;