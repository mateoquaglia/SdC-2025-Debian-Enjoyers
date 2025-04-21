
# TP2 - Explicación

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

---

## Código en C (`process_gini.c`)

**Funcionamiento:**
- Abre y lee el archivo `gini.json`.
- Extrae el nombre del país y el índice GINI de cada entrada.
- Convoca el código en ensamblador para convertir el índice GINI (`float`) a un entero y sumar `+1`.
- Imprime el nombre del país y el índice GINI procesado en el terminal.

---

## Código en Assembler (`convert.asm`)

**Funcionamiento:**
- Recibe un número flotante como parámetro desde el programa en C.
- Convierte el número flotante a entero utilizando instrucciones de la **unidad de punto flotante (FPU)**.
- Suma el valor `+1`.
- Devuelve el resultado al programa en C.
