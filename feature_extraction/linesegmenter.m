function [segments] = linesegmenter(image)

[starters, intersections] = starter_intersection(image);
previousdirection = 0;
currentpixel = [0,0];
image = [image,zeros(size(image,1),1)];  
image = [zeros(1,size(image,2));image];
image = [zeros(size(image,1),1),image];
image = [image;zeros(1,size(image,2))];
minor_starters_queue = [];
starters  =  starters + 1;
intersections  =  intersections + 1;

if isempty(starters) 
    [r,c] = find(image == 1);
    coordinates = [r,c];
    starter1 = coordinates(1,:);
    starter2 = coordinates(end,:);
    minor_starters_queue = [starter1;starter2];
end

N = 1;
segments = {};
starters_queue = starters; 
visited = [];

while(isnotempty(starters_queue) || isnotempty(minor_starters_queue))
    currentsegment = [];
    if isnotempty(starters_queue)
        if isnotmember(starters_queue(1,:),visited)
            current_starter = starters_queue(1,:);
            starters_queue = del_pixel(current_starter,starters_queue);
            currentpixel = findneighbours(image,current_starter);
            visited = [visited;current_starter];
            currentsegment = [currentsegment;current_starter];
            nextdirection = finddirection(current_starter,currentpixel);
            previousdirection = nextdirection;
        else
            starters_queue = del_pixel(starters_queue(1,:),starters_queue);
            continue; 
        end
    elseif (isempty(starters_queue)  &&  isnotempty(minor_starters_queue))
        currentminor = minor_starters_queue(1,:);
        currentsegment = [];
        if ismymember(currentminor,visited) 
            minor_starters_queue = del_pixel(currentminor,minor_starters_queue);
            continue;
        end
        visited = [visited;currentminor]; 
        neighbours = findneighbours(image,currentminor); 
        temp = 1;
        while temp <= size(neighbours,1) 
            current_neighbour = neighbours(temp,:);
            if (ismymember(current_neighbour,visited) || ismymember(current_neighbour,minor_starters_queue))
                neighbours = del_pixel(current_neighbour,neighbours);
                temp = 1;
            else
                temp = temp + 1;
            end
        end
        unvisited_neighbours = neighbours;
        if size(unvisited_neighbours,1) > 2
            minor_starters_queue = del_pixel(currentminor,minor_starters_queue);
            continue;
        end
        if size(unvisited_neighbours,1) == 2
            discarded = unvisited_neighbours(1,:);
            currentpixel = unvisited_neighbours(2,:);
            currentsegment = [currentsegment;currentminor];
            minor_starters_queue = [minor_starters_queue;discarded];
        elseif isempty(unvisited_neighbours)
            minor_starters_queue = del_pixel(currentminor,minor_starters_queue);
            continue;
        elseif size(unvisited_neighbours,1) == 1
            currentpixel = unvisited_neighbours;
            currentsegment = [currentsegment;currentminor];
        end
    end
    while(isnotmember(currentpixel,visited))
        if(isnotmember(currentpixel,intersections)  &&  isnotmember(currentpixel,starters_queue))
            neighbours = findneighbours(image,currentpixel);
            visited = [visited;currentpixel];
            temp = 1;
            while temp <= size(neighbours,1)
                current_neighbour = neighbours(temp,:);
                if (ismymember(current_neighbour,visited))
                    neighbours = del_pixel(current_neighbour,neighbours);
                    temp = 1;
                else
                    temp = temp + 1;
                end
            end
            if size(neighbours,1) > 2 
                temp = 1;
                while temp <= size(neighbours,1)
                    current_neighbour = neighbours(temp,:);
                    if (ismymember(current_neighbour,minor_starters_queue))
                        neighbours = del_pixel(current_neighbour,neighbours);
                        temp = 1;
                    else
                        temp = temp + 1;
                    end
                end
            end
            if isempty(neighbours)  
                currentsegment = [currentsegment;currentpixel];
                segments{N} = currentsegment;
                N = N + 1;
                break;
            end
            if size(neighbours,1) == 1
                nextpixel = neighbours;
            elseif size(neighbours,1) == 2 
                first_neighbour = neighbours(1,:);
                second_neighbour = neighbours(2,:);
                if ismymember(first_neighbour,intersections) || ismymember(second_neighbour,intersections)
                    currentsegment = [currentsegment;currentpixel];
                    if ismymember(first_neighbour,intersections)
                        currentsegment = [currentsegment;first_neighbour];
                        segments{N} = currentsegment;
                        N = N + 1;
                        visited = [visited;first_neighbour];
                        minor_starters_queue = [minor_starters_queue;second_neighbour];
                    else
                        currentsegment = [currentsegment;second_neighbour];
                        segments{N} = currentsegment;
                        N = N + 1;
                        visited = [visited;second_neighbour];
                        minor_starters_queue = [minor_starters_queue;first_neighbour];
                    end
                    minor_starters_queue = [minor_starters_queue;first_neighbour;second_neighbour];
                    break;
                end
                neighbour_one_direction = finddirection(currentpixel,first_neighbour);
                neighbour_two_direction = finddirection(currentpixel,second_neighbour);
                if(neighbour_one_direction == previousdirection)
                    neighbours = del_pixel(second_neighbour,neighbours);
                    nextpixel = neighbours;
                else
                    neighbours = del_pixel(first_neighbour,neighbours);
                    nextpixel = neighbours;
                end
            elseif size(neighbours,1) > 2
                unconsidered = neighbours;
                for i = 1:size(neighbours,1)
                    current_neighbour = neighbours(i,:);
                    if ismymember(current_neighbour,intersections)
                        unconsidered = del_pixel(current_neighbour,unconsidered);
                        visited = [visited;current_neighbour];
                        currentsegment = [currentsegment;current_neighbour];
                        segments{N} = currentsegment;
                        N = N + 1;
                        currentsegment = [];
                        break;
                    end
                end
                minor_starters_queue = [minor_starters_queue;unconsidered];
                break;
            end
            currentsegment = [currentsegment;currentpixel];
            previousdirection = finddirection(currentpixel,nextpixel);
            previouspixel = currentpixel;
            currentpixel = nextpixel;  
        elseif (ismymember(currentpixel,intersections)) 
            visited = [visited;currentpixel];
            neighbours = findneighbours(image,currentpixel);
            unvisited_neighbours = []; 
            for i = 1:size(neighbours,1)
                if isnotmember(neighbours(i,:),visited)
                    unvisited_neighbours = [unvisited_neighbours;neighbours(i,:)];
                end
            end
            unvisited_directions = [];
            direction_flag = 0; 
            for i = 1:size(unvisited_neighbours,1)
                current_neighbour = unvisited_neighbours(i,:);
                current_neighbour_direction = finddirection(currentpixel,current_neighbour);
                if current_neighbour_direction == previousdirection
                    direction_flag = 1;
                    currentsegment = [currentsegment;currentpixel];
                    currentpixel = current_neighbour;
                    unvisited_neighbours = del_pixel(current_neighbour,unvisited_neighbours);
                    minor_starters_queue = [minor_starters_queue;unvisited_neighbours];
                    unvisited_neighbours = [];
                    break;
                end
            end
            if direction_flag == 0
                minor_starters_queue = [minor_starters_queue;unvisited_neighbours];
                currentsegment = [currentsegment;currentpixel];
                segments{N} = currentsegment;
                N = N + 1;
            end
        elseif (ismymember(currentpixel,starters_queue))
            currentsegment = [currentsegment;currentpixel];
            starters_queue = del_pixel(currentpixel,starters_queue);
            visited = [visited;currentpixel];
            segments{N} = currentsegment;
            N = N + 1;
        elseif (ismymember(currentpixel,minor_starters_queue))
            currentsegment = [currentsegment;currentpixel];
            minor_starters_queue = del_pixel(currentpixel,minor_starters_queue);
            visited = [visited;currentpixel];
            segments{N} = currentsegment;
            N = N + 1;
        end
    end
end

for i = 1:(N-1)
    segments{i} = segments{i} - 1;
end