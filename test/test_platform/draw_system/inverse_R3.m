pos = [70 50 60];
link_length = [58.31 61.64];

%%theta3 = atand(pos(2)/pos(1))
link_help_2 = sqrt(link_length(2)^2 - pos(2)^2);

costheta2 = (pos(1)^2 + pos(3)^2 - link_length(1)^2 - link_help_2^2)/(2*link_length(1)*link_help_2);

sentheta2_1 = -sqrt(1-costheta2^2);
sentheta2_2 = sqrt(1-costheta2^2);
 
theta2_1 = atand(sentheta2_1/costheta2);
theta2_2 = atand(sentheta2_2/costheta2);

theta1_1 = atand(pos(3)/pos(1))-atand((link_help_2*sentheta2_1)/(link_length(1)+link_help_2*costheta2));
theta1_2 = atand(pos(3)/pos(1))-atand((link_help_2*sentheta2_2)/(link_length(1)+link_help_2*costheta2));

x1_1=link_length(1)*cosd(theta1_1);
x1_2=link_length(1)*cosd(theta1_2);

z1_1=link_length(1)*sind(theta1_1);
z1_2=link_length(1)*sind(theta1_2);

x = [0 x1_1 pos(1)];
y = [0    0 pos(2)];
z = [0 z1_1 pos(3)];

draw_axis(120);
plot3(x,y,z);

x = [0 x1_2 pos(1)];
y = [0    0 pos(2)];
z = [0 z1_2 pos(3)];
plot3(x,y,z);