import socket
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