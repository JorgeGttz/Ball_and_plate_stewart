i=10
angles_rerun =  [[1,2,3],[10,20,30],[100,2,30]]
translation_rerun = [[6,7,8],[700,345,567],[10,100,2]]

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
    print("{}The rerun memory values are{}".format("-"*4,"-"*4))
    print("|record|   angles    | translation |")
    
    for i in range(len(angles_input)):
        print("|    {}| {} | {} |".format(str(i+1).rjust(2,' '),list_str(angles_input[i]),list_str(translation_input[i])))

print_records(angles_rerun,translation_rerun)