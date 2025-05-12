import random
# Variables Globales
participantes = {1: 'Dilan', 2: 'Sofia'}
participantes_activos = participantes
participantes_eliminados = {}

def main():
    while True:
        print("""\nBienvenido al Concurso de Dharma
        Ingrese una opción:
        1. Registrar Jugador
        2. Mostrar Participantes Activos
        3. Mostrar Participantes Eliminados
        4. Eliminar Jugador
        0. Salir""")
        try:
            opc = int(input("Ingrese una opción: "))
            if opc == 1:
                registro_participantes()
            elif opc == 2:
                mostrar_jugadores(participantes)
            elif opc == 3:
                mostrar_participantes_eliminadoss(participantes_eliminados)
            elif opc == 4:
                eliminar_jugadores(participantes_activos)
            elif opc == 0:
                print("Chaito Haider jajaj.")
                break
            else:
                print("Opción inválida.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

def registro_participantes():
    while True:
        numero = input("Ingrese el número del participante: ")
        if numero.isdigit():
            nombre = input(f"Ingrese el nombre del jugador {numero}: ")
            participantes[int(numero)] = nombre
            print("Participante registrado:", participantes)
            break
        else:
            print("Se ha ingresado un valor no numérico.")

def mostrar_jugadores(participantes):
    print(participantes)

def mostrar_participantes_eliminadoss(participantes_eliminados):
    print(participantes_eliminados)

def eliminar_jugadores(participantes_activos):

    cantidad_eliminados = int(input("Ingrese la cantidad de jugadores a eliminar: "))
    total_jugadores = len(participantes_activos)
    for i in range(cantidad_eliminados):
        participante_eliminado = random.randint(1, total_jugadores)
        if participante_eliminado in participantes_activos:
            participantes_eliminados[participante_eliminado] = participantes_activos.get(participante_eliminado)
            participantes_activos.pop(participante_eliminado)
            print("activos", participantes_activos)
            print("eliminados", participantes_eliminados)

if __name__ == '__main__':
    main()
