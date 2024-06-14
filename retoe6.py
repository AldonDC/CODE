#Importación de librerías
import time
import serial
import threading
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Función para mejorar el flujo
def inputs():
    global stop_thread
    input()
    stop_thread = True

# Configuración del puerto serial
ser = serial.Serial(
    port = "/dev/ttyUSB0",
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1)  # Ajusta el puerto y baudrate 


# Crear archivo CSV y escribir encabezados
with open('datos_tractor3.csv', 'w', newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(['Engine Speed', 'Vehicle Speed', 'Gear'])
    
stop_thread = False

# Listas para almacenar los datos en tiempo real
velocidad_motor = []
velocidad_vehiculo = []
marcha = []
tiempos = []
vel_motor = []
vel_v = []
marchas = []

threading.Thread(target=inputs).start()

plt.ion()
#fig, axs = plt.subplots(2, 2, figsize = (12, 8))

# Función para actualizar y mostrar la gráfica de velocidad del vehículo
def actualizar_grafica_velocidad_vehiculo():
    plt.subplot(3, 1, 1)
    plt.plot(tiempos, vel_v, 'g-')
    plt.xlabel('Tiempo')
    plt.ylabel('Velocidad del vehículo')
    plt.title('Velocidad del vehículo en tiempo real')

# Función para actualizar y mostrar la gráfica de velocidad del motor
def actualizar_grafica_velocidad_motor():
    plt.subplot(3, 1, 2)
    plt.plot(tiempos, vel_motor,'b-')
    plt.xlabel('Tiempo')
    plt.ylabel('Velocidad del motor')
    plt.title('Velocidad del motor en tiempo real')

# Función para actualizar y mostrar la gráfica de marcha
def actualizar_grafica_marcha():
    plt.subplot(3, 1, 3)
    plt.plot(tiempos, marchas,'r-')
    plt.xlabel('Tiempo')
    plt.ylabel('Marcha')
    plt.title('Marcha en tiempo real')
    
while not stop_thread:
    # Leer datos desde STM32 a través de UART
    data = ser.readline().decode().strip()
    if data:
        data_list = data.split(',')
        try:
            # Asignar valores de la lectura a una variable
            motor = data_list[0]
            vehicle = data_list[1]
            gear = data_list[2]
            
            # Imprimir los datos en la consola
            print(f"Velocidad del motor: {motor}, Velocidad del vehículo: {vehicle}, Marcha: {gear}")

            # Agregar valores leídos a una lista   
            vel_motor.append(float(motor))
            vel_v.append(float(vehicle))
            marchas.append(float(gear))
            
            # Obtener el tiempo actual
            tiempos.append(len(tiempos) + 1)
            
            # Escribir datos en el archivo CSV
            with open('datos_tractor3.csv', 'a', newline='') as archivo_csv:
                writer = csv.writer(archivo_csv)
                writer.writerow([motor, vehicle, gear])
                
            # Actualizar y mostrar las gráficas
            plt.clf()
            actualizar_grafica_velocidad_vehiculo()
            actualizar_grafica_velocidad_motor()
            actualizar_grafica_marcha()

            # Ajustar el diseño de las subgráficas
            plt.tight_layout()
            plt.draw()

            # Mostrar las gráficas y generar delay
            plt.pause(0.01)
            time.sleep(0.1)
            
        except KeyboardInterrupt:
            break

# Cierra el puerto serial y muestra la gráfica final
ser.close()
plt.ioff()
plt.show()
