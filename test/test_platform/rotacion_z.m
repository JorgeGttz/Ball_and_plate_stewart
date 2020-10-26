epsilon = 90;
MR = [cosd(epsilon) -sind(epsilon) 0;sind(epsilon) cosd(epsilon) 0;0 0 1];
pos = [1 0 0 ];

new = pos*MR
