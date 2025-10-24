import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import math

ARCHIVO_NUMEROS = "numeros.txt"
ARCHIVO_ELIMINADOS = "eliminados.txt"

# ---- Funciones auxiliares ----
def leer_numeros():
    if not os.path.exists(ARCHIVO_NUMEROS):
        return []
    with open(ARCHIVO_NUMEROS, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def guardar_numero(numero):
    numeros = leer_numeros()
    if numero in numeros:
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


# Centrar cualquier ventana tkinter en pantalla sin cambiar su tamaño.
def center_window(win):
    """Centra la ventana `win` en la pantalla.
    - Usa el tamaño ya establecido por `win.geometry()` si está disponible.
    - Llama a update_idletasks() para obtener dimensiones reales antes de posicionar.
    """
    try:
        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()

        # Si las dimensiones aún no están disponibles, intentar parsear geometry()
        if w <= 1 or h <= 1:
            try:
                geom = win.geometry()  # formato: WxH+X+Y
                size = geom.split('+')[0]
                w, h = map(int, size.split('x'))
            except Exception:
                w = max(200, win.winfo_reqwidth())
                h = max(100, win.winfo_reqheight())

        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")
    except Exception:
        # No interrumpir la ejecución si algo falla; centrado es un añadido no crítico.
        pass

# ---- Mostrar número asignado ----
def mostrar_numero_asignado(numero):
    temp = tk.Toplevel()
    temp.title("Número asignado")
    temp.geometry("500x300")
    temp.resizable(False, False)
    center_window(temp)

    label = tk.Label(temp, text=f"Tu número asignado es:", font=("Comic Sans MS", 26, "bold"))
    label.pack(pady=40)

    label_num = tk.Label(temp, text=str(numero), font=("Comic Sans MS", 60, "bold"), fg="green")
    label_num.pack(pady=10)

    boton_aceptar = tk.Button(temp, text="Aceptar", font=("Comic Sans MS", 20, "bold"),
                              bg="black", fg="white", relief="flat",
                              command=temp.destroy)
    boton_aceptar.pack(pady=30)

    temp.mainloop()

# ---- Ventana para ingresar ----
def ventana_ingresar(menu):
    menu.destroy()
    ventana = tk.Tk()
    ventana.title("Registro")
    ventana.geometry("1280x720")
    ventana.resizable(False, False)
    center_window(ventana)
    try:
        ventana.iconbitmap("assets/DharmaIcon.ico")
    except:
        pass

    try:
        fondo_img = Image.open("assets/fondo4.png")
        fondo_photo = ImageTk.PhotoImage(fondo_img)
        fondo_label = tk.Label(ventana, image=fondo_photo)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        ventana.fondo_ref = fondo_photo
    except:
        pass

    # Botón volver
    boton_volver = tk.Button(
        ventana, text="⬅ Volver",
        command=lambda: volver_menu(ventana, iniciar_programa),
        bg="red", fg="white", font=("Comic Sans MS", 16, "bold"),
        relief="flat", bd=0, highlightthickness=0
    )
    boton_volver.place(x=1170, y=10, width=90, height=40)

    # --- Nuevo registro automático ---
    def registrar_aleatorio():
        numeros_existentes = leer_numeros()
        todos = set(map(str, range(1, 201)))
        disponibles = list(todos - set(numeros_existentes))

        if not disponibles:
            messagebox.showwarning("Sin números disponibles", "Ya se asignaron todos los números del 1 al 200.")
            return

        numero_asignado = random.choice(disponibles)
        if guardar_numero(numero_asignado):
            mostrar_numero_asignado(numero_asignado)

    boton_registrar = tk.Button(
        ventana, text="Registrar participante", command=registrar_aleatorio,
        bg="green", fg="white", font=("Comic Sans MS", 24, "bold"),
        relief="flat", bd=0, highlightthickness=0
    )
    boton_registrar.place(relx=0.5, rely=0.5, anchor="center", width=400, height=100)

    ventana.mainloop()

# ---- Ventana mostrar eliminados ----
# ---- Ventana mostrar eliminados ----
def ventana_mostrar_eliminados(eliminados, callback_refrescar):
    temp = tk.Toplevel()
    temp.title("Jugadores Eliminados...")
    temp.geometry("800x600")
    temp.resizable(False, False)
    center_window(temp)

    titulo = tk.Label(temp, text="Números eliminados", font=("Comic Sans MS", 28, "bold"),
                      bg="black", fg="white", relief="flat")
    titulo.place(relx=0.5, rely=0.1, anchor="center")

    label_num = tk.Label(temp, text="", font=("Comic Sans MS", 60, "bold"),
                         relief="flat")
    label_num.place(relx=0.5, rely=0.5, anchor="center")

    # --- Nuevo cálculo dinámico del tiempo ---
    vivos_restantes = len(leer_numeros())

    def calcular_tiempo(vivos):
        """Ajusta la velocidad según cuántos jugadores quedan vivos."""
        if vivos > 100:
            return 150      # Muchos vivos → rápido
        elif vivos > 50 and vivos <= 100:
            return 600      # Intermedio → velocidad media
        elif vivos > 25 and vivos <= 50:
            return 1000     # Menos → un poco más lento
        else:
            return 2000     # Muy pocos vivos → lento, emocionante

    tiempo_actual = calcular_tiempo(vivos_restantes)

    def mostrar(i=0):
        if i < len(eliminados):
            label_num.config(text=eliminados[i])
            temp.after(tiempo_actual, lambda: mostrar(i + 1))
        else:
            temp.destroy()
            callback_refrescar()

    mostrar()
    temp.mainloop()


# ---- Animación de sorteo sorpresa ----
def ventana_sorteo_rapido(todos):
    temp = tk.Toplevel()
    temp.title("🎁 Sorteo Sorpresa 🎁")
    temp.geometry("800x600")
    temp.resizable(False, False)
    center_window(temp)
    
    label_titulo = tk.Label(temp, text="Sorteo Sorpresa", font=("Comic Sans MS", 32, "bold"), fg="black")
    label_titulo.pack(pady=40)

    label_num = tk.Label(temp, text="", font=("Comic Sans MS", 80, "bold"), fg="red")
    label_num.pack(pady=80)

    label_final = tk.Label(temp, text="", font=("Comic Sans MS", 28, "bold"), fg="black")
    label_final.pack(pady=40)

    lista = todos[:]
    random.shuffle(lista)

    def mostrar(i=0):
        if i < len(lista):
            label_num.config(text=lista[i])
            temp.after(100, lambda: mostrar(i + 1))
        else:
            ganador = random.choice(lista)
            label_num.config(text=str(ganador), fg="red")
            label_final.config(text="🎉 ¡Has Ganado el Sorteo! 🎉")

    mostrar()
    temp.mainloop()

# ---- Mostrar fichas ----
def mostrar_fichas(frame, numeros, color):
    # Guardar datos en el frame para poder re-renderizar al cambiar tamaño.
    frame._dharma_nums = list(numeros)
    frame._dharma_color = color

    def render(event=None):
        # Redibuja todas las fichas según el tamaño actual del frame.
        for widget in frame.winfo_children():
            widget.destroy()

        cantidad = len(getattr(frame, '_dharma_nums', []))
        if cantidad == 0:
            return

        columnas = math.ceil(math.sqrt(cantidad))
        filas = math.ceil(cantidad / columnas)

        frame.update_idletasks()
        w = frame.winfo_width() or frame.winfo_reqwidth()
        h = frame.winfo_height() or frame.winfo_reqheight()
        cell_w = max(1, w // columnas)
        cell_h = max(1, h // filas)
        size = min(cell_w, cell_h)
        font_size = max(6, size // 3)

        for i, num in enumerate(frame._dharma_nums):
            fila = i // columnas
            col = i % columnas
            lbl = tk.Label(frame, text=num, font=("Comic Sans MS", font_size, "bold"),
                           width=1, height=1, relief="solid", bd=2, highlightthickness=0,
                           bg=frame._dharma_color, fg="white")
            lbl.place(x=col * cell_w, y=fila * cell_h, width=cell_w, height=cell_h)

    # Render inicial
    render()

    # Vincular re-renderizado cuando el frame cambia de tamaño (solo una vez)
    if not getattr(frame, '_dharma_bound', False):
        frame.bind('<Configure>', render)
        frame._dharma_bound = True

# ---- Ventana consultar ----
def ventana_consultar(menu):
    if menu is not None:
        try: menu.destroy()
        except: pass

    ventanacon = tk.Tk()
    ventanacon.title("👻 Consultar")
    ventanacon.geometry("1920x1080")
    ventanacon.resizable(True, True)
    center_window(ventanacon)
    try:
        ventanacon.iconbitmap("assets/DharmaIcon.ico")
    except: pass

    try:
        fondo_img = Image.open("assets/fondo5.png")
        fondo_photo = ImageTk.PhotoImage(fondo_img)
        fondo_label = tk.Label(ventanacon, image=fondo_photo)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        ventanacon.fondo_ref = fondo_photo
    except: pass

    boton_volver = tk.Button(
        ventanacon, text="⬅",
        command=lambda: volver_menu(ventanacon, iniciar_programa),
        bg="#f5abcb", fg="white", font=("Comic Sans MS", 16, "bold"),
        relief="flat", bd=0, highlightthickness=0
    )
    boton_volver.place(x=1170, y=10, width=90, height=40)

    # --- INICIO DE MODIFICACIÓN: Reemplazo del Label 'Jugadores Vivos' por la imagen "JugadoresV.png" ---
    try:
        # Cargar y redimensionar la imagen para que encaje con el Label de título (400x80 píxeles)
        img_vivos = Image.open("assets/JugadoresV.png")
        img_vivos_resized = img_vivos.resize((400, 90))
        img_vivos_tk = ImageTk.PhotoImage(img_vivos_resized)

        # Crear un Label para la imagen y colocarlo en la posición original
        label_vivos = tk.Label(ventanacon, image=img_vivos_tk, bd=0, background= "#f5abcb")
        label_vivos.image = img_vivos_tk # Mantener referencia
        label_vivos.place(relx=0.25, rely=0.075, anchor="center") # Ajustado a 0.075 para mejor centrado vertical

    except Exception as e:
        # Fallback si la imagen no se carga (mantener el Label original)
        label_vivos = tk.Label(ventanacon, text="Jugadores vivos", font=("Roboto", 26, "bold"), fg="#2ecc71")
        label_vivos.place(relx=0.25, rely=0.05, anchor="center")
        print(f"Error al cargar la imagen 'JuagadoresV.png': {e}")
    # --- FIN DE MODIFICACIÓN ---

    frame_vivos = tk.Frame(ventanacon, bg="white", relief="flat", bd=0, highlightthickness=0)
    frame_vivos.place(relx=0.25, rely=0.5, anchor="center", relwidth=0.4, relheight=0.7)
    ventanacon.update_idletasks()
    mostrar_fichas(frame_vivos, sorted(leer_numeros(), key=lambda x: int(x)), "#09C272")

    eliminados = []
    if os.path.exists(ARCHIVO_ELIMINADOS):
        with open(ARCHIVO_ELIMINADOS, "r", encoding="utf-8") as f:
            eliminados = [line.strip() for line in f if line.strip()]

    # ---- MODIFICACIÓN: Imagen + Premio oculto ----
    premio = len(eliminados) * 1000
    premio_str = str(premio)
    if len(leer_numeros()):
        premio_oculto = premio_str

    try:
        img_premio = Image.open("assets/HuchaRX.png").resize((80, 80))
        img_premio_tk = ImageTk.PhotoImage(img_premio)
        label_img = tk.Label(ventanacon, image=img_premio_tk, bg="#f5abcb")
        label_img.image = img_premio_tk
        label_img.place(relx=0.08, rely=0.92, anchor="center")

        label_premio_texto = tk.Label(
            ventanacon, text=f"${premio_oculto}",
            font=("Comic Sans MS", 22, "bold"), fg="black", bg="#f5abcb", relief="flat"
        )
        label_premio_texto.place(relx=0.17, rely=0.92, anchor="center")

    except Exception as e:
        label_premio_texto = tk.Label(
            ventanacon, text=f"Premio actual: ${premio_oculto}",
            font=("Comic Sans MS", 22, "bold"), bg="yellow", fg="black", relief="flat"
        )
        label_premio_texto.place(relx=0.17, rely=0.90, anchor="center")

    # ------------------------------------------

    # --- Reemplazo del Label por la imagen "JuagadoresE.png" (Previa modificación) ---
    try:
        # Cargar y redimensionar la imagen para que encaje con el espacio del Label (aprox. 400x80 píxeles)
        img_eliminados = Image.open("assets/JuagadoresE.png")
        img_eliminados_resized = img_eliminados.resize((400, 90))
        img_eliminados_tk = ImageTk.PhotoImage(img_eliminados_resized)

        # Crear un Label para la imagen y colocarlo en la posición original (relx=0.75, rely=0.075)
        label_eliminados = tk.Label(ventanacon, image=img_eliminados_tk, bd=0, bg="#f5abcb")
        label_eliminados.image = img_eliminados_tk # Mantener referencia
        label_eliminados.place(relx=0.75, rely=0.075, anchor="center")

    except Exception as e:
        # Fallback si la imagen no se carga (mantener el Label original)
        label_eliminados = tk.Label(ventanacon, text="Jugadores eliminados", font=("Comic Sans MS", 26, "bold"), fg="#e74c3c")
        label_eliminados.place(relx=0.75, rely=0.05, anchor="center")
        print(f"Error al cargar la imagen 'JuagadoresE.png': {e}")
    # ------------------------------------------

    frame_eliminados = tk.Frame(ventanacon, bg="white", relief="flat", bd=0, highlightthickness=0)
    frame_eliminados.place(relx=0.75, rely=0.5, anchor="center", relwidth=0.4, relheight=0.7)
    mostrar_fichas(frame_eliminados, sorted(eliminados, key=lambda x: int(x)), "#c63637")


    def eliminar_mitad():
        numeros = leer_numeros()
        if not numeros:
            messagebox.showwarning("Advertencia", "No hay números para eliminar")
            return
        if len(numeros) != 3:
            cantidad = math.floor(len(numeros) / 2)
        elif len(numeros) == 3:
            cantidad = math.ceil(len(numeros) / 2)
        eliminados_sel = random.sample(numeros, cantidad)
        mover_a_eliminados(eliminados_sel)

        def refrescar_consulta():
            try: ventanacon.destroy()
            except: pass
            ventana_consultar(None)

        ventana_mostrar_eliminados(eliminados_sel, refrescar_consulta)

    # --- Botón Eliminar (REEMPLAZADO POR IMAGEN) ---
    try:
    # Cargar la imagen del botón eliminar
        img_eliminar = Image.open("assets/eliminarjugadores.png")
        img_eliminar_resized = img_eliminar.resize((170, 60))  # Mismo tamaño que el botón original
        img_eliminar_tk = ImageTk.PhotoImage(img_eliminar_resized)
    
        boton_eliminar = tk.Button(
            ventanacon, image=img_eliminar_tk, command=eliminar_mitad,
            relief="flat", bd=0, highlightthickness=0, bg="#f5abcb"
        )
        boton_eliminar.image = img_eliminar_tk  # Mantener referencia
        boton_eliminar.place(relx=0.61, rely=0.9, anchor="center", width=150, height=40)
    
    except Exception as e:
        # Fallback en caso de error al cargar la imagen
        boton_eliminar = tk.Button(
            ventanacon, text="Eliminar", command=eliminar_mitad,
            bg="black", fg="white", font=("Comic Sans MS", 14, "bold"),
            relief="flat", bd=0, highlightthickness=0
        )
        boton_eliminar.place(relx=0.61, rely=0.9, anchor="center", width=150, height=40)
        print(f"Error al cargar la imagen 'eliminarjugadores.png': {e}")

    # --- Botón de sorteo sorpresa ---
    def sorteo_sorpresa():
        vivos = leer_numeros()
        eliminados_local = []
        if os.path.exists(ARCHIVO_ELIMINADOS):
            with open(ARCHIVO_ELIMINADOS, "r", encoding="utf-8") as f:
                eliminados_local = [line.strip() for line in f if line.strip()]
        todos = list(set(vivos + eliminados_local))
        if not todos:
            messagebox.showwarning("Sorteo", "No hay jugadores registrados para el sorteo.")
            return
        ventana_sorteo_rapido(todos)

    boton_sorteo = tk.Button(
        ventanacon, text="?", command=sorteo_sorpresa,
        bg="black", fg="white", font=("Comic Sans MS", 18, "bold"),
        relief="flat", bd=0, highlightthickness=0
    )
    boton_sorteo.place(relx=0.70, rely=0.9, anchor="center", width=40, height=40)

    ventanacon.mainloop()

# ---- Menú principal ----
def iniciar_programa():
    menu = tk.Tk()
    menu.title("HALLOWOD")
    menu.geometry("900x600")
    menu.resizable(False, False)
    center_window(menu)
    try: menu.iconbitmap("assets/DharmaIcon.ico")
    except: pass

    try:
        fondo_img = Image.open("assets/fondo4.png")
        fondo_photo = ImageTk.PhotoImage(fondo_img)
        fondo_label = tk.Label(menu, image=fondo_photo)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        menu.fondo_ref = fondo_photo
    except: pass

    boton_ingresar = tk.Button(
        menu, text="Registrar participante", command=lambda: ventana_ingresar(menu),
        bg="#d94667", fg="black", font=("Comic Sans MS", 24, "bold"),
        relief="flat", bd=0, highlightthickness=0
    )
    boton_ingresar.place(relx=0.5, rely=0.45, anchor="center", width=450, height=100)

    boton_consultar = tk.Button(
        menu, text="Consultar", command=lambda: ventana_consultar(menu),
        bg="#d94667", fg="black", font=("Comic Sans MS", 24, "bold"),
        relief="flat", bd=0, highlightthickness=0
    )
    boton_consultar.place(relx=0.5, rely=0.65, anchor="center", width=400, height=100)

    menu.mainloop()

# ---- Ventana inicial ----
ventana = tk.Tk()
ventana.title("HALLOWOD")
ventana.geometry("500x600")
ventana.resizable(False, False)
center_window(ventana)
try: ventana.iconbitmap("assets/DharmaIcon.ico")
except: pass

try:
    fondo_imagen = Image.open("assets/fondoRX.png")
    fondo_foto = ImageTk.PhotoImage(fondo_imagen)
    fondo_label = tk.Label(ventana, image=fondo_foto)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    ventana.fondo_ref = fondo_foto
except: pass
    
try:
    boton_inicio_imagen = Image.open("assets/boton_iniciarRX.png")
    boton_inicio_foto = ImageTk.PhotoImage(boton_inicio_imagen)
    boton_inicio = tk.Button(ventana, image=boton_inicio_foto,
                             command=lambda: volver_menu(ventana, iniciar_programa),
                             bd=0, highlightthickness=0, relief="flat")
    boton_inicio.place(relx=0.5, rely=0.7, anchor=tk.CENTER, width=300, height=100)
    ventana.boton_ref = boton_inicio_foto
except:
    boton_inicio = tk.Button(ventana, text="Iniciar",
                             command=lambda: volver_menu(ventana, iniciar_programa),
                             font=("Comic Sans MS", 24, "bold"),
                             relief="flat", bd=0, highlightthickness=0)
    boton_inicio.place(relx=0.5, rely=0.7, anchor=tk.CENTER, width=300, height=100)

ventana.mainloop()