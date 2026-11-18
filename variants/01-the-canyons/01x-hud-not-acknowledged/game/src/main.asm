; STARBRAZE II, step 1 of 17: the canyons. PAL C64. Assemble
; this file: it includes the others.
;
; Level 1, THE CANYONS of Varkonia Prime:
;  - The start of the level, still: the near layer (rows
;    0-9, 14-21), the far mesas (rows 10-13), the HUD (rows
;    22-24).
        .cpu "6502"
        .include "memory.asm"
        .include "../assets/generated/assets.inc"

        * = $0801
        .word basic_end         ; BASIC line: 10 SYS 2061
        .word 10
        .byte $9e
        .text "2061"
        .byte 0
basic_end:
        .word 0

entry:
        sei                     ; no interrupts here
        cld
        ldx #$ff                ; fresh stack
        txs
        jsr kernal_out          ; BASIC and KERNAL out
        jsr move_store          ; the packed levels,
                                ; title.asm's module
        jmp game_start

; The main loop: one turn a frame, when the HUD starts
; (frame_flag); the picture is still: the turn has no work.
frame_loop:
        lda frame_flag
        beq frame_loop
        lda #0
        sta frame_flag
joy_ready:                      ; the tests stop here
frame_ready:                    ; the tests look here
        jmp frame_loop

        .include "irq.asm"
        .include "vic.asm"
        .include "level.asm"
        .include "data.asm"

        * = AUDIO               ; from $8000
        .align 256
rock_lines:
stage_1:                        ; the store's 2nd piece
        .binary "../assets/generated/store1.bin"
        .fill 8 * 256 - STAGE_LEN_1
LEVEL_W2:                       ; the level's maps
stage_2:                        ; and the store's 3rd piece
        .binary "../assets/generated/store2.bin"
high_end:
        .cerror LEVEL_W2 + LEVEL_W2_SIZE > $d000, "LEVEL_W2"
        .cerror * > $d000, "the code reaches the I/O"
        .cerror STORE + STORE_SIZE > $fffa, "the store"
