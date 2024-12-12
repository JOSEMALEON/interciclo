import time
import random
import tkinter as tk

def contador_solo_modo_continuo():
    """
    Función que genera un tiempo aleatorio entre 5 y 10 segundos.
    El contador inicial no aparece en la pantalla. Solo se muestra el
    contador en modo continuo con cambio de color según el tiempo extra.
    Ambos botones "Detener" y "Reiniciar" están visibles desde el principio,
    alineados uno al lado del otro en la parte superior de la ventana.
    El semáforo actúa de forma diferente: pasa de rojo a amarillo tras 3 segundos,
    y se mantiene en amarillo hasta que termine el primer temporizador.
    """
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Contador con Semáforo Animado")
    ventana.geometry("400x500")  # Ajustar el tamaño de la ventana
    ventana.resizable(False, False)  # Evitar redimensionar la ventana
    ventana.configure(bg="white")  # Fondo blanco para toda la ventana
    
    # Centrar la ventana en la pantalla
    ancho_ventana = 400
    alto_ventana = 500
    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    # Calcular las coordenadas para centrar la ventana
    posicion_x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    posicion_y = (alto_pantalla // 2) - (alto_ventana // 2)
    # Establecer la posición de la ventana
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

    # Canvas para mostrar el semáforo (sin fondo)
    canvas = tk.Canvas(ventana, width=200, height=300)
    canvas.pack(pady=20)

    # Crear los círculos para las luces del semáforo (más pequeños y menos separados)
    circulo_rojo = canvas.create_oval(60, 40, 140, 120, fill="gray")
    circulo_amarillo = canvas.create_oval(60, 120, 140, 200, fill="gray")
    circulo_verde = canvas.create_oval(60, 200, 140, 280, fill="gray")

    # Crear la etiqueta para el contador (sin fondo)
    etiqueta = tk.Label(ventana, text="", font=("Arial", 40), bg="white")
    etiqueta.pack(expand=True)

    # Frame para los botones (sin fondo)
    frame_boton = tk.Frame(ventana, bg="white")
    frame_boton.pack(side="top", pady=10)

    # Botón para detener el contador (sin fondo)
    detener = tk.BooleanVar(value=False)
    def detener_contador():
        detener.set(True)

    boton_detener = tk.Button(frame_boton, text="Detener", command=detener_contador, font=("Arial", 16), bg="SystemButtonFace")
    boton_detener.pack(side="left", padx=10)

    # Botón de reiniciar (sin fondo)
    def reiniciar():
        ventana.destroy()
        contador_solo_modo_continuo()

    boton_reiniciar = tk.Button(frame_boton, text="Reiniciar", command=reiniciar, font=("Arial", 16), bg="SystemButtonFace")
    boton_reiniciar.pack(side="left", padx=10)

    # Función para cambiar el semáforo a rojo
    def encender_rojo():
        canvas.itemconfig(circulo_rojo, fill="red")
        ventana.after(3000, encender_amarillo)  # Después de 3 segundos, cambia a amarillo

    # Función para cambiar el semáforo a amarillo
    def encender_amarillo():
        canvas.itemconfig(circulo_amarillo, fill="yellow")
        # El semáforo permanecerá en amarillo hasta que termine el temporizador
        # No cambia a verde hasta que el primer temporizador termine

    # Función para cambiar el semáforo a verde
    def encender_verde():
        canvas.itemconfig(circulo_verde, fill="green")
        # El semáforo puede continuar o hacer lo que desees tras el temporizador

    # Generar un tiempo aleatorio entre 5 y 10 segundos
    tiempo_aleatorio = random.uniform(5, 10)

    # Función para manejar el tiempo inicial
    def esperar_tiempo_random(inicio):
        tiempo_actual = time.time() - inicio
        if tiempo_actual >= tiempo_aleatorio:
            # Cambiar al modo continuo después del tiempo inicial
            encender_verde()  # Cambia a verde una vez que el temporizador termine
            actualizar_contador(time.time())  # Iniciar contador
            return

        # Continuar esperando sin bloquear el bucle
        ventana.after(10, esperar_tiempo_random, inicio)

    # Función para actualizar el contador en modo continuo
    def actualizar_contador(inicio):
        if detener.get():
            return  # Detener el contador si se pulsa el botón

        tiempo_actual = time.time() - inicio
        tiempo_extra = tiempo_actual

        # Cambiar el color según el tiempo extra
        if tiempo_extra < 0.5:
            ventana.configure(bg="green")
        else:
            ventana.configure(bg="red")

        # Calcular segundos y milisegundos
        segundos = int(tiempo_actual)
        milisegundos = int((tiempo_actual - segundos) * 1000)
        etiqueta.config(text=f"{segundos:02d}:{milisegundos:03d}")

        # Programar la próxima actualización
        ventana.after(10, actualizar_contador, inicio)

    # Iniciar la espera del tiempo aleatorio inicial
    inicio = time.time()

    # Cambiar el semáforo a rojo al principio
    encender_rojo()

    # Iniciar la espera del primer temporizador
    ventana.after(1, esperar_tiempo_random, inicio)

    # Ejecutar el bucle principal de la ventana
    ventana.mainloop()

# Llamar a la función
contador_solo_modo_continuo()