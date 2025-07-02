import tkinter as tk
from PIL import Image, ImageTk

#ventana Principal
ventana = tk.Tk()
ventana.title("👻 HALLOWOD 👻")
ventana.geometry("500x600")

#fondo
fondo_imagen = Image.open("assets/fondoRX.png")
fondo_foto = ImageTk.PhotoImage(fondo_imagen)

#titulo principal
titulo_imagen = Image.open("assets/tituloRX.png").convert("RGBA")
# Redimensionar la imagen del título
titulo_imagen = titulo_imagen.resize((400, 100))
titulo_foto = ImageTk.PhotoImage(titulo_imagen)

# Etiqueta de fondo
fondo_label = tk.Label(ventana, image = fondo_foto)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)    

# Etiqueta de título
titulo_label = tk.Label(ventana, image=titulo_foto)
titulo_label.pack(pady=20)


# Icono
ventana.iconbitmap("assets/icono.ico")

ventana.resizable(False, False)

ventana.mainloop()  # Solo una vez