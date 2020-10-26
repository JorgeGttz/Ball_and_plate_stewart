function [theta_2,theta_1]=inverse_kinematic(origin,position,length)
    
    if position(1) < 0
        negative = 1;
    else
        negative = 0;
    end
    
    position(1) = abs(position(1));
    cos_theta2 = ((position(1)^2+position(2)^2-length(1)^2-length(2)^2)/(2*length(1)*length(2)));
    sen_theta2_1 = -sqrt(1-cos_theta2^2);
    sen_theta2_2 = sqrt(1-cos_theta2^2);
    theta_2 =[atand(sen_theta2_1/cos_theta2) atand(sen_theta2_2/cos_theta2)]; 
    
    theta_1 = [(atand(position(2)/position(1))-atand((sen_theta2_1*length(2))/(length(1)+length(2)*cos_theta2))) (atand(position(2)/position(1))-atand((sen_theta2_2*length(2))/(length(1)+length(2)*cos_theta2)))];
    if negative == 1
        theta_1(1) = 180-theta_1(1);
        theta_1(2) = 180-theta_1(2);
        theta_2(1) = theta_2(1)*-1;
        theta_2(2) = theta_2(2)*-1;
    end
    x_1 = [origin(1) length(1)*cosd(theta_1(1))+origin(1) length(1)*cosd(theta_1(1))+length(2)*cosd(theta_2(1)+theta_1(1))+origin(1)];
    y_1 = [origin(2) length(1)*sind(theta_1(1))+origin(2) length(1)*sind(theta_1(1))+length(2)*sind(theta_2(1)+theta_1(1))+origin(2)];
    
    x_2 = [origin(1) length(1)*cosd(theta_1(2))+origin(1) length(1)*cosd(theta_1(2))+length(2)*cosd(theta_2(2)+theta_1(2))+origin(1)];
    y_2 = [origin(2) length(1)*sind(theta_1(2))+origin(2) length(1)*sind(theta_1(2))+length(2)*sind(theta_2(2)+theta_1(2))+origin(2)];
    
    if isreal(x_1(2))
        plot(x_1,y_1,'r');
        hold on;
        grid on;
        plot(x_2,y_2,'b');
    else
        errordlg('No Llego :c','ERRORRRRRRRRRR');
    end
end