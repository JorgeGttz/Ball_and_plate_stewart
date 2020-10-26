import numpy as np
import platform,os,math

def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def position_translate(position,delta):
    """
    ---Translate an specific point ---
    [x,y,z,1][1  0  0  1 = [x+dx,y+dy,z+dz,1]
              0  1  0  0
              0  0  1  0
              dx dy dz 0]
     position_translate(position,delta)
    """
    position.append(1) #Add to the enteredosition 1, we need it to multiply matrix
    pos_mat = np.matrix(position)


    translation_matrix = np.matrix([[1,0,0,1],[0,1,0,0],[0,0,1,0],[delta[0],delta[1],delta[2],0]])

    new_pos = position*translation_matrix
    new_pos = new_pos[0,:-1]
    #new_pos = np.asarray(new_pos)
    position.pop()
    return new_pos

def position_rotate(position,angles):
    """
    ---Rotate an specific point by the axis ---
     position_rotate(position,angles)

     position_rotate([x,y,z],[yaw,pitch,roll])

     Example:
        Rotate [0,0,1] by yaw 90 degrees

        position_rotate([0,0,1],[90,0,0])
    """
    mat_point = np.matrix(position)
    for i in range(len(angles)):
        angles[i] = math.radians(angles[i])

    rot_roll  = np.matrix([[1,0,0],[0,math.cos(angles[2]), -math.sin(angles[2])],[0,math.sin(angles[2]),math.cos(angles[2])]])
    rot_pitch = np.matrix([[math.cos(angles[1]),0,-math.sin(angles[1])],[0,1,0],[math.sin(angles[1]),0,math.cos(angles[1])]])
    rot_yaw   = np.matrix([[math.cos(angles[0]),-math.sin(angles[0]),0],[math.sin(angles[0]),math.cos(angles[0]),0],[0,0,1]])
    return mat_point*rot_roll*rot_pitch*rot_yaw

def get_servo_angle(position_input,links_length,base_input):
    if len(links_length) != 2:
        print("You should put only two links_length")
    if len(position_input[0]) != 3 or len(base_input[0]) != 3:
        print("This function is only available for 3 DOF with 2 links_length")
    
    theta1=[]
    theta2=[]
    
    current_point=0
    side_angles = [0,120,240]
    
    for current_angle in side_angles:
        #print("--- Point {}---".format(current_point))
        #print("Angle = {}".format(current_angle))
        position = position_rotate(position_input[current_point],[current_angle,0,0]).tolist()[0]
        base = position_rotate(base_input[current_point],[current_angle,0,0]).tolist()[0]
        
        #print("Plate {}".format(position))
        #print("Base {}".format(base))
        #print("Before translate {}".format(position))
        position = position_translate(position,[-base[0],-base[1],-base[2]]).tolist()[0]
        #print("After translate {}".format(position))
        
        help_link = math.sqrt(math.pow(links_length[1],2)-math.pow(position[1],2))

        costheta2 = (math.pow(position[0],2)+math.pow(position[2],2)-math.pow(links_length[0],2)-math.pow(help_link,2))/(2*links_length[0]*help_link)

        sentheta2 = [-math.sqrt(1 - math.pow(costheta2,2)),math.sqrt(1 - math.pow(costheta2,2))]
        
        theta2_c = []
        theta1_c = []
        
        theta2_c = [math.degrees(math.atan(sentheta2[0]/costheta2)),math.degrees(math.atan(sentheta2[1]/costheta2))]

        theta1_c = [math.atan(float(position[2])/float(position[0]))-math.atan((help_link*sentheta2[0])/(links_length[0]+help_link*costheta2))]
        theta1_c.append(math.atan(float(position[2])/float(position[0]))-math.atan((help_link*sentheta2[1])/(links_length[0]+help_link*costheta2)))
        theta1_c[0] = math.degrees(theta1_c[0])
        theta1_c[1] = math.degrees(theta1_c[1])
        
        if position[0] < 0:
            theta1_c[0] = theta1_c[0]+180
            theta1_c[1] = theta1_c[1]+180
        theta1.append(theta1_c)
        theta2.append(theta2_c)
        current_point+=1
        ###antipoint
        #print("--- Point {}---".format(current_point))
        #print("Angle = {}".format(current_angle))
        position = position_rotate(position_input[current_point],[current_angle,0,0]).tolist()[0]
        base = position_rotate(base_input[current_point],[current_angle,0,0]).tolist()[0]
        
        #print("Plate {}".format(position))
        #print("Base {}".format(base))
        #print("Before translate {}".format(position))
        position = position_translate(position,[-base[0],-base[1],-base[2]]).tolist()[0]
        #print("After translate {}".format(position))
        
        help_link = math.sqrt(math.pow(links_length[1],2)-math.pow(position[1],2))

        costheta2 = (math.pow(position[0],2)+math.pow(position[2],2)-math.pow(links_length[0],2)-math.pow(help_link,2))/(2*links_length[0]*help_link)

        sentheta2 = [math.sqrt(1 - math.pow(costheta2,2)),-math.sqrt(1 - math.pow(costheta2,2))]
        
        theta2_c = []
        theta1_c = []
        
        theta2_c = [math.degrees(math.atan(sentheta2[0]/costheta2)),math.degrees(math.atan(sentheta2[1]/costheta2))]

        theta1_c = [math.atan(float(position[2])/float(position[0]))-math.atan((help_link*sentheta2[0])/(links_length[0]+help_link*costheta2))]
        theta1_c.append(math.atan(float(position[2])/float(position[0]))-math.atan((help_link*sentheta2[1])/(links_length[0]+help_link*costheta2)))
        
        theta1_c[0] = math.degrees(theta1_c[0])
        theta1_c[1] = math.degrees(theta1_c[1])
        
        if position[0] < 0:
            theta1_c[0] = theta1_c[0]+180
            theta1_c[1] = theta1_c[1]+180
        theta1.append(theta1_c)
        theta2.append(theta2_c)
        current_point+=1
        
    return theta1,theta2

def base_points(radio):
    points =[]
    for angle in [240,300,0,60,120,180]:
        points.append([radio*math.cos(math.radians(angle)),radio*math.sin(math.radians(angle)),0])
    return points

def plate_points(centroid_dist,scrap,euler_angles,translation):
    #Make the point for the translation
    point = [0,-centroid_dist,0]

    points=[]
    rot_angles = [0,-120,-240]
    for side_angle in rot_angles:
        anticlock = position_translate(point,[-(scrap/2),-scrap,0]).tolist()[0]
        anticlock = position_rotate(anticlock,[side_angle,0,0]).tolist()[0]
        anticlock = position_rotate(anticlock,[euler_angles[0],euler_angles[1],euler_angles[2]]).tolist()[0]
        anticlock = position_translate(anticlock,translation).tolist()[0]
        #print("anticlock = {}".format(anticlock))
        points.append(anticlock)
        clock = position_translate(point,[(scrap/2),-scrap,0]).tolist()[0]
        clock = position_rotate(clock,[side_angle,0,0]).tolist()[0]
        clock = position_rotate(clock,[euler_angles[0],euler_angles[1],euler_angles[2]]).tolist()[0]
        clock = position_translate(clock,translation).tolist()[0]
        #print("clock = {}".format(clock))
        points.append(clock)
    return points
    
    

def points_to_xyz(points):
    x = []
    y = []
    z = []
    for i in points:
        x.append(i[0])
        y.append(i[1])
        z.append(i[2])
    return x,y,z

def draw_by_points(points,ax,fig,color):
    x,y,z = points_to_xyz(points)
    
    x.append(x[0])
    y.append(y[0])
    z.append(z[0])
    
    ax.plot3D(x,y,z,c=color)
    #fig.canvas.draw()
    
def draw_axis(axis_x,axis_y,axis_z,ax,fig):
    ax.set_xlim(-axis_x,axis_x)
    ax.set_ylim(-axis_y,axis_y)
    ax.set_zlim(0,axis_z)

    x = [-axis_x,0]
    y = [0,0]
    z = [0,0]
    ax.plot3D(x,y,z,'--r')
    #fig.canvas.draw()
    x = [0,axis_x]
    y = [0,0]
    z = [0,0]
    ax.plot3D(x,y,z,'r')
    #fig.canvas.draw()
    x = [0,0]
    y = [-axis_y,0]
    z = [0,0]
    ax.plot3D(x,y,z,'--b')
    #fig.canvas.draw()
    x = [0,0]
    y = [0,axis_y]
    z = [0,0]
    ax.plot3D(x,y,z,'b')
    #fig.canvas.draw()
    x = [0,0]
    y = [0,0]
    z = [0,axis_z]
    ax.plot3D(x,y,z,'g')
    #fig.canvas.draw()

def draw_servo(base_points,plate_points,servos_length,angles,ax,fig):
    servo_points=[]
    rot_angle = [0,120,240]
    
    point = 0
    
    for side_angle in rot_angle:
        end_servo = []
        #print("Point {}".format(point))
        rotated_point = position_rotate(base_points[point],[side_angle,0,0]).tolist()[0] 
        #print("Grado 1 = {}\nGrado 2 = {}".format(angles[point][0],angles[point][1]))
        #La solucion es con theta1[1]
        end_servo.append([rotated_point[0]+servos_length*math.cos(math.radians(angles[point][0])),rotated_point[1],rotated_point[2]+servos_length*math.sin(math.radians(angles[point][0]))])
        end_servo.append([rotated_point[0]+servos_length*math.cos(math.radians(angles[point][1])),rotated_point[1],rotated_point[2]+servos_length*math.sin(math.radians(angles[point][1]))])
        end_servo[0] = position_rotate(end_servo[0],[-side_angle,0,0,]).tolist()[0]
        end_servo[1] = position_rotate(end_servo[1],[-side_angle,0,0,]).tolist()[0]
        servo_points.append(end_servo)
        #print("The length 1 is {}".format(two_points_length(servo_points[point][0],base_points[point])))
        #print("The length 2 is {}".format(two_points_length(servo_points[point][1],base_points[point])))
        
        point+=1
        end_servo = []
        #print("Point {}".format(point))
        rotated_point = position_rotate(base_points[point],[side_angle,0,0]).tolist()[0] 
        #print("Grado 1 = {}\nGrado 2 = {}".format(angles[point][0],angles[point][1]))
        ###La solucion es con theta1[0] (Se invierte la posision)
        end_servo.append([rotated_point[0]+servos_length*math.cos(math.radians(angles[point][0])),rotated_point[1],rotated_point[2]+servos_length*math.sin(math.radians(angles[point][0]))])
        end_servo.append([rotated_point[0]+servos_length*math.cos(math.radians(angles[point][1])),rotated_point[1],rotated_point[2]+servos_length*math.sin(math.radians(angles[point][1]))])
        end_servo[0] = position_rotate(end_servo[0],[-side_angle,0,0,]).tolist()[0]
        end_servo[1] = position_rotate(end_servo[1],[-side_angle,0,0,]).tolist()[0]
        servo_points.append(end_servo)
        #print("The length 1 is {}".format(two_points_length(servo_points[point][0],base_points[point])))
        #print("The length 2 is {}".format(two_points_length(servo_points[point][1],base_points[point])))
        point+=1
    

    for i in range(6):
        ax.plot3D([base_points[i][0],servo_points[i][0][0]],[base_points[i][1],servo_points[i][0][1]],[base_points[i][2],servo_points[i][0][2]],'k')
        ax.plot3D([plate_points[i][0],servo_points[i][0][0]],[plate_points[i][1],servo_points[i][0][1]],[plate_points[i][2],servo_points[i][0][2]],'k')
        #fig.canvas.draw()
        ax.plot3D([base_points[i][0],servo_points[i][1][0]],[base_points[i][1],servo_points[i][1][1]],[base_points[i][2],servo_points[i][1][2]],':k')
        ax.plot3D([plate_points[i][0],servo_points[i][1][0]],[plate_points[i][1],servo_points[i][1][1]],[plate_points[i][2],servo_points[i][1][2]],':k')
        #fig.canvas.draw()
    
def two_points_length(pointa,pointb):
    dis = math.sqrt(math.pow(pointb[0]-pointa[0],2)+math.pow(pointb[1]-pointa[1],2)+math.pow(pointb[2]-pointa[2],2))
    return dis

def map_value(x,in_min,in_max,out_min,out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def set_servo_values(servos_value,min_val,max_val,lim_min,lim_max,mode = "offline",servos = []):
    maped_servos = []
    min_p = [90,0,90,0,90,0]
    max_p = [180,90,180,90,180,90]
    
    end_correctly= True
    for i in range(6):
        maped_servos.append(int(map_value(servos_value[i],min_p[i],max_p[i],min_val[i],max_val[i])))
        
        if  not(is_number_in(maped_servos[i],lim_min[i],lim_max[i])):
            print("It's not posible to set {} position to servo {}".format(maped_servos[i],i))
            end_correctly = False
            break
    if end_correctly:
        if mode == "online":
            #print("Setting servos pos in PCA9685")
            for i in range(6):
                #print("Servo {} in {} degree".format(i,maped_servos[i]))
                servos[i].angle = maped_servos[i]
    return end_correctly
        
def is_number_in(number,min_v,max_v):
    if number in range(min_v,max_v+1):
        return True
    else:
        return False
    
def list_str(lista):
    str_l = ""
    loop = 0
    for i in lista:
        if loop != 2:
            str_l+=str(i).rjust(3,' ')+","
        else:
            str_l+=str(i).rjust(3,' ')
        loop+=1
    return str_l

def print_records(angles_input,translation_input):
    for i in range(len(angles_input)):       
        angles_input[i]= list(map(int,angles_input[i]))
        translation_input[i]= list(map(int,translation_input[i]))
    
    print("{}The rerun memory values are{}".format("-"*4,"-"*4))
    print("|record|   angles    | translation |")
    
    for i in range(len(angles_input)):
        print("|    {}| {} | {} |".format(str(i+1).rjust(2,' '),list_str(angles_input[i]),list_str(translation_input[i])))

def save_records(angles_input,translation_input,file_name):
    file = open(file_name+".txt","w")
    for i in range(len(angles_input)):
        if i == (len(angles_input)-1):
            file.write(list_str(angles_input[i])+"#"+list_str(translation_input[i]))
        else:
            file.write(list_str(angles_input[i])+"#"+list_str(translation_input[i])+"\n")
    file.close()

def read_records(file_name):
    try:
        file = open(file_name+".txt","r")
        file = file.read()
        file = file.split("\n")
        angles = []
        translation = []
        loop=1
        for current_record in file:
            current_record = current_record.split("#")
            angles.append(list(map(int,current_record[0].split(","))))
            translation.append(list(map(int,current_record[1].split(","))))
        return angles,translation


    except:
        print("\n\x1b[1;31m",end="")
        print("Error: The file {} wasn't foound\n".format(file_name))
        print("\x1b[0;37m",end="")