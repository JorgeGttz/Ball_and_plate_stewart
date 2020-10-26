#function maping

def one():
    global num
    num=10
    return None           
    


def two():
    global num
    num=5
    return None

def three():
    return "three"

def case_funtions(argument):
    switcher = {
        1: one(),
        2: two(),
        3: three()
    }
    func = switcher.get(argument, lambda: "Invalid month")
    #print(func)
    
case_funtions(1)
print(num)

