function direction = finddirection(first, second)

direction = 0;
position = second - first;

if position == [1,0]
    direction = 1;
elseif position == [1,-1]
    direction = 2;
elseif position == [0,-1]
    direction = 3;
elseif position == [-1,-1]
    direction = 4;
elseif position == [-1,0]
    direction = 5;
elseif position == [-1,1]
    direction = 6;
elseif position == [0,1]
    direction = 7;
elseif position == [1,1]
    direction = 8;
end