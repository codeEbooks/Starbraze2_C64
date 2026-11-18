; The SHIELD CORE's sphere on the screen (core.asm has the
; rest): in the high part, after the boss engine (the low
; part is full).

; --- the sphere on the screen (boss_draw, early in a turn,
; before the beam draws rows 8-13) -------------------------
; What boss_update asked for (cb_paint): 1 its cells on
; (the characters they showed: nothing changes yet) and its
; colours, 2 its colours (a colour a row), 3 white, 4 the
; arena's cells again (codes, colours: cb_save). In ENTER,
; after its cells are on, CB_GROW_FRAMES frames: two lines
; of its characters, from the equator out (sphere_line).
sphere_draw:
        jsr sphere_asked
        lda boss_state          ; ENTER, frames CB_PREP + 1
        cmp #ST_ENTER           ; to + 24: lines 23 - k and
        bne _done               ; 24 + k, k from 0
        lda boss_timer
        sec
        sbc #CB_PREP + 1
        bcc _done
        cmp #CB_GROW_FRAMES
        bcs _done
        sta b_tmp + 1
        clc
        adc #SPHERE_LINES / 2
        jsr sphere_line
        lda #SPHERE_LINES / 2 - 1
        sec
        sbc b_tmp + 1
        jmp sphere_line
_done:
        rts

sphere_asked:
        lda cb_paint
        bne +
        rts
+       ldx #0
        stx cb_paint
        cmp #2
        beq _own
        bcc _on
        cmp #4
        beq _gone
        ldx #SPHERE_CELLS - 1   ; white
-       ldy cb_cell,x
        lda #8 | CB_FLASH_OWN
        sta SPHERE_COLOURS,y
        dex
        bpl -
        rts
_on:
        ldx #SPHERE_CELLS - 1   ; its cells
-       ldy cb_cell,x
        txa
        clc
        adc #SPHERE_FIRST
        sta SPHERE_AT,y
        dex
        bpl -
_own:
        ldx #SPHERE_COLS - 1    ; its colours
-       .for r_k in range(SPHERE_ROWS)
        lda #8 | SPHERE_OWN[r_k]
        sta SPHERE_COLOURS + r_k * 40,x
        .endfor
        dex
        bpl -
        rts
_gone:
        ldx #SPHERE_CELLS - 1
-       ldy cb_cell,x
        lda cb_save,x
        sta SPHERE_AT,y
        lda cb_save + SPHERE_CELLS,x
        sta SPHERE_COLOURS,y
        dex
        bpl -
        rts

; Line A (0-47) of the sphere's characters, from
; sphere_data into its codes: the line of its row's six.
sphere_line:
        tax
        and #%00000111
        sta b_tmp
        txa
        lsr a
        lsr a
        lsr a
        tax
        lda b_tmp               ; its row's first byte + the
        clc                     ; line (under 256)
        adc cb_row,x
        tax
        clc
        adc #<sphere_data
        sta src
        lda #>sphere_data
        adc #0
        sta src + 1
        txa
        clc
        adc #<(CHARSET + 8 * SPHERE_FIRST)
        sta dst
        lda #>(CHARSET + 8 * SPHERE_FIRST)
        adc #0
        sta dst + 1
        ldy #8 * (SPHERE_COLS - 1)
-       lda (src),y
        sta (dst),y
        tya
        sec
        sbc #8
        tay
        bcs -
        rts

cb_row:                         ; a row's first byte
        .for r_k in range(SPHERE_ROWS)
        .byte r_k * 8 * SPHERE_COLS
        .endfor
cb_cell:                        ; cell k's place from the
        .for r_k in range(SPHERE_ROWS)  ; sphere's first
        .for c_k in range(SPHERE_COLS)
        .byte r_k * 40 + c_k
        .endfor
        .endfor
