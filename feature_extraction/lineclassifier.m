function [featurevector] = lineclassifier(image)

down = 1;        
downleft = 2;
left = 3;
upleft = 4;
up = 5;
upright = 6;
right = 7;
downright = 8;
image = prep_image(image);
skel_size = length(find(image == 1));

if skel_size <= 1
    featurevector = -1*ones(1,9);
    return;
end

segments = linesegmenter(image);
N_segments = numel(segments);
segmentdirection = {};

for i = 1 : N_segments
    currentsegment = segments{i};
    currentdirectionvector = [];
    if size(currentsegment,1) == 1
        error('At lineclassifier.m, you have a segment with only one pixel');
    else
        for j = 1 : (size(currentsegment,1)-1)
            currentpixel = currentsegment(j,:);
            nextpixel = currentsegment(j+1,:);
            nextdirection = finddirection(currentpixel,nextpixel);
            currentdirectionvector = [currentdirectionvector;nextdirection];
        end
    end
    segmentdirection{i} = currentdirectionvector;
end

Truelines = {};
N = 1;

for i = 1 : N_segments
    currentdir_segment = segmentdirection{i};
    if numel(currentdir_segment) > 2 
        j = 1;
        currentline = [];
        while j < numel(currentdir_segment)
            previousdirection = currentdir_segment(j);
            nextdirection = currentdir_segment(j+1);
            rule_one = (previousdirection == upright | previousdirection == downleft) & (nextdirection == downright | nextdirection == upleft);
            rule_two = (previousdirection == downright | previousdirection == upleft) & (nextdirection == upright | nextdirection == downleft);
            if (rule_one || rule_two)
                Truelines{N} = [currentline;previousdirection;nextdirection];
                N = N + 1;
                if j+2 >= numel(currentdir_segment)  
                    break;
                else
                    j = j + 2;
                end
            else
                currentline = [currentline;currentdir_segment(j)];
                j = j + 1;
                if j == numel(currentdir_segment)
                    Truelines{N} = [currentline;currentdir_segment(end)];
                    N = N + 1;
                    break;
                end
            end
        end
    elseif numel(currentdir_segment) < 3
        currentdir_segment(:) = currentdir_segment(1); 
        currentline = currentdir_segment;
        Truelines{N} = currentline;
        N = N + 1;
    end
end

N_Truelines = numel(Truelines);
Normallines = {}; 
N = 1;

for i = 1 : N_Truelines
    currentline = Truelines{i};
    currentlength = numel(currentline);
    occurencematrix = [];
    for j = 1 : 8        
        occurencematrix = [occurencematrix,numel(find(currentline == j))];
    end
    currentmaxoccurence = max(occurencematrix); 
    current_max_direction = find(currentmaxoccurence == occurencematrix); 
    repetition = numel(current_max_direction)-1; 
    if repetition ~= 0
    end
    Normallines{N} = current_max_direction(1)*ones(1,currentlength);% in case two dir types occured same no.of times,first dir is taken
    N = N + 1;
end
 
N_horizontal = 0;
N_vertical = 0;  
N_rightslant = 0;
N_leftslant = 0;
L_horizontal = 0;
L_vertical = 0;  
L_rightslant = 0;
L_leftslant = 0; 
N_Normallines = numel(Normallines);

for i = 1 : N_Normallines
    currentline = Normallines{i};
    firstelement = currentline(1);
    if firstelement == left || firstelement == right
        N_horizontal = N_horizontal + 1;
        L_horizontal = L_horizontal + length(currentline);
    elseif firstelement == up || firstelement == down
        N_vertical = N_vertical + 1;
        L_vertical = L_vertical + length(currentline);
    elseif firstelement == upleft || firstelement == downright
        N_leftslant = N_leftslant + 1;
        L_leftslant = L_leftslant + length(currentline);
    elseif firstelement == upright || firstelement == downleft
        N_rightslant = N_rightslant + 1;
        L_rightslant = L_rightslant + length(currentline);
    end
end

V_horizontal = 1-((N_horizontal)/10)*2;
V_vertical = 1-((N_vertical)/10)*2;
V_rightslant = 1-((N_rightslant)/10)*2;
V_leftslant = 1-((N_leftslant)/10)*2;

if skel_size ~= 0
    norm_horizontal = L_horizontal/skel_size;
    norm_vertical = L_vertical/skel_size;
    norm_rightslant = L_rightslant/skel_size;
    norm_leftslant = L_leftslant/skel_size;
else
    norm_horizontal = -1;
    norm_vertical = -1;
    norm_rightslant = -1;
    norm_leftslant = -1;
end

filled_area = skel_size/numel(image);
featurevector = [V_horizontal,V_vertical,V_rightslant,V_leftslant,norm_horizontal,norm_vertical,norm_rightslant,norm_leftslant,filled_area];