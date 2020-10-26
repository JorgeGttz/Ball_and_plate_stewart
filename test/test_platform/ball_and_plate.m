%Creacion de la base del ball and plate
base_radius=10;
base_number = 6;
draw_axis(15);
[x_base,y_base,z_base]=draw_polygon(base_radius,base_number);

%Creacion del primer eje del servo
length_01 = 5;
theta=[45 125];
new_pos = [x_base(6)+length_01*cosd(theta(1)) y_base(6) z_base(6)+length_01*sind(theta(1))];
new_pos_2 = [x_base(5)+length_01*cosd(theta(2)) y_base(5) z_base(5)+length_01*sind(theta(2))]
plot3([x_base(6) new_pos(1)],[y_base(6) new_pos(2)],[z_base(6) new_pos(3)],'c');
plot3([x_base(5) new_pos_2(1)],[y_base(5) new_pos_2(2)],[z_base(5) new_pos_2(3)],'k');
%creacion de la rotacion en Z
% epsilon =-120;
% 
% matriz_rotacion = [cosd(epsilon) -sind(epsilon) 0;sind(epsilon) cosd(epsilon) 0;0 0 1];
% new_pos = [x_base(6)+length_01*cosd(theta(1)) y_base(6) z_base(6)+length_01*sind(theta(1))];
% new_rot = new_pos*matriz_rotacion;
% plot3([x_base(2) new_rot(1)],[y_base(2) new_rot(2)],[z_base(2) new_rot(3)],'m');
% 
% epsilon =-240;
% matriz_rotacion = [cosd(epsilon) -sind(epsilon) 0;sind(epsilon) cosd(epsilon) 0;0 0 1];
% new_pos = [x_base(6)+length_01*cosd(theta(1)) y_base(6) z_base(6)+length_01*sind(theta(1))];
% new_rot = new_pos*matriz_rotacion;
% plot3([x_base(4) new_rot(1)],[y_base(4) new_rot(2)],[z_base(4) new_rot(3)],'b');