# Importa las bibliotecas necesarias
import time
import serial
import threading
import csv
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly import offline
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# Variable global para detener los hilos
stop_thread = False

# Configura el puerto serial
ser = serial.Serial(
    port="/dev/ttyUSB0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1  # Ajusta el puerto y baudrate
)

# Listas para almacenar los datos en tiempo real
velocidad_motor = []
velocidad_vehiculo = []
marcha = []
tiempos = []

# Crear la ventana principal
root = tk.Tk()
root.title("Control del Tractor")

# Crear las etiquetas y los campos de entrada para cada parámetro
labels = ["Aceleración", "Torque", "Freno", "Direccionales"]
entries = []

for label in labels:
    frame = tk.Frame(root)
    frame.pack()

    label_widget = tk.Label(frame, text=label)
    label_widget.pack(side=tk.LEFT)

    entry = tk.Entry(frame)
    entry.pack(side=tk.RIGHT)
    entries.append(entry)

# Crear una función para manejar el botón de enviar
def enviar():
    for i, entry in enumerate(entries):
        print(f"{labels[i]}: {entry.get()}")
    
    # Aquí puedes agregar el código para enviar los datos a la Raspberry Pi
    # Por ejemplo, podrías usar la biblioteca 'serial' para enviar los datos a través de un puerto serial
    data_to_send = ",".join([entry.get() for entry in entries])
    ser.write(data_to_send.encode())

# Crear el botón de enviar
boton_enviar = tk.Button(root, text="Enviar", command=enviar)
boton_enviar.pack()

# Función para leer datos desde el STM32 a través de UART
def read_data():
    global stop_thread
    while not stop_thread:
        # Leer datos desde STM32 a través de UART
        data = ser.readline().decode().strip()
        if data:
            data_list = data.split(',')
            try:
                motor = float(data_list[0])
                vehicle = float(data_list[1])
                gear = float(data_list[2])

                # Imprimir los datos en la consola
                print(f"Velocidad del motor: {motor}, Velocidad del vehículo: {vehicle}, Marcha: {gear}")

                # Añadir datos a las listas
                velocidad_motor.append(motor)
                velocidad_vehiculo.append(vehicle)
                marcha.append(gear)
                tiempos.append(len(tiempos) + 1)

                # Escribir datos en el archivo CSV
                with open('datos_tractor4.csv', 'a', newline='') as archivo_csv:
                    writer = csv.writer(archivo_csv)
                    writer.writerow(['Engine Speed', 'Vehicle Speed', 'Gear'])
                time.sleep(0.1)
            except (IndexError, ValueError):
                print("Error: no se pudo leer los datos correctamente")
    ser.close()

# Función para detener el hilo con la entrada del usuario
def inputs():
    global stop_thread
    input()
    stop_thread = True

# Función para actualizar las gráficas
def update_plot():
    global stop_thread
    fig = make_subplots(rows=3, cols=1, subplot_titles=('Velocidad del vehículo', 'Velocidad del motor', 'Marcha'))

    vehicle_speed_trace = go.Scatter(x=[], y=[], mode='lines', name='Velocidad del vehículo')
    engine_speed_trace = go.Scatter(x=[], y=[], mode='lines', name='Velocidad del motor')
    gear_trace = go.Scatter(x=[], y=[], mode='lines', name='Marcha')

    fig.add_trace(vehicle_speed_trace, row=1, col=1)
    fig.add_trace(engine_speed_trace, row=2, col=1)
    fig.add_trace(gear_trace, row=3, col=1)

    fig.update_layout(height=800, width=600, title_text="Datos del Tractor en Tiempo Real")
    plot_url = offline.plot(fig, auto_open=False)

    while not stop_thread:
        fig.data[0].x = tiempos
        fig.data[0].y = velocidad_vehiculo

        fig.data[1].x = tiempos
        fig.data[1].y = velocidad_motor

        fig.data[2].x = tiempos
        fig.data[2].y = marcha

        offline.plot(fig, filename=plot_url, auto_open=False)
        time.sleep(2)

# Iniciar los hilos
threading.Thread(target=inputs).start()
threading.Thread(target=read_data).start()
threading.Thread(target=update_plot).start()

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
