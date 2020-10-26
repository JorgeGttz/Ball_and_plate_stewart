function draw_system_plate(translation,euler,handles)
%Dibujar la base hexagonal de nuestra plataforma y obtener los puntos 
rotula = 117.22;
base_radius=92;
base_number = 6;

plate_radius=91.98;
scrap_length = 6;
plate_height=0;

servo_length = 16.46;

alpha=[30;
       30;
       30];
   
theta=[150;
       150;
       150];  

   
   
draw_axis(120);
[positions]=draw_polygon(base_radius,base_number,'-.r');
[clock_point,anti_clock_point]=draw_plate(plate_radius,scrap_length,plate_height,'-.b',euler,translation);


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
    right_servo(plane,:) = [positions(1,6)+servo_length*cosd(alpha(plane,1)) positions(2,6) positions(3,6)+servo_length*sind(alpha(plane,1))];
    right_servo(plane,:) = right_servo(plane,:)*rot_matrix;
    left_servo(plane,:)  = [positions(1,5)+servo_length*cosd(theta(plane,1)) positions(2,5) positions(3,5)+servo_length*sind(theta(plane,1))];
    left_servo(plane,:) = left_servo(plane,:)*rot_matrix;
end
%%Right servos are 6,4 and 2
%%Left servos are 5, 1 and 3

%%%%%%%%%%%%%%%%%%%%%%%%actualizar positiones
set(handles.x1_pos,'String',strcat('X1=',num2str(anti_clock_point(1,1))));
set(handles.y1_pos,'String',strcat('Y1=',num2str(anti_clock_point(1,2))));
set(handles.Z1_pos,'String',strcat('Z1=',num2str(anti_clock_point(1,3))));
x1 = anti_clock_point(1,1)
% right_servo(1,2)
% anti_clock_point(1,2)
y1 = abs(anti_clock_point(1,2))-abs(right_servo(1,2))
z1 = anti_clock_point(1,3)
theta_servo = get_theta([x1,y1,z1],[servo_length rotula]);
positions(1,6)
% theta

set(handles.x2_pos,'String',strcat('X2=',num2str(clock_point(2,1))));
set(handles.y2_pos,'String',strcat('Y2=',num2str(clock_point(2,2))));
set(handles.z2_pos,'String',strcat('Z2=',num2str(clock_point(2,3))));

set(handles.x3_pos,'String',strcat('X3=',num2str(anti_clock_point(2,1))));
set(handles.y3_pos,'String',strcat('Y3=',num2str(anti_clock_point(2,2))));
set(handles.z3_pos,'String',strcat('Z3=',num2str(anti_clock_point(2,3))));

set(handles.x4_pos,'String',strcat('X4=',num2str(clock_point(3,1))));
set(handles.y4_pos,'String',strcat('Y4=',num2str(clock_point(3,2))));
set(handles.z4_pos,'String',strcat('Z4=',num2str(clock_point(3,3))));

set(handles.x5_pos,'String',strcat('X5=',num2str(anti_clock_point(3,1))));
set(handles.y5_pos,'String',strcat('Y5=',num2str(anti_clock_point(3,2))));
set(handles.z5_pos,'String',strcat('Z5=',num2str(anti_clock_point(3,3))));

set(handles.x6_pos,'String',strcat('X6=',num2str(clock_point(1,1))));
set(handles.y6_pos,'String',strcat('Y6=',num2str(clock_point(1,2))));
set(handles.z6_pos,'String',strcat('Z6=',num2str(clock_point(1,3))));

%%%%%%%%%%%%%%%%%%%%%%%%%%
rotate3d on;
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
end