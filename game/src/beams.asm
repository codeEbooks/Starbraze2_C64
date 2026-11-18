; Level 2's beams: in tract C, the energy bridges, beams {14}
; fall from the pylons to row 9 and rise from posts on the {14}
; deck to row 15. Level 3's spines too, out of the alien's {14}
; ribs. Each level its own characters (beam_bytes, in its {14}
; LEVEL_W1). Their cells are characters of their own, one {14}
; code for the beams down (beam_down), one for those up {14}
; (beam_up): 0, the level has none. A beam is off (its {14}
; character empty), dimmed (drawn: not rock) or on (drawn {14}
; and rock: rock_lines has its lines, ship.asm). A cycle of {14}
; BEAM_CYCLE frames (beam_timer): the beams down dimmed from {14}
; BEAM_DOWN_DIM, on from BEAM_DOWN_ON, off from BEAM_UP_DIM, {14}
; when the beams up are dimmed; those on from BEAM_UP_ON, {14}
; off when the cycle starts again. Each frame, for the next {14}
; one (update_varkon). A level whose beam_module is not 0 {14}
; (level 6) has its beams driven by the station's module, {14}
; with its own cycle (P3_BEAMS), here at the same point of {14}
; the turn (before the Varkon: a character changed later {14}
; could be seen by the beam half old, half new). {14}
;|; Level 2's beams: in tract C, the energy bridges, beams {10-13}
;|; fall from the pylons to row 9 and rise from posts on the {10-13}
;|; deck to row 15. Level 3's spines too, out of the alien's {10-13}
;|; ribs. Each level its own characters (beam_bytes, in its {10-13}
;|; LEVEL_W1). Their cells are characters of their own, one {10-13}
;|; code for the beams down (beam_down), one for those up {10-13}
;|; (beam_up): 0, the level has none. A beam is off (its {10-13}
;|; character empty), dimmed (drawn: not rock) or on (drawn {10-13}
;|; and rock: rock_lines has its lines, ship.asm). A cycle of {10-13}
;|; BEAM_CYCLE frames (beam_timer): the beams down dimmed from {10-13}
;|; BEAM_DOWN_DIM, on from BEAM_DOWN_ON, off from BEAM_UP_DIM, {10-13}
;|; when the beams up are dimmed; those on from BEAM_UP_ON, {10-13}
;|; off when the cycle starts again. Each frame, for the next {10-13}
;|; one (update_varkon). {10-13}
;|; Level 2's beams: in tract C, the energy bridges, beams {9-9}
;|; fall from the pylons to row 9 and rise from posts on the {9-9}
;|; deck to row 15. Each level its own characters (beam_bytes, {9-9}
;|; in its LEVEL_W1). Their cells are characters of their own, {9-9}
;|; one code for the beams down (beam_down), one for those up {9-9}
;|; (beam_up): 0, the level has none. A beam is off (its {9-9}
;|; character empty), dimmed (drawn: not rock) or on (drawn {9-9}
;|; and rock: rock_lines has its lines, ship.asm). A cycle of {9-9}
;|; BEAM_CYCLE frames (beam_timer): the beams down dimmed from {9-9}
;|; BEAM_DOWN_DIM, on from BEAM_DOWN_ON, off from BEAM_UP_DIM, {9-9}
;|; when the beams up are dimmed; those on from BEAM_UP_ON, {9-9}
;|; off when the cycle starts again. Each frame, for the next {9-9}
;|; one (update_varkon). {9-9}

; At the level's start: both off (the characters come
; empty), the cycle's last frame.
beam_reset:
        lda #BEAM_CYCLE - 1
        sta beam_timer
        rts

beam_step:
        lda beam_module         ; the station's module's {14}
        beq beam_plain          ; beams (station.asm: {14}
        jmp P3_BEAMS            ; st_beams) {14}
beam_plain: ; {14}
        lda beam_down           ; none in this level
        beq _done
        lda arena               ; none in the arena: there
        bne _done               ; their codes may be STAGE
                                ; CLEAR's letters
        lda beam_timer
        clc
        adc #1
        and #BEAM_CYCLE - 1
        sta beam_timer
        cmp #BEAM_DOWN_DIM
        bne +
        ldx beam_up             ; the cycle again: up off,
        ldy #0                  ; down dimmed
        jsr set_beam
        ldx beam_down
        ldy #1
        jmp set_beam
+       cmp #BEAM_DOWN_ON
        bne +
        ldx beam_down           ; down on
        ldy #2
        jmp set_beam
+       cmp #BEAM_UP_DIM
        bne +
        ldx beam_down           ; down off, up dimmed
        ldy #0
        jsr set_beam
        ldx beam_up
        ldy #1
        jmp set_beam
+       cmp #BEAM_UP_ON
        bne _done
        ldx beam_up             ; up on
        ldy #2
        jmp set_beam
_done:
        rts

        .cerror BEAM_CYCLE & (BEAM_CYCLE - 1) != 0, "cycle"

; Beam code X, its character Y: 0 off, 1 dimmed, 2 on
; (beam_bytes: 8 bytes each); its lines in rock_lines only
; when it is on.
set_beam:
        txa                     ; dst: CHARSET + 8 X
        sta dst
        lda #0
        .rept 3
        asl dst
        rol a
        .endrept
        adc #>CHARSET           ; (C = 0)
        sta dst + 1
        tya
        sta temp
        asl a
        asl a
        asl a
        sta src                 ; its 8 bytes' place
        tya
        pha
        ldy #0
-       sty src + 1
        ldy src
        lda beam_bytes,y
        ldy src + 1
        sta (dst),y
        inc src
        iny
        cpy #8
        bne -
        pla
        cmp #2
        beq _rock
        lda #0                  ; off, dimmed: not rock
        .for b_k in range(8)
        sta rock_lines + b_k * 256,x
        .endfor
        rts
_rock:
        .for b_k in range(8)
        lda beam_bytes + 16 + b_k
        sta rock_lines + b_k * 256,x
        .endfor
        rts
