function [x,y,z]=draw_polygon(radius,number)
    x=[];
    y=[];
    z=[];
    loop = 1;
    for angle=0:(360/number):360
        x(loop)=radius*cosd(angle);
        y(loop)=radius*sind(angle);
        z(loop)=0;
        loop=loop+1;
    end
    plot3(x,y,z);
    grid on;
end
