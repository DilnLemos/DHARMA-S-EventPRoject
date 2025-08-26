import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import math

ARCHIVO_NUMEROS = "numeros.txt"
ARCHIVO_ELIMINADOS = "eliminados.txt"


def leer_numeros():
    if not os.path.exists(ARCHIVO_NUMEROS):
        return []
    with open(ARCHIVO_NUMEROS, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def guardar_numero(numero):
    numeros = leer_numeros()
    if numero in numeros:
        messagebox.showwarning("Advertencia", f"El número {numero} ya está registrado")
        return False
    elif not numero.isdigit():
        messagebox.showwarning("Advertencia", "Solo se permiten dígitos")
        return False
    with open(ARCHIVO_NUMEROS, "a", encoding="utf-8") as f:
        f.write(str(numero) + "\n")
    return True


def mover_a_eliminados(numeros):
    with open(ARCHIVO_ELIMINADOS, "a", encoding="utf-8") as f:
        for n in numeros:
            f.write(str(n) + "\n")

    vivos = leer_numeros()
    restantes = vivos[:]
    for n in numeros:
        if n in restantes:
            restantes.remove(n)

    with open(ARCHIVO_NUMEROS, "w", encoding="utf-8") as f:
        for n in restantes:
            f.write(str(n) + "\n")


def volver_menu(ventana, callback):
    ventana.destroy()
    callback()


def ventana_ingresar(menu):
    menu.destroy()
    ventana = tk.Tk()
    ventana.title("👻 Ingresar dígitos 👻")
    ventana.geometry("1280x720")
    ventana.resizable(False, False)
    try:
        ventana.iconbitmap("assets/icono.ico")
    except:
        pass

    try:
        fondo_img = Image.open("assets/fondo.png")
        fondo_photo = ImageTk.PhotoImage(fondo_img)
        fondo_label = tk.Label(ventana, image=fondo_photo)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        ventana.fondo_ref = fondo_photo
    except:
        pass

    boton_volver = tk.Button(
        ventana, text="⬅ Volver",
        command=lambda: volver_menu(ventana, iniciar_programa),
        bg="red", fg="white", font=("Arial", 16, "bold")
    )
    boton_volver.place(x=1170, y=10, width=90, height=40)

    entry = tk.Entry(ventana, font=("Arial", 28), justify="center")
    entry.place(relx=0.5, rely=0.4, anchor="center", width=400, height=60)

    def registrar():
        valor = entry.get().strip()
        if valor:
            if guardar_numero(valor):
                entry.delete(0, tk.END)
                messagebox.showinfo("Éxito", f"Se registró el número: {valor}")

    boton_registrar = tk.Button(
        ventana, text="Registrar",
        command=registrar,
        bg="green", fg="white", font=("Arial", 24, "bold")
    )
    boton_registrar.place(relx=0.5, rely=0.55, anchor="center", width=300, height=80)

    ventana.mainloop()


def ventana_mostrar_eliminados(eliminados, callback_refrescar):
    temp = tk.Toplevel()
    temp.title("👻 Eliminando... 👻")
    temp.geometry("800x600")
    temp.resizable(False, False)

    titulo = tk.Label(temp, text="Números eliminados", font=("Arial", 28, "bold"), bg="black", fg="white")
    titulo.place(relx=0.5, rely=0.1, anchor="center")

    label_num = tk.Label(temp, text="", font=("Arial", 60, "bold"))
    label_num.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar(i=0):
        if i < len(eliminados):
            label_num.config(text=eliminados[i])
            temp.after(2000, lambda: mostrar(i + 1))
        else:
            temp.destroy()
            callback_refrescar()

    mostrar()
    temp.mainloop()


# ---- Mostrar fichas sin scrollbar, ajustando tamaño dinámicamente ----
def mostrar_fichas(frame, numeros, color):
    for widget in frame.winfo_children():
        widget.destroy()

    cantidad = len(numeros)
    if cantidad == 0:
        return

    # Calcular cantidad de filas/columnas cuadradas
    columnas = math.ceil(math.sqrt(cantidad))
    filas = math.ceil(cantidad / columnas)

    # Dimensiones del frame
    frame.update_idletasks()
    w = frame.winfo_width()
    h = frame.winfo_height()

    # Tamaño de cada celda
    cell_w = max(1, w // columnas)
    cell_h = max(1, h // filas)
    size = min(cell_w, cell_h)

    font_size = max(6, size // 3)

    for i, num in enumerate(numeros):
        fila = i // columnas
        col = i % columnas
        lbl = tk.Label(
            frame,
            text=num,
            font=("Arial", font_size, "bold"),
            width=1, height=1,
            relief="solid",
            bg=color,
            fg="white"
        )
        lbl.place(x=col * cell_w, y=fila * cell_h, width=cell_w, height=cell_h)


def ventana_consultar(menu):
    if menu is not None:
        try:
            menu.destroy()
        except:
            pass

    ventanacon = tk.Tk()
    ventanacon.title("👻 Consultar")
    ventanacon.geometry("1280x720")
    ventanacon.resizable(False, False)
    try:
        ventanacon.iconbitmap("assets/icono.ico")
    except:
        pass

    try:
        fondo_img = Image.open("assets/fondo.png")
        fondo_photo = ImageTk.PhotoImage(fondo_img)
        fondo_label = tk.Label(ventanacon, image=fondo_photo)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        ventanacon.fondo_ref = fondo_photo
    except:
        pass

    boton_volver = tk.Button(
        ventanacon, text="⬅ Volver",
        command=lambda: volver_menu(ventanacon, iniciar_programa),
        bg="red", fg="white", font=("Arial", 16, "bold")
    )
    boton_volver.place(x=1170, y=10, width=90, height=40)

    # --- Jugadores vivos ---
    label_vivos = tk.Label(ventanacon, text="Jugadores vivos", font=("Arial", 26, "bold"), fg="#2ecc71")
    label_vivos.place(relx=0.25, rely=0.05, anchor="center")

    frame_vivos = tk.Frame(ventanacon, bg="white")
    frame_vivos.place(relx=0.25, rely=0.5, anchor="center", relwidth=0.4, relheight=0.7)

    ventanacon.update_idletasks()
    mostrar_fichas(frame_vivos, leer_numeros(), "#27ae60")

    # --- Premio actual ---
    eliminados = []
    if os.path.exists(ARCHIVO_ELIMINADOS):
        with open(ARCHIVO_ELIMINADOS, "r", encoding="utf-8") as f:
            eliminados = [line.strip() for line in f if line.strip()]

    premio = len(eliminados) * 1500
    label_premio = tk.Label(
        ventanacon,
        text=f"Premio actual: ${premio}",
        font=("Arial", 22, "bold"),
        bg="yellow", fg="black"
    )
    label_premio.place(relx=0.17, rely=0.90, anchor="center")

    # --- Jugadores eliminados ---
    label_eliminados = tk.Label(ventanacon, text="Jugadores eliminados", font=("Arial", 26, "bold"), fg="#e74c3c")
    label_eliminados.place(relx=0.75, rely=0.05, anchor="center")

    frame_eliminados = tk.Frame(ventanacon, bg="white")
    frame_eliminados.place(relx=0.75, rely=0.5, anchor="center", relwidth=0.4, relheight=0.7)

    mostrar_fichas(frame_eliminados, eliminados, "#c0392b")

    def eliminar_mitad():
        numeros = leer_numeros()
        if not numeros:
            messagebox.showwarning("Advertencia", "No hay números para eliminar")
            return

        cantidad = math.ceil(len(numeros) / 2)
        eliminados_sel = random.sample(numeros, cantidad)
        mover_a_eliminados(eliminados_sel)

        def refrescar_consulta():
            try:
                ventanacon.destroy()
            except:
                pass
            ventana_consultar(None)

        ventana_mostrar_eliminados(eliminados_sel, refrescar_consulta)

    boton_eliminar = tk.Button(
        ventanacon, text="Eliminar mitad",
        command=eliminar_mitad,
        bg="black", fg="white", font=("Arial", 14, "bold")
    )
    boton_eliminar.place(relx=0.89, rely=0.9, anchor="center", width=150, height=40)

    ventanacon.mainloop()


def iniciar_programa():
    menu = tk.Tk()
    menu.title("👻 HALLOWOD MENÚ 👻")
    menu.geometry("900x600")
    menu.resizable(False, False)
    try:
        menu.iconbitmap("assets/icono.ico")
    except:
        pass

    try:
        fondo_img = Image.open("assets/fondo.png")
        fondo_photo = ImageTk.PhotoImage(fondo_img)
        fondo_label = tk.Label(menu, image=fondo_photo)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        menu.fondo_ref = fondo_photo
    except:
        pass

    boton_ingresar = tk.Button(
        menu, text="Ingresar",
        command=lambda: ventana_ingresar(menu),
        bg="#d94667", fg="black", font=("Arial", 24, "bold")
    )
    boton_ingresar.place(relx=0.5, rely=0.45, anchor="center", width=400, height=100)

    boton_consultar = tk.Button(
        menu, text="Consultar",
        command=lambda: ventana_consultar(menu),
        bg="#d94667", fg="black", font=("Arial", 24, "bold")
    )
    boton_consultar.place(relx=0.5, rely=0.65, anchor="center", width=400, height=100)

    menu.mainloop()


# ---- Ventana inicial ----
ventana = tk.Tk()
ventana.title("👻 HALLOWOD 👻")
ventana.geometry("500x600")
ventana.resizable(False, False)
try:
    ventana.iconbitmap("assets/icono.ico")
except:
    pass

try:
    fondo_imagen = Image.open("assets/fondoRX.png")
    fondo_foto = ImageTk.PhotoImage(fondo_imagen)
    fondo_label = tk.Label(ventana, image=fondo_foto)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    ventana.fondo_ref = fondo_foto
except:
    pass

try:
    boton_inicio_imagen = Image.open("assets/boton_iniciarRX.png")
    boton_inicio_foto = ImageTk.PhotoImage(boton_inicio_imagen)
    boton_inicio = tk.Button(ventana, image=boton_inicio_foto,
                             command=lambda: volver_menu(ventana, iniciar_programa),
                             bd=0, highlightthickness=0)
    boton_inicio.place(relx=0.5, rely=0.7, anchor=tk.CENTER, width=300, height=100)
    ventana.boton_ref = boton_inicio_foto
except:
    boton_inicio = tk.Button(ventana, text="Iniciar",
                             command=lambda: volver_menu(ventana, iniciar_programa),
                             font=("Arial", 24, "bold"))
    boton_inicio.place(relx=0.5, rely=0.7, anchor=tk.CENTER, width=300, height=100)

ventana.mainloop()
