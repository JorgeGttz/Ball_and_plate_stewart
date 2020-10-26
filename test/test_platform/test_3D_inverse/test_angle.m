pos = [4,6,7];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
theta01 = atand(pos(2)/pos(1));

rot_mat = [cosd(theta01) -sind(theta01) 0;
           sind(theta01)  cosd(theta01) 0;
                      0              0  1];

new = pos*rot_mat;

draw_axis(10);
hold on;
grid on;

x = [0 10*cosd(theta01)];
y = [0 10*sind(theta01)];
z = [0 0];
plot3(x,y,z);

x = [0 pos(1)];
y = [0 pos(2)];
z = [0 pos(3)];
plot3(x,y,z);

x = [0 new(1)];
y = [0 new(2)];
z = [0 new(3)];
plot3(x,y,z);