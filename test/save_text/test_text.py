#How to import text files 

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

#angles = [[10,20,30],[11,21,31],[12,22,32]]
#trans = [[40,50,60],[41,51,61],[42,52,62]]
#save_records(angles,trans,"test1")