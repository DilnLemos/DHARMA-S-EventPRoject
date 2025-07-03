import tkinter as tk
from PIL import Image, ImageTk

def iniciar_programa():
    # Cerrar la ventana de inicio
    ventana.destroy()

    # Crear nueva ventana del menú
    menu = tk.Tk()
    menu.title("👻 HALLOWOD MENÚ 👻")
    menu.geometry("600x700")
    menu.resizable(False, False)
    menu.iconbitmap("assets/icono.ico")

    # Fondo del menú
    fondo_menu_img = Image.open("assets/fondo.png")
    fondo_menu_photo = ImageTk.PhotoImage(fondo_menu_img)

    fondo_label_menu = tk.Label(menu, image=fondo_menu_photo)
    fondo_label_menu.place(x=0, y=0, relwidth=1, relheight=1)

    # Mantener referencia de la imagen para evitar que se elimine de memoria
    menu.fondo_ref = fondo_menu_photo

    menu.mainloop()


#ventana Principal
ventana = tk.Tk()
ventana.title("👻 HALLOWOD 👻")
ventana.geometry("500x600")
ventana.resizable(False, False)
ventana.iconbitmap("assets/icono.ico")

#fondo
fondo_imagen = Image.open("assets/fondoRX.png")
fondo_foto = ImageTk.PhotoImage(fondo_imagen)

fondo_label = tk.Label(ventana, image=fondo_foto)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

# Botón
boton_inicio_imagen = Image.open("assets/boton_iniciarRX.png")
boton_inicio_foto = ImageTk.PhotoImage(boton_inicio_imagen)

boton_inicio = tk.Button(ventana, image=boton_inicio_foto, command=iniciar_programa, bd=0, highlightthickness=0)
boton_inicio.place(relx=0.5, rely=0.7, anchor=tk.CENTER, width=300, height=100)

# Referencias para evitar que las imágenes se borren de memoria
ventana.fondo_ref = fondo_foto
ventana.boton_ref = boton_inicio_foto

ventana.mainloop()
