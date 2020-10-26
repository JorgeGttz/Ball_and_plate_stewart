#Simulacion de ciclo switch case

def switch_demo(argument):
    switcher  = {
        1: print("Hola"),
        2: print("Adios"),
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10:"October",
        11:"November",
        12:"December"
    }

    switcher.get(argument,"Invalid month")

switch_demo(2)
