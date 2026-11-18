; The sound effects: short, six of them (sfx.py): the three
; ships' shots, the Varkon's plasma, the ship hurt and
; exploding. They sound in two of the modes:
;  - SOUND FX: each on its own voice (sfx_voice): the
;    ship's shots on voice 1, the plasma on voice 2, the
;    ship's harm on voice 3;
;  - MUSIC + FX: all on voice 3, the music on the others.
; On its voice an effect starts if none of a higher priority
; (sfx_pri) sounds there or waits to; one of the same
; priority starts again: each shot is heard.
;
; The game calls sfx_start with the effect's number (FX_*)
; where the thing happens, in its turn: the effect waits on
; its voice (fx_next) for the main loop's sfx_play, after
; the music. Its data (sfx_data) are a header and rows: the
; header its frames a row, attack and decay, sustain and
; release, its pulse width; a row a waveform with the gate
; on and a note (the music's frequency table). sfx_play
; starts a waiting effect with its gate off in the copy (the
; SID starts its envelope again in the next frame), then
; writes a row every so many frames; after the last row,
; the gate off: the sound fades with its release, and the
; voice is free.

; Effect A, from the game's turn: on its voice, if the mode
; sounds effects and no higher one is there. X and Y kept.
sfx_start:
        sta sfx_new
        stx sfx_keep
        sty sfx_keep + 1
        ldx #2                  ; MUSIC + FX: voice 3
        ldy sound_mode
        cpy #MODE_MUSIC_FX
        beq _voice
        cpy #MODE_FX            ; MUSIC, SILENT: none
        bne _done
        tay                     ; SOUND FX: its own
        ldx sfx_voice,y
_voice:
        ldy sfx_new
        lda sfx_pri,y           ; not over a higher one
        cmp fx_pri,x
        bcc _done
        sta fx_pri,x
        iny                     ; it waits: its number + 1
        tya
        sta fx_next,x
_done:
        ldx sfx_keep
        ldy sfx_keep + 1
        rts

; A frame of the effects (sound_frame, after the music): on
; each voice, an effect waiting starts (its envelope and
; pulse width in the copy, the gate off; its first row in
; the next frame); an effect playing, its frames a row over,
; writes its next row (frequency, waveform and gate); none
; left, the gate off and the voice free.
sfx_play:
        ldx #2
_voice:
        ldy fx_next,x           ; one waiting?
        beq _play
        lda #0
        sta fx_next,x
        lda #1                  ; its first row: next frame
        sta fx_tick,x
        lda sfx_first - 1,y     ; (Y: its number + 1)
        tay                     ; Y: its data
        clc
        adc #FX_HEADER
        sta fx_pos,x
        lda sfx_data,y          ; its frames a row
        sta fx_speed,x
        stx fx_voice
        lda voice_regs,x        ; X: the voice's registers
        tax
        lda sfx_data + 1,y      ; attack and decay
        sta sid_shadow + 5,x
        lda sfx_data + 2,y      ; sustain and release
        sta sid_shadow + 6,x
        lda sfx_data + 3,y      ; the pulse width
        sta sid_shadow + 3,x
        lda #0
        sta sid_shadow + 2,x
        sta sid_shadow + 4,x    ; the gate off
        ldx fx_voice
        jmp _next
_play:
        lda fx_pos,x            ; 0: no effect
        beq _next
        dec fx_tick,x
        bne _next
        lda fx_speed,x
        sta fx_tick,x
        ldy fx_pos,x
        lda sfx_data,y          ; the waveform, gate on
        beq _end                ; 0: the end
        sta mus_work
        lda sfx_data + 1,y      ; the note
        tay
        lda freq_lo,y           ; its frequency
        sta mus_freq
        lda freq_hi,y
        sta mus_freq + 1
        ldy voice_regs,x
        lda mus_freq
        sta sid_shadow,y
        lda mus_freq + 1
        sta sid_shadow + 1,y
        lda mus_work
        sta sid_shadow + 4,y
        lda fx_pos,x            ; the next row
        clc
        adc #2
        sta fx_pos,x
_next:
        dex
        bmi +
        jmp _voice
+       rts
_end:
        sta fx_pos,x            ; (0) the voice free
        sta fx_pri,x
        ldy voice_regs,x
        lda sid_shadow + 4,y    ; the gate off
        and #%11111110
        sta sid_shadow + 4,y
        jmp _next
