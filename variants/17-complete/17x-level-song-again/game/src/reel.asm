; Only with -D RECORD_SFX=1: the sound effects one after
; the other, in SOUND FX, one each FX_REEL_FRAMES frames,
; then silence; the level stands still. The main loop's
; sound frame, once a frame (frame_flag, the HUD's
; interrupt), as in the game.
sfx_reel:
        lda #MODE_FX
        jsr sound_set
        ldx #0                  ; X: the effect
_effect:
        lda #FX_REEL_FRAMES
        sta count
        txa
        jsr sfx_start           ; (it keeps X)
_frame:
        jsr _sound
        dec count
        bne _frame
        inx
        cpx #FX_COUNT
        bne _effect
-       jsr _sound              ; then the releases fade
        jmp -
_sound:
        lda frame_flag          ; a frame: its sound
        beq _sound
        lda #0
        sta frame_flag
        txa
        pha
        jsr music_play
        jsr sfx_play
        pla
        tax
        rts
