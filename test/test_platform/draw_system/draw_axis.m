function draw_axis(tam)
    plot3([0 1*tam],[0 0],[0 0],'r');
    hold on;
    grid on;
    plot3([-1*tam 0],[0 0],[0 0],'--r');
    plot3([0 0],[0 1*tam],[0 0],'b');
    plot3([0 0],[-1*tam 0],[0 0],'--b');
    plot3([0 0],[0 0],[0 1*tam],'g');
    %plot3([0 0],[0 0],[-1*tam 0],'--g');
end