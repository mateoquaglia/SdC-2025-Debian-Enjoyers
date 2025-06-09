import os
import socket
import threading
import time

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
        return 0  # Simula un valor bajo (0)

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