function [servo_theta]=get_theta(pos,link_length)
%pos = [70 50 60];
%link_length = [58.31 61.64];

%%theta3 = atand(pos(2)/pos(1))
link_help_2 = sqrt(link_length(2)^2 - pos(2)^2);

costheta2 = (pos(1)^2 + pos(3)^2 - link_length(1)^2 - link_help_2^2)/(2*link_length(1)*link_help_2);

sentheta2_1 = -sqrt(1-costheta2^2);
sentheta2_2 = sqrt(1-costheta2^2);
 
theta2_1 = atand(sentheta2_1/costheta2);
theta2_2 = atand(sentheta2_2/costheta2);

theta1_1 = atand(pos(3)/pos(1))-atand((link_help_2*sentheta2_1)/(link_length(1)+link_help_2*costheta2));
theta1_2 = atand(pos(3)/pos(1))-atand((link_help_2*sentheta2_2)/(link_length(1)+link_help_2*costheta2));

servo_theta = [theta1_1 theta1_2]
end