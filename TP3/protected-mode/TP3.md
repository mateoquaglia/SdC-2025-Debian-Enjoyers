
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

---

## Comparación de objdump con hd

En `main.img`:

- El programa empieza en offset 0x0000.
- Cuando BIOS carga `main.img`, estará en dirección 0x7C00.

Se verifica en `hd`:

- Datos desde 0x0000 (no vacíos).
- 0x55AA en offset 0x01FE (requerido por BIOS).

---

## Grabar la imagen en un pendrive y probar

**[Comentario: Adjuntar foto de la prueba física]**

---

## ¿Para qué se utiliza la opción `--oformat binary` en el linker?

- Para generar una salida binaria cruda, eliminando encabezados o metadatos.
- Deja sólo los bytes necesarios para ejecutar.

---

## Crear un código assembler para pasar a modo protegido (sin macros)

**[Comentario: Adjuntar código de ejemplo]**

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

## Uso de GDB en Assembler

- Iniciar imagen en QEMU con el comando "qemu-system-i386 -drive format=raw,file=protected_mode.img -boot a -s -S -monitor stdio".
- Conectar GDB a QEMU.
- Colocar breakpoints.
- Avanzar paso a paso.

**[Comentario: Adjuntar captura de la sesión de GDB]**

---


