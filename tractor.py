import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Función para calcular las RPM
def calcular_rpm(velocidad_angular, radio_rueda, relacion_transmision):
    return (velocidad_angular * 60) / (2 * np.pi * radio_rueda * relacion_transmision)

# Generar datos aleatorios
np.random.seed(0)  # Para reproducibilidad
velocidad_angular = np.random.uniform(5, 15, 100)  # Velocidades angulares entre 5 y 15 rad/s
radio_rueda = np.random.uniform(0.3, 0.7, 100)  # Radios de rueda entre 0.3 y 0.7 metros
relacion_transmision = 10  # Relación de transmisión constante

# Calcular RPM
rpm = calcular_rpm(velocidad_angular, radio_rueda, relacion_transmision)

# Crear DataFrame para almacenar los datos
datos = pd.DataFrame({
    'Velocidad angular de la rueda (rad/s)': velocidad_angular,
    'Radio de la rueda (m)': radio_rueda,
    'Relación de transmisión': relacion_transmision,
    'RPM': rpm
})

# Guardar los datos en un archivo CSV
ruta_csv = 'datos_tractor4.csv'
datos.to_csv(ruta_csv, index=False)

# Visualizar la información
plt.figure(figsize=(12, 6))

# Gráfico de RPM vs Velocidad Angular de la Rueda
plt.subplot(1, 2, 1)
plt.scatter(datos['Velocidad angular de la rueda (rad/s)'], datos['RPM'], color='blue')
plt.title('RPM vs Velocidad Angular de la Rueda')
plt.xlabel('Velocidad Angular (rad/s)')
plt.ylabel('RPM')

# Gráfico de RPM vs Radio de la Rueda
plt.subplot(1, 2, 2)
plt.scatter(datos['Radio de la rueda (m)'], datos['RPM'], color='red')
plt.title('RPM vs Radio de la Rueda')
plt.xlabel('Radio de la Rueda (m)')
plt.ylabel('RPM')

plt.tight_layout()
plt.show()
