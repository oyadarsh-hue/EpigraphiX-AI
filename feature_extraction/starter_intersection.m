function [starters_list,intersections] = starter_intersection(image)

image = [image,zeros(size(image,1),1)]; 
image = [zeros(1,size(image,2));image];
image = [zeros(size(image,1),1),image]; 
image = [image;zeros(1,size(image,2))];
row = size(image,1);
column = size(image,2);
starters_list = [];
intersections = [];

for m = 2 : (row-1)
    for n = 2 : (column-1)
        if (image(m,n) == 1)
            neighberhood = image(m-1:m+1,n-1:n+1);
            neighbours = numel(find(neighberhood == 1))-1;
            if neighbours == 1
                starters_list = [starters_list;[m,n]];
            end
            if neighbours == 3 
                surrounders = findneighbours(image,[m,n]);
                directions = [];
                trueneighbours = 3;
                for i = 1 : 3
                    currentdirection = finddirection([m,n],surrounders(i,:));
                    directions = [directions,currentdirection];
                end
                for i = 1 : 3
                    currentdirection = directions(i);
                    if currentdirection == 1
                        adjacency = find(directions == 8 | directions == 2, 1);
                        if isempty(adjacency)
                            continue;
                        else
                            trueneighbours = trueneighbours - 1;
                            break;
                        end
                    elseif currentdirection == 8
                        adjacency = find(directions == 7 |directions == 1, 1);
                        if isempty(adjacency)
                            continue;
                        else
                            trueneighbours = trueneighbours - 1;
                            break;
                        end                        
                    else
                        adjacency = find(directions == currentdirection-1 | directions == currentdirection+1, 1);
                        if isempty(adjacency)
                            continue;
                        else
                            trueneighbours = trueneighbours - 1;
                            break;
                        end
                    end
                end                
                if trueneighbours == 3
                    intersections = [intersections;[m,n]];
                end
            end
            if neighbours == 4
                surrounders = findneighbours(image,[m,n]);
                cornerpixels = 0;
                directpixels = 0;
                for i = 1 : 4
                    currentdirection = finddirection([m,n],surrounders(i,:));
                    if(rem(currentdirection,2) == 0) 
                        cornerpixels = cornerpixels + 1;
                    else
                        directpixels = directpixels + 1;
                    end
                end
                if cornerpixels ~= 2
                    intersections = [intersections;[m,n]];
                end
            end
            if neighbours > 4
                intersections = [intersections;[m,n]];
            end
        end
    end
end
starters_list = starters_list - 1;
intersections = intersections - 1;