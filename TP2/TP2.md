# Trabajo Práctico Nº2 – Stack Frame


## Integrantes del Grupo

- **BERRA, Facundo Horacio**  
- **ESPEJO, Alejandro Andres** 
- **QUAGLIA, Mateo** 

---

##  Profesores

- **JORGE, Javier Alejandro**   
- **SOLINAS, Miguel Ángel** 
- **LAMBERTI, Germán** 
Facultad de Ciencias Exactas, Físicas y Naturales – UNC

---

##  Grupo

**Debian Enjoyers**   

# Explicación

## Enunciado

Diseñar e implementar cálculos en ensamblador. La capa superior recuperará información de una API REST.  
Se recomienda el uso de **API REST y Python**.  

Los datos de consulta realizados deben ser entregados a un programa en **C** que convocará rutinas en **ensamblador** para que hagan los cálculos de conversión y devuelvan los resultados a las capas superiores. Luego, el programa en C o Python mostrará los cálculos obtenidos.

---

## Resumen del flujo general

### Python:
- Obtiene los datos del índice GINI desde la API y los guarda en un archivo JSON.

### C:
- Lee el archivo JSON, procesa los datos y llama a la función ensambladora para realizar cálculos.

### Assembler:
- Convierte los valores flotantes a enteros.
- Suma `+1`.
- Devuelve el resultado al programa en C.

---

## Código en Python (`TP2.py`)

**Propósito:**  
Recuperar los datos del índice GINI desde la API del Banco Mundial y guardarlos en un archivo JSON (`gini.json`).

**Funcionamiento:**
- Consulta la API para una lista de países usando sus códigos.
- Extrae los valores del país y los valores del índice GINI de la respuesta de la API.
- Guarda los datos en un archivo JSON en formato estructurado, donde cada entrada contiene el nombre del país y su índice GINI.


  ![WhatsApp Image 2025-04-21 at 11 28 46](https://github.com/user-attachments/assets/b1b3dc9f-faf6-4968-a366-e2aa605dc032)

---

## Código en C (`process_gini.c`)

**Funcionamiento:**
- Abre y lee el archivo `gini.json`.
- Extrae el nombre del país y el índice GINI de cada entrada.
- Convoca el código en ensamblador para convertir el índice GINI (`float`) a un entero y sumar `+1`.
- Imprime el nombre del país y el índice GINI procesado en el terminal.


  ![WhatsApp Image 2025-04-21 at 11 28 27](https://github.com/user-attachments/assets/983be0e7-588f-4786-b3b0-2b16f15f7605)

---

## Código en Assembler (`convert.asm`)

**Funcionamiento:**
- Recibe un número flotante como parámetro desde el programa en C.
- Convierte el número flotante a entero utilizando instrucciones de la **unidad de punto flotante (FPU)**.
- Suma el valor `+1`.
- Devuelve el resultado al programa en C.


  ![WhatsApp Image 2025-04-21 at 11 27 58 (1)](https://github.com/user-attachments/assets/f4598e02-09e7-436f-9e8e-5b3f182f4dbd)


## Compilación del código en ensamblador
- nasm -f elf32 convert.asm -o convert.o

## Compilación del código en C + ensamblador
- gcc -m32 -g -o process_gini process_gini.c convert.o -ljson-c

## Ejecutar el programa
- ./process_gini

![WhatsApp Image 2025-04-21 at 11 26 27](https://github.com/user-attachments/assets/a8075d3b-2277-404b-ab52-a17561f39115)

## Usar GDB para depurar
- gdb ./process_gini
  
## Comandos útiles dentro de GDB:
- (gdb) break main           # Coloca un punto de ruptura en main
- (gdb) run                  # Ejecuta el programa
- (gdb) step                 # Ejecuta línea por línea (entra a funciones)
- (gdb) next                 # Ejecuta siguiente línea (sin entrar en funciones)
- (gdb) info registers       # Muestra el contenido de los registros
- (gdb) x/4xb &variable      # Inspecciona la memoria en una dirección
- (gdb) quit                 # Salir del depurador

**Ejecución Info resgisters**

![WhatsApp Image 2025-04-21 at 11 26 03 (1)](https://github.com/user-attachments/assets/2e37298b-e382-4824-9ba7-7e19018f9eba)

