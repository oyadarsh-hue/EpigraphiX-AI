function [neighbours] = findneighbours(image, coords)

imwindow = image((coords(1)-1):(coords(1)+1),(coords(2)-1):(coords(2)+1));
neighbours = [];
imwindow(2,2) = 0; 
indexes = find(imwindow == 1);

for i = 1 : length(indexes)
    currentindex = indexes(i);
    row = rem(currentindex,3);
    if(row == 0)
        row = 3; 
    end
    column = ceil(currentindex/3);
    neighbours = [neighbours;[row,column]];
end

neighbours(:,1) = coords(1)+(neighbours(:,1)-2);
neighbours(:,2) = coords(2)+(neighbours(:,2)-2);