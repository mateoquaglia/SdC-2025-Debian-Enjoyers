
# TP3

## UNIVERSIDAD NACIONAL DE CÓRDOBA 
### FACULTAD DE CIENCIAS EXACTAS, FÍSICAS Y NATURALES

# TRABAJO PRÁCTICO Nº 3
## “Modo Protegido”

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

## ¿Qué es UEFI?

UEFI es una especificación que define una interfaz entre el firmware del sistema operativo y el hardware. A diferencia del BIOS, UEFI permite:

- Soporte para discos duros de más de 2 TB (usando el sistema de particiones GPT en lugar de MBR).
- Interfaz gráfica más avanzada (en vez de solo texto).
- Soporte para arranque seguro (Secure Boot).
- Mejor manejo de drivers y periféricos antes de cargar el sistema operativo.

UEFI (Unified Extensible Firmware Interface) es una interfaz de firmware moderna que reemplaza al tradicional BIOS (Basic Input/Output System) en muchos computadores actuales. UEFI es el software de bajo nivel que se ejecuta cuando enciendes tu computadora, antes de que cargue el sistema operativo.

### ¿Cómo puedes usar UEFI?

Puedes interactuar con UEFI principalmente de dos formas:

- Durante el arranque del sistema:
    - Presiona una tecla especial como F2, DEL, ESC, F10, dependiendo del fabricante, justo después de encender el equipo para entrar en la configuración de UEFI.
- Desde allí puedes configurar el orden de arranque, activar o desactivar Secure Boot, habilitar virtualización, entre otros.

### Función que podrías usar desde UEFI

Una función típica del entorno UEFI es la llamada a funciones del boot manager para iniciar sistemas operativos. Por ejemplo:

```c
EFI_STATUS BootManagerLoadBootOption(EFI_BOOT_MANAGER_LOAD_OPTION *BootOption, VOID **ImageHandle);
```

Esta función carga una entrada del gestor de arranque definida en la tabla UEFI, lo que permite iniciar un sistema operativo o una utilidad preinstalada.

---

## Vulnerabilidades en UEFI

A lo largo del tiempo, se han descubierto múltiples formas en que el sistema UEFI ha sido vulnerado por actores maliciosos.

- **LoJax (2018):** Malware que logró instalarse directamente en el firmware del equipo. Persistía incluso después de formatear el disco o reinstalar el sistema operativo.

- **MoonBounce (2022):** Ataque aún más difícil de detectar porque operaba completamente desde el firmware.

- **Errores de fabricantes:** Configuraciones inseguras que permitían alterar el firmware o desactivar funciones críticas como el arranque seguro.

- **Thunderbolt vulnerabilities:** Permiten modificar configuraciones del firmware si no está protegida correctamente la escritura en la memoria del firmware.

---

## ¿Qué es CSME y MEBx?

El **Converged Security and Management Engine (CSME)** es parte del **Intel Management Engine (ME)**, un subsistema independiente dentro del chipset de los procesadores Intel.

Funciones de CSME:

- Administración remota de dispositivos.
- Seguridad en el arranque (Secure Boot, autenticación de hardware).
- Soporte para Intel AMT (Active Management Technology).
- Almacenamiento seguro de claves criptográficas y TPM integrado.

---

## ¿Qué es coreboot? ¿Qué productos lo incorporan? ¿Cuáles son las ventajas de su utilización?

**coreboot** es un proyecto de firmware libre y de código abierto que reemplaza al firmware propietario tradicional (BIOS o UEFI).

Productos que incorporan coreboot:

- Dispositivos Chromebook.
- Portátiles de Purism (Librem), System76 (algunos modelos), MINISFORUM.
- Servidores y estaciones de trabajo open-source.
- Algunas placas base Intel/AMD específicas.
- ThinkPads antiguos (T60, X200, X220).

### Ventajas de coreboot:

1. Código abierto y auditable.
2. Arranque más rápido.
3. Sin componentes propietarios (en algunos casos).
4. Mayor seguridad.
5. Más control sobre el hardware.
6. Menor superficie de ataque.

---

## ¿Qué es un linker?

Un **linker** (enlazador) une varios fragmentos de código objeto en un ejecutable o biblioteca final.

### ¿Qué hace un linker?

- Resuelve símbolos.
- Combina código objeto en un ejecutable.
- Agrega bibliotecas necesarias.
- Asigna direcciones de memoria.

### ¿Qué es la dirección que aparece en el script del linker? ¿Por qué es necesaria?

La dirección (load address) organiza la memoria de forma precisa. Permite:

- Control del layout de memoria.
- Evitar superposición.
- Compatibilidad con hardware o bootloaders.
- Seguridad y separación de segmentos.
- Relocalización o carga dinámica.
- 
![image](https://github.com/user-attachments/assets/f86bc8a9-c2fe-47a3-accf-45f708b591ab)
![image](https://github.com/user-attachments/assets/9a68dd35-21da-4baf-8a39-ddb8d06142eb)

---

## Comparación de objdump con hd

En `main.img`:

- El programa empieza en offset 0x0000.
- Cuando BIOS carga `main.img`, estará en dirección 0x7C00.

Se verifica en `hd`:

- Datos desde 0x0000 (no vacíos).
- 0x55AA en offset 0x01FE (requerido por BIOS).
- 
![image](https://github.com/user-attachments/assets/3dbc2fae-4f54-4c33-b1da-d18d40be332a)


---

## Grabar la imagen en un pendrive y probar

![image](https://github.com/user-attachments/assets/e16aabfa-f7fd-4808-a12d-05c32cb79599)
![image](https://github.com/user-attachments/assets/7f57a680-43f9-442a-a72e-7988899c0b7a)



---

## ¿Para qué se utiliza la opción `--oformat binary` en el linker?

- Para generar una salida binaria cruda, eliminando encabezados o metadatos.
- Deja sólo los bytes necesarios para ejecutar.

---

## Crear un código assembler para pasar a modo protegido (sin macros)
-Iniciamos la imagen con: "nasm -g -o protected_mode.img protected_mode.asm"
-Ejecutamos qemu con "qemu-system-i386 -drive format=raw,file=protected_mode.img -boot a -s -S -monitor stdio"
-Iniciamos GDB con "gdb" en otra terminal
-Comenzamos la lectura de archivos
**Código de assembler**
![image](https://github.com/user-attachments/assets/f3adf079-17a6-4abd-8af9-12ed8b376216)
**Implementacion de los codigos previos**
![WhatsApp Image 2025-05-05 at 11 19 23](https://github.com/user-attachments/assets/718575aa-1579-4064-80e8-abbaae2151b1)

**Lectura de registros con GDB**
-Se coloca un breakpoint en la seccion donde se ingresa a modo protegido.
-Se leen los registros con "info registers"
![WhatsApp Image 2025-05-05 at 11 12 08](https://github.com/user-attachments/assets/dd87ae1b-9076-4ab1-8084-959a29b253f5)




---

## ¿Cómo sería un programa con dos descriptores de memoria diferenciados (código y datos)?

**Uso de Descriptores de Memoria:**

- **Segmento de Código:** Solo lectura y ejecución.
- **Segmento de Datos:** Lectura y escritura.

**Configuración:**

- Crear GDT con ambos descriptores.
- Ajustar registros de segmento (DS, ES, FS, etc.).

---

## Cambiar los bits de acceso del segmento de datos a solo lectura y verificar con GDB

1. Crear GDT con permisos adecuados.
2. Intentar escribir en segmento de solo lectura.
3. Resultado: Excepción SIGSEGV (Segmentation Fault) confirmada con GDB.

---

## ¿Con qué valor se cargan los registros de segmento en modo protegido?

- Se cargan con **selectores**, no direcciones físicas.
- Ejemplo de instrucción:

```assembly
movw $0x10, %ax
movw %ax, %ds
```

- 0x10 representa un selector de segmento.

Permite protección de memoria, aislamiento de procesos, multitarea segura.

---

## Uso de GDB en hello world

- Iniciar imagen en QEMU.
- Conectar GDB a QEMU.
- Colocar breakpoints.
- Avanzar paso a paso escribiendo "hello world" letra por letra.
- 
![image](https://github.com/user-attachments/assets/58dc88af-f995-4f8a-b3fc-f83bec09e4f3)
![image](https://github.com/user-attachments/assets/ca53a4f5-f787-412a-a4e2-efe87ac4a306)



---


