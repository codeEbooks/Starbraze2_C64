; The loading screen of a file from the disk (phase.asm
; reads it), and its words: in the HUD's hole (hole.asm),
; the low memory being full.

; The loading screen on screen A: rows 0-21 blank, the
; number and name of the file's phase (file_phase), the bar,
; LOADING; the HUD's characters for the whole screen (rows
; 22-24, the HUD, stay as they are, VARKONIA in place of a
; boss's bar). No interrupts: the VIC-II set here.
phase_screen:
        jsr boss_reset          ; VARKONIA again
        lda #0
        tax
-       sta SCREEN_A,x          ; rows 0-21: 880 bytes
        sta SCREEN_A + $100,x
        sta SCREEN_A + $200,x
        inx
        bne -
        ldx #22 * 40 - $300 - 1
-       sta SCREEN_A + $300,x
        dex
        bpl -
        ldx ph_want             ; the file's phase:
        lda file_phase - 1,x    ; PHASE n, its name
        tax
        ldy ph_words_lo - 1,x
        lda ph_words_hi - 1,x
        jsr ph_words
        jsr ph_reset
        lda #HUD_D018
        sta $d018
        lda #D016_BASE
        sta $d016
        lda #0
        sta $d021
        lda #D022_HUD
        sta $d022
        lda #D023_HUD
        sta $d023
        jmp screen_on

; The bar empty, LOADING under it.
ph_reset:
        ldx #PH_CELLS - 1
-       lda #PH_EMPTY
        sta PH_BAR,x
        lda #PH_BAR_COLOUR
        sta PH_BAR_COLOURS,x
        dex
        bpl -
        lda #0
        sta ph_cell
        ldy #<ph_loading
        lda #>ph_loading
                                ; (on into ph_words)

; Words on screen A from a list at A:Y (high, low): a
; record is a count, a screen offset, a colour, the codes;
; a count 0 ends it.
ph_words:
        sty src
        sta src + 1
_record:
        ldy #0
        lda (src),y             ; the count: 0, the end
        beq _done
        tax
        iny
        lda (src),y             ; the offset: on screen A
        sta dst                 ; and in the colour RAM
        sta vector
        iny
        lda (src),y
        clc
        adc #>SCREEN_A
        sta dst + 1
        adc #(>COLOURS) - (>SCREEN_A)
        sta vector + 1
        iny
        lda (src),y             ; the colour
        sta count
        lda src                 ; src: on the codes
        clc
        adc #4
        sta src
        bcc +
        inc src + 1
+       ldy #0
-       lda (src),y
        sta (dst),y
        lda count
        sta (vector),y
        iny
        dex
        bne -
        tya                     ; src: on the next record
        clc
        adc src
        sta src
        bcc _record
        inc src + 1
        bne _record
_done:
        rts

; PH_WAIT frames, counted on the beam (no interrupts).
ph_pause:
        ldx #PH_WAIT
-       lda $d012               ; line 250: once a frame
        cmp #250
        bne -
-       cmp $d012
        beq -
        dex
        bne --
ph_waited:                      ; the tests look here
        rts

        .include "../assets/generated/phase.inc"
