function features = feature_extractor(image)

if size(image,3) == 3
    image = rgb2gray(image);
    image = im2bw(image, graythresh(image));
end    

image = bwmorph(image, 'skel', inf);
image = discourser(image);

row = size(image,1);
column = size(image,2);
add_rows = 0; 
add_columns = 0;

if row < 9
    add_rows = 9-row;
end

if column < 9
    add_columns = 9-column;
end

if mod(add_rows,2) == 0
    image = [zeros(add_rows/2,column);image;zeros(add_rows/2,column)];
else
    image = [zeros((add_rows-1)/2,column);image;zeros((add_rows+1)/2,column)];
end

row = size(image,1);
if mod(add_columns,2) == 0
    image = [zeros(row,(add_columns)/2),image,zeros(row,(add_columns)/2)];
else
    image = [zeros(row,(add_columns-1)/2),image,zeros(row,(add_columns+1)/2)];
end
column = size(image,2);

n_rows = ceil(row/3)*3-row;
n_columns = ceil(column/3)*3-column;

if mod(n_rows,2) == 0
    image = [zeros(n_rows/2,column);image;zeros(n_rows/2,column)];
else
    image = [zeros((n_rows-1)/2,column);image;zeros((n_rows+1)/2,column)];
end

row = size(image,1);
if mod(n_columns,2) == 0
    image = [zeros(row,(n_columns)/2),image,zeros(row,(n_columns)/2)];
else
    image = [zeros(row,(n_columns-1)/2),image,zeros(row,(n_columns+1)/2)];
end

column = size(image,2); 
zone_height = row/3;
zone_width = column/3;

zone11 = image(1:zone_height,1:zone_width);
zone12 = image(1:zone_height,(zone_width+1):2*zone_width);
zone13 = image(1:zone_height,(2*zone_width+1):end);

zone21 = image((zone_height+1):2*zone_height,1:zone_width);
zone22 = image((zone_height+1):2*zone_height,(zone_width+1):2*zone_width);
zone23 = image((zone_height+1):2*zone_height,(2*zone_width+1):end);

zone31 = image((2*zone_height+1):end,1:zone_width);
zone32 = image((2*zone_height+1):end,(zone_width+1):2*zone_width);
zone33 = image((2*zone_height+1):end,(2*zone_width+1):end);

zone11_features = lineclassifier(zone11);
zone12_features = lineclassifier(zone12);
zone13_features = lineclassifier(zone13);

zone21_features = lineclassifier(zone21);
zone22_features = lineclassifier(zone22);
zone23_features = lineclassifier(zone23);

zone31_features = lineclassifier(zone31);
zone32_features = lineclassifier(zone32);
zone33_features = lineclassifier(zone33);

euler = bweuler(image);
features = [zone11_features; zone12_features; zone13_features; zone21_features; zone22_features; zone23_features; zone31_features; zone32_features; zone33_features];
features = [reshape(features',numel(features),1);euler];

stats = regionprops(bwlabel(image),'all');
eccentricity = stats.Eccentricity;
extent = stats.Extent;
orientation = stats.Orientation;
regional_features = [eccentricity; extent; orientation];
features = [features; regional_features];