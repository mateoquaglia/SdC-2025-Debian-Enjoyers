[BITS 16]
[ORG 0x7C00]         ; Dirección típica de carga para bootloaders

cli                  ; Desactiva interrupciones

; --- GDT ---
gdt_start:
    ; Descriptor nulo
    dd 0x0
    dd 0x0

    ; Segmento de código (base 0x0, límite 0xFFFFF, tipo 0x9A)
    dw 0xFFFF          ; Límite 0-15
    dw 0x0000          ; Base 0-15
    db 0x00            ; Base 16-23
    db 10011010b       ; Acceso: código, ejecutable, leído, presente
    db 11001111b       ; Flags: 4K, 32-bit
    db 0x00            ; Base 24-31

    ; Segmento de datos (base 0x0, límite 0xFFFFF, tipo 0x92)
    dw 0xFFFF
    dw 0x0000
    db 0x00
    db 10010010b       ; Acceso: datos, lectura/escritura, presente
    db 11001111b
    db 0x00
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

; --- Cargar GDT ---
lgdt [gdt_descriptor]

; --- Habilitar modo protegido ---
mov eax, cr0
or eax, 1
mov cr0, eax

; --- Hacer far jump para cambiar CS ---
jmp 0x08:protected_mode_entry

; --- Código en modo protegido ---
[BITS 32]
protected_mode_entry:
    ; Cargar los segmentos con el selector de datos (0x10)
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    ; No se hace nada más, solo un bucle infinito sin errores
hang:
    jmp hang

; --- Sector de arranque debe terminar en 0xAA55 ---
times 510-($-$$) db 0
dw 0xAA55
