# TP3

## UNIVERSIDAD NACIONAL DE CÓRDOBA 
### FACULTAD DE CIENCIAS EXACTAS, FÍSICAS Y NATURALES

# TRABAJO PRÁCTICO Nº 3
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

# Informe Técnico – TP: Driver de Caracteres y Visualización de Señales

## 1. Introducción

Este trabajo práctico tiene como objetivo implementar un **Controlador de Dispositivo de Caracteres (CDD)** en un sistema Linux embebido (Raspberry Pi) para sensar dos señales externas, permitiendo su lectura desde espacio de usuario mediante una aplicación que las grafique en tiempo real.

Se utilizan técnicas de desarrollo a nivel de kernel, emulación de hardware y desarrollo de aplicaciones gráficas en Python, logrando una interacción completa entre capas de software y hardware simulado.

---

## 2. Objetivos

- Desarrollar un **driver de caracteres** en espacio kernel que permita la lectura de dos señales.
- Permitir la **selección dinámica** de la señal a observar desde el espacio de usuario.
- Implementar una aplicación en Python para la **visualización gráfica** de la señal seleccionada.
- **Emular** el entorno de desarrollo usando QEMU y una imagen de Raspberry Pi.
- Documentar y demostrar el funcionamiento del sistema completo.

---

## 3. Desarrollo

### 3.1 Driver de Caracteres

Se implementó un módulo de kernel en C que:

- Registra un dispositivo de caracteres (`/dev/mi_cdd`).
- Simula dos señales periódicas con actualización cada 1 segundo.
- Permite al usuario seleccionar qué señal observar mediante `write()` o `ioctl`.
- Devuelve el valor de la señal seleccionada al leer desde el dispositivo.

> 📸 **[Agregar aquí capturas del código del driver]**

### 3.2 Generación de Señales

Las señales fueron generadas por software, simulando entradas digitales periódicas (por ejemplo, funciones senoidales o cuadradas). Se utilizó un timer interno del módulo para actualizar los valores sin intervención del usuario.

> 📸 **[Agregar aquí capturas de las señales simuladas]**

### 3.3 Emulación con QEMU

Se configuró un entorno de emulación de Raspberry Pi utilizando QEMU con una imagen ARM de Linux. El driver fue compilado utilizando la toolchain cruzada `arm-linux-gnueabihf-gcc` y cargado con `insmod` dentro del entorno emulado.

> 📸 **[Agregar aquí capturas de la emulación funcionando]**

### 3.4 Aplicación de Usuario en Python

Se desarrolló una aplicación en Python 3 que:

- Abre el archivo de dispositivo `/dev/mi_cdd`.
- Envía el número de señal a leer (0 o 1).
- Lee datos de la señal seleccionada una vez por segundo.
- Grafica los valores en tiempo real utilizando `matplotlib`.
- Resetea el gráfico automáticamente al cambiar de señal.

> 📸 **[Agregar aquí capturas del código Python y gráficos]**

---

## 4. Resultados

- El sistema permite seleccionar, leer y visualizar cualquiera de las dos señales simuladas.
- La aplicación reacciona correctamente ante el cambio de señal, limpiando y ajustando la gráfica.
- Se comprobó el correcto funcionamiento del CDD en entorno emulado con QEMU.
- El driver responde de forma estable, manteniendo coherencia en los datos entregados al usuario.

> 📸 **[Agregar aquí capturas de resultados y gráficas]**

---

## 5. Conclusiones

- Se logró cumplir con los objetivos propuestos, construyendo un flujo completo de interacción entre kernel y usuario.
- La emulación en QEMU permitió trabajar de forma segura sin necesidad de hardware físico.
- El sistema es escalable: el CDD podría extenderse para incluir más señales o agregar operaciones adicionales vía `ioctl`.
- Se consolidaron conocimientos de programación de bajo nivel, comunicación entre procesos, manejo de dispositivos y visualización de datos.

---

## 6. Tecnologías y Herramientas Utilizadas

- Lenguaje C (para desarrollo del módulo kernel)
- Python 3 (para la aplicación de usuario)
- `matplotlib` (gráficas en tiempo real)
- QEMU (emulación de Raspberry Pi)
- Toolchain cruzada ARM (`arm-linux-gnueabihf-gcc`)
- Make, Bash, Git

---



