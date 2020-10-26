import re

patron = re.compile(r'[A-Za-z][0-9]+([,][0-9]+)*$')

while True:
    input = raw_input("Enter a command or valid expression: ")

    if input == "break":
        break
    else:
        if patron.match(input):
            char = input[0]
            digits = input[1:]

            if digits.find(','):
                digits = digits.split(',')

            print ("Your char was {} and your digits were: ".format(char))
            print (digits)
        else:
            print("Invalid expression or command")
