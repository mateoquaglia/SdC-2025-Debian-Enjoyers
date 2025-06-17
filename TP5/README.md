# TP5

## UNIVERSIDAD NACIONAL DE CÓRDOBA 
### FACULTAD DE CIENCIAS EXACTAS, FÍSICAS Y NATURALES

# TRABAJO PRÁCTICO Nº 5
## “Device drivers”

### Grupo
**Debian Enjoyers**

### Integrantes del Grupo
- BERRA, Facundo Horacio
- ESPEJO, Alejandro Andres
- QUAGLIA, Mateo

### Profesores
- JORGE, Javier Alejandro
- SOLINAS, Miguel Ángel
- LAMBERTI, Germán

---

# Informe – TP: Driver de Caracteres y Visualización de Señales

##  Objetivo

Diseñar e implementar un CDD (Controlador de Dispositivo de Caracteres) que permita sensar dos señales externas con un periodo de 1 segundo. Una aplicación de usuario deberá poder:
- Seleccionar cuál de las dos señales desea leer.


- Leer y graficar dicha señal en función del tiempo.


- Resetear el gráfico al cambiar de señal.


---

## Estructura del Sistema
- CDD en espacio kernel: dispositivo de caracteres que expone dos señales.


- Aplicación en espacio de usuario (Python): interfaz para seleccionar señal y graficar.


- Emulación del entorno: Raspberry Pi emulada con QEMU.


- Señales externas: generadas por software con actualización cada segundo.

---

## Paso 1: Implementación del CDD (cdd_simulated.py)

```
import os
import socket
import threading
import time
import random

# Simulación de GPIO para entornos no Raspberry Pi
class MockGPIO:
   BCM = "BCM"
   IN = "IN"

   def setmode(self, mode):
       print(f"MockGPIO: setmode({mode})")

   def setup(self, pin, mode):
       print(f"MockGPIO: setup(pin={pin}, mode={mode})")

   def input(self, pin):
       print(f"MockGPIO: input(pin={pin})")
       return random.randint(0, 100)  # Devuelve un valor aleatorio entre 0 y 100

   def cleanup(self):
       print("MockGPIO: cleanup()")

# Usar MockGPIO en lugar de RPi.GPIO
GPIO = MockGPIO()

HOST = '/tmp/cdd_socket'  # Socket local
current_signal = 'A'
clients = []

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BCM)
SIGNAL_A_PIN = 17  # Pin GPIO para la señal A
SIGNAL_B_PIN = 27  # Pin GPIO para la señal B
GPIO.setup(SIGNAL_A_PIN, GPIO.IN)
GPIO.setup(SIGNAL_B_PIN, GPIO.IN)

def read_gpio_signal(pin):
   """
   Lee el estado del pin GPIO y devuelve un valor simulado.
   """
   return GPIO.input(pin)

def generate_signals():
   """
   Lee las señales de los pines GPIO y las envía a los clientes conectados.
   """
   while True:
       time.sleep(1)  # Simular un período de 1 segundo
       for client in clients[:]:
           conn = client['conn']
           sig = client['signal']
           try:
               # Leer el valor de la señal desde el GPIO
               if sig == 'A':
                   value = read_gpio_signal(SIGNAL_A_PIN)
               else:
                   value = read_gpio_signal(SIGNAL_B_PIN)

               # Enviar datos al cliente
               data = f"{sig},{int(time.time())},{value}\n"
               conn.sendall(data.encode())
               print(f"Enviando datos a cliente: {data.strip()}")  # Depuración
           except Exception as e:
               print(f"Error enviando datos al cliente: {e}")  # Depuración
               clients.remove(client)

def handle_client(conn):
   """
   Maneja la conexión con un cliente.
   """
   clients.append({'conn': conn, 'signal': 'A'})  # Cada cliente empieza con señal A
   print("Cliente conectado")  # Depuración
   try:
       while True:
           data = conn.recv(1024)
           if not data:
               break
           cmd = data.decode().strip().upper()
           if cmd in ['A', 'B']:
               for c in clients:
                   if c['conn'] == conn:
                       c['signal'] = cmd
                       print(f"Cliente cambió a señal: {cmd}")  # Depuración
   except Exception as e:
       print(f"Error manejando cliente: {e}")  # Depuración
   finally:
       # Eliminar cliente de la lista al desconectarse
       clients[:] = [c for c in clients if c['conn'] != conn]
       conn.close()
       print("Cliente desconectado")  # Depuración

def start_server():
   """
   Inicia el servidor del CDD simulado.
   """
   try:
       os.unlink(HOST)
   except FileNotFoundError:
       pass
   s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
   s.bind(HOST)
   s.listen()
   print("CDD Simulado corriendo...")  # Depuración

   # Iniciar el generador de señales en un hilo separado
   threading.Thread(target=generate_signals, daemon=True).start()

   while True:
       conn, _ = s.accept()
       threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
   try:
       start_server()
   finally:
       GPIO.cleanup()  # Limpiar configuración de GPIO al salir

 ```

- Se crea un módulo de kernel que registra un dispositivo de caracteres.


- Las señales se generan mediante la funcion “generate_signals()” la cual en nuestro caso decidimos optar valores aleatorios tomados de 0 a 100 cada segundo. 


### Paso 2: Aplicación en Python (app_user.py)

``` import socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

HOST = '/tmp/cdd_socket'  # Ruta del socket UNIX

# Variables globales para almacenar los datos
timestamps = []
values = []
current_signal = "A"  # Señal actual (A o B)

def update_graph(frame):
   """
   Función que actualiza el gráfico en tiempo real.
   """
   plt.cla()  # Limpiar el gráfico
   plt.plot(timestamps, values, label=f"Señal {current_signal}")
   plt.xlabel("Tiempo (s)")
   plt.ylabel("Valor de la señal")
   plt.title(f"Gráfico de la señal {current_signal}")
   plt.legend()
   plt.grid()

def main():
   global current_signal, timestamps, values

   try:
       # Conectar al servidor
       with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
           s.connect(HOST)
           print("Conectado al servidor")

           # Configurar el gráfico
           fig = plt.figure()
           ani = FuncAnimation(fig, update_graph, interval=1000)

           while True:
               # Pedir al usuario que ingrese una señal
               signal = input("Ingresa la señal a enviar (A o B, o 'exit' para salir): ").strip().upper()
               if signal == 'EXIT':
                   print("Cerrando conexión...")
                   break
               elif signal not in ['A', 'B']:
                   print("Señal inválida. Ingresa 'A', 'B' o 'exit'.")
                   continue

               # Enviar la señal al servidor
               s.sendall(signal.encode())
               print(f"Señal enviada al servidor: {signal}")
               current_signal = signal  # Actualizar la señal actual

               # Recibir datos del servidor
               data = s.recv(1024).decode().strip()
               if not data:
                   print("Conexión cerrada por el servidor.")
                   break

               # Procesar múltiples líneas de datos
               for line in data.split("\n"):
                   if line:
                       try:
                           _, timestamp, value = line.split(",")
                           timestamps.append(int(timestamp))
                           values.append(int(value))
                       except ValueError:
                           print(f"Error procesando línea: {line}")

               # Mostrar el gráfico
               plt.pause(0.1)

           plt.ioff()  # Desactivar el modo interactivo
           plt.show()  # Mostrar el gráfico final

   except ConnectionResetError:
       print("Conexión cerrada por el servidor.")
   except Exception as e:
       print(f"Error: {e}")

if __name__ == "__main__":
   main()

 ```

- Envía un comando para el usuario seleccione la señal que se esta muestreando y graficando (ej: señal "A" o señal "B").

- Lee los datos en tiempo real y los grafica usando matplotlib.

- Al momento de ejecutar el comando "A" o "B" se actualiza la señal muestreada por medio del plot, y se observan los nuevos valores que va tomando, debido a esto el gráfico se reinicia y se ajusta.

### Paso 3: Ejecución del código
- El código se ejecuta en 2 terminales, en una ejecutamos “python3 cdd_simulated.py” el cual inicia el socket, y luego ejecutamos en otra terminal “python3 app_user.py” para poder ir actualizando las señales.

- Procedemos a adjuntar capturas de como se observan las señales (aclarando que entre una y otra fueron pasando segundos, por eso se ve más avanzada en el tiempo)

![WhatsApp Image 2025-06-15 at 23 58 04](https://github.com/user-attachments/assets/fe8ae82c-0215-46da-bde4-304456f024c5)

<img width="1009" alt="Captura de pantalla 2025-06-16 a la(s) 12 50 10 a  m" src="https://github.com/user-attachments/assets/3687b04b-d470-4013-b2cc-e2c74b4a0dd4" />


### Paso 4: Emulación de Raspberry Pi en QEMU

- Se utilizó QEMU para emular una Raspberry Pi con Linux, 
 La imagen utilizada se descargó de:
 [raspios_oldstable_lite_armhf (Buster)](https://downloads.raspberrypi.org/raspios_oldstable_lite_armhf/images/)

- El comando que utilizamos para ejecutar QEMU y que comience la simulación fue:

``` 
qemu-system-arm \
  -kernel ~/Escritorio/SDC/TP5/qemu-rpi-kernel/kernel-qemu-4.19.50-buster \
  -dtb ~/Escritorio/SDC/TP5/qemu-rpi-kernel/versatile-pb.dtb \
  -m 256 \
  -M versatilepb \
  -cpu arm1176 \
  -no-reboot \
  -append "root=/dev/sda2 panic=1" \
  -drive file=~/Escritorio/2021-12-02-raspios-buster-armhf-lite.img,format=raw \
  -net nic -net user,hostfwd=tcp::5023-:22 \
  -audio none \
  -nographic

 ```


## Paso 5: Conexión SSH a la Raspberry Pi emulada
- Luego ya ingresando el usuario y la contraseña, la manera más efectiva que encontramos para cargar en código en la raspberry era por medio de localhost, entonces utilizamos:
``` sh -p 5023 pi@localhost ```
y ya estando conectados al local host, utilizamos el “wget” para actualizar el código en la raspberry en caso de que le hayamos hecho modificaciones.

```
wget http://10.0.2.2:8000/cdd_simulated.py
wget http://10.0.2.2:8000/app_user.py

```
posterior a esto, ejecutamos el código normalmente con

```
python3 cdd_simulated.py
python3 app_user.py

```
y procedemos a ver la ejecución:

<img width="1009" alt="Captura de pantalla 2025-06-16 a la(s) 12 57 25 a  m" src="https://github.com/user-attachments/assets/527b7d39-fc43-4618-9f18-b91d3dab836f" />
<img width="1012" alt="Captura de pantalla 2025-06-16 a la(s) 12 57 41 a  m" src="https://github.com/user-attachments/assets/961d83ff-9b5f-4cf4-bf3f-b219cc8ef841" />



---

## Conclusiones

- Se logró implementar el código funcional en la raspberry pi, no es posible observar gráficamente las señales en el plot de python puesto que al ser una versión “lite” de Raspios la utilizada, no tiene interfaz gráfica, y el código a pesar de ir variando entre las señales perfectamente, la única forma de observar el plot era por fuera de la raspberry.
- El sistema al momento de probarlo en el entorno de emulación, nos encontramos ciertas complicaciones, puesto que la versión que habíamos descargado de la raspberry era muy moderna y QEMU no la soportaba, entonces debimos descargar la versión del año 2021 que adjuntamos arriba.
  [Link de Versión 2021](https://downloads.raspberrypi.org/raspios_oldstable_lite_armhf/images/raspios_oldstable_lite_armhf-2021-12-02/)
- Por medio de matplotlib entonces logramos que la aplicación gráfica sea capaz de representar y cambiar entre las dos señales en tiempo real, cumpliendo así con la consigna.


---



