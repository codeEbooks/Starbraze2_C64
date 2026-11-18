; The score: six digits, BCD, three bytes (score: the units
; and tens first). Each Varkon destroyed adds its kind's
; points (kind_pts_*, BCD: tens and units, thousands and
; hundreds); every EXTRA_EVERY ten thousand a ship more, up
; to LIVES_MAX; the best so far (hi_score) follows it. The
; HUD shows both when they change. A new game (no ships
; left) starts from 0; the best stays.
;
; The decimal mode (SED) is on only here; the interrupts
; that add or subtract (the field's) clear it first.

EXTRA_EVERY = $01               ; BCD, ten thousands

; Kind Y's points to the score. X kept.
score_add:
        sed
        clc
        lda score
        adc kind_pts_lo,y
        sta score
        lda score + 1
        adc kind_pts_hi,y
        sta score + 1
        lda score + 2
        adc #0
        sta score + 2
        bcc +
        lda #$99                ; past 999 990: it stays
        sta score + 2
        sta score + 1
        lda #$90
        sta score
+       lda score + 2           ; a ship more?
        cmp next_life
        bcc _best
        lda next_life           ; the next one
        clc
        adc #EXTRA_EVERY
        bcc +
        lda #$ff                ; past 99: never again
+       sta next_life
        cld
        lda ship_lives
        cmp #LIVES_MAX
        bcs _best
        inc ship_lives
        lda #1
        sta hud_dirty
_best:
        cld
        lda #1
        sta score_dirty
        lda score + 2           ; better than the best?
        cmp hi_score + 2
        bcc _done
        bne _new
        lda score + 1
        cmp hi_score + 1
        bcc _done
        bne _new
        lda score
        cmp hi_score
        bcc _done
        beq _done
_new:
        lda score
        sta hi_score
        lda score + 1
        sta hi_score + 1
        lda score + 2
        sta hi_score + 2
_done:
        rts

; (score_reset, score_init and score_shown, the start of the
; program and of a game, are in title.asm.)

; The digits of the score and of the best into the HUD, if
; they have changed: a digit is DIGIT_CODE + its value. Only
; the bytes (two digits) not yet shown (shown_*).
score_digits:
        lda score_dirty
        bne +
        rts
+       lda #0
        sta score_dirty
        ldx #2                  ; from the high byte
        ldy #0
_byte:
        lda score,x
        cmp shown_score,x
        beq +
        sta shown_score,x
        jsr _two
        sta SCREEN_A + SCORE_CELL + 1,y
        lda v_tmp
        sta SCREEN_A + SCORE_CELL,y
+       lda hi_score,x
        cmp shown_hi,x
        beq +
        sta shown_hi,x
        jsr _two
        sta SCREEN_A + HI_CELL + 1,y
        lda v_tmp
        sta SCREEN_A + HI_CELL,y
+       iny
        iny
        dex
        bpl _byte
        rts
_two:                           ; A: a BCD byte; its digits:
        pha                     ; v_tmp the high one, A the
        lsr a                   ; low one
        lsr a
        lsr a
        lsr a
        clc
        adc #DIGIT_CODE
        sta v_tmp
        pla
        and #%00001111
        clc
        adc #DIGIT_CODE
        rts

        .cerror DIGIT_CODE > 255 - 9, "score_digits"
