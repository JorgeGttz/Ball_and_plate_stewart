%Dibujar la base hexagonal de nuestra plataforma y obtener los puntos 
base_radius=10;
base_number = 6;

plate_radius=5;
scrap_length = 2;
plate_height=12;

length = [5];

alpha=[30;
       30;
       30];
   
theta=[150;
       150;
       150];  

   
   
draw_axis(15);
[positions]=draw_polygon(base_radius,base_number,'-.r');
[clock_point,anti_clock_point]=draw_plate(plate_radius,scrap_length,plate_height,'-.b',[0 0 0],[0 0 0]);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%        Alpha and Theta Matrix
%   PLANE_1   [DOF_1   DOF_2   DOF_3]
%   PLANE_2   [DOF_1   DOF_2   DOF_3]
%   PLANE_3   [DOF_1   DOF_2   DOF_3]
%   Alpha(2,3)   -- Plane2,DOF3
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

right_servo=[];
left_servo=[];

plane_angles = [0 -120 -240];
for plane=1:3
    rot_matrix = [cosd(plane_angles(plane)) -sind(plane_angles(plane)) 0;sind(plane_angles(plane)) cosd(plane_angles(plane)) 0;0 0 1];
    right_servo(plane,:) = [positions(1,6)+length(1)*cosd(alpha(plane,1)) positions(2,6) positions(3,6)+length(1)*sind(alpha(plane,1))];
    right_servo(plane,:) = right_servo(plane,:)*rot_matrix;
    left_servo(plane,:)  = [positions(1,5)+length(1)*cosd(theta(plane,1)) positions(2,5) positions(3,5)+length(1)*sind(theta(plane,1))];
    left_servo(plane,:) = left_servo(plane,:)*rot_matrix;
end
%%Right servos are 6,4 and 2
%%Left servos are 5, 1 and 3
 plot3([positions(1,6) right_servo(1,1)],[positions(2,6) right_servo(1,2)],[positions(3,6) right_servo(1,3)],'c');
 plot3([positions(1,5) left_servo(1,1)],[positions(2,5) left_servo(1,2)],[positions(3,5) left_servo(1,3)],'m');
 
 plot3([positions(1,2) right_servo(2,1)],[positions(2,2) right_servo(2,2)],[positions(3,2) right_servo(2,3)],'c');
 plot3([positions(1,1) left_servo(2,1)],[positions(2,1) left_servo(2,2)],[positions(3,1) left_servo(2,3)],'m');
 
 plot3([positions(1,4) right_servo(3,1)],[positions(2,4) right_servo(3,2)],[positions(3,4) right_servo(3,3)],'c');
 plot3([positions(1,3) left_servo(3,1)],[positions(2,3) left_servo(3,2)],[positions(3,3) left_servo(3,3)],'m');
 %%%%%%%%%%%%Dibuja longitudes del tie rod
 
 for i=1:3
    plot3([right_servo(i,1) anti_clock_point(i,1)],[right_servo(i,2) anti_clock_point(i,2)],[right_servo(i,3) anti_clock_point(i,3)],'--c');
    plot3([left_servo(i,1)  clock_point(i,1)],[left_servo(i,2) clock_point(i,2)],[left_servo(i,3) clock_point(i,3)],'--m');
 end
 %plot3([positions(1,5) left_servo(1,1)],[positions(2,5) left_servo(1,2)],[positions(3,5) left_servo(1,3)],':m');
