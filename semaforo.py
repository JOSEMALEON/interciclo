import tkinter as tk
import time
import random
import os

class Semaforo:
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("Reto Semaforo")

        # Centrar ventana
        ancho_ventana = 370
        alto_ventana = 650
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()
        x_pos = (ancho_pantalla - ancho_ventana) // 2
        y_pos = (alto_pantalla - alto_ventana) // 2
        ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

        # Estado de ejecución
        self.ejecutando = False
        
        # Duraciones (fijas) para rojo y amarillo en segundos
        self.tiempo_rojo = 5
        self.tiempo_amarillo = 2

        # Variables de tiempo
        self.inicio_ciclo = None    # Momento en que se presionó "Iniciar"
        self.inicio_verde = None    # Momento en que se encendió la luz verde

        # Crear un lienzo para el semáforo, tamaño intermedio
        self.lienzo = tk.Canvas(ventana, width=150, height=450, bg="black")
        self.lienzo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Círculos para las luces
        self.luz_roja = self.lienzo.create_oval(25, 25, 125, 125, fill="gray")
        self.luz_amarilla = self.lienzo.create_oval(25, 165, 125, 265, fill="gray")
        self.luz_verde = self.lienzo.create_oval(25, 305, 125, 405, fill="gray")

        # Etiquetas para mostrar información
        self.etiqueta_instrucciones = tk.Label(ventana, text="Presiona 'Iniciar' para comenzar.\nCuando esté en verde, 'Detener' guardará el tiempo.", font=("Arial", 12))
        self.etiqueta_instrucciones.grid(row=1, column=0, columnspan=2, pady=10)

        self.etiqueta_cronometro = tk.Label(ventana, text="Tiempo: 0.00s", font=("Arial", 12))
        self.etiqueta_cronometro.grid(row=2, column=0, columnspan=2, pady=5)

        self.etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 12), fg="blue")
        self.etiqueta_resultado.grid(row=3, column=0, columnspan=2, pady=5)

        # Botones Iniciar y Detener
        self.boton_iniciar = tk.Button(ventana, text="Iniciar", font=("Arial", 12), command=self.iniciar)
        self.boton_iniciar.grid(row=4, column=0, pady=10, padx=10)

        self.boton_detener = tk.Button(ventana, text="Detener", font=("Arial", 12), command=self.detener)
        self.boton_detener.grid(row=4, column=1, pady=10, padx=10)

        # Enlace para el teclado
        ventana.bind("<space>", lambda event: self.detener())

        # Ruta del archivo de puntuaciones en el mismo directorio que el script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.archivo_puntuaciones = os.path.join(base_dir, "puntuaciones.txt")

    def iniciar(self):
        if not self.ejecutando:
            self.ejecutando = True
            self.inicio_ciclo = time.time()
            self.etiqueta_resultado.config(text="")
            # Iniciar el ciclo del semáforo
            self.a_rojo()
            # Actualiza el cronómetro
            self.actualizar_cronometro()

    def detener(self):
        # Si se presiona "Detener" mientras la luz está en verde, se mide el tiempo.
        if self.ejecutando and self.esta_verde_encendida():
            diferencia = time.time() - self.inicio_verde
            self.etiqueta_resultado.config(text=f"Tiempo desde verde hasta detener: {diferencia:.2f}s")
            # Guardar la puntuación en el archivo
            self.guardar_puntuacion(diferencia)
        
        self.ejecutando = False

    def a_rojo(self):
        if not self.ejecutando:
            return
        # ROJO
        self.encender_luz("roja")
        self.ventana.after(self.tiempo_rojo * 1000, self.a_amarillo)

    def a_amarillo(self):
        if not self.ejecutando:
            return
        # AMARILLO
        self.encender_luz("amarilla")
        self.ventana.after(self.tiempo_amarillo * 1000, self.a_verde)

    def a_verde(self):
        if not self.ejecutando:
            return
        # VERDE (se mantiene hasta que el usuario presione "Detener")
        self.inicio_verde = time.time()
        self.encender_luz("verde")

    def encender_luz(self, color):
        # Reiniciar todas las luces a gris
        self.lienzo.itemconfig(self.luz_roja, fill="gray")
        self.lienzo.itemconfig(self.luz_amarilla, fill="gray")
        self.lienzo.itemconfig(self.luz_verde, fill="gray")

        # Encender la luz correspondiente
        if color == "roja":
            self.lienzo.itemconfig(self.luz_roja, fill="red")
        elif color == "amarilla":
            self.lienzo.itemconfig(self.luz_amarilla, fill="yellow")
        elif color == "verde":
            self.lienzo.itemconfig(self.luz_verde, fill="green")

    def esta_verde_encendida(self):
        # Verifica si la luz verde está encendida
        color_actual = self.lienzo.itemcget(self.luz_verde, "fill")
        return color_actual == "green"

    def actualizar_cronometro(self):
        if self.ejecutando and self.inicio_ciclo is not None:
            transcurrido = time.time() - self.inicio_ciclo
            self.etiqueta_cronometro.config(text=f"Tiempo: {transcurrido:.2f}s")
            self.ventana.after(100, self.actualizar_cronometro)  # Actualiza cada 0.1s

    def guardar_puntuacion(self, puntuacion):
        # Leer las puntuaciones existentes
        puntuaciones = []
        if os.path.exists(self.archivo_puntuaciones):
            with open(self.archivo_puntuaciones, "r") as f:
                for linea in f:
                    linea = linea.strip()
                    if linea:
                        try:
                            puntuaciones.append(float(linea))
                        except ValueError:
                            pass

        # Añadir la nueva puntuación
        puntuaciones.append(puntuacion)

        # Ordenar las puntuaciones de menor a mayor
        puntuaciones.sort()

        # Sobrescribir el archivo con las puntuaciones ordenadas
        with open(self.archivo_puntuaciones, "w") as f:
            for p in puntuaciones:
                f.write(f"{p:.2f}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = Semaforo(root)
    root.mainloop()
