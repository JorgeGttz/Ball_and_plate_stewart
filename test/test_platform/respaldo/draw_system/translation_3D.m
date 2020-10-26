function new_pos=translation_3D(position,translation)
    position(4) = 1;
    
    TM = [            1              0               0     0;
                      0              1               0     0;
                      0              0               1     0
          translation(1) translation(2)  translation(3)    0];
    new_pos = position*TM;
    new_pos = new_pos(1,1:3);
end