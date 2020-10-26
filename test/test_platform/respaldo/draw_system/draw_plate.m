function [clock_point,anti_clock_point]=draw_plate(centroid_dist,scrap,height,style,euler_angles,translation)

point = [0 -centroid_dist];
point(3) = 1;

anti_clock_mat = [1 0 0;0 1 0;(scrap/2) -scrap 1];
clock_mat = [1 0 0;0 1 0;-(scrap/2) -scrap 1];

anti_clock_point=[];
clock_point=[];
rot_angles = [0 -120 -240];

side=1;
rot_roll_mat = [1 0 0;0 cosd(euler_angles(3)) -sind(euler_angles(3));0 sind(euler_angles(3)) cosd(euler_angles(3))];
rot_pitch_mat = [cosd(euler_angles(2)) 0 -sind(euler_angles(2));0 1 0;sind(euler_angles(2)) 0 cosd(euler_angles(2))];
rot_yaw_mat = [cosd(euler_angles(1)) -sind(euler_angles(1)) 0;sind(euler_angles(1)) cosd(euler_angles(1)) 0;0 0 1];

for angle = rot_angles
    anti_clock_point(side,:) = point*anti_clock_mat;
    clock_point(side,:)= point*clock_mat;
    
    rot_mat = [cosd(angle) -sind(angle);sind(angle) cosd(angle)];
    
    clock_point(side,1:2)=clock_point(side,1:2)*rot_mat;
    clock_point(side,3)=height;    
    clock_point(side,:)=translation_3D(clock_point(side,:),[translation(1) translation(2) translation(3)]);
    clock_point(side,:)=clock_point(side,:)*rot_roll_mat*rot_pitch_mat*rot_yaw_mat;
    
    anti_clock_point(side,1:2)=anti_clock_point(side,1:2)*rot_mat;
    anti_clock_point(side,3)=height;
    anti_clock_point(side,:)=translation_3D(anti_clock_point(side,:),[translation(1) translation(2) translation(3)]);
    anti_clock_point(side,:)=anti_clock_point(side,:)*rot_roll_mat*rot_pitch_mat*rot_yaw_mat;
    side=side+1;
end
anti_clock_point(1,:)
%de = traslation_3D(anti_clock_point(1,:),[5,5,5]);
%de
plot3([clock_point(1,1) anti_clock_point(1,1)],[clock_point(1,2) anti_clock_point(1,2)],[clock_point(1,3) anti_clock_point(1,3)],style);
hold on;
grid on;
axis([-15 15 -15 15 0 15]);
plot3([anti_clock_point(1,1) clock_point(2,1)],[anti_clock_point(1,2) clock_point(2,2)],[anti_clock_point(1,3) clock_point(2,3)],style);
plot3([clock_point(2,1) anti_clock_point(2,1)],[clock_point(2,2) anti_clock_point(2,2)],[clock_point(2,3) anti_clock_point(2,3)],style);
plot3([anti_clock_point(2,1) clock_point(3,1)],[anti_clock_point(2,2) clock_point(3,2)],[anti_clock_point(2,3) clock_point(3,3)],style);
plot3([clock_point(3,1) anti_clock_point(3,1)],[clock_point(3,2) anti_clock_point(3,2)],[clock_point(3,3) anti_clock_point(3,3)],style);
plot3([anti_clock_point(3,1) clock_point(1,1)],[anti_clock_point(3,2) clock_point(1,2)],[anti_clock_point(3,3) clock_point(1,3)],style);
end
