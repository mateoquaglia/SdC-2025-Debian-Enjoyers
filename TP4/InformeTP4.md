# Desafío 1

## ¿Qué es un checkinstall y para qué sirve?
Un **checkinstall** es un proceso o una herramienta que se utiliza durante la instalación de software, con el fin de realizar un seguimiento de los archivos que se están instalando y para crear un paquete que los contenga.

## ¿Con qué acciones se puede mejorar la seguridad del kernel? ¿Qué son los rootkits?
Hay varias formas de mejorar la seguridad del kernel:

1. **Requerir la firma digital de módulos**: Esto asegura que los módulos cargados estén firmados, reduciendo el riesgo de cargar módulos maliciosos.
2. **Modo "Kernel Lockdown"**: Impide cargar módulos no firmados, lo que disminuye significativamente el riesgo de ataques.
3. **Auditorías de seguridad**: Herramientas como AppArmor o SELinux permiten detectar comportamientos anómalos.

Si no se aplican estas prácticas de seguridad y los atacantes logran acceso al nivel raíz del sistema, pueden instalar **rootkits**. Los rootkits son herramientas que habilitan una puerta trasera en el sistema, permitiendo a los atacantes robar datos y controlar el sistema.

## Realizar el empaquetamiento de HelloWorld "Checklist"

---

# Desafío 2
![image](https://github.com/user-attachments/assets/907737e3-4134-4100-9928-367209a531d4)

## ¿Qué diferencias observan entre los dos `modinfo`?
La principal diferencia es que uno de los módulos es personalizado, mientras que el otro es genérico. Ambos tienen la misma licencia ("GPL"), pero difieren en otros aspectos.
![image](https://github.com/user-attachments/assets/0c2c2c63-c5bc-4fd7-8597-fb884a0dd20a)

## Diferencias entre módulos de los integrantes
Commiteadas en este repositorio se pueden encontrar los archivos txt generados por cada integrante del grupo y cada archivo que muertra la diferencia entre los módulos que cada uno.


## Utilizamos el comando `lsmod`
En el caso del integrante "Facu", hay muchos módulos que se encuentran sin uso pero disponibles, como:
- `bridge`
- `overlay`
- `input_leds`
- `usbhid`
- `joydev`

  
![image](https://github.com/user-attachments/assets/267e2888-e920-4b7d-8ffc-0baf2bc138a8)

Estos módulos tienen sus bytes particulares, pero ninguno está en uso en este momento.

Cuando el driver de un dispositivo no está disponible, el dispositivo no funcionará correctamente o fallará. Por ejemplo, si falta el módulo de una tarjeta de red, esta no podrá conectarse.

## Realizando `hwinfo` y `cat hwinfo_report.txt`
![image](https://github.com/user-attachments/assets/e02d2f95-557e-4797-8324-6ce51ece3a50)

Obtenemos un listado como el siguiente:  
[https://gist.github.com/FacundoBerra/c00edae1e3764349fc96facff3ca5d85](https://gist.github.com/FacundoBerra/c00edae1e3764349fc96facff3ca5d85)

---

## Módulo vs Programa

### Módulo:
- Es un fragmento de código que se puede cargar dinámicamente dentro del kernel del sistema operativo.
- Sirve para extender las funcionalidades del kernel sin necesidad de recompilar (ej. drivers, sistemas de archivos).
- Funciona a nivel kernel (privilegios altos).
- **Ejemplo**: Driver de una tarjeta de red.

### Programa:
- Es una aplicación o proceso que corre en espacio de usuario.
- Tiene acceso limitado a hardware y recursos a través de llamadas al sistema.
- Puede ser interactivo o de línea de comandos.
- **Ejemplo**: Un editor de texto, navegador, `ls`, etc.

---

## Uso del comando `strace`
El comando `strace` muestra todas las llamadas al sistema (syscalls) que realiza un programa mientras se ejecuta. Estas llamadas son la forma en que el programa interactúa con el sistema operativo.

---

## ¿Qué es un segmentation fault?
Un **segmentation fault** ocurre cuando un programa intenta acceder a una región de memoria que no tiene permiso para usar. Esto puede suceder, por ejemplo:
1. Leer o escribir en una dirección no válida.
2. Acceder a memoria fuera de los límites de un arreglo.
3. Usar un puntero no inicializado o nulo.

### ¿Cómo lo maneja el kernel?
1. **Protección de memoria**: El kernel utiliza la Unidad de Gestión de Memoria (MMU) para dividir la memoria en páginas y asignar permisos (lectura, escritura, ejecución) a cada una.
2. **Señal SIGSEGV**: El kernel envía una señal `SIGSEGV` (segmentation violation) al proceso que causó el error.
3. **Terminación del proceso**: Si el programa no maneja la señal `SIGSEGV`, el kernel termina el proceso y genera un mensaje de error (como "Segmentation fault (core dumped)").

### ¿Cómo lo maneja un programa?
Un programa puede manejar un segmentation fault utilizando un manejador de señales (`signal` o `sigaction`). Por ejemplo:

```c
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

void sigsegv_handler(int sig) {
    printf("Segmentation fault detected! Signal: %d\n", sig);
    exit(1); // Terminar el programa de forma controlada
}

int main() {
    signal(SIGSEGV, sigsegv_handler); // Registrar el manejador de SIGSEGV

    int *ptr = NULL;
    *ptr = 42; // Esto causará un segmentation fault

    return 0;
}
```
En este caso, el programa captura la señal SIGSEGV y ejecuta el manejador en lugar de terminar abruptamente.

Conclusión
El kernel detecta el acceso no válido y envía la señal SIGSEGV. Si el programa no maneja la señal, el kernel termina el proceso.
### Firmar módulo de Kernel
A partir de la documentacion brindada por los profesores de la catedra “https://askubuntu.com/questions/770205/how-to-sign-kernel-modules-with-sign-file”
realizamos los pasos de dicho documento el cual adjuntamos en la imagen siguiente:

![image](https://github.com/user-attachments/assets/fb4918c1-8999-488f-85c3-a695854493b7)

### Compilacion de Modulo de Kernel
Al reiniciar, se accede al MOK Manager, una interfaz azul para gestionar claves de Secure Boot.
![WhatsApp Image 2025-05-28 at 17 49 39](https://github.com/user-attachments/assets/67a32a3d-4611-43f5-9c55-df69dfb12232)

![WhatsApp Image 2025-05-28 at 17 49 45](https://github.com/user-attachments/assets/904eb1ae-0e20-4e51-a028-bbe3026b47fa)

El sistema muestra:

Número de serie

Emisor y sujeto

Fechas de validez

Huella digital (fingerprint)

Sirve para confirmar que es la clave correcta.

![WhatsApp Image 2025-05-28 at 17 49 50](https://github.com/user-attachments/assets/a44a1d0c-638f-40d2-bed0-5fb8ad2ece81)

Confirmar el enrolamiento

![WhatsApp Image 2025-05-28 at 17 49 58](https://github.com/user-attachments/assets/3179a7c1-8f36-4d93-8e92-ae20b1ed5432)

Se introduce la contraseña establecida al ejecutar mokutil para autorizar la operación

![WhatsApp Image 2025-05-28 at 17 50 05](https://github.com/user-attachments/assets/1816aae2-fa8c-4bd3-bd5e-e82353e8e564)

Seleccionar la clave desde el disco

Se muestra una lista de discos y particiones (puede ser desde USB o disco interno)

Se navega hasta donde esté guardado el archivo .der y se selecciona.

![image](https://github.com/user-attachments/assets/b0bbc61f-fc56-4131-8963-67867868b3e5)

La clave se guarda en la base de datos MOK del sistema.

### ¿Qué pasa si tu compañero tiene Secure Boot habilitado y quiere cargar un módulo que vos compilaste?
No podrá cargarlo. El kernel lo rechazará automáticamente porque el módulo no está firmado con una clave válida reconocida por el sistema, y esto sucede porque Secure Boot, al estar habilitado, no permite la carga de módulos que no estén firmados digitalmente con una clave que el sistema reconozca como válida.
El módulo, aunque haya sido correctamente compilado, no tiene una firma válida para el sistema.


