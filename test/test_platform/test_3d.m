original = [5,0,5]

MT = [1 0 0;0 0 -1;0 1 0]


new = original*MT

plot3([0 original(1)],[0 original(2)],[0 original(3)],'c');
hold on;
grid on;
plot3([0 new(1)],[0 new(2)],[0 new(3)],'m');

plot3([0 10],[0 0],[0 0],'r');
plot3([-10 0],[0 0],[0 0],'--r');
plot3([0 0],[0 10],[0 0],'b');
plot3([0 0],[-10 0],[0 0],'--b');
plot3([0 0],[0 0],[0 10],'g');
plot3([0 0],[0 0],[-10 0],'--g');