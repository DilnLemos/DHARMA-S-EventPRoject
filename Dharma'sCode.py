
def main():
    menu()
    pass

def menu():

    print("""Bienvenido al Concurso de Dharma
            Ingrese una opcion:
            1. Registrar Jugador
            0. salir""")
    opc = int(input("Ingrese una opcion: "))
    while opc != 0:
        if opc == 1:
            registro_participantes()
        elif opc == 0:
            break



def registro_participantes():

    participantes = {}
    global numero
    numero = ''
    bool_numero = False
    while bool_numero == False:
        numero = input("Ingrese el número del participante:")
        if not numero.isdigit():
            print("Se ha ingresado un valor no numérico.")
        else:
            nombre = input(f"Ingrese el nombre del jugador {numero}:")
            participantes[int(numero)] = nombre
            print(participantes)
            bool_numero = True






if __name__ == '__main__':
    main()