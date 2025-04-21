; filepath: /home/facundo/Escritorio/SDC/Entrega 2/convert.asm
section .text
    global convert

convert:
    ; Entrada: número flotante en el stack
    ; Salida: número entero en eax
    fld dword [esp + 4]    ; Cargar el float desde el stack
    fistp dword [esp + 4]  ; Convertir a entero y almacenar en el stack
    mov eax, [esp + 4]     ; Mover el entero a eax
    add eax, 1             ; Sumar 1
    ret

section .note.GNU-stack noalloc noexec nowrite progbits