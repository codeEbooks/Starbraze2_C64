; STARBRAZE II, step 2 of 17: scrolling. PAL C64. Assemble
; this file: it includes the others.
;
; Level 1, THE CANYONS of Varkonia Prime:
;  - It scrolls from right to left at the speeds of the
;    level, with the far mesas at half speed and the stars
;    in three planes, to the arena at its end.
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

; The main loop: one turn a frame, when the HUD starts.
; First what has a deadline at the top of the screen: the
; camera; then the screens' work, the camera of the next
; turn; then, in the frame's lower half, rows 0-9 of the
; next frame (ahead).
frame_loop:
        lda frame_flag
        beq frame_loop
        lda #0
        sta frame_flag
        lda frame_count         ; the frame of the turn
        sta turn_count
joy_ready:                      ; the tests stop here
        jsr move_camera
        lda swap_flag
        beq +
        jsr flip_front          ; the back screen in front
+
        lda arena               ; the arena: no work of
        beq +                   ; the screens
        jmp _plan
+       lda swap_flag
        beq _steps
        jsr colour_bottom       ; the swap: rows 15-21
        jsr swap_back           ; the new column
        jmp _far
_steps:
        lda speed + 1           ; under a pixel a frame, and
        bne +                   ; the camera on to its next
        lda cam_frac            ; pixel next frame (when the
        clc                     ; stars move, in ahead): no
        adc speed               ; step of the back screen
        bcs _far                ; (there is time: 16 frames
+       jsr prepare_back        ; a column, 8 of them still)
_far:
        lda far_flag            ; the far layer: a column on
        beq +
        jsr far_step
+
_plan:
        jsr camera_plan         ; the next turn's camera
frame_ready:                    ; the tests look here
        jsr ahead               ; rows 0-9 of the next frame
        jmp frame_loop

        .include "irq.asm"
        .include "vic.asm"
        .include "level.asm"
        .include "scroll.asm"
        .include "stars.asm"
        .include "data.asm"

        * = AUDIO               ; from $8000
        .include "fast.asm"
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
