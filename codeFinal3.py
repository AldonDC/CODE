import serial
import time
import threading
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

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

def send_right():
    time.sleep(0.5)  # Ajustar el delay según sea necesario
    ser.write(b'\x01')  # Envía el byte 0x01 para indicar dirección derecha

def send_left():
    time.sleep(0.5)  # Ajustar el delay según sea necesario
    ser.write(b'\x03')  # Envía el byte 0x03 para indicar dirección izquierda

def send_stop():
    time.sleep(0.5)  # Ajustar el delay según sea necesario
    ser.write(b'\x02')  # Envía el byte 0x02 para indicar freno

# Crear la ventana de la GUI
window = tk.Tk()
window.title("Datos del Tractor en Tiempo Real")

# Crear el frame para los botones
button_frame = tk.Frame(window)
button_frame.pack()

# Crear los botones para las direcciones
right_button = tk.Button(button_frame, text="Right", command=send_right, width=10, height=2)
left_button = tk.Button(button_frame, text="Left", command=send_left, width=10, height=2)
stop_button = tk.Button(button_frame, text="Brake", command=send_stop, width=10, height=2)

# Añadir los botones al frame
right_button.grid(row=0, column=0, padx=5, pady=5)
left_button.grid(row=0, column=1, padx=5, pady=5)
stop_button.grid(row=0, column=2, padx=5, pady=5)

# Definir las listas
velocidad_motor = []
velocidad_vehiculo = []
marcha = []
tiempos = []

# Crear un archivo CSV y escribir los encabezados
with open('datos_tractorFINAL2.csv', 'w', newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(['Engine Speed', 'Vehicle Speed', 'Gear'])

# Función para leer datos desde el STM32 a través de UART
def read_data():
    global stop_thread
    while not stop_thread:
        # Leer datos desde STM32 a través de UART
        data = ser.readline().decode().strip()
        if data:
            data_list = data.split(',')
            if len(data_list) == 3:
                try:
                    motor = float(data_list[0])
                    vehicle = float(data_list[1])
                    gear = int(float(data_list[2]))  # Convertir a float y luego a int

                    # Imprimir los datos en la consola
                    print(f"Velocidad del motor: {motor}, Velocidad del vehículo: {vehicle}, Marcha: {gear}")
                    # Añadir datos a las listas
                    velocidad_motor.append(motor)
                    velocidad_vehiculo.append(vehicle)
                    marcha.append(gear)
                    tiempos.append(len(tiempos) + 1)

                    # Escribir datos en el archivo CSV
                    with open('datos_tractorFINAL2.csv', 'a', newline='') as archivo_csv:
                        writer = csv.writer(archivo_csv)
                        writer.writerow([motor, vehicle, gear])
                    time.sleep(0.1)
                except (IndexError, ValueError) as e:
                    pass  # Ignorar los errores de conversión y formato
            # else:
            #     print(f"Error: datos recibidos no tienen el formato esperado: {data_list}")

# Función para actualizar las gráficas en tiempo real
def update_plot(i):
    ax1.clear()
    ax2.clear()
    ax3.clear()

    ax1.plot(tiempos, velocidad_vehiculo, label="Vehicle Speed", color='blue')
    ax2.plot(tiempos, velocidad_motor, label="Engine Speed", color='red')
    ax3.plot(tiempos, marcha, label="Gear", color='green')

    ax1.set_title("Velocidad del vehículo")
    ax2.set_title("Velocidad del motor")
    ax3.set_title("Marcha")

    ax1.legend()
    ax2.legend()
    ax3.legend()

# Crear la figura y los ejes para matplotlib
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

# Ajustar el espacio entre las gráficas
plt.subplots_adjust(hspace=0.5)

# Integrar la figura de matplotlib en tkinter
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()

# Iniciar los hilos
threading.Thread(target=read_data).start()

# Iniciar la animación de matplotlib
ani = animation.FuncAnimation(fig, update_plot, interval=1000)

# Iniciar el bucle principal de la GUI en el hilo principal
window.mainloop()

# Detener los hilos al cerrar la ventana
stop_thread = True
ser.close()
