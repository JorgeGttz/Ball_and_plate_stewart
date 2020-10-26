original = [0 0 0 1]
matriz_distancia = [0 5 0];

MT = [1 0 0 0;0 1 0 0;0 0 1 0;matriz_distancia(1) matriz_distancia(2) matriz_distancia(3) 1];


new = original*MT

plot3([0 10],[0 0],[0 0],'r');
hold on;
grid on;
plot3([-10 0],[0 0],[0 0],'--r');
plot3([0 0],[0 10],[0 0],'b');
plot3([0 0],[-10 0],[0 0],'--b');
plot3([0 0],[0 0],[0 10],'g');
plot3([0 0],[0 0],[-10 0],'--g');

plot3([0 original(1)],[0 original(2)],[0 original(3)],'c');
plot3([0 new(1)],[0 new(2)],[0 new(3)],'m');
