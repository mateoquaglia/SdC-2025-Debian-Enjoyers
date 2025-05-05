[BITS 16]
[ORG 0x7C00]         ; Dirección de carga típica para un bootloader

cli                  ; 1. Desactivar interrupciones

; 2. Crear la GDT
gdt_start:
    ; Null descriptor (obligatorio)
    dd 0x0
    dd 0x0

    ; Código (base=0x0, limite=0xFFFFF, tipo=0x9A)
    dw 0xFFFF          ; Límite 0-15
    dw 0x0000          ; Base 0-15
    db 0x00            ; Base 16-23
    db 10011010b       ; Acceso: código ejecutable, leído, presente
    db 11001111b       ; Flags: 4K granularity, 32-bit segment
    db 0x00            ; Base 24-31

    ; Datos (base=0x0, limite=0xFFFFF, tipo=0x92)
    dw 0xFFFF          ; Límite 0-15
    dw 0x0000          ; Base 0-15
    db 0x00            ; Base 16-23
    db 10010010b       ; Acceso: datos, leído/escrito, presente
    db 11001111b       ; Flags: 4K granularity, 32-bit segment
    db 0x00            ; Base 24-31
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1 ; Tamaño GDT - 1
    dd gdt_start               ; Dirección GDT

; 3. Cargar la GDT
lgdt [gdt_descriptor]

; 4. Activar modo protegido
mov eax, cr0
or eax, 1
mov cr0, eax

; 5. Far jump para actualizar CS y pasar a 32 bits
jmp 0x08:protected_mode_entry

; ------ Ahora estamos en modo protegido (32 bits) ------
[BITS 32]
protected_mode_entry:
    ; Configurar los registros de segmento
    mov ax, 0x10      ; Selector de segmento de datos
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    ; Intentar escribir en el segmento de datos de solo lectura (esto causará un fallo)
    mov eax, 0x12345678
    mov [0x100000], eax    ; Intentar escribir en la memoria protegida

hang:
    jmp hang

times 510-($-$$) db 0 ; Rellenar hasta el byte 510
dw 0xAA55             ; Firma de arranque (MBR boot signature)

